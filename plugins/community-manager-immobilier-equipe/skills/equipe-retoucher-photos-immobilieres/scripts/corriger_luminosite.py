#!/usr/bin/env python3
"""Correction tonale non générative : Pillow pour les images, NumPy par bandes.

Ne choisit pas les réglages et ne remplace pas le contrôle visuel. N'écrase aucun
fichier. Le rapport JSON sur stdout décrit un candidat, jamais une livraison.
"""
import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import tempfile
import time

import numpy as np
from PIL import Image, ImageCms, ImageOps

ENGINE_VERSION = "pillow-developpement-4"
SRGB_PROFILE = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
DECODE = np.arange(256, dtype=np.float32) / 255
DECODE = np.where(DECODE <= 0.04045, DECODE / 12.92,
                  ((DECODE + 0.055) / 1.055) ** 2.4)
HIGHLIGHT_PROTECTION_SRGB = 220
HIGHLIGHT_LIMIT = float(DECODE[HIGHLIGHT_PROTECTION_SRGB])
SHADOW_LIMIT = float(DECODE[160])
IMAGE_DEFAULTS = {"temperature": 0.0, "tint": 0.0, "contrast": 1.0, "saturation": 1.0}
IMAGE_BOUNDS = {"temperature": (-0.25, 0.25), "tint": (-0.20, 0.20),
                "contrast": (0.85, 1.15), "saturation": (0.85, 1.15)}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def normalize_image_settings(settings=None):
    """Réglages relatifs, décidés visuellement ; aucune estimation automatique WB."""
    if settings is None:
        settings = {}
    if not isinstance(settings, dict) or set(settings) - set(IMAGE_DEFAULTS):
        raise ValueError("reglages_image doit contenir uniquement temperature, tint, contrast, saturation.")
    normalized = dict(IMAGE_DEFAULTS)
    for name, value in settings.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} doit être un nombre fini.")
        value = float(value)
        low, high = IMAGE_BOUNDS[name]
        if not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f"{name} doit être compris entre {low} et {high}.")
        normalized[name] = value
    return normalized


def has_correction(settings):
    return (any(settings.get(name, 0.0) != 0.0 for name in ("exposure_ev", "shadows", "highlights"))
            or any(settings.get(name, default) != default for name, default in IMAGE_DEFAULTS.items()))


def validate_settings(exposure_ev, shadows, highlights, temperature=0.0, tint=0.0,
                      contrast=1.0, saturation=1.0, require_change=True):
    for name, value, low, high in [
        ("exposure_ev", exposure_ev, -1.5, 3.0),
        ("shadows", shadows, 0.0, 2.0),
        ("highlights", highlights, 0.0, 0.8),
    ]:
        if not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f"{name} doit être compris entre {low} et {high}.")
    image_settings = normalize_image_settings({"temperature": temperature, "tint": tint,
                                               "contrast": contrast, "saturation": saturation})
    if require_change and not has_correction(dict(image_settings, exposure_ev=exposure_ev,
                                                  shadows=shadows, highlights=highlights)):
        raise ValueError("Aucune correction demandée : copier la source sans recompression.")


def linear_luminance(rgb):
    linear = DECODE[rgb]
    return linear[..., 0] * .2126 + linear[..., 1] * .7152 + linear[..., 2] * .0722


def bounded_lift(luminance, gain, limit):
    """Courbe monotone ancrée en 0 et limit, identité au-dessus du seuil.

    Le raccord est continu. Aucun mélange spatial ou masque flouté ne peut
    produire de halo. La pente du raccord peut comprimer le contraste local.
    """
    below = np.minimum(luminance, limit)
    lifted = gain * below / (1.0 + (gain - 1.0) * below / limit)
    return np.where(luminance < limit, lifted, luminance)


def preserve_gamut(candidate, reference, limits):
    """Réduire la correction chromatique vers sa référence valide, à luminance constante.

    Les deux couleurs ont la même luminance. Leur mélange reste donc iso-luminant,
    sans clipping par canal ni assombrissement de tout le pixel pour rentrer au gamut.
    """
    delta = candidate - reference
    allowable = np.ones_like(delta)
    np.divide(limits - reference, delta, out=allowable, where=delta > 1e-12)
    np.divide(-reference, delta, out=allowable, where=delta < -1e-12)
    amount = np.clip(np.min(allowable, axis=-1), 0, 1)
    return np.clip(reference + delta * amount[..., None], 0, 1)


def bounded_contrast(luminance, contrast):
    """Courbe en S monotone, ancrée en noir et au seuil de hautes lumières."""
    x = np.minimum(luminance / HIGHLIGHT_LIMIT, 1.0)
    target = HIGHLIGHT_LIMIT * (x + 4.0 * (contrast - 1.0) * x * (1.0 - x) * (x - .5))
    return np.where(luminance < HIGHLIGHT_LIMIT, target, luminance)


def correct_rgb(rgb, exposure_ev, shadows, highlights, temperature=0.0, tint=0.0,
                contrast=1.0, saturation=1.0):
    """Lumière sélective puis couleur iso-luminante ; réglages neutres par défaut."""
    validate_settings(exposure_ev, shadows, highlights, temperature, tint, contrast,
                      saturation, require_change=False)
    linear = DECODE[rgb]
    luminance = (linear[..., 0] * .2126 + linear[..., 1] * .7152
                 + linear[..., 2] * .0722)
    # Deux applications monotones : ombres sous 160, puis tons sous 220.
    # Ne pas mélanger un masque décroissant avec une forte correction globale :
    # ce mélange peut inverser les tons juste avant les hautes lumières.
    target = bounded_lift(luminance, 1.0 + 2.0 * shadows, SHADOW_LIMIT)
    gain = 2.0 ** exposure_ev
    if exposure_ev >= 0:
        target = bounded_lift(target, gain, HIGHLIGHT_LIMIT)
    else:
        # Une baisse d'exposition est une demande manuelle explicite.
        target = gain * target / (1.0 + (gain - 1.0) * target)
    target -= highlights * target ** 3 * (1.0 - target)
    if contrast != 1.0:
        target = bounded_contrast(target, contrast)
    ratio = np.divide(target, luminance, out=np.ones_like(target), where=luminance > 0)
    peak = linear.max(axis=2)
    # Ne créer aucun canal à 255 si ce pixel n'en contenait pas déjà.
    # Les couleurs déjà saturées restent limitées par leur canal dominant.
    channel_limit = np.where(peak < 1.0, DECODE[254], 1.0)
    max_gain = np.divide(channel_limit, peak, out=np.full_like(peak, np.inf), where=peak > 0)
    ratio = np.minimum(ratio, max_gain)
    corrected = np.clip(linear * ratio[..., None], 0, 1)
    if temperature != 0.0 or tint != 0.0 or saturation != 1.0:
        # Température positive = plus chaud ; teinte positive = plus magenta.
        # Ce sont des corrections relatives sur RGB développé, pas des Kelvin RAW.
        limits = np.where(rgb == 255, 1.0, DECODE[254])
        y = (corrected[..., 0] * .2126 + corrected[..., 1] * .7152
             + corrected[..., 2] * .0722)
        if temperature != 0.0 or tint != 0.0:
            gains = np.exp2(np.array([temperature + .5 * tint, -tint,
                                     -temperature + .5 * tint], dtype=np.float32))
            candidate = corrected * gains
            candidate_y = (candidate[..., 0] * .2126 + candidate[..., 1] * .7152
                           + candidate[..., 2] * .0722)
            scale = np.divide(y, candidate_y, out=np.ones_like(y), where=candidate_y > 0)
            candidate *= scale[..., None]
            corrected = preserve_gamut(candidate, corrected, limits)
        if saturation != 1.0:
            candidate = y[..., None] + saturation * (corrected - y[..., None])
            corrected = preserve_gamut(candidate, corrected, limits)
    encoded = np.where(corrected <= 0.0031308, corrected * 12.92,
                       1.055 * corrected ** (1 / 2.4) - 0.055)
    return np.rint(np.clip(encoded, 0, 1) * 255).astype(np.uint8)


def correct_file(source, output, exposure_ev=0.0, shadows=0.0, highlights=0.0,
                 temperature=0.0, tint=0.0, contrast=1.0, saturation=1.0):
    validate_settings(exposure_ev, shadows, highlights, temperature, tint, contrast, saturation)
    start = time.perf_counter()
    source = Path(source).expanduser().resolve(strict=True)
    output = Path(output).expanduser().absolute()
    if source == output.resolve() or output.exists() or output.is_symlink():
        raise ValueError("La destination doit être nouvelle et différente de la source.")
    if output.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        raise ValueError("Choisir une destination .jpg, .jpeg ou .png.")
    source_hash = sha256(source)
    warnings = []
    with Image.open(source) as opened:
        if opened.format not in {"JPEG", "PNG", "WEBP", "TIFF", "BMP"}:
            raise ValueError("Format non pris en charge par ce moteur 8 bits.")
        if opened.format == "PNG":
            with source.open("rb") as header:
                png_header = header.read(25)
            if len(png_header) < 25 or png_header[24] > 8:
                raise ValueError("PNG haute profondeur : conversion silencieuse en 8 bits refusée.")
        if getattr(opened, "n_frames", 1) != 1:
            raise ValueError("Image animée ou multipage : traitement explicite nécessaire.")
        if opened.mode not in {"RGB", "RGBA", "L", "LA", "P", "CMYK"}:
            raise ValueError("Mode non pris en charge sans perte de profondeur ; conserver la source.")
        if opened.format == "TIFF":
            bits = opened.tag_v2.get(258, (8,))
            if any(v > 8 for v in (bits if isinstance(bits, tuple) else (bits,))):
                raise ValueError("TIFF haute profondeur : ne pas convertir silencieusement en 8 bits.")
        original_size = opened.size
        source_mode = opened.mode
        has_alpha = "A" in opened.getbands() or "transparency" in opened.info
        if has_alpha and output.suffix.lower() != ".png":
            raise ValueError("La transparence impose une sortie PNG.")
        icc = opened.info.get("icc_profile")
        dpi = opened.info.get("dpi")
        if not icc and opened.format == "PNG" and "srgb" not in opened.info:
            gamma = opened.info.get("gamma")
            if gamma is not None and not math.isclose(gamma, 1 / 2.2, abs_tol=0.001):
                raise ValueError("PNG avec gamma non sRGB sans profil ICC : conversion refusée.")
            chroma = opened.info.get("chromaticity")
            srgb_chroma = (0.3127, 0.3290, 0.64, 0.33, 0.30, 0.60, 0.15, 0.06)
            if chroma is not None and not np.allclose(chroma, srgb_chroma, atol=0.0001):
                raise ValueError("PNG avec primaires non sRGB sans profil ICC : conversion refusée.")
        image = ImageOps.exif_transpose(opened)
        alpha = image.convert("RGBA").getchannel("A") if has_alpha else None
        exif = image.getexif()
        exif_details = dict(exif.get_ifd(34665)) if 34665 in exif else {}
        # L'orientation est appliquée aux pixels ; ne pas reporter une ancienne rotation.
        exif.pop(274, None)
        for tag, size in ((256, image.width), (257, image.height)):
            if tag in exif:
                exif[tag] = size
        for tag, size in ((40962, image.width), (40963, image.height)):
            if tag in exif_details:
                exif_details[tag] = size
            exif.pop(tag, None)
        if icc:
            profile = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            cms_input = image if image.mode in {"RGB", "L", "CMYK"} else image.convert("RGB")
            image = ImageCms.profileToProfile(cms_input, profile, SRGB_PROFILE,
                                              outputMode="RGB")
        else:
            if image.mode == "CMYK":
                raise ValueError("CMYK sans profil ICC : couleurs non fiables, conversion refusée.")
            if exif_details.get(40961, exif.get(40961, 1)) != 1:
                raise ValueError("Espace couleur non sRGB sans profil ICC : conversion refusée.")
            if image.mode != "RGB":
                image = image.convert("RGB")
            warnings.append("Sans profil ICC : source interprétée en sRGB.")
        # exif_transpose a fourni une image indépendante : libérer le décodeur
        # avant d'allouer la sortie pleine définition et les bandes NumPy.
        opened.close()
        width, height = image.size
        result = Image.new("RGB", image.size)
        sample_before, sample_after = [], []
        # Limiter la mémoire de calcul pour les lots de photos haute définition.
        for top in range(0, height, 64):
            box = (0, top, width, min(top + 64, height))
            data = np.asarray(image.crop(box), dtype=np.uint8)
            corrected = correct_rgb(data, exposure_ev, shadows, highlights, temperature, tint, contrast, saturation)
            result.paste(Image.fromarray(corrected), box)
            sample_before.append(data[::16, ::16].reshape(-1, 3))
            sample_after.append(corrected[::16, ::16].reshape(-1, 3))
        if alpha is not None:
            result.putalpha(alpha)
        exif.pop(40961, None)
        exif_details[40961] = 1
        exif[34665] = exif_details
        save_options = {"icc_profile": SRGB_PROFILE.tobytes(), "exif": exif.tobytes()}
        if dpi:
            save_options["dpi"] = dpi
        fmt = "PNG" if output.suffix.lower() == ".png" else "JPEG"
        if fmt == "JPEG":
            save_options.update(quality=95, subsampling=0)
        else:
            save_options.update(compress_level=3)
        output.parent.mkdir(parents=True, exist_ok=True)
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".tmp", delete=False) as temp:
                temp_name = temp.name
                result.save(temp, format=fmt, **save_options)
                temp.flush()
                os.fsync(temp.fileno())
            with Image.open(temp_name) as check:
                check.verify()
            with Image.open(temp_name) as check:
                if check.size != (width, height) or check.format != fmt:
                    raise ValueError("Dimensions ou format de sortie inattendus.")
            if sha256(source) != source_hash:
                raise ValueError("La source a changé pendant le traitement ; résultat non validé.")
            # Publication atomique sans écrasement, même si un autre agent a créé le nom.
            os.link(temp_name, output)
        finally:
            if temp_name is not None:
                Path(temp_name).unlink(missing_ok=True)
    before = np.concatenate(sample_before)
    after = np.concatenate(sample_after)
    protected = linear_luminance(before) >= HIGHLIGHT_LIMIT - 1e-7
    return {
        "engine": ENGINE_VERSION, "source_name": source.name,
        "source_sha256": source_hash, "source_mode": source_mode,
        "source_dimensions_before_orientation": list(original_size),
        "output_path": str(output), "output_sha256": sha256(output),
        "dimensions": [width, height], "format": fmt,
        "settings": {"exposure_ev": exposure_ev, "shadows": shadows, "highlights": highlights,
                     "temperature": temperature, "tint": tint, "contrast": contrast, "saturation": saturation},
        "elapsed_seconds": round(time.perf_counter() - start, 3),
        "encoded_size_bytes": output.stat().st_size,
        "sample_statistics_before_encoding": {
            "near_white_before": round(float(np.mean(np.max(before, axis=1) >= 254)), 5),
            "near_white_after": round(float(np.mean(np.max(after, axis=1) >= 254)), 5),
            "highlight_protection_srgb": HIGHLIGHT_PROTECTION_SRGB,
            "protected_sample_pixels": int(protected.sum()),
            "protected_sample_pixels_changed": int(np.sum(protected & np.any(before != after, axis=1))),
            "protected_sample_linear_luminance_max_delta": round(float(np.max(
                np.abs(linear_luminance(after)[protected] - linear_luminance(before)[protected])))
                if protected.any() else 0.0, 6),
            "new_clipped_sample_channels": int(np.sum((before < 255) & (after == 255))),
        },
        "warnings": warnings, "status": "candidate_requires_visual_review",
        "enregistre": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--exposure-ev", type=float, default=0.0)
    parser.add_argument("--shadows", type=float, default=0.0)
    parser.add_argument("--highlights", type=float, default=0.0)
    parser.add_argument("--temperature", type=float, default=0.0, help="Correction relative : positif chaud, négatif froid, entre -0.25 et 0.25.")
    parser.add_argument("--tint", type=float, default=0.0, help="Correction relative : positif magenta, négatif vert, entre -0.20 et 0.20.")
    parser.add_argument("--contrast", type=float, default=1.0, help="Contraste modéré, de 0.85 à 1.15 ; 1 neutre.")
    parser.add_argument("--saturation", type=float, default=1.0, help="Saturation modérée, de 0.85 à 1.15 ; 1 neutre.")
    args = parser.parse_args()
    try:
        report = correct_file(args.source, args.output, args.exposure_ev, args.shadows, args.highlights,
                              args.temperature, args.tint, args.contrast, args.saturation)
    except (OSError, ValueError, ImageCms.PyCMSError) as error:
        parser.exit(2, f"Correction refusée : {error}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

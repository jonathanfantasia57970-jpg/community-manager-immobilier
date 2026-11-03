#!/usr/bin/env python3
"""Première passe Pillow parallèle, numérotée, sans validation visuelle.

Le registre local suit les artefacts, jamais leur transfert vers un service.
"""
import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from contextlib import contextmanager
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import time

import numpy as np
from PIL import Image, ImageCms, ImageOps

from corriger_luminosite import (SRGB_PROFILE, HIGHLIGHT_LIMIT, HIGHLIGHT_PROTECTION_SRGB,
                                 correct_file, correct_rgb, linear_luminance, sha256,
                                 normalize_image_settings, has_correction, IMAGE_DEFAULTS)

LEVELS = ("normal", "un_peu_plus_lumineux", "beaucoup_plus_lumineux")
REGISTRY_NAME = "suivi-lot-rapide.json"
COPY_SUCCESS = {"copiee_a_revoir", "copiee_a_controler"}
SUCCESS = {"produite_a_revoir", "produite_a_controler"} | COPY_SUCCESS
CALIBRATION_VERSION = "developpement-selectif-4"


def natural_key(value):
    return [(1, int(part)) if part.isdigit() else (0, part.casefold())
            for part in re.split(r"(\d+)", value)]


def write_json(path, value):
    """Remplacer atomiquement un registre dont le coordinateur est propriétaire."""
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                         prefix=".suivi-", delete=False) as stream:
            temp_name = stream.name
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name:
            Path(temp_name).unlink(missing_ok=True)


@contextmanager
def registry_lock(output):
    """Un seul coordinateur par répertoire ; verrou OS libéré à l'arrêt."""
    import fcntl
    lock_path = output / ".suivi-lot-rapide.lock"
    if lock_path.is_symlink():
        raise ValueError("Verrou symbolique refusé.")
    with lock_path.open("a") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError("Un traitement utilise déjà ce dossier de sortie.") from error
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def estimate_settings(source, niveau, reglages_image=None):
    """Calibrer le rendu combiné avec des réglages couleur explicites, sans les deviner."""
    image_settings = normalize_image_settings(reglages_image)
    with Image.open(source) as opened:
        if getattr(opened, "n_frames", 1) != 1:
            raise ValueError("Animation ou image multipage : traitement explicite nécessaire.")
        if opened.format not in {"JPEG", "PNG", "WEBP", "TIFF", "BMP"}:
            raise ValueError("Format non pris en charge par cette première passe.")
        alpha = "A" in opened.getbands() or "transparency" in opened.info
        fmt = opened.format
        orientation = int(opened.getexif().get(274, 1))
        dimensions = list(opened.size[::-1] if orientation in {5, 6, 7, 8} else opened.size)
        # La réduction ne concerne que le calcul des réglages, jamais la sortie.
        preview = ImageOps.exif_transpose(opened)
        preview.thumbnail((192, 192))
        mask = np.asarray(preview.convert("RGBA"))[..., 3] > 0 if alpha else None
        icc = opened.info.get("icc_profile")
        if icc:
            profile = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            cms_input = preview if preview.mode in {"RGB", "L", "CMYK"} else preview.convert("RGB")
            preview = ImageCms.profileToProfile(cms_input, profile, SRGB_PROFILE, outputMode="RGB")
        else:
            preview = preview.convert("RGB")
        rgb = np.asarray(preview, dtype=np.uint8)
        luma = rgb[..., 0] * .2126 + rgb[..., 1] * .7152 + rgb[..., 2] * .0722
        values = luma[mask] if mask is not None else luma.ravel()
        if not values.size:
            raise ValueError("Aucun pixel visible pour estimer la luminosité.")
        p25, median, p90 = np.percentile(values, [25, 50, 90])
    index = LEVELS.index(niveau)
    visible = np.ones(rgb.shape[:2], dtype=bool) if mask is None else mask
    linear_y = linear_luminance(rgb)
    # Garder le masque de la SOURCE lors des mesures du rendu : les fenêtres
    # claires ne pilotent pas le gain, et les pixels ne changent pas de population.
    eligible = visible & (linear_y > 0) & (linear_y < HIGHLIGHT_LIMIT - 1e-7)
    protected = visible & ~eligible & (linear_y > 0)
    if eligible.any():
        source_values = luma[eligible]
        p25, median, p90 = np.percentile(source_values, [25, 50, 90])
        target_median = max(median, (160., 180., 198.)[index])
        target_p25 = min((100., 118., 135.)[index], p25 + (25., 40., 55.)[index])
    else:
        target_median, target_p25 = median, p25

    def measure(strength):
        corrected = correct_rgb(rgb, 3.0 * strength, 1.5 * strength, 0.0, **image_settings)
        out_luma = corrected[..., 0] * .2126 + corrected[..., 1] * .7152 + corrected[..., 2] * .0722
        measured = out_luma[eligible] if eligible.any() else out_luma[visible]
        return np.percentile(measured, [25, 50, 90])

    low, high = 0.0, 1.0
    baseline_p25, baseline_median, _ = measure(0.0)
    if not eligible.any() or (baseline_median >= target_median - 1 and baseline_p25 >= target_p25 - 1):
        high = 0.0
    else:
        # Recherche bornée sur aperçu ; un seul encodage pleine définition.
        for _ in range(12):
            middle = (low + high) / 2
            q25, q50, _ = measure(middle)
            if q50 >= target_median - 1 and q25 >= target_p25 - 1:
                high = middle
            else:
                low = middle
    settings = {"exposure_ev": round(3.0 * high, 4), "shadows": round(1.5 * high, 4),
                "highlights": 0.0, **image_settings}
    after_p25, after_median, after_p90 = measure(high)
    # Une miniature peut neutraliser un motif coloré fin : ne jamais annuler
    # une correction explicite de couleur/contraste sur cette seule preuve.
    if image_settings == IMAGE_DEFAULTS and np.array_equal(correct_rgb(rgb, **settings), rgb):
        settings = {"exposure_ev": 0.0, "shadows": 0.0, "highlights": 0.0, **IMAGE_DEFAULTS}
    statistics = {"luma_p25": round(float(p25), 2), "luma_mediane": round(float(median), 2),
                  "luma_p90": round(float(p90), 2), "cible_mediane": round(float(target_median), 2),
                  "cible_p25": round(float(target_p25), 2),
                  "population_calibration": "pixels_visibles_non_noirs_sous_seuil_protection",
                  "seuil_protection_srgb": HIGHLIGHT_PROTECTION_SRGB,
                  "fraction_pixels_proteges": round(float(protected.sum() / visible.sum()), 5),
                  "fraction_pixels_eligibles": round(float(eligible.sum() / visible.sum()), 5),
                  "fraction_noirs_absolus": round(float(np.sum(visible & (linear_y == 0)) / visible.sum()), 5),
                  "apercu_apres_p25": round(float(after_p25), 2),
                  "apercu_apres_mediane": round(float(after_median), 2),
                  "apercu_apres_p90": round(float(after_p90), 2),
                  "limite_correction_atteinte": bool((not eligible.any() and np.any(visible & (linear_y == 0)))
                                                    or after_median < target_median - 1
                                                    or after_p25 < target_p25 - 1)}
    return settings, statistics, alpha, dimensions, fmt


def copy_exact(source, output, expected_hash, dimensions, fmt):
    """Copie atomique sans écrasement ; une copie n'est pas une retouche."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
            temporary = stream.name
            with source.open("rb") as input_stream:
                shutil.copyfileobj(input_stream, stream)
            stream.flush()
            os.fsync(stream.fileno())
        if sha256(temporary) != expected_hash or sha256(source) != expected_hash:
            raise ValueError("La source a changé pendant la copie.")
        with Image.open(temporary) as check:
            check.verify()
        os.link(temporary, output)
    finally:
        if temporary:
            Path(temporary).unlink(missing_ok=True)
    return {"engine": "copie_octets", "output_path": str(output), "output_sha256": expected_hash,
            "dimensions": dimensions, "format": fmt, "encoded_size_bytes": output.stat().st_size}


def process_photo(source, output, plan):
    start = time.perf_counter()
    result = dict(plan)
    result["tentatives"] = 0
    try:
        settings, statistics, alpha, dimensions, fmt = estimate_settings(source, plan["niveau_luminosite"], plan.get("reglages_image"))
        result.update(settings=settings, statistiques_apercu=statistics)
        if sha256(source) != plan["source_sha256"]:
            raise ValueError("La source a changé depuis l'affectation.")
        copy = not has_correction(settings)
        extension = source.suffix.lower() if copy else (".png" if alpha else ".jpg")
        target = output / (plan["output_stem"] + extension)
        if target.exists() or target.is_symlink():
            raise ValueError("Nom de sortie occupé ; fichier existant préservé.")
        result["output_name"] = target.name
        if copy:
            report = copy_exact(source, target, plan["source_sha256"], dimensions, fmt)
        else:
            result["tentatives"] = 1
            report = correct_file(source, target, **settings)
        if report.get("source_sha256", plan["source_sha256"]) != plan["source_sha256"]:
            raise ValueError("La source a changé pendant la préparation ; résultat à réconcilier.")
        report.pop("status", None)
        report.pop("output_path", None)
        result.update(report, status="copiee_a_controler" if copy else "produite_a_controler")
    except Exception as error:
        result.update(status="erreur", error=str(error))
    result.update(elapsed_seconds=round(time.perf_counter() - start, 3),
                  enregistre=False, controle_visuel="non_effectue", niveau_atteint=None,
                  validation_utilisateur="en_attente")
    return result


def output_verified(output, version):
    name = version.get("output_name")
    if not name or Path(name).name != name:
        return False
    path = output / name
    return path.is_file() and not path.is_symlink() and sha256(path) == version.get("output_sha256")


def current_version(photo):
    number = photo.get("version_courante", photo["versions"][-1]["version"])
    return next(version for version in photo["versions"] if version["version"] == number)


def run_batch(inventory_path, output, niveau, workers=3, retry_errors=False, recalibrate=False):
    if niveau not in LEVELS or not 1 <= workers <= 5:
        raise ValueError("Niveau inconnu ou workers hors de l'intervalle 1 à 5.")
    inventory = json.loads(Path(inventory_path).read_text(encoding="utf-8"))
    if inventory.get("enumeration_errors"):
        raise ValueError("Inventaire incomplet : résoudre les erreurs d'énumération.")
    entries = inventory["photos"]
    # Valider tous les réglages avant la création des sorties et les affectations.
    for row in entries:
        row["reglages_image"] = normalize_image_settings(row.get("reglages_image"))
    identities = [str(row.get("source_id") or row["source_key"]) for row in entries]
    if len(set(identities)) != len(identities):
        raise ValueError("Identités source dupliquées dans l'inventaire.")
    output = Path(output).expanduser().absolute()
    if output.is_symlink():
        raise ValueError("Dossier de sortie symbolique refusé.")
    output.mkdir(parents=True, exist_ok=True)
    # Échouer avant le calcul si un montage distant ne supporte pas os.link.
    with tempfile.TemporaryDirectory(prefix=".controle-ecriture-", dir=output) as probe:
        first, second = Path(probe) / "source", Path(probe) / "lien"
        first.write_bytes(b"ok")
        try:
            os.link(first, second)
        except OSError as error:
            raise ValueError("Calculer sur un disque natif supportant les liens physiques, "
                             "puis transférer les résultats vers le service distant.") from error
    registry = output / REGISTRY_NAME
    if registry.is_symlink():
        raise ValueError("Registre symbolique refusé.")
    with registry_lock(output):
        if registry.exists():
            state = json.loads(registry.read_text(encoding="utf-8"))
            if state.get("schema_version") != 1 or state.get("workflow") != "pillow_rapide":
                raise ValueError("Registre inconnu : migration explicite nécessaire.")
        else:
            state = {"schema_version": 1, "workflow": "pillow_rapide", "photos": []}
        state.update(niveau_luminosite=niveau, workers=workers, calibration_version=CALIBRATION_VERSION)
        by_id = {photo["source_identity"]: photo for photo in state["photos"]}
        next_number = max((photo["numero"] for photo in state["photos"]), default=0) + 1
        jobs, active = [], []
        for row in sorted(entries, key=lambda item: (natural_key(item["relative_path"]), str(item.get("source_id") or item["source_key"]))):
            identity = str(row.get("source_id") or row["source_key"])
            image_settings = row["reglages_image"]
            if identity not in by_id:
                photo = {"source_identity": identity, "numero": next_number, "versions": []}
                next_number += 1
                by_id[identity] = photo
                state["photos"].append(photo)
            photo = by_id[identity]
            photo.update(relative_path=row["relative_path"], source_id=row.get("source_id"), source_key=row.get("source_key"))
            active.append(photo)
            source = Path(row["local_path"]).expanduser().absolute()
            try:
                if source.is_symlink():
                    raise ValueError("Source symbolique refusée.")
                source_hash = sha256(source)
                if row.get("sha256") and source_hash != row["sha256"]:
                    raise ValueError("Source différente de l'inventaire : refaire l'inventaire.")
                problem = None
            except (OSError, ValueError) as error:
                source_hash, problem = None, str(error)
            reusable = next((version for version in reversed(photo["versions"])
                             if not problem and version.get("source_sha256") == source_hash
                             and version.get("niveau_luminosite") == niveau
                             and normalize_image_settings(version.get("reglages_image")) == image_settings
                             and (not recalibrate or version.get("calibration_version") == CALIBRATION_VERSION)
                             and version["status"] in SUCCESS
                             and output_verified(output, version)), None)
            if reusable is not None:
                photo["version_courante"] = reusable["version"]
                continue
            latest = next((version for version in reversed(photo["versions"])
                           if version.get("source_sha256") == source_hash
                           and version.get("niveau_luminosite") == niveau
                           and normalize_image_settings(version.get("reglages_image")) == image_settings), None)
            if latest:
                photo["version_courante"] = latest["version"]
            same = (latest and latest.get("source_sha256") == source_hash
                    and latest.get("niveau_luminosite") == niveau
                    and (not recalibrate or latest.get("calibration_version") == CALIBRATION_VERSION))
            if same and latest["status"] in SUCCESS:
                if output_verified(output, latest):
                    continue
                latest.update(status="resultat_local_manquant_ou_modifie")
            if same and latest["status"] == "a_traiter" and not problem:
                jobs.append((source, latest))
                continue
            if same and not retry_errors:
                if latest["status"] == "en_cours":
                    latest["status"] = "interrompu_a_reconcilier"
                continue
            version_number = max((v["version"] for v in photo["versions"]), default=0) + 1
            while True:
                stem = f'{photo["numero"]:02d}' + (f"_v{version_number}" if version_number > 1 else "")
                if not any(output.glob(stem + ".*")):
                    break
                version_number += 1
            plan = {"version": version_number, "source_sha256": source_hash,
                    "calibration_version": CALIBRATION_VERSION, "reglages_image": image_settings,
                    "niveau_luminosite": niveau, "output_stem": stem, "status": "a_traiter",
                    "tentatives": 0, "enregistre": False,
                    "controle_visuel": "non_effectue", "niveau_atteint": None,
                    "validation_utilisateur": "en_attente"}
            photo["versions"].append(plan)
            photo["version_courante"] = version_number
            if problem:
                plan.update(status="erreur", error=problem)
            else:
                jobs.append((source, plan))
        # Le mapping et les affectations existent avant toute écriture d'image.
        write_json(registry, state)
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            pending_jobs = iter(jobs)
            futures = {}

            def fill_slots():
                while len(futures) < workers:
                    job = next(pending_jobs, None)
                    if job is None:
                        break
                    source, plan = job
                    plan.update(status="en_cours", tentatives=1)
                    write_json(registry, state)
                    futures[executor.submit(process_photo, source, output, plan)] = plan

            fill_slots()
            while futures:
                completed, _ = wait(futures, return_when=FIRST_COMPLETED)
                for future in completed:
                    plan = futures.pop(future)
                    plan.update(future.result())
                    write_json(registry, state)
                # Seules les places libérées reçoivent une nouvelle affectation.
                fill_slots()
        ready = sum(current_version(photo)["status"] in SUCCESS for photo in active)
        summary = {"photos": len(active), "produites_ou_reutilisees": ready,
                   "copies_sans_retouche": sum(current_version(p)["status"] in COPY_SUCCESS for p in active),
                   "limites_luminosite": sum(bool(current_version(p).get("statistiques_apercu", {}).get("limite_correction_atteinte")) for p in active),
                   "erreurs_ou_a_reconcilier": len(active) - ready, "executions": len(jobs),
                   "workers": workers, "elapsed_seconds": round(time.perf_counter() - start, 3),
                   "registre": str(registry), "controle_visuel": "non_effectue", "enregistre": False}
        state["dernier_bilan"] = summary
        write_json(registry, state)
        return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventaire_json", type=Path)
    parser.add_argument("dossier_sortie", type=Path)
    parser.add_argument("--niveau", required=True, choices=LEVELS)
    parser.add_argument("--workers", type=int, default=3, choices=range(1, 6))
    parser.add_argument("--retry-errors", action="store_true", help="Nouvelle tentative explicite pour les erreurs/interruption, avec version distincte.")
    parser.add_argument("--recalibrate", action="store_true", help="Reprise demandée après changement de calibration, avec version distincte.")
    args = parser.parse_args()
    try:
        report = run_batch(args.inventaire_json, args.dossier_sortie, args.niveau, args.workers,
                           args.retry_errors, args.recalibrate)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f"Lot refusé : {error}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["erreurs_ou_a_reconcilier"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

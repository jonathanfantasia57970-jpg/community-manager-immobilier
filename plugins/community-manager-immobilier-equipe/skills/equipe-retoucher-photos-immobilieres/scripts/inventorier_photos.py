#!/usr/bin/env python3
"""Inventorier les sources locales sans retoucher ni écrire aucun fichier."""
import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".heic", ".heif",
              ".avif", ".bmp", ".dng", ".raw", ".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2"}
OUTPUT_FOLDERS = {"photos retouchées", "photos retouchees"}

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def inventory(source, recursive=False, output_subdir="Photos retouchées"):
    source = Path(source).expanduser().resolve(strict=True)
    if not source.is_dir():
        raise ValueError("La source doit être un dossier.")
    if (not output_subdir.strip() or output_subdir in {".", ".."}
            or "/" in output_subdir or chr(92) in output_subdir):
        raise ValueError("Le sous-dossier de sortie doit être un nom simple.")
    excluded = OUTPUT_FOLDERS | {output_subdir.casefold()}
    if source.name.casefold() in excluded:
        raise ValueError("Le dossier source semble être un dossier de résultats.")
    candidates, walk_errors = [], []
    def walk_error(error):
        walk_errors.append({"path": str(error.filename), "error": str(error)})
    for root, directories, filenames in os.walk(source, followlinks=False, onerror=walk_error):
        directories[:] = sorted(
            d for d in directories
            if not d.startswith(".") and d.casefold() not in excluded
            and not (Path(root) / d).is_symlink()
        ) if recursive else []
        for name in sorted(filenames):
            path = Path(root) / name
            if (not name.startswith(".") and not path.is_symlink()
                    and path.is_file() and path.suffix.lower() in EXTENSIONS):
                candidates.append(path)
    candidates.sort(key=lambda p: p.relative_to(source).as_posix().casefold())
    counts = Counter(p.stem.casefold() for p in candidates)
    records = []
    try:
        from PIL import Image
        try:
            import pillow_heif
            pillow_heif.register_heif_opener()
        except ImportError:
            pass
    except ImportError:
        Image = None
    for path in candidates:
        relative = path.relative_to(source).as_posix()
        source_key = hashlib.sha256(relative.encode("utf-8")).hexdigest()
        label = path.stem.encode("utf-8")[:120].decode("utf-8", errors="ignore")
        if counts[path.stem.casefold()] > 1:
            label += "__" + source_key[:12]
        record = {"source_key": source_key, "relative_path": relative,
                  "local_path": str(path), "source_extension": path.suffix.lower(),
                  "proposed_edited_name": label + "_retouchee.png",
                  "proposed_unchanged_name": label + "_conservee" + path.suffix.lower(),
                  "status": "pending_visual_review"}
        try:
            record["size_bytes"] = path.stat().st_size
            record["sha256"] = sha256(path)
        except OSError as error:
            record.update(status="source_read_error", error=str(error))
            records.append(record)
            continue
        if Image is None:
            record["probe_warning"] = "Pillow indisponible ; utiliser un lecteur compatible."
        else:
            try:
                with Image.open(path) as check:
                    check.verify()
                with Image.open(path) as picture:
                    width, height = picture.size
                    orientation = int(picture.getexif().get(274, 1))
                    record.update(format=picture.format, mode=picture.mode,
                                  pixel_dimensions=[width, height], exif_orientation=orientation,
                                  displayed_dimensions=[height, width] if orientation in {5, 6, 7, 8}
                                  else [width, height])
            except Exception as error:
                record.update(status="needs_compatible_reader_or_repair", probe_warning=str(error))
        records.append(record)
    for field in ("proposed_edited_name", "proposed_unchanged_name"):
        collisions = Counter(item[field].casefold() for item in records)
        for item in records:
            if collisions[item[field].casefold()] > 1:
                proposed = Path(item[field])
                item[field] = proposed.stem[:100] + "__" + item["source_key"] + proposed.suffix
    return {"schema_version": 1, "source_local_path": str(source),
            "output_subdir": output_subdir, "recursive": recursive,
            "photo_count": len(records), "enumeration_errors": walk_errors, "photos": records}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--output-subdir", default="Photos retouchées")
    args = parser.parse_args()
    try:
        result = inventory(args.source, args.recursive, args.output_subdir)
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["enumeration_errors"]:
        parser.exit(1)

if __name__ == "__main__":
    main()

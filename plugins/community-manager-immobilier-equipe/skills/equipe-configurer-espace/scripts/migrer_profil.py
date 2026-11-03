#!/usr/bin/env python3
"""Add missing profile fields only; default is a read-only preview."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile

PLUGIN = Path(__file__).resolve().parents[3]

def merge_missing(current, defaults):
    if not isinstance(current, dict) or not isinstance(defaults, dict):
        raise ValueError('Le profil et le modèle doivent être des objets JSON.')
    result = copy.deepcopy(current)
    for key, value in defaults.items():
        if key not in result:
            result[key] = copy.deepcopy(value)
        elif isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_missing(result[key], value)
    return result

def prepare(raw, defaults):
    current = json.loads(raw)
    if not isinstance(current, dict):
        raise ValueError('Le profil doit être un objet JSON.')
    if current.get('schema_version', 1) not in (1, 2):
        raise ValueError('Version de profil inconnue : aucune migration automatique.')
    merged = merge_missing(current, defaults)
    # Existing version is preserved: fields are additive, not a schema rewrite.
    return merged

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', required=True, type=Path)
    parser.add_argument('--expected-sha256')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    path = args.profile.resolve(strict=True)
    if path.is_relative_to(PLUGIN):
        parser.error('Le profil personnel doit rester hors du plugin.')
    defaults = json.loads((PLUGIN / 'assets/profil-conseiller.template.json').read_text())
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    merged = prepare(raw, defaults)
    changed = merged != json.loads(raw)
    result = {'state':'preview','sha256':digest,'changed':changed,'profile':merged}
    if not args.apply:
        print(json.dumps(result, ensure_ascii=False, indent=2)); return
    if args.expected_sha256 != digest:
        parser.error('Empreinte attendue absente ou obsolète : relire le profil.')
    if not changed:
        print(json.dumps({'state':'unchanged','sha256':digest})); return
    lock = path.with_name(path.name + '.migration.lock')
    lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    temp = None
    try:
        if path.read_bytes() != raw:
            raise ValueError('Le profil a changé ; aucune écriture.')
        backup = path.with_name(path.name + '.before-' + digest + '.json')
        with backup.open('xb') as out:
            os.chmod(backup, 0o600); out.write(raw); out.flush(); os.fsync(out.fileno())
        fd, temp = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent)
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            out.write(json.dumps(merged, ensure_ascii=False, indent=2) + '\n')
            out.flush(); os.fsync(out.fileno())
        if path.read_bytes() != raw:
            raise ValueError('Changement concurrent : sauvegarde conservée, aucune écriture.')
        os.replace(temp, path); temp = None
        if json.loads(path.read_bytes()) != merged:
            raise ValueError('Vérification échouée ; conserver la sauvegarde et rapprocher la source.')
        print(json.dumps({'state':'migrated','backup':str(backup),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
    finally:
        if temp: Path(temp).unlink(missing_ok=True)
        os.close(lock_fd); lock.unlink()

if __name__ == '__main__':
    main()

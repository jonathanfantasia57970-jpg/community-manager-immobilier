#!/usr/bin/env python3
"""Resolve an exact packaged skill and optional contained reference; read-only."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def resolve(name, reference=None):
    routes = json.loads((ROOT/'references/skills-map.json').read_text())['skills']
    if name not in routes:
        raise ValueError('Skill absent de ce plugin : ' + name)
    main = (ROOT/routes[name]).resolve(strict=True)
    if not main.is_relative_to(ROOT) or main.name != 'SKILL.md':
        raise ValueError('Route de skill invalide.')
    result = {'skill':name,'skill_file':str(main),'plugin_root':str(ROOT)}
    if reference is not None:
        relative = Path(reference)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Utiliser une référence contenue dans le skill.')
        target = (main.parent/relative).resolve(strict=True)
        if not target.is_relative_to(main.parent) or not target.is_file():
            raise ValueError('Référence absente ou extérieure au skill.')
        result['reference_file'] = str(target)
    return result

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill');parser.add_argument('--reference')
    args=parser.parse_args()
    try: print(json.dumps(resolve(args.skill,args.reference),ensure_ascii=False))
    except (ValueError, OSError) as exc: parser.exit(1,str(exc)+'\n')

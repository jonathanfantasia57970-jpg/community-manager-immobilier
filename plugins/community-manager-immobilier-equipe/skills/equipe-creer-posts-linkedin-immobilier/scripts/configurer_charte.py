#!/usr/bin/env python3
"""Create a personal style outside the immutable plugin, without external calls."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def build(profile):
    identity, brand = profile.get('identity', {}), profile.get('brand', {})
    name = brand.get('signature_name') or identity.get('name')
    if not isinstance(name, str) or not name.strip() or any(x in name for x in ('{', '}', 'CONFIG_')):
        raise ValueError('Renseigner le nom public confirmé du conseiller.')
    style = json.loads((ROOT / 'assets/charte-linkedin.json').read_text())
    roles = brand.get('signature_role') or [identity.get('role') or 'Conseiller immobilier']
    if not isinstance(roles, list) or not 1 <= len(roles) <= 2 or not all(isinstance(x, str) and x.strip() for x in roles):
        raise ValueError('Le titre confirmé doit contenir une ou deux lignes.')
    leadership = profile.get('editorial', {}).get('linkedin', {}).get('leadership_enabled', False)
    if not leadership and any('leader' in x.casefold() for x in roles):
        raise ValueError('Leadership désactivé : retirer le titre de leader du profil.')
    style['signature']['name'] = name.strip()
    style['signature']['role_lines'] = roles
    colors = brand.get('colors')
    if colors is not None:
        import re
        if not isinstance(colors, dict) or not all(k in style['colors'] and isinstance(v, str) and re.fullmatch(r'#[0-9A-Fa-f]{6}', v) for k, v in colors.items()):
            raise ValueError('Couleurs : clés de la charte et codes hexadécimaux à six chiffres requis.')
        style['colors'].update(colors)
    style['profile_id'] = profile.get('profile_id')
    return style

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    plugin_root = ROOT.parents[1]
    if out.is_relative_to(plugin_root) or out == args.profile.resolve():
        raise ValueError('Enregistrer la charte personnelle hors du plugin, sans écraser le profil.')
    style = build(json.loads(args.profile.read_text()))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x', encoding='utf-8') as f:
        f.write(json.dumps(style, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'style': str(out), 'state': 'configured', 'visual_validation': 'pending'}))

if __name__ == '__main__':
    main()

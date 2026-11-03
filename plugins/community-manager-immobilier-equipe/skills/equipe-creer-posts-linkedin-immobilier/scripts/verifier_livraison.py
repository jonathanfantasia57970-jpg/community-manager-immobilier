#!/usr/bin/env python3
"""Check the requested image link and/or post-block syntax in a prepared response.

This checks a local artifact and message text, never user receipt or UI rendering.
"""
import argparse
import json
from pathlib import Path
import re
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path)
    proof = parser.add_mutually_exclusive_group()
    proof.add_argument('--composition', type=Path, help='Proof produced by composer_visuel.py for a new visual')
    proof.add_argument('--existing-image', action='store_true', help='Repair delivery of an unchanged historical image, without claiming current typography compliance')
    parser.add_argument('--library-result', type=Path, help='Complete successful Library create/replace result for this exported PNG')
    parser.add_argument('--response', required=True, type=Path)
    parser.add_argument('--reviewed-text', type=Path, action='append', help='Exact text actually reviewed; repeat in block order for a series')
    parser.add_argument('--require-post-block', action='store_true',
                        help='Require complete social_post writing blocks when supported.')
    args = parser.parse_args()
    if not args.image and not args.require_post_block:
        parser.error('Préciser --image ou --require-post-block.')
    if (args.composition or args.existing_image or args.library_result) and not args.image:
        parser.error('Les contrôles du visuel exigent --image.')
    if args.image and not (args.composition or args.existing_image):
        parser.error('Un nouveau visuel exige --composition ; --existing-image est réservé à une réparation de livraison.')
    if args.require_post_block and not args.reviewed_text:
        parser.error('Préciser --reviewed-text pour vérifier la version exacte livrée.')
    if args.reviewed_text and not args.require_post_block:
        parser.error('--reviewed-text exige --require-post-block.')
    try:
        response = args.response.read_text(encoding='utf-8')
        # A link inside a code fence is displayed as code, not a download link.
        visible_lines = []
        fence = None
        for line in response.splitlines(keepends=True):
            # Preserve offsets so block content can be compared against the raw response.
            masked = re.sub(r'[^\r\n]', ' ', line)
            marker = re.match(r'^\s*(`{3,}|~{3,})', line)
            if marker:
                current = marker.group(1)
                if fence is None:
                    fence = current
                elif current[0] == fence[0] and len(current) >= len(fence):
                    fence = None
                visible_lines.append(masked)
                continue
            if fence is None and not line.startswith(('    ', '\t')):
                visible_lines.append(line)
            else:
                visible_lines.append(masked)
        visible = ''.join(visible_lines)
        block_count = 0
        post_contents = []
        if args.require_post_block:
            starts = list(re.finditer(r'^:::writing[^\n]*(?:\n|$)', visible, re.MULTILINE))
            if not starts:
                raise ValueError('Le post doit être présenté dans un bloc de rédaction social_post.')
            identifiers = set()
            for index, start in enumerate(starts):
                header = re.fullmatch(r':::writing\{([^\n]*)\}[ \t]*\n?', start.group())
                if not header:
                    raise ValueError('L’en-tête du bloc de rédaction est mal formé.')
                metadata = header.group(1)
                pair = r'(?:variant="social_post"\s+id="([0-9]{5})"|id="([0-9]{5})"\s+variant="social_post")'
                attributes = re.fullmatch(r'\s*' + pair + r'\s*', metadata)
                if not attributes:
                    raise ValueError('Le bloc exige variant="social_post" et un id de cinq chiffres.')
                identifier = attributes.group(1) or attributes.group(2)
                if identifier in identifiers:
                    raise ValueError('Chaque bloc doit avoir un id unique.')
                identifiers.add(identifier)
                end = re.search(r'^:::[ \t]*$', visible[start.end():], re.MULTILINE)
                if not end or (index + 1 < len(starts) and start.end() + end.start() > starts[index + 1].start()):
                    raise ValueError('Le bloc de rédaction doit être fermé.')
                post = response[start.end():start.end() + end.start()].strip()
                if not post:
                    raise ValueError('Le bloc de rédaction est vide.')
                post_contents.append(post)
                block_count += 1
            reviewed = [path.read_text(encoding='utf-8').strip() for path in args.reviewed_text]
            if post_contents != reviewed:
                raise ValueError('Le texte livré diffère du texte relu ; fournir un --reviewed-text par bloc, dans le même ordre.')
        visible = re.sub(r'(`+).*?\1', '', visible, flags=re.DOTALL)
        result = {'valid': True, 'checked': 'reviewed_text_and_post_block', 'user_receipt_verified': False,
                  'editorial_quality_verified': False}
        if args.require_post_block:
            result['post_blocks'] = block_count
            result['reviewed_text_matches'] = True
        if args.image:
            if not args.image.is_absolute():
                raise ValueError('Le chemin de l’image doit être absolu.')
            if any(c in str(args.image) for c in ' ()\n\r'):
                raise ValueError('Utiliser un chemin de fichier compatible avec le lien Markdown.')
            if not args.image.is_file() or args.image.stat().st_size == 0:
                raise ValueError('Le fichier image est absent ou vide.')
            from PIL import Image
            with Image.open(args.image) as img:
                dimensions = img.size
                img.verify()
            if args.composition:
                from composer_visuel import verify
                result.update(verify(args.composition, args.image))
            else:
                result.update(composition_verified=False, historical_delivery_repair=True)
            target = 'sandbox:' + str(args.image)
            if args.library_result:
                saved = json.loads(args.library_result.read_text(encoding='utf-8'))
                saved = saved.get('structuredContent', saved)
                if saved.get('status') != 'succeeded' or saved.get('operation') not in ('create_library_file', 'replace_library_file'):
                    raise ValueError('La sauvegarde native n’est pas confirmée.')
                library_id = saved.get('library_file_id', '')
                if not re.fullmatch(r'libfile_[a-zA-Z0-9]+', library_id):
                    raise ValueError('Identifiant natif absent ou invalide.')
                if saved.get('file_name') != args.image.name or saved.get('file_size_bytes') != args.image.stat().st_size:
                    raise ValueError('La sauvegarde native ne correspond pas au nom et à la taille du fichier contrôlé.')
                target = 'https://chatgpt.com/library?file_id=' + library_id + '&account_id=personal'
            pattern = r'(?<!!)\[[^\]\n]+\]\(' + re.escape(target) + r'\)'
            if not re.search(pattern, visible):
                raise ValueError('La réponse finale ne contient pas le lien de téléchargement vers cette image.')
            result.update(checked='image_file_and_prepared_response',
                          image=str(args.image), dimensions=dimensions)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, ImportError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())

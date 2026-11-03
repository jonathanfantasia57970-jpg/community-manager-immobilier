#!/usr/bin/env python3
"""Apply the canonical typography as real pixels and verify the resulting PNG.

Mechanical layout only: no generative photo editing, retouching or silent crop.
The proof binds the actual source, headline, font, style, overlay and final file.
It does not judge identity, contrast, existing text in the photo or editorial value.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path

from PIL import Image, ImageOps
import fitz
import typographie as typo

STYLE_PATH = typo.STYLE_PATH
FONT_PATH = typo.ROOT / 'assets' / typo.STYLE['font']


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def record(path):
    path = Path(path).resolve()
    return {'path': str(path), 'sha256': digest(path)}


def raster(svg):
    with fitz.open(stream=svg.encode(), filetype='svg') as doc:
        png = doc[0].get_pixmap(alpha=True).tobytes('png')
    with Image.open(io.BytesIO(png)) as im:
        return im.convert('RGBA')


def background(path, format_name='4:5'):
    page = typo.layout(format_name)['canvas']
    target = (page['width'], page['height'])
    with Image.open(path) as im:
        photo = ImageOps.exif_transpose(im).convert('RGBA')
    # Permit raster rounding only; never crop a face to satisfy the template.
    if abs(photo.width - photo.height * target[0] / target[1]) > 2:
        raise ValueError(f'La photo doit être au format {format_name} : revoir son cadrage avant composition.')
    if photo.getchannel('A').getextrema() != (255, 255):
        raise ValueError('La photographie doit être opaque.')
    return photo.resize(target, Image.Resampling.LANCZOS)


def compose(photo, headline, output, illustration_ia=True, format_name='4:5'):
    photo, headline, output = [Path(p).resolve() for p in (photo, headline, output)]
    if output.suffix.lower() != '.png':
        raise ValueError('Exporter le composé en PNG pour vérifier ses pixels sans perte.')
    overlay_svg = output.with_suffix('.calque.svg')
    overlay_png = output.with_suffix('.calque.png')
    proof = output.with_suffix('.composition.json')
    if any(p in (photo, headline, STYLE_PATH.resolve(), FONT_PATH.resolve())
           for p in (output, overlay_svg, overlay_png, proof)):
        raise ValueError('Les sorties ne doivent écraser aucun fichier source.')
    lines = json.loads(headline.read_text(encoding='utf-8'))
    svg = typo.render_overlay(lines, illustration_ia, format_name)
    overlay = raster(svg)
    final = Image.alpha_composite(background(photo, format_name), overlay).convert('RGB')
    output.parent.mkdir(parents=True, exist_ok=True)
    overlay_svg.write_text(svg, encoding='utf-8')
    overlay.save(overlay_png)
    final.save(output)
    data = {
        'schema_version': 1, 'method': 'canonical_overlay_v1',
        'photo': record(photo), 'headline': record(headline),
        'style': record(STYLE_PATH), 'font': record(FONT_PATH),
        'overlay_svg': record(overlay_svg), 'overlay_png': record(overlay_png),
        'output': record(output), 'dimensions': list(final.size),
        'illustration_ia': illustration_ia, 'format': format_name,
        'limits': 'Assemblage vérifiable, pas validation du contenu ni preuve de réception utilisateur.'
    }
    proof.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'image': str(output), 'composition': str(proof), 'dimensions': list(final.size)}


def verify(proof, image):
    data = json.loads(Path(proof).read_text(encoding='utf-8'))
    if data.get('schema_version') != 1 or data.get('method') != 'canonical_overlay_v1':
        raise ValueError('Preuve de composition inconnue.')
    image = Path(image).resolve()
    if Path(data['output']['path']).resolve() != image:
        raise ValueError('La preuve ne concerne pas le fichier livré.')
    for key in ('photo', 'headline', 'style', 'font', 'overlay_svg', 'overlay_png', 'output'):
        if digest(data[key]['path']) != data[key]['sha256']:
            raise ValueError(f'Fichier modifié depuis la composition : {key}.')
    if data['style']['sha256'] != digest(STYLE_PATH) or data['font']['sha256'] != digest(FONT_PATH):
        raise ValueError('Le calque ne correspond pas à la charte et à la police courantes.')
    if not isinstance(data.get('illustration_ia'), bool):
        raise ValueError('Origine de la photographie non spécifiée.')
    lines = json.loads(Path(data['headline']['path']).read_text(encoding='utf-8'))
    svg = typo.render_overlay(lines, data['illustration_ia'], data['format'])
    if Path(data['overlay_svg']['path']).read_text(encoding='utf-8') != svg:
        raise ValueError('Le calque SVG ne correspond pas au texte et à la charte.')
    expected_overlay = raster(svg)
    with Image.open(data['overlay_png']['path']) as im:
        actual_overlay = im.convert('RGBA')
    if actual_overlay.size != expected_overlay.size or actual_overlay.tobytes() != expected_overlay.tobytes():
        raise ValueError('Le calque PNG ne correspond pas aux tracés canoniques.')
    expected = Image.alpha_composite(background(data['photo']['path'], data['format']), expected_overlay).convert('RGB')
    with Image.open(image) as im:
        if im.format != 'PNG':
            raise ValueError('Le fichier livré doit être le PNG composé.')
        actual = im.convert('RGB')
        if im.convert('RGBA').getchannel('A').getextrema() != (255, 255):
            raise ValueError('Le fichier composé ne doit pas avoir de transparence.')
    if list(actual.size) != data['dimensions'] or actual.size != expected.size or actual.tobytes() != expected.tobytes():
        raise ValueError('Le fichier final ne correspond pas à la photo avec le calque appliqué.')
    return {'composition_verified': True, 'image': str(image),
            'output_sha256': digest(image), 'style_sha256': digest(STYLE_PATH),
            'font_sha256': digest(FONT_PATH), 'editorial_quality_verified': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    make = sub.add_parser('compose')
    make.add_argument('--photo', required=True, type=Path)
    make.add_argument('--headline-json', required=True, type=Path)
    make.add_argument('--output', required=True, type=Path)
    make.add_argument('--authentic-photo', action='store_true', help='Omit Illustration IA only for a genuinely ungenerated photo')
    make.add_argument('--format', choices=['4:5', '1:1', '9:16'], default='4:5')
    check = sub.add_parser('verify')
    check.add_argument('--composition', required=True, type=Path)
    check.add_argument('--image', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'compose':
            result = compose(args.photo, args.headline_json, args.output, not args.authentic_photo, args.format)
        else:
            result = verify(args.composition, args.image)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({'valid': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

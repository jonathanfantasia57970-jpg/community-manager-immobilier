#!/usr/bin/env python3
"""Render only vector typography; never opens or alters a photograph.

Requires fontTools and PyMuPDF. Outputs outlined SVG plus transparent PNG.
For final layout, import the PNG/SVG unchanged into the composing application.
"""
import argparse
import os
from copy import deepcopy
import json
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
STYLE_PATH = Path(os.environ.get('CM_CHARTE', ROOT / 'assets/charte-linkedin.json')).resolve()
STYLE = json.loads(STYLE_PATH.read_text())


def layout(format_name='4:5'):
    heights = {'4:5': 1350, '1:1': 1080, '9:16': 1920}
    if format_name not in heights:
        raise ValueError('Format non pris en charge : choisir 4:5, 1:1 ou 9:16.')
    style = deepcopy(STYLE)
    offset = heights[format_name] - style['canvas']['height']
    style['canvas']['height'] += offset
    style['signature']['y'] += offset
    style['disclosure']['baseline'] += offset
    return style


@lru_cache(maxsize=4)
def font(weight):
    source = TTFont(ROOT / 'assets' / STYLE['font'])
    return instantiateVariableFont(source, {'wght': weight}, inplace=True)


def measure(text, weight, size):
    f = font(weight)
    cmap = f.getBestCmap()
    for c in text:
        if ord(c) not in cmap:
            raise ValueError(f'Unsupported character: {c!r}')
    return sum(f['hmtx'][cmap[ord(c)]][0] for c in text) * size / f['head'].unitsPerEm


def outline(text, weight, size, x, baseline, color):
    f = font(weight)
    glyphs, cmap = f.getGlyphSet(), f.getBestCmap()
    scale = size / f['head'].unitsPerEm
    paths = []
    for c in text:
        name = cmap[ord(c)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        if pen.getCommands():
            paths.append(f'<path fill="{color}" transform="translate({x:.4f} {baseline:.4f}) scale({scale:.8f} {-scale:.8f})" d="{pen.getCommands()}"/>')
        x += f['hmtx'][name][0] * scale
    return ''.join(paths), x


def signature():
    name = STYLE['signature'].get('name')
    if not name or name in {'le conseiller', '{NOM_CONSEILLER}'} or 'CONFIG_' in name:
        raise ValueError('Configurer le nom du conseiller avec configurer_charte.py et CM_CHARTE avant rendu.')
    s, c = STYLE['signature'], STYLE['colors']
    parts = [f'<rect width="{s["rule_width"]}" height="{s["rule_height"]}" fill="{c["accent"]}"/>']
    for text, weight, size, y in [(s['name'], s['name_weight'], s['name_size'], s['name_baseline'])] + [(line, s['role_weight'], s['role_size'], s['role_baseline'] + i*s['role_line_height']) for i, line in enumerate(s['role_lines'])]:
        if measure(text, weight, size) > s['width']:
            raise ValueError('Signature exceeds its fixed width')
        parts.append(outline(text, weight, size, 0, y, c.get('text', c['white']))[0])
    return ''.join(parts)


def render_signature():
    s = STYLE['signature']
    return svg(s['width'], s['height'], signature(), s['name'] + ' — ' + ' '.join(s['role_lines']))


def svg(width, height, content, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><title>{escape(title)}</title>{content}</svg>'


def render_overlay(lines, illustration_ia=False, format_name='4:5'):
    style = layout(format_name)
    c, h, page, s = style['colors'], style['headline'], style['canvas'], style['signature']
    if not isinstance(lines, list) or not 1 <= len(lines) <= h['max_lines'] or any(not isinstance(line, list) or not line for line in lines):
        raise ValueError('Provide one to four nonempty headline lines')
    if any(not isinstance(span, dict) or not isinstance(span.get('text'), str) or not span['text'] for line in lines for span in line):
        raise ValueError('Each span needs nonempty text')
    if any(not isinstance(span.get('accent', False), bool) for line in lines for span in line):
        raise ValueError('Accent must be a boolean')
    if any(not ''.join(span['text'] for span in line).strip() for line in lines):
        raise ValueError('Headline lines cannot contain only whitespace')
    available = page['width'] - 2*page['margin']
    widest = max(sum(measure(span['text'], h['weight'], h['size']) for span in line) for line in lines)
    size = min(h['size'], h['size'] * available / widest)
    if size < h['min_size']:
        raise ValueError('Headline too long: reflow or rewrite; do not reduce the fixed minimum size')
    parts = []
    for i, line in enumerate(lines):
        x = page['margin']
        for span in line:
            path, x = outline(span['text'], h['weight'], size, x, h['baseline'] + i*size*h['line_height'], c['accent'] if span.get('accent') else c.get('text', c['white']))
            parts.append(path)
    parts.append(f'<g transform="translate({s["x"]} {s["y"]})">{signature()}</g>')
    if illustration_ia:
        d = style['disclosure']
        parts.append(outline(d['text'], d['weight'], d['size'], d['x'], d['baseline'], c.get('text', c['white']))[0])
    return svg(page['width'], page['height'], ''.join(parts), ' '.join(span['text'] for line in lines for span in line))


def save(content, output):
    import fitz
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.svg').write_text(content)
    doc = fitz.open(stream=content.encode(), filetype='svg')
    doc[0].get_pixmap(alpha=True).save(output.with_suffix('.png'))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--signature', action='store_true')
    group.add_argument('--headline-json', type=Path, help='JSON array of lines; each line contains {text, accent?} spans')
    p.add_argument('--output', required=True, type=Path, help='Output stem or .svg/.png path')
    p.add_argument('--illustration-ia', action='store_true', help='Add the fixed disclosure for a synthetic scene')
    p.add_argument('--format', choices=['4:5', '1:1', '9:16'], default='4:5')
    a = p.parse_args()
    content = render_signature() if a.signature else render_overlay(json.loads(a.headline_json.read_text()), a.illustration_ia, a.format)
    save(content, a.output)
    print(json.dumps({'svg': str(a.output.with_suffix('.svg')), 'png': str(a.output.with_suffix('.png'))}))

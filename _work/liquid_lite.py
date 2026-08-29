# -*- coding: utf-8 -*-
"""A tiny evaluator for the illustration and ornament snippets.

Not a Liquid implementation — just enough to pull the real SVG out of the two
snippets so the static preview shows the same artwork the storefront will,
instead of a hand-copied duplicate that drifts.

Both snippets are a single {% case name %} whose branches contain only literal
SVG plus {{ c }} (tone colour), {{ s }} / {{ h }} (size) and {{ u }} (uid).
"""
import re, os

TONES = {
    'brass': '#B0854A',
    'oud':   '#6C4824',
    'ink':   '#14100C',
    'bone':  '#EFE6D6',
}


def _branches(path):
    src = open(path, encoding='utf-8').read()
    # strip the doc comment so its examples are never mistaken for markup
    src = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', src, flags=re.S)
    out = {}
    for m in re.finditer(
            r"\{%-?\s*when\s+'([a-z0-9-]+)'\s*-?%\}(.*?)(?=\{%-?\s*when\s|\{%-?\s*endcase)",
            src, re.S):
        out[m.group(1)] = m.group(2)
    return out


ILL = _branches(os.path.join('..', 'snippets', 'illustration.liquid'))
ORN = _branches(os.path.join('..', 'snippets', 'ornament.liquid'))


def _resolve(body, tone, size, uid, opacity):
    c = TONES.get(tone, 'currentColor')
    reps = {
        'c': c, 'u': uid or tone, 's': str(size), 'h': str(size),
        'size': str(size), 'tone': tone,
        'opacity': str(opacity), 'o': str(opacity),
    }

    # {%- liquid ... -%} blocks inside a branch only compute local defaults;
    # drop them and rely on the substitutions above.
    body = re.sub(r'\{%-?\s*liquid.*?-?%\}', '', body, flags=re.S)
    body = re.sub(r'\{%-?\s*assign.*?-?%\}', '', body, flags=re.S)

    # {{ x | filter: y }} -> the bare variable
    def var(m):
        name = m.group(1).split('|')[0].strip()
        return reps.get(name, '')
    body = re.sub(r'\{\{\s*([^}]+?)\s*\}\}', var, body)

    # unresolved control flow would only leak tags into the page
    body = re.sub(r'\{%.*?%\}', '', body, flags=re.S)
    return body.strip()


def illustration(name, tone='brass', size=None, uid=None, opacity=0.28):
    body = ILL.get(name)
    if body is None:
        return f'<!-- illustration {name} not found -->'
    if size is None:
        size = {'soundwave-line': 20, 'tile-pattern': 420, 'waveform': 64,
                'plectrum': 14}.get(name, 120)
    return _resolve(body, tone, size, uid, opacity)


def ornament(name, tone='brass', size=None):
    body = ORN.get(name)
    if body is None:
        return f'<!-- ornament {name} not found -->'
    return _resolve(body, tone, size or 18, tone, 1)


if __name__ == '__main__':
    print('illustration branches:', sorted(ILL))
    print('ornament branches   :', sorted(ORN))
    for n in sorted(ILL):
        svg = illustration(n)
        print(f'  {n:18} {len(svg):5} chars  starts {svg[:40]!r}')

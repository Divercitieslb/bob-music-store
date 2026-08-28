# -*- coding: utf-8 -*-
"""Vector riq mark, drawn to match the supplied Bob Music Store logo.

The riq (the O of BOB) cannot be lifted out of the raster because the letter
strokes pass behind it. Redrawing it geometrically gives a mark that is crisp
at 16px and at 1000px, in the logo's own palette and ornament language.

Structure, outside in:
  brass jingle discs -> cream rim -> dark arabesque band -> dark hoop -> cream head
"""
import math, os

INK    = '#2E2318'   # the deep brown of the letterforms
BAND   = '#6B4526'   # arabesque band
BRASS  = '#B8873F'   # jingles
CREAM  = '#F2EADA'   # drum head / rim
BONE   = '#EFE6D6'


def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def star4(cx, cy, r_out, r_in, rot=0.0):
    pts = []
    for i in range(8):
        a = rot + i * 45.0
        r = r_out if i % 2 == 0 else r_in
        pts.append(pol(cx, cy, r, a))
    return 'M ' + ' L '.join(f'{x:.2f},{y:.2f}' for x, y in pts) + ' Z'


def ring(cx, cy, r_out, r_in):
    return (f'M {cx-r_out:.2f},{cy:.2f} '
            f'A {r_out:.2f},{r_out:.2f} 0 1,0 {cx+r_out:.2f},{cy:.2f} '
            f'A {r_out:.2f},{r_out:.2f} 0 1,0 {cx-r_out:.2f},{cy:.2f} Z '
            f'M {cx-r_in:.2f},{cy:.2f} '
            f'A {r_in:.2f},{r_in:.2f} 0 1,1 {cx+r_in:.2f},{cy:.2f} '
            f'A {r_in:.2f},{r_in:.2f} 0 1,1 {cx-r_in:.2f},{cy:.2f} Z')


def disc(cx, cy, r):
    return (f'M {cx-r:.2f},{cy:.2f} '
            f'A {r:.2f},{r:.2f} 0 1,0 {cx+r:.2f},{cy:.2f} '
            f'A {r:.2f},{r:.2f} 0 1,0 {cx-r:.2f},{cy:.2f} Z')


def riq(size=200, simple=False):
    """simple=True drops the fine lattice - used for favicon sizes."""
    c = size / 2
    R = size / 2
    p = []

    r_jingle_ring = R * 0.845
    r_jingle = R * 0.150
    r_rim_out = R * 0.815
    r_band_out = R * 0.760
    r_band_in = R * 0.610
    r_hoop_out = R * 0.585
    r_hoop_in = R * 0.545
    r_head = R * 0.535

    # brass jingles peeking out behind the rim
    for i in range(8):
        x, y = pol(c, c, r_jingle_ring, i * 45.0 + 22.5)
        p.append(f'<path d="{disc(x, y, r_jingle)}" fill="{BRASS}"/>')

    # cream rim
    p.append(f'<path d="{disc(c, c, r_rim_out)}" fill="{CREAM}"/>')
    p.append(f'<path d="{ring(c, c, r_rim_out, r_rim_out - R*0.018)}" fill="{INK}" opacity=".55"/>')

    # dark arabesque band
    p.append(f'<path d="{ring(c, c, r_band_out, r_band_in)}" fill="{BAND}"/>')

    if not simple:
        r_mid = (r_band_out + r_band_in) / 2
        cell = (r_band_out - r_band_in) * 0.48
        for i in range(16):
            x, y = pol(c, c, r_mid, i * 22.5)
            p.append(f'<path d="{star4(x, y, cell, cell*0.40, i*22.5)}" fill="{CREAM}" opacity=".92"/>')
        # hairlines top and bottom of the band
        p.append(f'<path d="{ring(c, c, r_band_out, r_band_out - R*0.014)}" fill="{CREAM}"/>')
        p.append(f'<path d="{ring(c, c, r_band_in + R*0.014, r_band_in)}" fill="{CREAM}"/>')

    # dark hoop + cream head
    p.append(f'<path d="{ring(c, c, r_hoop_out, r_hoop_in)}" fill="{INK}"/>')
    p.append(f'<path d="{disc(c, c, r_head)}" fill="{BONE}"/>')

    return '\n  '.join(p)


def svg(size, simple=False, bg=None, pad=0.0):
    box = size
    b = f'<rect width="{box}" height="{box}" fill="{bg}"/>' if bg else ''
    inner = riq(size * (1 - pad * 2), simple)
    off = size * pad
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {box} {box}" '
            f'role="img" aria-label="Bob Music Store">'
            f'<title>Bob Music Store</title>{b}'
            f'<g transform="translate({off},{off})">\n  {inner}\n</g></svg>')


A = '../assets'
os.makedirs(A, exist_ok=True)
open(f'{A}/mark.svg', 'w', encoding='utf-8').write(svg(200))
open(f'{A}/favicon.svg', 'w', encoding='utf-8').write(svg(64, simple=True, bg=INK, pad=0.06))
print('mark.svg + favicon.svg written')

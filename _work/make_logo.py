# -*- coding: utf-8 -*-
"""Generate the Bob Music identity.

The mark is the pierced rosette (shamsa) cut into the soundboard of an oud -
the one object that belongs equally to the Arabic half of this catalogue and
to the guitars on the other wall. It replaces the O of BOB.

Everything is built from real geometry (no traced curves) so it holds at
16px favicon size and at 2000px banner size, and it is drawn as separate
filled shapes rather than even-odd cut-outs so rendering is predictable.
"""
import math, os

INK   = '#14110F'
BRASS = '#C08A3E'
OUD   = '#8A5A32'
BONE  = '#F4F0E9'


def circle(cx, cy, r):
    """Full circle as two arcs - a single near-360 arc leaves a visible nick."""
    return (f'M {cx-r:.3f},{cy:.3f} '
            f'A {r:.3f},{r:.3f} 0 1,0 {cx+r:.3f},{cy:.3f} '
            f'A {r:.3f},{r:.3f} 0 1,0 {cx-r:.3f},{cy:.3f} Z')


def annulus(cx, cy, r_out, r_in):
    """Ring: outer circle clockwise, inner circle anticlockwise (nonzero fill)."""
    return (f'M {cx-r_out:.3f},{cy:.3f} '
            f'A {r_out:.3f},{r_out:.3f} 0 1,0 {cx+r_out:.3f},{cy:.3f} '
            f'A {r_out:.3f},{r_out:.3f} 0 1,0 {cx-r_out:.3f},{cy:.3f} Z '
            f'M {cx-r_in:.3f},{cy:.3f} '
            f'A {r_in:.3f},{r_in:.3f} 0 1,1 {cx+r_in:.3f},{cy:.3f} '
            f'A {r_in:.3f},{r_in:.3f} 0 1,1 {cx-r_in:.3f},{cy:.3f} Z')


def star(cx, cy, n, r_out, r_in, phase=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        a = phase + math.pi * i / n
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return 'M ' + ' L '.join(f'{x:.3f},{y:.3f}' for x, y in pts) + ' Z'


def rosette(size=120, colour=BRASS, n=12):
    """Concentric oud rosette: rim ring, ring of pierced dots, 12-point star."""
    c = size / 2
    R = size / 2
    g = [f'<path d="{annulus(c, c, R, R * 0.895)}" fill="{colour}"/>']

    # ring of dots, sitting in the open field between rim and star
    r_ring = R * 0.735
    r_dot = R * 0.072
    for i in range(n * 2):
        a = 2 * math.pi * i / (n * 2) - math.pi / 2
        g.append(f'<path d="{circle(c + r_ring*math.cos(a), c + r_ring*math.sin(a), r_dot)}" fill="{colour}"/>')

    # thin inner ring framing the star
    g.append(f'<path d="{annulus(c, c, R*0.585, R*0.535)}" fill="{colour}"/>')
    # the 12-point star itself
    g.append(f'<path d="{star(c, c, n, R*0.455, R*0.245)}" fill="{colour}"/>')
    return '\n  '.join(g)


def logo(width=620, ink=INK, accent=BRASS, sub=None):
    """B [rosette] B over spaced MUSIC. The rosette is the O."""
    sub = sub or accent
    h = 168
    # B is set at 112px; its cap height is ~80px spanning y=24..104, centre y=64.
    # The rosette is sized to that cap height and optically centred on it.
    ros = 86
    bx1, ros_x, bx2 = 8, 100, 204
    ros_y = 64 - ros / 2
    g = rosette(ros, accent)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" role="img" aria-label="Bob Music">
  <title>Bob Music</title>
  <text x="{bx1}" y="104" font-family="'Space Grotesk','Helvetica Neue',Arial,sans-serif"
        font-size="112" font-weight="700" fill="{ink}">B</text>
  <g transform="translate({ros_x},{ros_y:.1f})">
  {g}
  </g>
  <text x="{bx2}" y="104" font-family="'Space Grotesk','Helvetica Neue',Arial,sans-serif"
        font-size="112" font-weight="700" fill="{ink}">B</text>
  <text x="13" y="147" font-family="'Space Mono','SFMono-Regular',monospace"
        font-size="22" letter-spacing="39.5" fill="{sub}">MUSIC</text>
</svg>'''


def mark_svg(size=120, colour=BRASS, bg=None):
    b = f'<rect width="{size}" height="{size}" rx="0" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'role="img" aria-label="Bob Music"><title>Bob Music</title>{b}\n  '
            f'{rosette(size, colour)}\n</svg>')


A = '../assets'
os.makedirs(A, exist_ok=True)
os.makedirs('../brand', exist_ok=True)

open(f'{A}/logo.svg', 'w', encoding='utf-8').write(logo())
open(f'{A}/logo-light.svg', 'w', encoding='utf-8').write(logo(ink=BONE, accent=BRASS))
open(f'{A}/mark.svg', 'w', encoding='utf-8').write(mark_svg(120, BRASS))
open(f'{A}/mark-ink.svg', 'w', encoding='utf-8').write(mark_svg(120, INK))
open(f'{A}/favicon.svg', 'w', encoding='utf-8').write(mark_svg(64, BRASS, INK))
print('identity written')

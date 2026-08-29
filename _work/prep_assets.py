# -*- coding: utf-8 -*-
"""Normalise the generated artwork for a Shopify theme.

Three problems with the files as delivered:
  * double extensions (hero-shop.jpg.jpg) and spaces/ampersands in names —
    Shopify asset URLs cannot carry those
  * 6-7 MB PNGs — 55 MB of assets against a 50 MB theme limit
  * far larger than any viewport needs

Resized to the largest size the layout actually requests, re-encoded as
progressive JPEG, and renamed to the slot each one fills.
"""
import os
from PIL import Image, ImageOps

A = '../assets'

# source filename -> (clean name, max width)
PLAN = {
    'hero-shop.jpg.jpg':                          ('hero-shop.jpg',          2200),
    'band-bench.jpg.png':                         ('band-bench.jpg',         2600),
    'feature-oud.jpg.png':                        ('feature-oud.jpg',        1800),
    'feature-percussion.jpg.png':                 ('feature-percussion.jpg', 1600),
    'look-oud.jpg.jpg':                           ('look-oud.jpg',           1800),
    'look-oud2.jpg.jpg':                          ('look-oud-wide.jpg',      2400),
    'look-darbuka.jpg.jpg':                       ('look-darbuka.jpg',       1500),
    'look-accordion.jpg.jpg':                     ('look-accordion.jpg',     1500),
    'look-audio.jpg.png':                         ('look-audio.jpg',         1800),
    'story-shop.jpg.png':                         ('story-shop.jpg',         1800),
    'Guitars & Bass Collection Banner.png':       ('banner-guitars.jpg',     2400),
    'Strings & Accessories Collection Banner.png':('banner-accessories.jpg', 2400),
    'Violins & Wind Collection Banner.png':       ('banner-violins-wind.jpg', 2400),
}

before = after = 0
rows = []
for src, (dst, maxw) in PLAN.items():
    p = os.path.join(A, src)
    if not os.path.exists(p):
        rows.append((src, 'MISSING', '', ''))
        continue
    b = os.path.getsize(p)
    before += b

    im = Image.open(p)
    im = ImageOps.exif_transpose(im).convert('RGB')
    w0, h0 = im.size
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)

    out = os.path.join(A, dst)
    im.save(out, 'JPEG', quality=82, optimize=True, progressive=True, subsampling=1)
    a = os.path.getsize(out)
    after += a
    rows.append((src, dst, f'{w0}x{h0} -> {im.width}x{im.height}',
                 f'{b/1048576:.1f} -> {a/1024:.0f} KB'))
    if src != dst:
        os.remove(p)

for r in rows:
    print(f'  {r[0][:44]:46} {r[1]:26} {r[2]:24} {r[3]}')

total = sum(os.path.getsize(os.path.join(A, f)) for f in os.listdir(A))
print(f'\nartwork  {before/1048576:.1f} MB -> {after/1048576:.1f} MB')
print(f'assets/  {total/1048576:.1f} MB total   (Shopify theme limit 50 MB)')

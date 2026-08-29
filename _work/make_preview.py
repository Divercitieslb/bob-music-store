# -*- coding: utf-8 -*-
"""Render static previews that mirror what the Liquid templates output.

Shopify Liquid cannot run locally without a store, so this reproduces the same
markup and class names against the real stylesheet, the real retouched images
and the real product data. It is a design proof, not part of the theme.
"""
import csv, os, collections, html, random
import taxonomy as T

CSV = '../import/bob-music-products.csv'
IMG = 'import/images/'
OUT = '..'

rows = list(csv.DictReader(open(CSV, encoding='utf-8')))
prods = [r for r in rows if r['Title']]
imgs_by_handle = collections.defaultdict(list)
for r in rows:
    if r['Image Src']:
        imgs_by_handle[r['Handle']].append(r['Image Src'].rsplit('/', 1)[-1])

by_tag = collections.defaultdict(list)
for p in prods:
    for t in p['Tags'].split(','):
        by_tag[t.strip()].append(p)


def esc(s):
    return html.escape(s or '', quote=True)


def card(p, eager=False):
    ims = imgs_by_handle.get(p['Handle'], [])
    src = IMG + ims[0] if ims else ''
    alt2 = f'<img src="{IMG}{ims[1]}" alt="" loading="lazy" aria-hidden="true">' if len(ims) > 1 else ''
    vendor = p['Vendor']
    vend = f'<p class="card__vendor">{esc(vendor)}</p>' if vendor not in ('Unbranded', 'Generic', 'Handmade', '') else ''
    badge = ''
    if 'Vintage & Collectible' in p['Tags']:
        badge = '<span class="badge badge--vintage">Vintage</span>'
    return f'''<article class="card">
  <div class="card__media {'card__media--alt' if alt2 else ''}">
    <img src="{src}" alt="{esc(p['Title'])}" width="700" height="700" loading="{'eager' if eager else 'lazy'}">{alt2}{badge}
  </div>
  <div class="card__body">{vend}
    <h3 class="card__title"><a href="preview-product.html">{esc(p['Title'])}</a></h3>
    <p class="card__price"><span class="price--ask">Price on request</span></p>
  </div>
</article>'''


HEAD = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Bob Music Store</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Karla:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/base.css">
<link rel="icon" href="assets/favicon.svg">
</head><body>
<a class="skip-link" href="#main">Skip to content</a>

<div class="announce"><div class="wrap"><div class="announce__inner">
  <span>Free delivery across Lebanon on orders over $150</span>
</div></div></div>

<header class="header">
  <div class="wrap"><div class="header__bar">
    <button class="icon-btn header__burger" aria-label="Open menu">
      <svg width="22" height="22" viewBox="0 0 20 20" fill="none"><path d="M2.5 5.5h15M2.5 10h15M2.5 14.5h15" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
    </button>
    <a class="header__logo" href="preview-home.html"><img src="assets/logo-primary.png" alt="Bob Music Store" width="1147" height="765"></a>
    <nav class="header__nav"><ul class="nav">{nav}</ul></nav>
    <div class="header__actions">
      <button class="icon-btn" aria-label="Search"><svg width="21" height="21" viewBox="0 0 20 20" fill="none"><circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.4"/><path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></button>
      <a class="icon-btn" href="#" aria-label="Account"><svg width="21" height="21" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="7" r="3.2" stroke="currentColor" stroke-width="1.4"/><path d="M3.8 17c.6-3.2 3.1-5 6.2-5s5.6 1.8 6.2 5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></a>
      <a class="icon-btn" href="#" aria-label="Cart"><svg width="21" height="21" viewBox="0 0 20 20" fill="none"><path d="M2.5 3h2l1.8 9.2a1.5 1.5 0 001.5 1.2h6.9a1.5 1.5 0 001.5-1.2L18 6H5.3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="8.5" cy="17" r="1.2" fill="currentColor"/><circle cx="15" cy="17" r="1.2" fill="currentColor"/></svg><span class="cart-count">2</span></a>
    </div>
  </div></div>
</header>
<main id="main">'''

DIVIDER = '''<div class="orn-divider orn-divider--center"><span class="orn-divider__rule"></span>
<svg width="60" height="18" viewBox="0 0 60 18" fill="none" aria-hidden="true">
<path d="M0 9h14M46 9h14" stroke="#B0854A" stroke-width="1"/>
<path d="M19 9 23 5 27 9 23 13Z" fill="#B0854A" opacity=".75"/><path d="M33 9 37 5 41 9 37 13Z" fill="#B0854A" opacity=".75"/>
<path d="M30 0.2 32.6 3.6 36.6 2.4 35.4 6.4 38.8 9 35.4 11.6 36.6 15.6 32.6 14.4 30 17.8 27.4 14.4 23.4 15.6 24.6 11.6 21.2 9 24.6 6.4 23.4 2.4 27.4 3.6Z" fill="#B0854A"/>
</svg><span class="orn-divider__rule"></span></div>'''

FOOT = '''</main>
<footer class="footer"><div class="wrap">
  <div class="footer__grid">
    <div class="footer__brand">
      <div class="footer__lockup">
        <img src="assets/mark.svg" alt="" width="56" height="56">
        <p class="nm">BOB</p>
        <p class="tg">All instruments. One passion.</p>
      </div>
      <p>A music shop in Beirut. Arabic percussion and ouds beside guitars, amplification and studio gear — every instrument checked on the bench before it goes out the door.</p>
      <div class="social">
        <a href="#" aria-label="Instagram"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.6"/><circle cx="17.2" cy="6.8" r="1.2" fill="currentColor"/></svg></a>
        <a href="#" aria-label="WhatsApp"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1112 20.2z"/></svg></a>
      </div>
    </div>
    <div><h4>Shop</h4><ul>{fcols}</ul></div>
    <div><h4>Help</h4><ul>
      <li><a href="#">Delivery &amp; returns</a></li><li><a href="#">Set-up service</a></li>
      <li><a href="#">Trade-in</a></li><li><a href="#">Contact</a></li></ul></div>
    <div><h4>Visit us</h4><ul>
      <li>Beirut, Lebanon</li><li><a href="#">+961 …</a></li>
      <li style="margin-top:.6rem;opacity:.75">Mon–Sat, 9:00–19:00</li></ul></div>
  </div>
  <div class="footer__bottom"><span>© 2026 Bob Music Store. All rights reserved.</span><span>Beirut, Lebanon</span></div>
</div></footer></body></html>'''


def nav_html():
    out = []
    for fh, ft in T.FAMILY.items():
        leaves = [(h, v[0]) for h, v in T.LEAF.items() if v[1] == fh]
        sub = ''.join(f'<li><a href="preview-collection.html">{esc(t)}</a></li>' for _h, t in leaves)
        mega = f'''<div class="mega"><div class="mega__inner">
          <div class="mega__col"><h3>{esc(ft)}</h3><ul class="mega__list">{sub}</ul></div>
          <div class="mega__col"><h3>Browse</h3><ul class="mega__list">
            <li><a href="#">New arrivals</a></li><li><a href="#">Vintage &amp; collectible</a></li>
            <li><a href="#">Beginner &amp; student</a></li><li><a href="#">Arabic instruments</a></li></ul></div>
          <div class="mega__feature"><p class="eyebrow">The bench</p><h3 class="h3">Played before it ships</h3>
            <p>Every instrument is checked, tuned and set up by hand before it leaves the shop.</p>
            <a class="link-arrow" href="#">Explore <svg width="14" height="10" viewBox="0 0 14 10" fill="none"><path d="M1 5h11M8.5 1.5L12 5l-3.5 3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a></div>
        </div></div>''' if leaves else ''
        chev = '<svg class="nav__chev" width="10" height="6" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        out.append(f'<li class="nav__item"><a class="nav__link" href="preview-collection.html">{esc(ft)} {chev}</a>{mega}</li>')
    return ''.join(out)


FCOLS = ''.join(f'<li><a href="#">{esc(t)}</a></li>' for t in list(T.FAMILY.values())[:6])
NAV = nav_html()


def page(name, title, body):
    open(f'{OUT}/{name}', 'w', encoding='utf-8').write(
        HEAD.format(title=title, nav=NAV) + body + FOOT.format(fcols=FCOLS))


# ---------------------------------------------------------------- home ----
hero_img = IMG + (imgs_by_handle.get('handmade-oud-carved-flower-rosette-two-tone-inlaid-bowl') or ['OUD-01-01.jpg'])[0]

tiles = []
for h, t in [('Darbuka', 'darbuka'), ('Oud', 'oud'), ('Guitars & Bass', 'guitars'),
             ('Accordions', 'accordions'), ('Audio & Studio', 'audio-studio'),
             ('Violins & Wind', 'violins-wind')]:
    ps = by_tag.get(h, [])
    im = IMG + imgs_by_handle[ps[0]['Handle']][0] if ps and imgs_by_handle.get(ps[0]['Handle']) else ''
    tiles.append(f'''<a class="tile" href="preview-collection.html">
      <img src="{im}" alt="{esc(h)}" loading="lazy">
      <div class="tile__label"><h3>{esc(h)}</h3><span>{len(ps)} products</span></div></a>''')

tabs = [('Darbuka', 'Darbuka'), ('Oud', 'Oud'), ('Guitars & Bass', 'Guitars'),
        ('Accordions', 'Accordions'), ('Microphones', 'Microphones')]
tab_btns, panels = [], []
for i, (tag, label) in enumerate(tabs):
    tab_btns.append(f'<button class="chip" aria-selected="{"true" if i == 0 else "false"}">{label}</button>')
    ps = by_tag.get(tag, [])[:10]
    panels.append(f'<div class="grid grid--products" {"" if i == 0 else "hidden"}>' +
                  ''.join(card(p) for p in ps) + '</div>')

home = f'''
<section class="hero">
  <div class="hero__media"><img src="{hero_img}" alt=""></div>
  <div class="hero__inner"><div class="hero__content">
    <p class="eyebrow">Beirut · All instruments. One passion.</p>
    <h1 class="h-display">Where the oud meets the amplifier</h1>
    <p class="lede">Two hundred and sixty-eight instruments under one roof — hand-inlaid darbukas and Egyptian ouds beside Fender, Shure and BOSS. Checked on the bench, played before it ships.</p>
    <div class="hero__cta">
      <a class="btn btn--light" href="preview-collection.html">Shop the catalogue</a>
      <a class="btn btn--outline-light" href="preview-collection.html">Arabic instruments</a>
    </div>
  </div></div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">The catalogue</p><h2 class="h1">Shop by instrument</h2>
        <p class="lede">Seven families, forty-three collections. Everything in the shop, sorted the way a player looks for it.</p></div>
      <a class="link-arrow" href="#">All collections <svg width="14" height="10" viewBox="0 0 14 10" fill="none"><path d="M1 5h11M8.5 1.5L12 5l-3.5 3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    </div>
    <div class="grid grid--3">{''.join(tiles)}</div>
  </div>
</section>

<section class="section section--shell">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">In the shop now</p><h2 class="h1">Featured products</h2></div></div>
    <div class="chiprow" style="margin-bottom:2rem">{''.join(tab_btns)}</div>
    {''.join(panels)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid--2" style="align-items:center;gap:clamp(2rem,5vw,5rem)">
      <div>
        <p class="eyebrow">The shop</p>
        <h2 class="h1" style="margin-bottom:1.25rem">A counter, a bench, and someone who plays</h2>
        <div class="rte"><p>Bob Music sits where two musical worlds overlap. On one wall, hand-inlaid darbukas, riqs and ouds built by makers in Egypt, Syria and Lebanon. On the other, the guitars, microphones and pedals any working band needs on a Friday night.</p>
        <p>We do not drop-ship. Everything here has been unboxed, checked and set up by hand — and if it needs a fret dressed or a head tuned before it leaves, that happens first.</p></div>
        <a class="btn btn--ghost" href="#" style="margin-top:1.5rem">Our story</a>
      </div>
      <div><img src="{IMG}{imgs_by_handle.get('vintage-ornate-oud-mother-of-pearl-stars-mosaic-inlay', ['OUD-02-01.jpg'])[0]}" alt="" style="width:100%;background:var(--shell)"></div>
    </div>
  </div>
</section>

<section class="section section--tight section--ink tile-bg">
  <div class="wrap">
    <div style="text-align:center;margin-bottom:2.5rem">
      <h2 class="h2">Why buy here</h2><div style="margin-top:1rem">{DIVIDER}</div>
    </div>
    <div class="grid grid--4">
      <div style="text-align:center;padding:1rem .5rem"><div style="color:var(--brass);display:flex;justify-content:center;margin-bottom:.9rem"><svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="M4 8h10M18 8h2M4 16h4M12 16h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="16" cy="8" r="2" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="16" r="2" stroke="currentColor" stroke-width="1.5"/></svg></div>
        <h3 class="h3" style="font-size:1.25rem;margin-bottom:.45rem">Set up on the bench</h3><p style="font-size:.92rem;color:#CFC3B0;margin:0">Checked, tuned and adjusted by hand before it leaves the shop.</p></div>
      <div style="text-align:center;padding:1rem .5rem"><div style="color:var(--brass);display:flex;justify-content:center;margin-bottom:.9rem"><svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><circle cx="6.5" cy="18" r="1.8" stroke="currentColor" stroke-width="1.5"/><circle cx="17" cy="18" r="1.8" stroke="currentColor" stroke-width="1.5"/></svg></div>
        <h3 class="h3" style="font-size:1.25rem;margin-bottom:.45rem">Delivered in Lebanon</h3><p style="font-size:.92rem;color:#CFC3B0;margin:0">Packed properly, with a hard case where the instrument needs one.</p></div>
      <div style="text-align:center;padding:1rem .5rem"><div style="color:var(--brass);display:flex;justify-content:center;margin-bottom:.9rem"><svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="M9 18V5l10-2v13" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><circle cx="6.5" cy="18" r="2.5" stroke="currentColor" stroke-width="1.5"/><circle cx="16.5" cy="16" r="2.5" stroke="currentColor" stroke-width="1.5"/></svg></div>
        <h3 class="h3" style="font-size:1.25rem;margin-bottom:.45rem">Makers we know</h3><p style="font-size:.92rem;color:#CFC3B0;margin:0">Ouds and darbukas from workshops in Egypt, Syria and Lebanon.</p></div>
      <div style="text-align:center;padding:1rem .5rem"><div style="color:var(--brass);display:flex;justify-content:center;margin-bottom:.9rem"><svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1112 20.2z"/></svg></div>
        <h3 class="h3" style="font-size:1.25rem;margin-bottom:.45rem">Ask us anything</h3><p style="font-size:.92rem;color:#CFC3B0;margin:0">Message the shop on WhatsApp — a player will answer, not a bot.</p></div>
    </div>
  </div>
</section>'''
page('preview-home.html', 'Home', home)

# The preview pane only repaints on navigation, so each band of the homepage
# also gets its own page that renders that band at the top of the viewport.
_parts = home.split('<section')
page('preview-home-2.html', 'Catalogue', '<section' + '<section'.join(_parts[2:4]))
page('preview-home-3.html', 'Story', '<section' + '<section'.join(_parts[4:]))

# ---------------------------------------------------------- collection ----
darb = by_tag.get('Darbuka', [])
facets = ''
for label, vals in [('Availability', [('In stock', 33), ('Sold', 2)]),
                    ('Vendor', [('Handmade', 24), ('Gawharet El Fan', 6), ('Power Beat', 3)]),
                    ('Finish', [('Mosaic', 18), ('Hammered metal', 4), ('Lacquer', 6), ('Marquetry', 4)])]:
    items = ''.join(
        f'<label class="facet__item"><input type="checkbox"><span>{esc(v)}</span><span class="facet__count num">{n}</span></label>'
        for v, n in vals)
    facets += f'<details class="facet" open><summary>{label} <svg class="nav__chev" width="10" height="6" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></summary><div class="facet__list">{items}</div></details>'

coll = f'''
<div class="wrap"><nav class="breadcrumb"><a href="preview-home.html">Home</a> <span>/</span> <a href="#">Percussion</a> <span>/</span> <span>Darbuka</span></nav></div>
<section class="section section--tight"><div class="wrap">
  <p class="eyebrow">{len(darb)} products</p>
  <h1 class="h1">Darbuka</h1>
  <div class="lede" style="margin-top:1rem"><p>The goblet drum at the centre of Arabic rhythm. Cast aluminium shells with tuneable synthetic heads, decorated by hand — mother-of-pearl mosaic, marquetry, hammered metal and lacquer. No two are identical.</p></div>
  <div style="margin-top:1.5rem">{DIVIDER}</div>
</div></section>
<div class="wrap"><div class="collection-layout">
  <aside class="facets">{facets}</aside>
  <div>
    <div class="toolbar"><span class="mono">{len(darb)} results</span>
      <select class="select"><option>Featured</option><option>Price, low to high</option><option>Newest</option></select></div>
    <div class="grid grid--products" style="padding-top:1.75rem">{''.join(card(p, i < 5) for i, p in enumerate(darb))}</div>
  </div>
</div></div>
<div style="height:4rem"></div>'''
page('preview-collection.html', 'Darbuka', coll)

# ------------------------------------------------------------- product ----
p = next(x for x in prods if x['Variant SKU'] == 'OUD-07')
ims = imgs_by_handle[p['Handle']]
thumbs = ''.join(
    f'<button class="pdp__thumb" aria-current="{"true" if i == 0 else "false"}"><img src="{IMG}{im}" alt=""></button>'
    for i, im in enumerate(ims))
rel = [x for x in by_tag.get('Oud', []) if x['Handle'] != p['Handle']][:5]

pdp = f'''
<div class="wrap"><nav class="breadcrumb"><a href="preview-home.html">Home</a> <span>/</span> <a href="preview-collection.html">Oud</a> <span>/</span> <span>{esc(p['Title'])}</span></nav></div>
<section class="section section--tight"><div class="wrap"><div class="pdp">
  <div class="pdp__gallery">
    <div class="pdp__main"><img src="{IMG}{ims[0]}" alt="{esc(p['Title'])}"></div>
    <div class="pdp__thumbs">{thumbs}</div>
  </div>
  <div class="pdp__info">
    <p class="eyebrow" style="margin:0">{esc(p['Vendor'])}</p>
    <h1 class="h1">{esc(p['Title'])}</h1>
    {DIVIDER}
    <p class="pdp__price"><span class="price--ask">Price on request</span></p>
    <p class="stock">One only — last in stock</p>
    <a class="btn btn--full" href="#"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2z"/></svg> Ask for a price</a>
    <a class="btn btn--ghost btn--full" style="margin-top:.6rem" href="#">Email an enquiry</a>
    <dl class="pdp__meta">
      <div><dt>SKU</dt><dd class="num">{esc(p['Variant SKU'])}</dd></div>
      <div><dt>Type</dt><dd>{esc(p['Type'])}</dd></div>
    </dl>
    <div class="rte" style="margin-top:.5rem">{p['Body (HTML)']}</div>
    <div class="acc" style="margin-top:1rem">
      <details open><summary>Shipping &amp; delivery <svg class="nav__chev" width="10" height="6" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></summary><div class="acc__body rte"><p>Delivered across Lebanon. We pack instruments ourselves — a hard case where the instrument needs one.</p></div></details>
      <details><summary>Set-up &amp; condition <svg class="nav__chev" width="10" height="6" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></summary><div class="acc__body rte"><p>Checked and set up on our bench before it ships.</p></div></details>
    </div>
  </div>
</div></div></section>
<section class="section section--shell"><div class="wrap">
  <div class="section-head"><div><p class="eyebrow">More like this</p><h2 class="h2">You may also like</h2></div></div>
  <div class="grid grid--products">{''.join(card(x) for x in rel)}</div>
</div></section>'''
page('preview-product.html', p['Title'], pdp)

# ------------------------------------------------- how we work ----
import preview_hiw
page('page-how-it-works.html', 'How we work', preview_hiw.build())

print('previews written: preview-home.html, preview-collection.html, '
      'preview-product.html, page-how-it-works.html')

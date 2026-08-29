# -*- coding: utf-8 -*-
"""Static render of the homepage, section for section against index.json.

Liquid cannot run without a store, so this mirrors the same markup and class
names using the real stylesheet, the real photography, the real product data
and — via liquid_lite — the real SVG out of snippets/illustration.liquid, so
nothing here is a hand-copied duplicate that can drift from the theme.
"""
import liquid_lite as L

BRANDS = ("Fender · Shure · BOSS · Roland · Yamaha · Audio-Technica · Epiphone · "
          "Squier · Laney · Behringer · Korg · M-Audio · D'Addario · Joyo · Mooer · "
          "Celestion · Hohner · Weltmeister · Paolo Soprani · Gawharet El Fan")

ARROW = ('<svg width="14" height="10" viewBox="0 0 14 10" fill="none">'
         '<path d="M1 5h11M8.5 1.5L12 5l-3.5 3.5" stroke="currentColor" '
         'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def wave(size=18, tone='brass'):
    return f'<div class="sec-wave">{L.illustration("soundwave-line", tone, size)}</div>'


def build(card, by_tag, IMG, imgs_by_handle, DIVIDER, hero_img, photos=None):
    P = (photos or {}).get

    # ------------------------------------------------------------- hero ----
    hero = f'''
<section class="hero hero--cinema">
  <div class="hero__stage" aria-hidden="true">
    <div class="hero__layer hero__layer--back"><img src="{P('hero-shop') or hero_img}" alt=""></div>
    <div class="hero__veil"></div><div class="hero__vignette"></div><div class="hero__glow"></div>
    <span class="hero__orn hero__orn--corner">{L.illustration('arabesque-corner','brass',96)}</span>
  </div>
  <div class="hero__inner"><div class="hero__content">
    <p class="eyebrow hero__eyebrow">{L.ornament('khatam','brass',14)} Beirut · All instruments. One passion.</p>
    <h1 class="h-display hero__title">Where the oud meets the amplifier</h1>
    <p class="lede">Hand-inlaid darbukas and Egyptian ouds on one wall. Fender, Shure and BOSS
      on the other. Every instrument checked on the bench before it leaves the shop.</p>
    <div class="hero__cta">
      <a class="btn btn--light" href="preview-collection.html">Shop the catalogue</a>
      <a class="btn btn--outline-light" href="preview-collection.html">Arabic instruments</a>
    </div>
  </div></div>
  <div class="hero__cue-wrap"><span class="hero__cue">
    <span class="hero__cue-rail"><span class="hero__cue-dot"></span></span> Scroll</span></div>
</section>'''

    # ------------------------------------------------------ brand marquee --
    marquee = ''.join(
        f'<span>{b.strip()}</span>{L.ornament("khatam","brass",11)}'
        for b in BRANDS.split('·')) * 2
    brands = f'''
<section class="marquee section--shell">
  <p class="eyebrow marquee__label">Brands we carry</p>
  <div class="marquee__track">{marquee}</div>
  <div class="marquee__wave">{L.illustration('soundwave-line','brass',14)}</div>
</section>'''

    # ----------------------------------------------------------- lookbook --
    looks = [
        ('look-oud', 'Made by hand', 'The oud',
         'Eleven instruments from workshops in Egypt, Syria and Lebanon.', 'wide'),
        ('look-darbuka', '45 in stock', 'Darbuka', 'No two shells alike.', 'narrow'),
        ('look-accordion', 'Vintage', 'Italian &amp; German accordions',
         'Castelfidardo, Klingenthal, and a Soviet bayan.', 'narrow'),
        ('look-audio', 'For the stage', 'Audio &amp; studio',
         'Microphones, amplifiers, pedals and PA.', 'wide'),
    ]
    panels = []
    for key, eyebrow, title, text, span in looks:
        p = P(key)
        media = (f'<img src="{p}" alt="{title}" loading="lazy">' if p
                 else '<div class="look__placeholder tile-bg"></div>')
        panels.append(f'''<a class="look look--{span}" href="preview-collection.html">{media}
      <div class="look__label">
        <span class="look__eyebrow">{L.illustration('plectrum','brass',11)} {eyebrow}</span>
        <h3>{title}</h3><p>{text}</p>
      </div></a>''')

    lookbook = f'''
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">The catalogue</p>
        <h2 class="h1">Two musical worlds, one shop</h2>
        {wave(20)}
        <p class="lede">Two hundred and sixty-eight instruments, sorted the way a player looks for them.</p></div>
      <a class="link-arrow" href="#">All collections {ARROW}</a>
    </div>
    <div class="lookbook">{''.join(panels)}</div>
  </div>
</section>'''

    # ------------------------------------------------------ split feature --
    def split(key, flip, eyebrow, heading, body, stats, cta, bg, wm):
        p = P(key)
        media = (f'<img src="{p}" alt="{heading}">' if p
                 else '<div class="split__placeholder tile-bg"></div>')
        st = ''
        if stats:
            st = '<dl class="split__stats">' + ''.join(
                f'<div><dt class="num">{v}</dt><dd>{l}</dd></div>' for v, l in stats) + '</dl>'
        btn = 'btn--light' if ('ink' in bg or 'espresso' in bg) else 'btn--ghost'
        return f'''<section class="split {bg} {'split--flip' if flip else ''} split--wm">
  <span class="split__wm">{L.illustration(wm,'brass',460)}</span>
  <div class="split__media">{media}</div>
  <div class="split__body">
    <span class="split__corner">{L.illustration('arabesque-corner','brass',92)}</span>
    <div class="split__inner">
      <p class="eyebrow">{eyebrow}</p>
      <h2 class="h1">{heading}</h2>
      <div style="margin:1.35rem 0 1.5rem">{DIVIDER}</div>
      <div class="rte split__text">{body}</div>
      {st}
      <a class="btn {btn}" href="preview-collection.html">{cta}</a>
    </div>
  </div>
</section>'''

    oud_room = split(
        'feature-oud', False, 'The oud room', 'An instrument you choose by ear',
        '<p>Every oud we stock is built by hand, so no two sound the same. A blonde '
        'spruce top speaks quickly and cuts through a room. A darker cedar top gives you '
        'warmth and a longer decay. The bowl — walnut, mahogany, or ribbed maple — decides '
        'how much of that sound comes back at you.</p>',
        [('11', 'Ouds in stock'), ('3', 'Countries of origin'), ('1', 'Of each, exactly')],
        'See the ouds', 'section--shell', 'oud-outline')

    percussion = split(
        'feature-percussion', True, 'Arabic percussion', 'The rhythm section of a whole region',
        '<p>Darbuka, riq, tabl and bendir — the instruments that carry Arabic music. Our '
        'darbukas come from workshops that still inlay mother-of-pearl by hand, one tessera '
        'at a time, which is why the shells in the photographs are the shells you receive.</p>',
        None, 'Shop percussion', 'section--ink', 'darbuka-outline')

    # ---------------------------------------------------------- stat band --
    figures = [('268', 'Instruments in stock', 'Every one photographed as it is'),
               ('42', 'Collections', 'Sorted the way a player looks'),
               ('81', 'Arabic instruments', 'Oud, darbuka, riq, tabl, ney'),
               ('31', 'Vintage &amp; collectible', 'One of each, exactly')]
    figs = ''.join(
        f'''<div class="statb__item">
          <dt class="statb__value num">{v}</dt>
          <dd class="statb__label">{l}<span class="statb__note">{n}</span></dd>
        </div>{L.ornament('khatam','brass',13) if i < 3 else ''}'''
        for i, (v, l, n) in enumerate(figures))
    statband = f'''
<section class="statb section--ink has-tessellation">
  <span class="sec-tess">{L.illustration('tile-pattern','brass',520,'sb',0.16)}</span>
  <div class="statb__media"><img src="{P('look-darbuka')}" alt=""></div>
  <div class="wrap statb__inner">
    <div style="text-align:center;margin-bottom:2.5rem">
      <p class="eyebrow">The shop in numbers</p>
      <h2 class="h1">What is on the wall today</h2>
    </div>
    <dl class="statb__grid">{figs}</dl>
  </div>
</section>'''

    # ------------------------------------------------------ featured tabs --
    tabs = [('Darbuka', 'Darbuka'), ('Oud', 'Oud'), ('Guitars & Bass', 'Guitars'),
            ('Accordions', 'Accordions'), ('Microphones', 'Microphones')]
    btns, pans = [], []
    for i, (tag, label) in enumerate(tabs):
        btns.append(f'<button class="chip" aria-selected="{"true" if i == 0 else "false"}">{label}</button>')
        ps = by_tag.get(tag, [])[:10]
        pans.append(f'<div class="grid grid--products"{"" if i == 0 else " hidden"}>'
                    + ''.join(card(p) for p in ps) + '</div>')
    featured = f'''
<section class="section">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">In the shop now</p>
      <h2 class="h1">Featured products</h2>{wave(18)}</div>
      <a class="link-arrow" href="#">View all {ARROW}</a></div>
    <div class="chiprow" style="margin-bottom:2rem">{''.join(btns)}</div>
    {''.join(pans)}
  </div>
</section>'''

    # -------------------------------------------------------- editorial ----
    bench = f'''
<section class="band band--tall">
  <div class="band__media"><img src="{P('band-bench')}" alt="The workbench"></div>
  <div class="band__inner wrap band__inner--left"><div class="band__content">
    <p class="eyebrow">The bench</p>
    <h2 class="h-display">Played before it ships</h2>
    <p class="lede band__lede">Nothing here is drop-shipped. Every instrument is unboxed,
      checked, tuned and set up by hand — and if it needs a fret dressed or a head brought
      up to pitch, that happens before it goes anywhere.</p>
    <a class="btn btn--light" href="#" style="margin-top:1.75rem">How we work</a>
  </div></div>
</section>'''

    # ------------------------------------------------------ scroll story ---
    chapters = [
        ('story-shop', 'One', 'It arrives',
         'Sometimes in a crate from Cairo, sometimes carried in by the person who made it.'),
        ('band-bench', 'Two', 'It goes on the bench',
         'Unboxed and checked. A fret dressed if it needs it, a head brought up to pitch.'),
        ('feature-oud', 'Three', 'It gets played',
         'Because a specification tells you nothing about how a bowl responds.'),
        ('look-oud-wide', 'Four', 'It leaves properly packed',
         'A hard case where the instrument needs one. Across Lebanon, and further when you ask.'),
    ]
    ch = ''.join(f'''<div class="ss__chapter">
        <div class="ss__inline"><img src="{P(k)}" alt=""></div>
        <p class="eyebrow">{i} · {e}</p>
        <h3 class="h2">{h}</h3>
        <p class="lede">{t}</p>
      </div>''' for i, (k, e, h, t) in
        ((c[1], c) for c in chapters))
    story = f'''
<section class="section section--shell ss">
  <div class="wrap">
    <div style="max-width:640px;margin-bottom:2.5rem">
      <p class="eyebrow">From the crate to your hands</p>
      <h2 class="h1">Four steps, every instrument</h2>{wave(18)}
    </div>
    <div class="ss__grid">
      <div class="ss__media"><img src="{P('feature-oud')}" alt=""></div>
      <div class="ss__col">{ch}</div>
    </div>
  </div>
</section>'''

    # ------------------------------------------------------------- quote ---
    quote = f'''
<section class="section qb">
  <div class="wrap qb__inner">
    <div class="qb__body">
      <div class="qb__mark">{L.illustration('rosette-draw','brass',72)}</div>
      <div style="margin:0 auto 1.5rem;max-width:320px">{DIVIDER}</div>
      <blockquote class="qb__quote">You do not choose an oud from a photograph. You choose
        it by ear, in a room, with the bowl against your chest.</blockquote>
      <p class="qb__attr">Bob<span>Behind the counter since the shop opened</span></p>
      <a class="btn btn--ghost" href="preview-collection.html" style="margin-top:1.5rem">See the ouds</a>
    </div>
    <div class="qb__media"><img src="{P('look-oud')}" alt=""></div>
  </div>
</section>'''

    # ------------------------------------------------- rest of the shop ----
    tiles = []
    for title, tag in [('Guitars & Bass', 'Guitars & Bass'),
                       ('Violins & Wind', 'Violins & Wind'),
                       ('Strings & Accessories', 'Strings & Accessories')]:
        ps = by_tag.get(tag, [])
        im = IMG + imgs_by_handle[ps[0]['Handle']][0] if ps and imgs_by_handle.get(ps[0]['Handle']) else ''
        tiles.append(f'''<a class="tile" href="preview-collection.html">
          <img src="{im}" alt="{title}" loading="lazy">
          <div class="tile__label"><h3>{title}</h3><span>{len(ps)} products</span></div></a>''')
    rest = f'''
<section class="section">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">Everything else</p>
      <h2 class="h1">The rest of the shop</h2></div>
      <a class="link-arrow" href="#">All collections {ARROW}</a></div>
    <div class="grid grid--3">{''.join(tiles)}</div>
  </div>
</section>'''

    props_items = [
        ('M4 8h10M18 8h2M4 16h4M12 16h8', 'Set up on the bench',
         'Checked, tuned and adjusted by hand before it leaves the shop.'),
        ('M2 7h11v9H2zM13 10h4l3 3v3h-7z', 'Delivered in Lebanon',
         'Packed properly, with a hard case where the instrument needs one.'),
        ('M9 18V5l10-2v13', 'Makers we know',
         'Ouds and darbukas from workshops in Egypt, Syria and Lebanon.'),
        ('M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2z', 'Ask us anything',
         'Message the shop on WhatsApp — a player will answer, not a bot.'),
    ]
    props_html = ''.join(f'''<div style="text-align:center;padding:1rem .5rem">
        <div style="color:var(--brass);display:flex;justify-content:center;margin-bottom:.9rem">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none"><path d="{d}"
            stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>
        <h3 class="h3" style="font-size:1.25rem;margin-bottom:.45rem">{t}</h3>
        <p style="font-size:.92rem;color:#CFC3B0;margin:0">{x}</p></div>'''
        for d, t, x in props_items)
    props = f'''
<section class="section section--tight section--ink has-tessellation">
  <span class="sec-tess">{L.illustration('tile-pattern','brass',520,'vp',0.16)}</span>
  <div class="wrap">
    <div style="text-align:center;margin-bottom:2.5rem">
      <h2 class="h2">Why buy here</h2><div style="margin-top:1rem">{DIVIDER}</div></div>
    <div class="grid grid--4">{props_html}</div>
  </div>
</section>'''

    return (hero + brands + lookbook + oud_room + statband + featured
            + bench + story + quote + percussion + rest + props)

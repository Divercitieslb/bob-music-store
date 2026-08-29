# -*- coding: utf-8 -*-
"""Render the How We Work page locally.

Imported by make_preview.py. It mirrors sections/how-it-works.liquid closely
enough to see the layout — the numbers, the rules between steps, the aside
panels and the closing card — without standing up a real Liquid engine. The
copy is read from templates/page.how-it-works.json so the two cannot drift.
"""
import json
import liquid_lite as L

ROOT = '..'


def build():
    d = json.load(open(f'{ROOT}/templates/page.how-it-works.json', encoding='utf-8'))
    hero = d['sections']['hero']['settings']
    sec = d['sections']['steps']
    s = sec['settings']
    props = d['sections']['props']
    closing = d['sections']['closing']['settings']

    out = []

    # --- opening band ------------------------------------------------------
    out.append(f'''
<section class="band band--short section--ink" style="--band-img:url(assets/{hero['default_asset']})">
  <div class="band__media"><img src="assets/{hero['default_asset']}" alt="{hero['image_alt']}"></div>
  <div class="band__scrim"></div>
  <div class="wrap band__inner band--left">
    <p class="eyebrow">{hero['eyebrow']}</p>
    <h1 class="h-display">{hero['heading']}</h1>
    <p class="band__text">{hero['text']}</p>
  </div>
</section>''')

    # --- the steps ---------------------------------------------------------
    steps = [sec['blocks'][k] for k in sec['block_order']]
    lis = []
    for i, b in enumerate(steps, 1):
        bs = b['settings']
        note = ''
        if bs.get('note'):
            note = (f'<p class="hiw__note">{L.illustration("plectrum", "brass", 13)}'
                    f'<span>{bs["note"]}</span></p>')
        ill = ''
        if bs.get('illustration', 'none') != 'none':
            ill = ('<div class="hiw__ill" aria-hidden="true">'
                   f'{L.illustration(bs["illustration"], "oud", 132)}</div>')
        lis.append(f'''
      <li class="hiw__step is-in">
        <div class="hiw__marker" aria-hidden="true">
          <span class="hiw__khatam">{L.ornament("khatam", "brass", 62)}</span>
          <span class="hiw__num">{i:02d}</span>
        </div>
        <div class="hiw__body">
          <h3 class="hiw__title">{bs['title']}</h3>
          <div class="hiw__text">{bs['text']}</div>
          {note}
        </div>
        {ill}
      </li>''')

    tess = ''
    if s.get('show_tile'):
        tess = ('<div class="hiw__tess" aria-hidden="true">'
                f'{L.illustration("tile-pattern", "brass", 460, uid="hiw", opacity=0.14)}</div>')

    out.append(f'''
<section class="section hiw {s.get('bg', '')}" id="main">
  {tess}
  <div class="wrap">
    <header class="hiw__head">
      <p class="eyebrow">{s['eyebrow']}</p>
      <h2 class="{s['size']}">{s['heading']}</h2>
      {L.ornament('divider', 'brass')}
      <div class="hiw__intro">{s['intro']}</div>
    </header>
    <ol class="hiw__list">{''.join(lis)}
    </ol>
    <div class="hiw__foot">
      <div class="hiw__foot-corner" aria-hidden="true">{L.illustration('arabesque-corner', 'brass', 74)}</div>
      <h3 class="h3">{s['foot_heading']}</h3>
      <p>{s['foot_text']}</p>
      <div class="hiw__foot-actions">
        <a class="btn" href="#">{s['foot_cta']}</a>
        <a class="btn btn--ghost" href="preview-collection.html">Browse the catalogue</a>
      </div>
    </div>
  </div>
</section>''')

    # --- value props -------------------------------------------------------
    pblocks = [props['blocks'][k]['settings'] for k in props['block_order']]
    cards = ''.join(
        f'<div style="text-align:center;padding:1rem .5rem">'
        f'<h3 class="h3" style="font-size:1.25rem;margin-bottom:.45rem">{p["title"]}</h3>'
        f'<p style="font-size:.92rem;color:var(--ink-60);margin:0">{p["text"]}</p></div>'
        for p in pblocks)
    out.append(f'''
<section class="section section--tight {props['settings']['bg']}">
  <div class="wrap">
    <div style="text-align:center;margin-bottom:2.5rem">
      <h2 class="h2">{props['settings']['heading']}</h2>
      <div style="margin-top:1rem">{L.ornament('divider', 'brass')}</div>
    </div>
    <div class="grid grid--4">{cards}</div>
  </div>
</section>''')

    # --- closing band ------------------------------------------------------
    out.append(f'''
<section class="band band--tall section--ink" >
  <div class="band__media"><img src="assets/{closing['default_asset']}" alt="{closing['image_alt']}"></div>
  <div class="band__scrim"></div>
  <div class="wrap band__inner band--centre">
    <p class="eyebrow">{closing['eyebrow']}</p>
    <h2 class="h1">{closing['heading']}</h2>
    <p class="band__text">{closing['text']}</p>
    <a class="btn btn--light" href="preview-collection.html">{closing['cta_label']}</a>
  </div>
</section>''')

    return '\n'.join(out)

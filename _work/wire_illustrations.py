# -*- coding: utf-8 -*-
"""Put the illustration set and the motion hooks into the actual sections.

Eight illustrations and a motion layer were built and then rendered nowhere.
This wires them in where they carry meaning rather than as decoration for its
own sake:

  soundwave-line    a divider under section headings — the shop sells sound
  tile-pattern      the ground of every ink panel, replacing the flat colour
  arabesque-corner  frames the split-feature copy column
  rosette-draw      draws itself beside the oud section as it scrolls in
  oud/darbuka-outline  large, faint, behind the family sections
  waveform          in the audio & studio panel
  plectrum          the marker on lookbook eyebrows

Plus [data-reveal] / [data-reveal-stagger] / [data-split] on the sections that
had none, so the motion layer has something to act on.
"""
import os

R = '..'
log = []


def patch(rel, pairs):
    p = os.path.join(R, rel)
    if not os.path.exists(p):
        log.append((rel, 'MISSING')); return
    s0 = s = open(p, encoding='utf-8').read()
    miss = []
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new, 1)
        else:
            miss.append(old.strip().splitlines()[0][:56])
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s)
    log.append((rel, f'{len(pairs)-len(miss)}/{len(pairs)}' + (f'  MISS {miss}' if miss else '')))


# ---------------------------------------------------------------- lookbook --
patch('sections/lookbook.liquid', [
    # a plectrum marks each eyebrow, and panels reveal in sequence
    ('<div class="lookbook">',
     '<div class="lookbook" data-reveal-stagger>'),
    ('<a class="look look--{{ block.settings.span }}" href="{{ url }}" {{ block.shopify_attributes }}>',
     '<a class="look look--{{ block.settings.span }}" href="{{ url }}" data-reveal {{ block.shopify_attributes }}>'),
    ('{%- if block.settings.eyebrow != blank -%}<span>{{ block.settings.eyebrow }}</span>{%- endif -%}',
     '''{%- if block.settings.eyebrow != blank -%}
              <span class="look__eyebrow">
                {% render 'illustration', name: 'plectrum', tone: 'brass', size: 11 %}
                {{ block.settings.eyebrow }}
              </span>
            {%- endif -%}'''),
    ('<h2 class="h1">{{ section.settings.heading }}</h2>',
     '''<h2 class="h1" data-split>{{ section.settings.heading }}</h2>
          <div class="sec-wave">{% render 'illustration', name: 'soundwave-line', tone: 'brass', size: 20 %}</div>'''),
])

# --------------------------------------------------------- split-feature ----
patch('sections/split-feature.liquid', [
    ('<div class="split__body">',
     '''<div class="split__body">
    <span class="split__corner" aria-hidden="true">
      {% render 'illustration', name: 'arabesque-corner', tone: 'brass', size: 92 %}
    </span>'''),
    ('<h2 class="h1">{{ section.settings.heading }}</h2>',
     '<h2 class="h1" data-split>{{ section.settings.heading }}</h2>'),
    ('<div class="split__inner">',
     '<div class="split__inner" data-reveal-stagger>'),
    ('<section class="split {{ section.settings.bg }} {% if flip %}split--flip{% endif %}">',
     '''<section class="split {{ section.settings.bg }} {% if flip %}split--flip{% endif %}{% if section.settings.watermark != blank %} split--wm{% endif %}">
  {%- if section.settings.watermark != blank -%}
    <span class="split__wm" aria-hidden="true">
      {% render 'illustration', name: section.settings.watermark, tone: 'brass', size: 460 %}
    </span>
  {%- endif -%}'''),
    ('{ "type": "checkbox", "id": "flip", "label": "Image on the right", "default": false },',
     '''{ "type": "checkbox", "id": "flip", "label": "Image on the right", "default": false },
    { "type": "select", "id": "watermark", "label": "Background line drawing", "default": "",
      "options": [
        { "value": "", "label": "None" },
        { "value": "oud-outline", "label": "Oud" },
        { "value": "darbuka-outline", "label": "Darbuka" },
        { "value": "rosette-draw", "label": "Oud rosette" }
      ] },'''),
])

# ------------------------------------------------------- category-grid ------
patch('sections/category-grid.liquid', [
    ('<div class="grid grid--3">', '<div class="grid grid--3" data-reveal-stagger>'),
    ('<a class="tile" href="{{ block.settings.url | default: col.url | default: \'#\' }}" {{ block.shopify_attributes }}>',
     '<a class="tile" href="{{ block.settings.url | default: col.url | default: \'#\' }}" data-reveal {{ block.shopify_attributes }}>'),
    ('<h2 class="h1">{{ section.settings.heading }}</h2>',
     '<h2 class="h1" data-split>{{ section.settings.heading }}</h2>'),
])

# ---------------------------------------------------- featured-products -----
patch('sections/featured-products.liquid', [
    ('<h2 class="h1">{{ section.settings.heading }}</h2>',
     '''<h2 class="h1" data-split>{{ section.settings.heading }}</h2>
          <div class="sec-wave">{% render 'illustration', name: 'soundwave-line', tone: 'brass', size: 18 %}</div>'''),
    ('<div class="grid grid--products" role="tabpanel" id="panel-{{ block.id }}"',
     '<div class="grid grid--products" data-reveal-stagger role="tabpanel" id="panel-{{ block.id }}"'),
])

# ----------------------------------------------------------- value-props ----
patch('sections/value-props.liquid', [
    ('<section class="section section--tight {{ section.settings.bg }} {% if section.settings.bg contains \'ink\' %}tile-bg{% endif %}">',
     '''<section class="section section--tight {{ section.settings.bg }}{% if section.settings.bg contains 'ink' or section.settings.bg contains 'espresso' %} has-tessellation{% endif %}">
  {%- if section.settings.bg contains 'ink' or section.settings.bg contains 'espresso' -%}
    <span class="sec-tess" aria-hidden="true">
      {% render 'illustration', name: 'tile-pattern', tone: 'brass', size: 520, opacity: 0.16 %}
    </span>
  {%- endif -%}'''),
    ('<div class="grid grid--4">', '<div class="grid grid--4" data-reveal-stagger>'),
    ('<div style="text-align:center;padding:1rem .5rem" {{ block.shopify_attributes }}>',
     '<div style="text-align:center;padding:1rem .5rem" data-reveal {{ block.shopify_attributes }}>'),
])

# --------------------------------------------------------- brand-marquee ----
patch('sections/brand-marquee.liquid', [
    ('<span class="visually-hidden">{{ section.settings.brands }}</span>',
     '''<div class="marquee__wave" aria-hidden="true">
    {% render 'illustration', name: 'soundwave-line', tone: 'brass', size: 14 %}
  </div>
  <span class="visually-hidden">{{ section.settings.brands }}</span>'''),
])

for rel, msg in log:
    print(f'  {rel:38} {msg}')

# -*- coding: utf-8 -*-
"""Fix the Liquid defects the audit found.

Four classes of bug, all silent — they render nothing rather than erroring:

1. `assign` used as a FILTER (`a | assign b = c`). assign is a tag.
2. `collections[section.settings.collection]` — a schema setting of type
   "collection" already returns the collection object. Using an object as a
   hash key returns nothing, so links fell back to "#" and grids to placeholders.
3. A filter inside a bracket lookup (`collections[product.type | handleize]`) —
   not permitted; the key parses as a nonsense path.
4. A filter inside a {% render %} argument (`loading: forloop.index0 | at_most: 4`)
   — the attribute scanner stops at the pipe, so `loading` received an integer
   and emitted loading="0".
"""
import os, re, sys

R = '..'
edits = []


def patch(rel, pairs, must_all=True):
    p = os.path.join(R, rel)
    if not os.path.exists(p):
        edits.append((rel, 'MISSING FILE'))
        return
    s0 = s = open(p, encoding='utf-8').read()
    missed = []
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        else:
            missed.append(old.strip().splitlines()[0][:70])
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s)
    edits.append((rel, f'{len(pairs)-len(missed)}/{len(pairs)} applied'
                       + (f'  MISSED: {missed}' if missed else '')))


# ------------------------------------------------ 1. assign-as-filter --------
patch('sections/split-feature.liquid', [(
"""            {%- liquid
              case i
                when 1 then assign sv = section.settings.stat_1 | assign sl = section.settings.stat_1_label
                when 2 then assign sv = section.settings.stat_2 | assign sl = section.settings.stat_2_label
                when 3 then assign sv = section.settings.stat_3 | assign sl = section.settings.stat_3_label
              endcase
            -%}""",
"""            {%- liquid
              case i
                when 1
                  assign sv = section.settings.stat_1
                  assign sl = section.settings.stat_1_label
                when 2
                  assign sv = section.settings.stat_2
                  assign sl = section.settings.stat_2_label
                when 3
                  assign sv = section.settings.stat_3
                  assign sl = section.settings.stat_3_label
              endcase
            -%}""")])

# ------------------------------- 2. object used as a collections[] key -------
COLL_FIX = [
    ('sections/split-feature.liquid',
     'assign col = collections[section.settings.collection]',
     'assign col = section.settings.collection'),
    ('sections/lookbook.liquid',
     'assign col = collections[block.settings.collection]',
     'assign col = block.settings.collection'),
    ('sections/category-grid.liquid',
     'assign col = collections[block.settings.collection]',
     'assign col = block.settings.collection'),
]
for rel, old, new in COLL_FIX:
    patch(rel, [(old, new)])

patch('sections/featured-products.liquid', [
    ('{%- assign col = collections[block.settings.collection] -%}',
     '{%- assign col = block.settings.collection -%}'),
    ('{{ block.settings.label | default: collections[block.settings.collection].title }}',
     '{{ block.settings.label | default: block.settings.collection.title }}'),
])

# ------------------------- 3+4. filters in lookups / render args -------------
patch('sections/main-collection.liquid', [
    ("{% render 'product-card', product: product, loading: forloop.index0 | at_most: 4 %}",
     "{%- assign card_loading = 'lazy' -%}\n"
     "              {%- if forloop.index0 < 4 -%}{%- assign card_loading = 'eager' -%}{%- endif -%}\n"
     "              {% render 'product-card', product: product, loading: card_loading %}"),
])

patch('sections/main-product.liquid', [
    ("{%- assign rel = collections[product.type | handleize].products | default: collection.products -%}",
     "{%- liquid\n"
     "    assign type_handle = product.type | handleize\n"
     "    assign rel = collections[type_handle].products\n"
     "    if rel == blank\n"
     "      assign rel = collection.products\n"
     "    endif\n"
     "  -%}"),
])

# ---------------------------- 5. product-card loading guard ------------------
patch('snippets/product-card.liquid', [
    ("assign loading = loading | default: 'lazy'",
     "unless loading == 'eager'\n    assign loading = 'lazy'\n  endunless"),
])

for rel, msg in edits:
    print(f'  {rel:44} {msg}')

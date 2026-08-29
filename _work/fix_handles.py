# -*- coding: utf-8 -*-
"""Make every collection handle match what Shopify generates from its title.

This is the cause of the reported 404s. collections.csv shipped handle
`guitars` for the title "Guitars & Bass"; a merchant creating that collection
in the admin gets the auto-generated handle `guitars-bass`, so every theme link
to /collections/guitars 404s and every homepage section pointing at it renders
empty. Seven of the 42 disagreed.

Aligning the handles to Shopify's own handleize output removes the failure mode
entirely — the setup then works whether the handle is typed explicitly or left
to generate itself.
"""
import os, re, sys

TAX = 'taxonomy.py'


def handleize(title):
    """Shopify's rule: lowercase, drop apostrophes and ampersands, collapse
    every remaining run of non-alphanumerics to a single hyphen."""
    t = title.lower().replace("'", '').replace('’', '')
    t = t.replace('&', ' ')
    t = re.sub(r'[^a-z0-9]+', '-', t)
    return t.strip('-')


src = open(TAX, encoding='utf-8').read()

# every ('handle', 'Title', [...]) leaf and every fam('handle', 'Title', ...)
renames = {}

for m in re.finditer(r"\('([a-z0-9-]+)',\s*(\"[^\"]+\"|'[^']+'),\s*\[", src):
    handle, title = m.group(1), m.group(2)[1:-1]
    want = handleize(title)
    if want != handle:
        renames[handle] = want

for m in re.finditer(r"fam\('([a-z0-9-]+)',\s*'([^']+)'", src):
    handle, title = m.group(1), m.group(2)
    want = handleize(title)
    if want != handle:
        renames[handle] = want

for m in re.finditer(r"'([a-z0-9-]+)':\s*'([^']+)',", src):
    # FEATURE dict
    handle, title = m.group(1), m.group(2)
    if handle in ('arabic-instruments', 'vintage-collectible', 'new-arrivals', 'beginner'):
        want = handleize(title)
        if want != handle:
            renames[handle] = want

if not renames:
    print('all handles already match handleize(title)')
    sys.exit(0)

print('renaming so the handle equals handleize(title):')
for a, b in sorted(renames.items()):
    print(f'    {a:22} -> {b}')

# rewrite the handles wherever they appear as a quoted token in taxonomy.py
out = src
for old, new in renames.items():
    out = re.sub(r"(?<=')" + re.escape(old) + r"(?=')", new, out)
open(TAX, 'w', encoding='utf-8').write(out)

# and in the homepage template, which references them directly
IDX = '../templates/index.json'
t = open(IDX, encoding='utf-8').read()
for old, new in renames.items():
    t = t.replace(f'"collection": "{old}"', f'"collection": "{new}"')
open(IDX, 'w', encoding='utf-8').write(t)

print('\nupdated taxonomy.py and templates/index.json')

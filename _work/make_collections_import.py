# -*- coding: utf-8 -*-
"""Emit a bulk-importable collections file.

Creating 42 smart collections by hand in the Shopify admin is about forty
minutes of clicking and is where the duplicate '-copy' handles came from.
Matrixify (free tier covers this) imports them in one pass from a CSV with
its own column names, so this writes that shape alongside a human-readable
checklist.

Every collection is a SMART collection with exactly one rule:
    product tag  is equal to  <Title>
because build_csv.py already writes that tag onto every product that belongs.
"""
import csv, os

SRC = '../import/collections.csv'
OUT_MATRIXIFY = '../import/collections-matrixify.csv'
OUT_README = '../import/collections-checklist.md'

DESCRIPTIONS = {
    'guitars': 'Acoustic, classical, electric and bass guitars — set up on the bench before they ship.',
    'oud': 'Handmade ouds from workshops in Egypt, Syria and Lebanon. No two sound the same.',
    'percussion': 'Darbuka, riq, tabl and bendir — the instruments that carry Arabic rhythm.',
    'accordions': 'Vintage Italian and German piano accordions, and a Soviet bayan.',
    'violins-wind': 'Violins, flutes, ney and recorders for students and players.',
    'audio-studio': 'Microphones, amplifiers, speakers, pedals and studio gear.',
    'accessories': 'Strings, straps, stands, tuners, pickups and cases.',
    'darbuka': 'Hand-inlaid goblet drums. Cast aluminium shells, tuneable heads, mother-of-pearl mosaic set one tessera at a time.',
    'arabic-instruments': 'The Arabic half of the shop — oud, darbuka, riq, tabl, ney and the strings that go with them.',
    'vintage-collectible': 'Instruments with a history. Sold as they are, described honestly.',
    'new-arrivals': 'The most recent additions to the shop.',
    'beginner': 'First instruments — student violins, recorders, kids’ guitars and starter outfits.',
}

rows = list(csv.DictReader(open(SRC, encoding='utf-8')))

with open(OUT_MATRIXIFY, 'w', newline='', encoding='utf-8') as f:
    cols = ['Handle', 'Title', 'Body HTML', 'Sort Order', 'Published',
            'Must Match', 'Rule: Product Column', 'Rule: Relation', 'Rule: Condition']
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({
            'Handle': r['Handle'],
            'Title': r['Title'],
            'Body HTML': DESCRIPTIONS.get(r['Handle'], ''),
            'Sort Order': 'best-selling',
            'Published': 'TRUE',
            'Must Match': 'all',
            'Rule: Product Column': 'Tag',
            'Rule: Relation': 'Equals',
            'Rule: Condition': r['Title'],
        })

by_level = {}
for r in rows:
    by_level.setdefault(r['Level'], []).append(r)

with open(OUT_README, 'w', encoding='utf-8') as f:
    f.write('# Collections — the 42 the theme expects\n\n')
    f.write('Every one is a **smart (automated) collection** with a single rule:\n\n')
    f.write('> Product **tag** — **is equal to** — *the collection title*\n\n')
    f.write('The products already carry those tags, so each collection fills itself.\n\n')
    f.write('## Fastest route\n\n')
    f.write('Install **Matrixify** (free tier is enough) and import\n')
    f.write('`import/collections-matrixify.csv`. That creates all 42 with their rules,\n')
    f.write('descriptions and sort order in one pass.\n\n')
    f.write('## By hand\n\n')
    f.write('Products → Collections → Create collection, for each row below. Set the\n')
    f.write('**handle** explicitly (Edit website SEO → URL handle) — if a handle is left to\n')
    f.write('generate itself and one already exists, Shopify appends a suffix and the\n')
    f.write('theme links stop resolving.\n\n')
    for level in ['Family', 'Feature'] + sorted(k for k in by_level if k.startswith('Under')):
        if level not in by_level:
            continue
        f.write(f'### {level}\n\n')
        f.write('| Handle | Title | Rule: tag equals |\n|---|---|---|\n')
        for r in by_level[level]:
            f.write(f"| `{r['Handle']}` | {r['Title']} | `{r['Title']}` |\n")
        f.write('\n')

print(f'wrote {OUT_MATRIXIFY}  ({len(rows)} collections)')
print(f'wrote {OUT_README}')

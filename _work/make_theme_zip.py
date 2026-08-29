# -*- coding: utf-8 -*-
"""Package the theme as a Shopify-uploadable ZIP.

The GitHub integration has applied only part of the repo: base.css is three
commits stale, snippets/ornament.liquid and snippets/illustration.liquid were
never uploaded at all, and sections/main-collection.liquid and
sections/main-product.liquid are missing or broken — which is why every
/collections/* and /products/* URL returns 404 while every other route is 200.

Uploading a ZIP writes the whole theme in one transaction and does not depend
on that integration.

Only the directories Shopify recognises are included; _work/, import/ and the
preview pages are left out.
"""
import os, zipfile, sys

ROOT = '..'
OUT = os.path.join(ROOT, 'bob-music-store-theme.zip')

THEME_DIRS = ('assets', 'config', 'layout', 'locales', 'sections', 'snippets', 'templates')

# Shopify rejects an upload containing anything outside these directories.
SKIP_NAMES = {'.DS_Store', 'Thumbs.db'}

count, total = 0, 0
missing = []

# every file a template or section depends on must be present
REQUIRED = [
    'layout/theme.liquid',
    'config/settings_schema.json',
    'config/settings_data.json',
    'templates/index.json', 'templates/collection.json', 'templates/product.json',
    'templates/cart.json', 'templates/search.json', 'templates/page.json',
    'templates/404.json', 'templates/list-collections.json',
    'templates/blog.json', 'templates/article.json', 'templates/password.json',
    'templates/gift_card.liquid',
    'sections/main-collection.liquid', 'sections/main-product.liquid',
    'sections/header.liquid', 'sections/footer.liquid',
    'snippets/ornament.liquid', 'snippets/illustration.liquid',
    'snippets/icon.liquid', 'snippets/product-card.liquid',
    'assets/base.css', 'assets/motion.css', 'assets/theme.js', 'assets/motion.js',
]
for r in REQUIRED:
    if not os.path.exists(os.path.join(ROOT, r)):
        missing.append(r)
if missing:
    print('REFUSING TO PACKAGE — required files absent:')
    for m in missing:
        print('   -', m)
    sys.exit(1)

if os.path.exists(OUT):
    os.remove(OUT)

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for d in THEME_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if not x.startswith('.')]
            for fn in sorted(filenames):
                if fn in SKIP_NAMES or fn.startswith('.'):
                    continue
                full = os.path.join(dirpath, fn)
                arc = os.path.relpath(full, ROOT).replace('\\', '/')
                z.write(full, arc)
                count += 1
                total += os.path.getsize(full)

size = os.path.getsize(OUT)
print(f'  {OUT}')
print(f'  {count} files, {total/1048576:.1f} MB uncompressed -> {size/1048576:.1f} MB zipped')
print(f'  Shopify limit for a theme upload is 50 MB: {"OK" if size < 50*1024*1024 else "TOO BIG"}')

# prove the previously-missing files are in the archive
with zipfile.ZipFile(OUT) as z:
    names = set(z.namelist())
print()
print('  files the live store is missing, now included:')
for f in ('snippets/ornament.liquid', 'snippets/illustration.liquid',
          'sections/main-collection.liquid', 'sections/main-product.liquid',
          'assets/base.css', 'templates/collection.json', 'templates/product.json'):
    print(f'    {"yes" if f in names else "NO "}  {f}')

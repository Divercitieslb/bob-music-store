#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stamp your GitHub owner/repo into the product import CSV.

    python scripts/set-image-urls.py OWNER REPO [BRANCH]

Rewrites every Image Src in import/bob-music-products.csv to a jsDelivr URL
pointing at this repository, so Shopify can pull the photographs in on import.
Run it after the first push, then commit and push the change.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, '..', 'import', 'bob-music-products.csv')
PATTERN = re.compile(r'https://cdn\.jsdelivr\.net/gh/[^/]+/[^@]+@[^/]+/import/images/')


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    owner, repo = argv[0], argv[1]
    branch = argv[2] if len(argv) > 2 else 'main'
    new = f'https://cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}/import/images/'

    if not os.path.exists(CSV):
        print(f'! not found: {CSV}')
        return 1

    with open(CSV, encoding='utf-8') as f:
        text = f.read()

    out, n = PATTERN.subn(new, text)
    if n == 0:
        print('! no image URLs matched — has this already been run?')
        return 1

    with open(CSV, 'w', encoding='utf-8', newline='') as f:
        f.write(out)

    print(f'rewrote {n} image URLs')
    print(f'  -> {new}<filename>.jpg')
    print('\nNow commit and push, then import the CSV in Shopify:')
    print('  git add import/bob-music-products.csv')
    print('  git commit -m "Point product images at this repo"')
    print('  git push')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))

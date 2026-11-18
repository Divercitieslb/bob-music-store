# -*- coding: utf-8 -*-
"""Rename the finished photographs to their SKUs and put them where the CSV
expects them.

The CSV points every Image Src at
    https://cdn.jsdelivr.net/gh/Divercitieslb/bob-music-store@catalogue/import/images/<SKU>-<nn>.jpg
so a file that is not on the CATALOGUE branch under import/images/ with exactly
that name will import as a broken image. Verified before writing this: jsDelivr
answers 200 for an existing name on that path and 404 for the placeholder the
original CSV still carries.

Usage:
    python place_newset_images.py <finished-dir> <repo-import-images-dir>

<finished-dir> holds files named after the SOURCE photo number (4.jpg, 6.jpg,
7_unmirrored.jpg …) or already named by SKU. Both are accepted.
"""
import os, shutil, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newset_keyboards import P                               # noqa: E402

EXPECT = (2048, 2048)


def main(src, dst):
    os.makedirs(dst, exist_ok=True)
    placed, missing, odd = [], [], []
    for p in P:
        for i, photo in enumerate(p['photos']):
            target = f'{p["sku"]}-{i + 1:02d}.jpg'
            for cand in (target, f'{photo}.jpg'):
                cp = os.path.join(src, cand)
                if os.path.exists(cp):
                    shutil.copy2(cp, os.path.join(dst, target))
                    try:
                        sz = Image.open(os.path.join(dst, target)).size
                        if sz != EXPECT:
                            odd.append(f'{target} is {sz[0]}x{sz[1]}, catalogue standard is 2048x2048')
                    except Exception as e:
                        odd.append(f'{target} unreadable: {e}')
                    placed.append(f'{cand} -> {target}')
                    break
            else:
                missing.append(f'{target}  (wanted source "{photo}") — {p["title"]}')

    for line in placed:
        print('  ', line)
    print(f'\nplaced {len(placed)} of {sum(len(x["photos"]) for x in P)}')
    if odd:
        print('\nWRONG SIZE — these will not match the rest of the catalogue:')
        for o in odd:
            print('   -', o)
    if missing:
        print('\nSTILL MISSING:')
        for m in missing:
            print('   -', m)
    return 1 if (missing or odd) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))

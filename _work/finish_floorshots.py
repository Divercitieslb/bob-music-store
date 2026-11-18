# -*- coding: utf-8 -*-
"""Finish the instruments that were photographed on a wood floor.

WHY THESE ARE NOT CUT OUT TO WHITE, which is what the rest of the catalogue is.
Four methods were built and measured against these frames:

  grabcut            removed the floor convincingly AND DELETED the Ketron's
                     right-hand speaker grille. Disqualifying.
  edge contour       product intact, but floorboard seams weld on as ragged
                     spurs; 87-93% of the frame survives as "product".
  inward scan        product intact, almost nothing removed.
  flood from edge    the floor is not one colour — pale board faces fall inside
                     any workable tolerance and the dark seams do not, so it
                     whitens the boards and leaves the seams as black streaks.

And the reason none of them works is measurable rather than a matter of tuning:
the Lab distance from the border-ring median was taken for every frame, and the
fraction of the instrument's own centre that falls INSIDE the floor's colour
spread is 83-99% on most of them. The floor's ring deviation in L* is 34-60 —
wood grain covers a huge range and these grey, silver and black instruments sit
inside it. There is no threshold that separates them.

So this does only what cannot go wrong:
  - trim the margin to the product plus a small border (margin only; the
    content box can never cut into the product)
  - gentle levels and tone
  - dissolve that border into white, so the grey card does not end on a hard
    line against the catalogue's white tiles
  - place it on the same 2048 canvas at the same fill ratio as the other 268
    products, so framing and scale match even though the backdrop does not

The real fix is a re-shoot on the white sheet the owner already uses — four of
this intake's seventeen photographs were taken on it.
"""
import os, sys, json
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageFilter

SIZE = 2048
FILL = 0.855
MARGIN = 0.055        # border kept around the product, as a fraction of its long side
FADE = 0.75           # how much of that border is spent fading to white
JPEG_Q = 92


def content_box(bgr, pad_frac=MARGIN):
    """Axis-aligned box around the instrument, from EDGE DENSITY not colour.

    Only ever trims the outer margin, so it is structurally incapable of
    cutting into the product — the worst case is that it trims nothing.
    """
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    g = cv2.bilateralFilter(g, 7, 50, 50)
    e = cv2.Canny(g, 40, 120).astype(np.float32) / 255.0
    h, w = e.shape

    def band(profile, lo=0.06):
        """FIRST to LAST row/column carrying detail — never the longest run.

        The longest-run version cut the Korg PS60's entire control panel off:
        the keybed is a longer continuous run of detail than the panel above
        it, so the "best" run was the keys and everything above them was
        discarded. First-to-last can only ever widen the box, so the worst case
        is that it trims nothing.
        """
        p = cv2.GaussianBlur(profile.reshape(-1, 1), (0, 0), 9).ravel()
        if p.max() <= 0:
            return 0, len(p) - 1
        on = np.where(p > p.max() * lo)[0]
        if on.size == 0:
            return 0, len(p) - 1
        return int(on[0]), int(on[-1])

    y0, y1 = band(e.sum(axis=1))
    x0, x1 = band(e.sum(axis=0))
    bw, bh = x1 - x0, y1 - y0
    pad = int(max(bw, bh) * pad_frac)
    return (max(0, x0 - pad), max(0, y0 - pad),
            min(w, x1 + pad + 1), min(h, y1 + pad + 1))


def fade_border(rgb, frac=MARGIN * FADE):
    """Dissolve the outermost border into white.

    Applied ONLY to the margin that content_box deliberately kept, so it cannot
    reach the instrument. A hard-edged grey rectangle sitting on a white tile
    is what makes a mixed catalogue look broken; a dissolve does not.
    """
    h, w = rgb.shape[:2]
    m = max(1, int(min(h, w) * frac))
    a = np.ones((h, w), np.float32)
    ramp = np.linspace(0.0, 1.0, m, dtype=np.float32) ** 1.5
    a[:m, :] = np.minimum(a[:m, :], ramp[:, None])
    a[-m:, :] = np.minimum(a[-m:, :], ramp[::-1][:, None])
    a[:, :m] = np.minimum(a[:, :m], ramp[None, :])
    a[:, -m:] = np.minimum(a[:, -m:], ramp[::-1][None, :])
    a = cv2.GaussianBlur(a, (0, 0), m * 0.22)[..., None]
    white = np.full_like(rgb, 255, dtype=np.float32)
    return (rgb.astype(np.float32) * a + white * (1 - a)).astype(np.uint8)


def tone(rgb):
    """Lift and clean the floor WITHOUT touching hue.

    Deliberately no desaturation: the Triton Extreme is genuinely dark blue,
    and the PS60's and Ringway's keys are genuinely yellowed — the listings say
    so. Washing either out would make the photographs disagree with the
    condition notes.
    """
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=1.4, tileGridSize=(8, 8)).apply(l)
    rgb = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2RGB)
    im = Image.fromarray(rgb)
    im = ImageEnhance.Brightness(im).enhance(1.04)
    im = ImageEnhance.Contrast(im).enhance(1.02)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=38, threshold=3))
    return np.asarray(im)


def place(rgb):
    h, w = rgb.shape[:2]
    s = (SIZE * FILL) / max(h, w)
    nw, nh = max(1, int(round(w * s))), max(1, int(round(h * s)))
    small = cv2.resize(rgb, (nw, nh),
                       interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    canvas = np.full((SIZE, SIZE, 3), 255, np.uint8)
    ox, oy = (SIZE - nw) // 2, (SIZE - nh) // 2
    canvas[oy:oy + nh, ox:ox + nw] = small
    return canvas


def process(path, out_path):
    bgr = cv2.imread(path)
    if bgr is None:
        return {'ok': False, 'why': 'unreadable'}
    x0, y0, x1, y1 = content_box(bgr)
    crop = bgr[y0:y1, x0:x1]
    if crop.size == 0:
        crop = bgr
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    rgb = tone(rgb)
    rgb = fade_border(rgb)
    out = place(rgb)
    Image.fromarray(out).save(out_path, quality=JPEG_Q, subsampling=0)
    sh = bgr.shape
    return {'ok': True, 'src': f'{sh[1]}x{sh[0]}',
            'cropped_to': f'{x1 - x0}x{y1 - y0}',
            'trimmed_pct': round((1 - ((x1 - x0) * (y1 - y0)) / (sh[0] * sh[1])) * 100, 1)}


if __name__ == '__main__':
    src, out, names = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
    os.makedirs(out, exist_ok=True)
    rep = {}
    for n in names:
        src_name, dst_name = (n.split('=') + [n])[:2] if '=' in n else (n, n)
        r = process(os.path.join(src, f'{src_name}.jpg'),
                    os.path.join(out, f'{dst_name}.jpg'))
        rep[dst_name] = r
        print(f'{dst_name:<14} {r.get("src","-"):>10} -> crop {r.get("cropped_to","-"):>10} '
              f'(trimmed {r.get("trimmed_pct",0):>4}%)' if r['ok'] else f'{dst_name}: {r["why"]}')
    json.dump(rep, open(os.path.join(out, 'report.json'), 'w'), indent=1)

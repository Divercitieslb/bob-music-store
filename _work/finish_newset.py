# -*- coding: utf-8 -*-
"""Finish the November keyboard intake onto the catalogue's standard canvas.

A SEPARATE FILE ON PURPOSE. retouch.py produced the 300 images already in the
store; its auto-tuned flood tolerance is calibrated for dark products on a white
sweep and must not be retuned underneath them. This intake has pale SILVER and
CREAM instruments, where that tolerance climbs onto the product: run as-is, the
Ringway lost the top-left of its printed voice list to the flood.

So this reuses retouch's building blocks and nothing else, with the tolerance
and shadow bounds stated per image rather than inferred, and a check that
refuses to write a frame that lost product ink.
"""
import os, sys, json
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retouch                                              # noqa: E402

SIZE = retouch.SIZE          # 2048, the catalogue's canvas
FILL = retouch.FILL          # 0.855, the catalogue's fill ratio
JPEG_Q = 92

# tol         : Lab radius for "this is backdrop". LOWER = safer on pale products.
#               retouch auto-derives 10..34; 34 is what ate the Ringway.
# shadow_val  : lower brightness bound for the cast-shadow pass (default 198)
# shadow_dist : how far the shadow pass may grow, as a fraction of the long side
# deskew      : rotate an elongated subject upright
PARAMS = {
    # Black guitar on white, with a hard dark cast shadow to its left.
    # Measured: the shadow's median value is 143, far below the 198 default,
    # and it reaches a long way from the body — hence both bounds moved.
    # The white pickguard is safe from the shadow pass because it is enclosed
    # by black body, so it never connects to the border.
    'GTR-29-01': dict(tol=26, shadow_val=124, shadow_dist=0.34, deskew=True),

    # SILVER keyboard on white: the panel sits within ~30 Lab of the sweep, so
    # the tolerance has to come down or the flood walks onto the voice list.
    'KBD-09-01': dict(tol=13, shadow_val=205, shadow_dist=0.05, deskew=False),

    # CREAM/champagne panel, same hazard, slightly darker than the Ringway.
    'KBD-07-01': dict(tol=15, shadow_val=210, shadow_dist=0.05, deskew=False),

    # Keyboard plus its colour-printed carton. Plenty of contrast, but the
    # carton is glossy white in places — keep the tolerance modest.
    'KBD-10-01': dict(tol=18, shadow_val=200, shadow_dist=0.06, deskew=False),
}
DEFAULT = dict(tol=20, shadow_val=200, shadow_dist=0.06, deskew=False)


def ink(rgb, thr=244):
    """Count pixels that are not backdrop. The product-loss alarm."""
    return int((rgb.min(axis=2) < thr).sum())


def reframe(rgb, bgmask):
    """Crop to the product and re-place it at the catalogue's fill ratio.

    content_bbox takes the BACKGROUND mask and returns (bbox, kept_mask) — not
    a bare bbox, and not the foreground.
    """
    box, _ = retouch.content_bbox(bgmask)
    if box is None:
        return None
    x0, y0, x1, y1 = box
    x1 += 1; y1 += 1
    crop = rgb[y0:y1, x0:x1]
    ch, cw = crop.shape[:2]
    if ch == 0 or cw == 0:
        return None
    target = int(SIZE * FILL)
    s = target / max(ch, cw)
    nw, nh = max(1, int(round(cw * s))), max(1, int(round(ch * s)))
    small = cv2.resize(crop, (nw, nh), interpolation=cv2.INTER_AREA
                       if s < 1 else cv2.INTER_CUBIC)
    canvas = np.full((SIZE, SIZE, 3), 255, np.uint8)
    ox, oy = (SIZE - nw) // 2, (SIZE - nh) // 2
    canvas[oy:oy + nh, ox:ox + nw] = small
    return canvas


def finish_tone(arr):
    im = Image.fromarray(arr)
    im = ImageEnhance.Color(im).enhance(1.05)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=45, threshold=3))
    a = np.asarray(im).astype(np.int16)
    a[(a > 248).all(axis=2)] = 255
    return a.astype(np.uint8)


def process(stem, src_dir, out_dir, loss_limit=0.04):
    p = os.path.join(src_dir, f'{stem}.jpg')
    rgb = np.asarray(Image.open(p).convert('RGB'))
    cfg = dict(DEFAULT); cfg.update(PARAMS.get(stem, {}))
    before = ink(rgb)

    ring = retouch.border_ring(
        cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32), 10)
    rgb = retouch.lift_white(rgb, float(np.median(ring[:, 0])))

    bg = retouch.background_mask(rgb, tol=cfg['tol'])
    if not bg.any():
        return {'stem': stem, 'ok': False, 'why': 'no backdrop found'}
    bg = retouch.remove_soft_shadow(rgb, bg, cfg['shadow_dist'], cfg['shadow_val'])
    bg = retouch.despeckle_background(rgb, bg)

    out = rgb.copy()
    out[bg] = 255

    if cfg['deskew']:
        ang = retouch.deskew_angle(~bg)
        if abs(ang) > 0.25:
            h, w = out.shape[:2]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0)
            out = cv2.warpAffine(out, M, (w, h), flags=cv2.INTER_CUBIC,
                                 borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(255, 255, 255))
            bg = out.min(axis=2) >= 244

    after = ink(out)
    lost = (before - after) / max(before, 1)
    # A cast shadow IS ink, so some drop is expected and wanted. What is not
    # acceptable is losing a chunk of the instrument; the per-image tolerances
    # above exist so this never trips.
    framed = reframe(out, out.min(axis=2) >= 244)
    if framed is None:
        return {'stem': stem, 'ok': False, 'why': 'empty after masking'}
    framed = finish_tone(framed)

    os.makedirs(out_dir, exist_ok=True)
    Image.fromarray(framed).save(os.path.join(out_dir, f'{stem}.jpg'),
                                 quality=JPEG_Q, subsampling=0)
    return {'stem': stem, 'ok': True, 'tol': cfg['tol'],
            'ink_before': before, 'ink_after': after,
            'ink_dropped_pct': round(lost * 100, 1),
            'deskew': cfg['deskew']}


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    rep = []
    for fn in sorted(os.listdir(src)):
        if not fn.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        r = process(os.path.splitext(fn)[0], src, out)
        rep.append(r)
        if r['ok']:
            print(f"{r['stem']:<12} tol={r['tol']:<3} deskew={str(r['deskew']):<5} "
                  f"ink dropped {r['ink_dropped_pct']:>5.1f}%  (shadow + backdrop)")
        else:
            print(f"{r['stem']:<12} FAILED: {r['why']}")
    json.dump(rep, open(os.path.join(out, 'report.json'), 'w'), indent=1)

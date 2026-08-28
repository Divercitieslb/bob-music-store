"""
Bob Music - product image retouch pipeline.

Design note: an earlier version segmented the product and composited it onto
white. That destroys product pixels wherever the mask is wrong (it ate the
edge of the Kelfar panel and tore up the guitar-label close-ups). This version
never cuts the product out. Instead it:

  1. lifts the white point so the sweep itself goes to pure 255
  2. flood-fills the background *from the image border only*, so an area can
     only be whitened if it connects to the edge - holes inside the product
     are structurally impossible
  3. derives the content bbox from that background mask
  4. deskews elongated near-vertical objects
  5. crops to the product and re-frames it at a constant fill ratio on a
     2048x2048 white canvas
  6. gentle levels / saturation / unsharp

Deterministic and re-runnable.
"""
import os, json, math, sys
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageFilter

SRC = 'raw'
OUT = 'clean'
SIZE = 2048          # final square canvas
FILL = 0.855         # longest product side as a fraction of the canvas
JPEG_Q = 90

# The oud photos carry a TikTok handle across the lower right. Where it lies on
# the white sweep, despeckle_background() removes it. Where it lies ON the
# instrument, remove_watermark_glyphs() masks just the bright glyph strokes and
# inpaints those - a blanket rectangle inpaint smeared colour across the body.
WATERMARK_BAND = {'OUD': (0.58, 0.64, 1.00, 0.82)}

# Close-ups of labels / rosettes. Tone only - no background work, no reframing.
DETAIL_SHOTS = {
    'GTR-01-02', 'GTR-03-02', 'GTR-04-02', 'GTR-05-02', 'GTR-06-02',
}

# Shot on a floor / among clutter: the background is not recoverable by
# flood fill, so these get grabcut and an explicit composite.
CLUTTERED = set()

# Per-image escapes for the handful the generic rules cannot reach.
#   shadow_val : lower luminance bound for the shadow pass (default 198)
#   crop       : fractional (x0, y0, x1, y1) pre-crop applied before anything
OVERRIDES = {
    # strong hard-edged cast shadow on a grey seamless
    'OUD-08-01': {'shadow_val': 138, 'shadow_dist': 0.30},
    'OUD-08-02': {'shadow_val': 138, 'shadow_dist': 0.30},
    # shot on a shop floor: crop to the case, then let the flood fill work
    'DRM-49-01': {'crop': (0.115, 0.075, 0.985, 0.885)},
}


# ----------------------------------------------------------------- utilities

def border_ring(a, k=10):
    return np.concatenate([
        a[:k].reshape(-1, a.shape[2]), a[-k:].reshape(-1, a.shape[2]),
        a[:, :k].reshape(-1, a.shape[2]), a[:, -k:].reshape(-1, a.shape[2]),
    ])


def lift_white(rgb, bg_lum):
    """Scale luminance so the sweep lands on 255 without clipping the product."""
    if bg_lum >= 253 or bg_lum < 150:
        return rgb
    gain = 255.0 / bg_lum
    gain = min(gain, 1.22)                     # never more than a modest lift
    out = rgb.astype(np.float32) * gain
    return np.clip(out, 0, 255).astype(np.uint8)


def background_mask(rgb, tol=None):
    """Pixels that are (a) close to the backdrop colour AND (b) connected to
    the image border. Nothing enclosed by the product can qualify."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab = cv2.GaussianBlur(lab, (0, 0), 1.2)
    ring = border_ring(lab, 10)
    bg = np.median(ring, axis=0)
    spread = np.percentile(np.linalg.norm(ring - bg, axis=1), 92)
    if tol is None:
        tol = float(np.clip(spread * 2.6 + 7.0, 10.0, 34.0))
    close = (np.linalg.norm(lab - bg, axis=2) < tol).astype(np.uint8)

    # keep only components touching the border
    n, labels = cv2.connectedComponents(close, 8)
    h, w = close.shape
    edge_ids = set(labels[0]) | set(labels[-1]) | set(labels[:, 0]) | set(labels[:, -1])
    edge_ids.discard(0)
    if not edge_ids:
        return np.zeros((h, w), bool)
    bgmask = np.isin(labels, list(edge_ids))
    # pull the boundary in slightly so we don't shave the product's soft edge
    bgmask = cv2.erode(bgmask.astype(np.uint8), np.ones((5, 5), np.uint8), 1).astype(bool)
    return bgmask


def remove_soft_shadow(rgb, bgmask, max_dist_frac=0.045, val_min=198):
    """Grow the background into the cast shadow.

    A shadow on a sweep is desaturated, lighter than the product, and lies
    close to the object. Growth is bounded by distance from the existing
    background so it can eat a shadow but never a whole pale product face.
    """
    h, w = bgmask.shape
    if not bgmask.any():
        return bgmask
    dist = cv2.distanceTransform((~bgmask).astype(np.uint8), cv2.DIST_L2, 5)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    sat, val = hsv[..., 1], hsv[..., 2]
    cand = ((dist <= max_dist_frac * max(h, w)) & (sat < 26) & (val > val_min)
            & ~bgmask)
    grown = bgmask | cand
    # only keep the part still connected to the border
    n, labels = cv2.connectedComponents(grown.astype(np.uint8), 8)
    edge = set(labels[0]) | set(labels[-1]) | set(labels[:, 0]) | set(labels[:, -1])
    edge.discard(0)
    return np.isin(labels, list(edge)) if edge else bgmask


def remove_watermark_glyphs(bgr, band, bright=232, lo=12, hi=8000):
    """Inpaint opaque watermark glyphs that sit on the product.

    Inside the band, bright pixels form two kinds of blob: one enormous one
    (the white sweep) and a handful of small ones (the glyph strokes lying on
    the instrument). Masking only the small ones means the inpaint touches the
    watermark and nothing else.
    """
    h, w = bgr.shape[:2]
    x0, y0, x1, y1 = (int(band[0] * w), int(band[1] * h),
                      int(band[2] * w), int(band[3] * h))
    sub = bgr[y0:y1, x0:x1]
    if sub.size == 0:
        return bgr, 0
    g = sub.min(axis=2)
    bw = (g > bright).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(bw, 8)
    if n <= 1:
        return bgr, 0
    biggest = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    mask = np.zeros(bw.shape, np.uint8)
    hits = 0
    for i in range(1, n):
        if i == biggest:
            continue
        if lo <= st[i, cv2.CC_STAT_AREA] <= hi:
            mask[lab == i] = 255
            hits += 1
    if not hits:
        return bgr, 0
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), 1)
    out = bgr.copy()
    out[y0:y1, x0:x1] = cv2.inpaint(sub, mask, 6, cv2.INPAINT_TELEA)
    return out, hits


def despeckle_background(rgb, bgmask):
    """Erase small, faint, isolated marks sitting on the sweep.

    This is what removes the TikTok handle from the oud photos: the text is a
    cluster of tiny light-grey components far smaller than the instrument, so
    it can be identified by size and tone without touching the product. Dark
    thin structures (strings, stand legs) are excluded by the tone test.
    """
    fgm = (~bgmask).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fgm, 8)
    if n <= 1:
        return bgmask
    areas = stats[1:, cv2.CC_STAT_AREA]
    biggest = areas.max()
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    sat = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[..., 1]
    out = bgmask.copy()
    for i, a in enumerate(areas, start=1):
        if a > biggest * 0.02 or a > rgb.shape[0] * rgb.shape[1] * 0.004:
            continue                       # too big to be a stray mark
        sel = lab == i
        if gray[sel].mean() > 186 and sat[sel].mean() < 42:
            out |= sel                     # faint + desaturated => not product
    return out


def content_bbox(bgmask, min_frac=0.0008):
    fg = ~bgmask
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN,
                          np.ones((7, 7), np.uint8), 1)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fg, 8)
    if n <= 1:
        h, w = bgmask.shape
        return (0, 0, w - 1, h - 1), fg.astype(bool)
    areas = stats[1:, cv2.CC_STAT_AREA]
    total = bgmask.size
    keep = [i + 1 for i, a in enumerate(areas)
            if a >= max(areas.max() * 0.03, total * min_frac)]
    m = np.isin(lab, keep)
    ys, xs = np.where(m)
    if len(ys) == 0:
        h, w = bgmask.shape
        return (0, 0, w - 1, h - 1), m
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())), m


def deskew_angle(mask):
    """Principal-axis tilt, only for elongated shapes already near vertical."""
    ys, xs = np.where(mask)
    if len(xs) < 500:
        return 0.0
    x, y = xs - xs.mean(), ys - ys.mean()
    vals, vecs = np.linalg.eigh(np.cov(np.vstack([x, y])))
    if vals[0] <= 1e-6:
        return 0.0
    if math.sqrt(vals[1] / max(vals[0], 1e-6)) < 2.2:
        return 0.0                              # round-ish: no meaningful axis
    vx, vy = vecs[:, 1]
    ang = math.degrees(math.atan2(vx, abs(vy)))
    return ang if 0.7 < abs(ang) < 10.0 else 0.0


def auto_levels(rgb, fg):
    """Gentle per-channel levels from the product pixels only."""
    out = rgb.astype(np.float32)
    px = out[fg]
    if px.size < 900:
        return rgb
    lo = np.percentile(px, 0.5, axis=0)
    hi = np.percentile(px, 99.5, axis=0)
    for c in range(3):
        l, h = float(lo[c]) - 6, min(255.0, float(hi[c]) + 4)
        if h - l < 40:
            continue
        out[..., c] = (out[..., c] - max(l, 0)) * (255.0 / (h - max(l, 0)))
    return np.clip(out, 0, 255).astype(np.uint8)


def inpaint_zones(bgr, zones):
    h, w = bgr.shape[:2]
    m = np.zeros((h, w), np.uint8)
    for x0, y0, x1, y1 in zones:
        cv2.rectangle(m, (int(x0 * w), int(y0 * h)),
                      (int(x1 * w), int(y1 * h)), 255, -1)
    return cv2.inpaint(bgr, m, 7, cv2.INPAINT_TELEA)


def grabcut_fg(bgr, iters=6):
    h, w = bgr.shape[:2]
    s = 700 / max(h, w)
    small = cv2.resize(bgr, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    sh, sw = small.shape[:2]
    m = np.zeros((sh, sw), np.uint8)
    rect = (int(sw * .06), int(sh * .06), int(sw * .88), int(sh * .88))
    try:
        cv2.grabCut(small, m, rect, np.zeros((1, 65), np.float64),
                    np.zeros((1, 65), np.float64), iters, cv2.GC_INIT_WITH_RECT)
    except cv2.error:
        return None
    out = ((m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD)).astype(np.uint8)
    out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8), 2)
    out = cv2.resize(out, (w, h), interpolation=cv2.INTER_NEAREST).astype(bool)
    return None if out.mean() < 0.03 or out.mean() > 0.96 else out


def finish(im, notes):
    im = ImageEnhance.Color(im).enhance(1.05)
    im = ImageEnhance.Contrast(im).enhance(1.03)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=45, threshold=3))
    a = np.asarray(im).astype(np.int16)
    a[(a > 248).all(axis=2)] = 255              # guarantee a literal white field
    return Image.fromarray(a.astype(np.uint8)), notes


# -------------------------------------------------------------------- driver

def process(fname, src_dir=SRC, out_name=None):
    stem = out_name or fname.rsplit('.', 1)[0]
    prefix = stem.split('-')[0]
    bgr = cv2.imread(os.path.join(src_dir, fname), cv2.IMREAD_COLOR)
    if bgr is None:
        return {'file': fname, 'error': 'unreadable'}
    ov = OVERRIDES.get(stem, {})
    if 'crop' in ov:
        H, W = bgr.shape[:2]
        cx0, cy0, cx1, cy1 = ov['crop']
        bgr = bgr[int(cy0 * H):int(cy1 * H), int(cx0 * W):int(cx1 * W)]
        notes_pre = ['pre-crop']
    else:
        notes_pre = []
    h0, w0 = bgr.shape[:2]
    notes = list(notes_pre)

    band = WATERMARK_BAND.get(prefix)
    if band:
        bgr, hits = remove_watermark_glyphs(bgr, band)
        if hits:
            notes.append(f'watermark-glyphs({hits})')

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # --- detail close-ups: tone + square crop only ----------------------
    if stem in DETAIL_SHOTS:
        im = Image.fromarray(rgb)
        side = min(im.size)
        l, t = (im.width - side) // 2, (im.height - side) // 2
        im = im.crop((l, t, l + side, t + side)).resize((SIZE, SIZE), Image.LANCZOS)
        im, notes = finish(im, notes + ['detail-crop'])
        os.makedirs(OUT, exist_ok=True)
        im.save(os.path.join(OUT, stem + '.jpg'), 'JPEG', quality=JPEG_Q,
                subsampling=0, optimize=True, progressive=True)
        return {'file': fname, 'stem': stem, 'src': [w0, h0], 'notes': notes}

    # --- cluttered scene: segment and composite -------------------------
    if stem in CLUTTERED:
        fg = grabcut_fg(bgr)
        if fg is not None:
            a = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 2.0)[..., None]
            a = np.clip((a - 0.35) / 0.45, 0, 1)
            rgb = (rgb * a + 255.0 * (1 - a)).astype(np.uint8)
            bgmask = ~fg
            notes.append('grabcut-composite')
        else:
            bgmask = background_mask(rgb)
    else:
        # --- normal path: lift white, flood the border background -------
        ring_lum = float(np.median(border_ring(
            cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)[..., None], 10)))
        rgb = lift_white(rgb, ring_lum)
        bgmask = background_mask(rgb)
        bgmask = remove_soft_shadow(rgb, bgmask,
                                    ov.get('shadow_dist', 0.045),
                                    ov.get('shadow_val', 198))
        bgmask = despeckle_background(rgb, bgmask)
        rgb = rgb.copy()
        rgb[bgmask] = 255
        notes.append(f'bg-flood(lum{ring_lum:.0f})')

    bbox, fg = content_bbox(bgmask)
    if fg.sum() < 800:                      # mask failed: keep the frame as-is
        fg = np.ones((h0, w0), bool)
        bbox = (0, 0, w0 - 1, h0 - 1)
        notes.append('bbox-fallback')

    rgb = auto_levels(rgb, fg)

    ang = 0.0 if stem in CLUTTERED else deskew_angle(fg)
    if ang:
        M = cv2.getRotationMatrix2D((w0 / 2, h0 / 2), -ang, 1.0)
        rgb = cv2.warpAffine(rgb, M, (w0, h0), flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        fg = cv2.warpAffine(fg.astype(np.uint8), M, (w0, h0),
                            flags=cv2.INTER_NEAREST, borderValue=0).astype(bool)
        ys, xs = np.where(fg)
        if len(ys):
            bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
        notes.append(f'deskew{ang:+.1f}')

    x0, y0, x1, y1 = bbox
    im = Image.fromarray(rgb).crop((x0, y0, x1 + 1, y1 + 1))
    pw, ph = im.size
    s = (SIZE * FILL) / max(pw, ph)
    nw, nh = max(1, round(pw * s)), max(1, round(ph * s))
    im = im.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
    canvas.paste(im, ((SIZE - nw) // 2, (SIZE - nh) // 2))

    out_im, notes = finish(canvas, notes)
    os.makedirs(OUT, exist_ok=True)
    out_im.save(os.path.join(OUT, stem + '.jpg'), 'JPEG', quality=JPEG_Q,
                subsampling=0, optimize=True, progressive=True)
    return {'file': fname, 'stem': stem, 'src': [w0, h0],
            'angle': round(ang, 2), 'notes': notes}


if __name__ == '__main__':
    files = sorted(f for f in os.listdir(SRC) if f.lower().endswith('.jpg'))
    if len(sys.argv) > 1:
        files = [f for f in files if any(k in f for k in sys.argv[1:])]
    report = []
    for i, f in enumerate(files, 1):
        report.append(process(f))
        if i % 25 == 0 or i == len(files):
            print(f'  {i}/{len(files)}', flush=True)
    json.dump(report, open('retouch_report.json', 'w'), indent=1)
    errs = [r for r in report if 'error' in r]
    print(f'done: {len(report)} processed, {len(errs)} errors')
    for e in errs:
        print('  ERROR', e)

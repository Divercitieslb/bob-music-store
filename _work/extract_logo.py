# -*- coding: utf-8 -*-
"""Cut the supplied Bob Music Store artwork to transparent PNGs.

Two source renders:
  dark-on-cream  -> the primary lockup, used on light backgrounds
  cream-on-white -> the reversed lockup, used on ink backgrounds

Both sit on a flat light field, so the background is removed by flooding in
from the border (never from inside), which cannot punch holes in the artwork.
The riq that forms the O is also cropped out on its own: it is the strongest
standalone mark and makes the favicon and social avatar.
"""
import os
import numpy as np
import cv2
from PIL import Image

D = r'C:\Users\Kojok\Downloads'
PRIMARY = os.path.join(D, 'ChatGPT Image Aug 28, 2026, 11_43_57 PM.png')
REVERSED = os.path.join(D, 'ChatGPT Image Aug 28, 2026, 11_46_56 PM.png')
OUT = '../assets'


def cut(path, tol=None, trim=True):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]

    lab = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    ring = np.concatenate([lab[:6].reshape(-1, 3), lab[-6:].reshape(-1, 3),
                           lab[:, :6].reshape(-1, 3), lab[:, -6:].reshape(-1, 3)])
    bg = np.median(ring, axis=0)
    spread = np.percentile(np.linalg.norm(ring - bg, axis=1), 95)
    t = tol if tol is not None else float(np.clip(spread * 2.4 + 5.0, 7.0, 20.0))

    close = (np.linalg.norm(cv2.GaussianBlur(lab, (0, 0), 0.9) - bg, axis=2) < t).astype(np.uint8)
    n, lb = cv2.connectedComponents(close, 8)
    edge = set(lb[0]) | set(lb[-1]) | set(lb[:, 0]) | set(lb[:, -1])
    edge.discard(0)
    bgmask = np.isin(lb, list(edge))

    alpha = (~bgmask).astype(np.float32)
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.7)
    alpha = np.clip((alpha - 0.28) / 0.5, 0, 1)

    rgba = np.dstack([a, alpha * 255]).astype(np.uint8)
    if trim:
        ys, xs = np.where(alpha > 0.12)
        pad = 10
        rgba = rgba[max(0, ys.min()-pad):min(h, ys.max()+pad),
                    max(0, xs.min()-pad):min(w, xs.max()+pad)]
    return Image.fromarray(rgba, 'RGBA')


def save(im, name, max_w=1600):
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    p = os.path.join(OUT, name)
    im.save(p, optimize=True)
    print(f'  {name}  {im.size}')


print('cutting artwork...')
primary = cut(PRIMARY)
save(primary, 'logo-primary.png')

if os.path.exists(REVERSED):
    rev = cut(REVERSED)
    save(rev, 'logo-reversed.png')
else:
    print('  (reversed render not found - skipped)')

# --- the riq alone: favicon / avatar / loading mark -----------------------
# It is the roundest, densest element; find it as the largest circle in the
# upper band of the primary lockup.
src = np.asarray(primary.convert('RGB'))
al = np.asarray(primary)[..., 3]
H, W = al.shape
band = al[: int(H * 0.72), :]
g = cv2.cvtColor(src[: int(H * 0.72), :], cv2.COLOR_RGB2GRAY)
circles = cv2.HoughCircles(cv2.medianBlur(g, 5), cv2.HOUGH_GRADIENT, dp=1.2,
                           minDist=int(W * 0.2), param1=110, param2=55,
                           minRadius=int(W * 0.09), maxRadius=int(W * 0.22))
if circles is not None:
    c = sorted(circles[0], key=lambda z: -z[2])[0]
    cx, cy, r = [int(v) for v in c]
    r = int(r * 1.10)
    x0, y0 = max(0, cx - r), max(0, cy - r)
    x1, y1 = min(W, cx + r), min(int(H * 0.72), cy + r)
    mark = primary.crop((x0, y0, x1, y1))
    save(mark, 'mark.png', 512)
    print(f'  riq mark found at ({cx},{cy}) r={r}')
else:
    print('  ! riq not auto-detected - mark.png not regenerated')

print('done')

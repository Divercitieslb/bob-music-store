"""Match the WhatsApp drop against the 225 already-listed photos.

Uses three perceptual hashes (dHash / aHash / pHash-DCT) plus a downsampled
colour signature. WhatsApp re-encodes, so exact hashes never match - we score
on Hamming distance and colour distance together.
"""
import os, json, itertools
import numpy as np
from PIL import Image


def _gray(path, n):
    im = Image.open(path).convert('L').resize((n, n), Image.LANCZOS)
    return np.asarray(im).astype(np.float32)


def dhash(path, n=16):
    g = _gray(path, n + 1)[:, :]
    return (g[:n, 1:] > g[:n, :n]).flatten()


def ahash(path, n=16):
    g = _gray(path, n)
    return (g > g.mean()).flatten()


def phash(path, n=32, k=8):
    g = _gray(path, n)
    # 2-D DCT-II via matrix multiply
    m = np.arange(n)
    C = np.cos(np.pi * (2 * m[None, :] + 1) * m[:, None] / (2 * n))
    d = C @ g @ C.T
    low = d[:k, :k].flatten()[1:]
    return low > np.median(low)


def colsig(path, n=8):
    im = Image.open(path).convert('RGB').resize((n, n), Image.LANCZOS)
    return np.asarray(im).astype(np.float32).flatten() / 255.0


def sig(path):
    return dict(d=dhash(path), a=ahash(path), p=phash(path), c=colsig(path))


def dist(s1, s2):
    dd = np.count_nonzero(s1['d'] != s2['d']) / s1['d'].size
    da = np.count_nonzero(s1['a'] != s2['a']) / s1['a'].size
    dp = np.count_nonzero(s1['p'] != s2['p']) / s1['p'].size
    dc = float(np.abs(s1['c'] - s2['c']).mean())
    return 0.34 * dd + 0.20 * da + 0.26 * dp + 0.20 * (dc * 2.2)


if __name__ == '__main__':
    old = sorted(os.listdir('raw'))
    oldsig = {}
    for f in old:
        oldsig[f] = sig(os.path.join('raw', f))
    print('hashed existing:', len(oldsig), flush=True)

    new = []
    for r, _, fs in os.walk('wa'):
        for x in fs:
            if x.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                new.append(os.path.join(r, x))
    new.sort()
    newsig = {p: sig(p) for p in new}
    print('hashed new:', len(newsig), flush=True)

    # 1. new vs existing catalogue
    vs_old = []
    for p, s in newsig.items():
        best = min(((dist(s, o), f) for f, o in oldsig.items()), key=lambda t: t[0])
        vs_old.append({'new': p, 'best_old': best[1], 'score': round(best[0], 4)})

    # 2. new vs new (internal duplicates)
    keys = list(newsig)
    internal = []
    for i, j in itertools.combinations(range(len(keys)), 2):
        d = dist(newsig[keys[i]], newsig[keys[j]])
        if d < 0.16:
            internal.append({'a': keys[i], 'b': keys[j], 'score': round(d, 4)})

    json.dump({'vs_old': vs_old, 'internal': internal},
              open('dedup.json', 'w'), indent=1)

    vs_old.sort(key=lambda r: r['score'])
    print('\n--- closest matches to already-listed photos ---')
    for r in vs_old[:40]:
        print(f"  {r['score']:.4f}  {os.path.basename(r['new'])[:46]:48} -> {r['best_old']}")
    import collections
    buckets = collections.Counter()
    for r in vs_old:
        s = r['score']
        b = ('<0.06 near-certain dupe' if s < 0.06 else
             '0.06-0.12 likely dupe' if s < 0.12 else
             '0.12-0.20 maybe' if s < 0.20 else 'new')
        buckets[b] += 1
    print('\n--- buckets ---')
    for k, v in buckets.most_common():
        print(f'  {v:4}  {k}')
    print(f'\ninternal near-duplicate pairs: {len(internal)}')

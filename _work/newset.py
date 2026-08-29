"""Decide which WhatsApp photos are genuinely new, then group the survivors
into products (multi-angle shots of one item become one listing)."""
import json, os, collections
import numpy as np
from dedup import sig, dist

d = json.load(open('dedup.json'))

# Thresholds calibrated by eye on the borderline sheets:
#  - packaged goods / boxes / string packets matched exactly, dupes ran to ~0.20
#  - darbukas are near-identical by design, so only a very tight score is a dupe
DUPE_GENERIC = 0.20
DUPE_PERCUSSION = 0.050

# Confirmed by visual inspection as dupes despite a loose score
CONFIRMED_DUPE_OLD = {
    'DRM-12-01.jpg', 'DRM-49-01.jpg', 'DRM-36-01.jpg',
    'DRM-30-01.jpg', 'DRM-39-01.jpg', 'DRM-52-01.jpg',
}

new_files, dupes = [], []
for r in d['vs_old']:
    old, s = r['best_old'], r['score']
    perc = old.startswith('DRM')
    lim = DUPE_PERCUSSION if perc else DUPE_GENERIC
    is_dupe = s < lim or (old in CONFIRMED_DUPE_OLD and s < 0.20)
    (dupes if is_dupe else new_files).append(r)

print(f'already listed (dupe): {len(dupes)}')
print(f'candidate new photos : {len(new_files)}')

# ---- group the candidates into products via single-link clustering ----------
paths = [r['new'] for r in new_files]
sigs = {p: sig(p) for p in paths}

parent = {p: p for p in paths}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra


CLUSTER_T = 0.115
for i in range(len(paths)):
    for j in range(i + 1, len(paths)):
        if dist(sigs[paths[i]], sigs[paths[j]]) < CLUSTER_T:
            union(paths[i], paths[j])

groups = collections.defaultdict(list)
for p in paths:
    groups[find(p)].append(p)
groups = [sorted(v) for v in groups.values()]
groups.sort(key=lambda g: g[0])

print(f'distinct new products: {len(groups)}')
print('images per product:', dict(collections.Counter(len(g) for g in groups)))

json.dump({'dupes': dupes, 'groups': groups}, open('newset.json', 'w'), indent=1)

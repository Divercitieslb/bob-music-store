"""Rename the WhatsApp photos onto their SKUs and run them through retouch."""
import json, os, shutil
import manifest, retouch

paths = json.load(open('cand.json'))
os.makedirs('raw_new', exist_ok=True)

plan = []          # (source path, SKU-NN stem)

# new products
for sku, v in sorted(manifest.NEW.items()):
    for i, ci in enumerate(v['cand'], start=1):
        plan.append((paths[ci], f'{sku}-{i:02d}'))

# extra angles for products already in the catalogue
for ci, sku in manifest.EXTRA_IMAGES.items():
    plan.append((paths[ci], f'{sku}-90'))       # -90.. => appended images

seen = set()
for src, stem in plan:
    if stem in seen:
        raise SystemExit(f'duplicate stem {stem}')
    seen.add(stem)
    dst = os.path.join('raw_new', stem + '.jpg')
    if not os.path.exists(dst):
        shutil.copy2(src, dst)

print(f'staged {len(plan)} images into raw_new/')

report = []
files = sorted(os.listdir('raw_new'))
for i, f in enumerate(files, 1):
    report.append(retouch.process(f, src_dir='raw_new'))
    if i % 25 == 0 or i == len(files):
        print(f'  {i}/{len(files)}', flush=True)
json.dump(report, open('retouch_report_new.json', 'w'), indent=1)
errs = [r for r in report if 'error' in r]
print(f'done: {len(report)} processed, {len(errs)} errors')
for e in errs:
    print('  ERROR', e)

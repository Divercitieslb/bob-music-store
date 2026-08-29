# -*- coding: utf-8 -*-
"""Build the Shopify product import for Bob Music Store.

Sources
  1. the original 202-product export  (cleaned: category, tags, SEO, weight)
  2. the 66 products identified in the WhatsApp drop (manifest.py)

Images point at the repo through jsDelivr, so Shopify pulls the retouched
files in on import and re-hosts them on its own CDN.

Outputs
  import/bob-music-products.csv   the import file
  import/price-sheet.csv          one row per product for the owner to price
  import/collections.csv          the collection list, with its smart rule
"""
import csv, os, re, html, json, shutil, collections
import taxonomy as T
import manifest as M

SRC_CSV = r'C:\Users\Kojok\Downloads\products_export_1 (15).csv'
CLEAN = 'clean'
OUT_IMG = '../import/images'
OUT_DIR = '../import'

# Set by the README step once the repo is pushed; until then Shopify import
# will simply skip images and they can be re-run with the correct owner/repo.
# Replaced by scripts/set-image-urls.py once the GitHub repo exists.
GH_OWNER = os.environ.get('GH_OWNER', 'YOUR-GITHUB-USERNAME')
GH_REPO = os.environ.get('GH_REPO', 'bob-music-store')
CDN = f'https://cdn.jsdelivr.net/gh/{GH_OWNER}/{GH_REPO}@main/import/images/'

COLUMNS = [
    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags',
    'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value',
    'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams',
    'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy',
    'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price',
    'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode',
    'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card',
    'SEO Title', 'SEO Description', 'Variant Weight Unit', 'Status',
]


def slug(s):
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return re.sub(r'-{2,}', '-', s)[:100]


def plain(htmltext):
    t = re.sub(r'<[^>]+>', ' ', htmltext or '')
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


STOPWORDS = {'a','an','the','and','or','with','for','of','in','on','to','from',
             'that','which','so','but','as','at','by','its','it'}


def seo_desc(title, body, ptype):
    """<=155 chars. First sentence where it fits, else a clean word-boundary
    trim with any dangling connective removed - no mid-clause cut-offs."""
    tail = ' — Bob Music Store, Beirut.'
    room = 155 - len(tail)
    base = plain(body)
    # Split on sentence ends, then re-join short fragments: a period after an
    # abbreviation ("No. 603", "1.8 m") is not a sentence boundary.
    parts = re.split(r'(?<=[.!?])\s+', base) if base else [title]
    first = parts[0]
    i = 1
    while len(first) < 70 and i < len(parts):
        first = (first + ' ' + parts[i]).strip()
        i += 1
    first = first.rstrip('.')
    if len(first) > room:
        words = first[:room].rsplit(' ', 1)[0].split(' ')
        while words and words[-1].lower().strip(',;:') in STOPWORDS:
            words.pop()
        first = ' '.join(words).rstrip(',;:—-')
    if not first:
        first = title
    return (first + tail).strip()


def tag_list(*groups):
    seen, out = set(), []
    for g in groups:
        if not g:
            continue
        items = g if isinstance(g, list) else [x.strip() for x in g.split(',')]
        for t in items:
            t = t.strip()
            if not t:
                continue
            k = t.lower()
            if k not in seen:
                seen.add(k)
                out.append(t)
    return out


rows_out = []
price_rows = []
used_images = []
warnings = []


def emit(handle, title, body, vendor, ptype, tags, sku, images,
         qty=1, status='active', options=None):
    """One product -> one row per image (Shopify's repeated-handle format)."""
    tl, low = title.lower(), ' '.join(tags).lower()
    cols = T.collections_for(ptype, low, tl)
    coll_tags = [T.title_for(c) for c in cols]
    all_tags = tag_list(coll_tags, tags)

    grams = T.WEIGHT.get(ptype, 500)
    cat = T.category_for(ptype)
    if not cat:
        warnings.append(f'no category for type "{ptype}" ({sku})')

    opt_name, opt_vals = 'Title', ['Default Title']
    if options:
        opt_name, opt_vals = options

    for vi, val in enumerate(opt_vals):
        for i, img in enumerate(images if vi == 0 else []):
            pass  # images are attached on the first variant's rows only

    first = True
    img_i = 0
    # variant rows
    for vi, val in enumerate(opt_vals):
        r = {c: '' for c in COLUMNS}
        r['Handle'] = handle
        r['Variant SKU'] = sku if len(opt_vals) == 1 else f'{sku}-{slug(val).upper()}'
        r['Option1 Name'] = opt_name
        r['Option1 Value'] = val
        r['Variant Grams'] = grams
        r['Variant Inventory Tracker'] = 'shopify'
        r['Variant Inventory Qty'] = qty
        r['Variant Inventory Policy'] = 'deny'
        r['Variant Fulfillment Service'] = 'manual'
        r['Variant Price'] = '0.00'
        r['Variant Requires Shipping'] = 'true'
        r['Variant Taxable'] = 'true'
        r['Variant Weight Unit'] = 'g'
        r['Gift Card'] = 'false'
        if first:
            r['Title'] = title
            r['Body (HTML)'] = body
            r['Vendor'] = vendor
            r['Product Category'] = cat
            r['Type'] = ptype
            r['Tags'] = ', '.join(all_tags)
            r['Published'] = 'true' if status == 'active' else 'false'
            r['Status'] = status
            r['SEO Title'] = (title[:57] + '…') if len(title) > 60 else title
            r['SEO Description'] = seo_desc(title, body, ptype)
        if first and images:
            r['Image Src'] = CDN + images[0]
            r['Image Position'] = 1
            r['Image Alt Text'] = f'{title} — Bob Music Store'
            img_i = 1
        rows_out.append(r)
        first = False

    # remaining images as their own rows
    for k in range(img_i, len(images)):
        r = {c: '' for c in COLUMNS}
        r['Handle'] = handle
        r['Image Src'] = CDN + images[k]
        r['Image Position'] = k + 1
        r['Image Alt Text'] = f'{title} — view {k + 1}'
        rows_out.append(r)

    used_images.extend(images)
    price_rows.append({
        'Handle': handle, 'SKU': sku, 'Title': title, 'Type': ptype,
        'Vendor': vendor, 'Collections': ' | '.join(T.title_for(c) for c in cols),
        'Price (USD)': '', 'Compare at (USD)': '', 'Cost (USD)': '', 'Qty': qty,
    })


# ------------------------------------------------------- 1. existing 202 ---
src = list(csv.DictReader(open(SRC_CSV, encoding='utf-8')))
by_handle = collections.OrderedDict()
for r in src:
    by_handle.setdefault(r['Handle'], []).append(r)

extra_for = collections.defaultdict(list)
for ci, sku in M.EXTRA_IMAGES.items():
    extra_for[sku].append(f'{sku}-90.jpg')

clean_files = set(os.listdir(CLEAN))

for handle, group in by_handle.items():
    head = group[0]
    sku = head['Variant SKU']
    imgs = []
    for r in group:
        if not r['Image Src']:
            continue
        stem = r['Image Src'].split('/')[-1].split('?')[0]
        if stem in clean_files:
            imgs.append(stem)
        else:
            warnings.append(f'missing cleaned image {stem} for {sku}')
    for e in extra_for.get(sku, []):
        if e in clean_files:
            imgs.append(e)

    emit(handle=handle, title=head['Title'], body=head['Body (HTML)'],
         vendor=head['Vendor'] or 'Bob Music Store', ptype=head['Type'],
         tags=head['Tags'], sku=sku, images=imgs,
         qty=int(head['Variant Inventory Qty'] or 1))

# ------------------------------------------------------------ 2. new 66 ---
for sku, v in sorted(M.NEW.items()):
    imgs = []
    for i in range(1, len(v['cand']) + 1):
        f = f'{sku}-{i:02d}.jpg'
        if f in clean_files:
            imgs.append(f)
        else:
            warnings.append(f'missing cleaned image {f}')
    body = f"<p>{v['body']}</p>"
    opts = None
    if v.get('option_name'):
        opts = (v['option_name'], v['option_values'])
    emit(handle=slug(v['title']), title=v['title'], body=body,
         vendor=v['vendor'], ptype=v['type'], tags=v['tags'],
         sku=sku, images=imgs, qty=1, options=opts)

# ------------------------------------------------------------------ write --
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(OUT_IMG, exist_ok=True)

with open(f'{OUT_DIR}/bob-music-products.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLUMNS)
    w.writeheader()
    w.writerows(rows_out)

with open(f'{OUT_DIR}/price-sheet.csv', 'w', newline='', encoding='utf-8') as f:
    cols = ['Handle', 'SKU', 'Title', 'Type', 'Vendor', 'Collections',
            'Price (USD)', 'Compare at (USD)', 'Cost (USD)', 'Qty']
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(price_rows)

# collection definitions
coll_rows = []
for h, t in T.FAMILY.items():
    coll_rows.append({'Handle': h, 'Title': t, 'Level': 'Family',
                      'Smart rule': f'Product tag is equal to "{t}"'})
for h, (t, fh, _types) in T.LEAF.items():
    coll_rows.append({'Handle': h, 'Title': t, 'Level': f'Under {T.FAMILY[fh]}',
                      'Smart rule': f'Product tag is equal to "{t}"'})
for h, t in T.FEATURE.items():
    coll_rows.append({'Handle': h, 'Title': t, 'Level': 'Feature',
                      'Smart rule': f'Product tag is equal to "{t}"'})
with open(f'{OUT_DIR}/collections.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['Handle', 'Title', 'Level', 'Smart rule'])
    w.writeheader()
    w.writerows(coll_rows)

# copy the retouched images the CSV actually references
copied = 0
for img in sorted(set(used_images)):
    s, d = os.path.join(CLEAN, img), os.path.join(OUT_IMG, img)
    if os.path.exists(s) and not os.path.exists(d):
        shutil.copy2(s, d)
        copied += 1

products = len({r['Handle'] for r in rows_out})
print(f'products      : {products}')
print(f'csv rows      : {len(rows_out)}')
print(f'images used   : {len(set(used_images))} (copied {copied})')
print(f'collections   : {len(coll_rows)}')
print(f'price sheet   : {len(price_rows)} rows')
if warnings:
    print(f'\nwarnings ({len(warnings)}):')
    for w_ in warnings[:15]:
        print('  -', w_)

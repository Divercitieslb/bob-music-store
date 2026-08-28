# Bob Music Store

A complete Shopify theme and product catalogue for Bob Music Store, Beirut —
*all instruments, one passion.*

- **268 products** across 7 families and 43 collections
- **300 retouched product photographs**, 2048×2048, pure white, consistent scale
- Custom theme built on Shopify **Online Store 2.0** (JSON templates + sections)
- Design language taken from the logo: ink, brass and bone, Cormorant Garamond
  and Karla, with Levantine geometric ornament

---

## 1. Two branches, on purpose

Shopify's GitHub integration syncs an **entire branch** as the theme and
enforces a **50 MB limit**. It does not read `.shopifyignore` — only the
Shopify CLI does. So the repo is split:

| Branch | Holds | Size | Who reads it |
|---|---|---|---|
| **`main`** | the theme only | 1.4 MB | Shopify (theme sync) |
| **`catalogue`** | 300 product images, import CSVs, build scripts, design previews | 124 MB | jsDelivr (image import), and you |

Your local folder has both — everything is on disk regardless of which branch
is checked out.

```
main                            catalogue
├── assets/                     ├── import/
│   ├── base.css                │   ├── bob-music-products.csv   ← import this
│   ├── theme.js                │   ├── price-sheet.csv          ← fill in prices
│   ├── logo-primary.png        │   ├── collections.csv
│   ├── mark.svg                │   └── images/   300 photographs
│   └── favicon.svg             ├── scripts/set-image-urls.py
├── config/                     ├── _work/        the build pipeline
├── layout/theme.liquid         └── preview-*.html  static design proofs
├── locales/
├── sections/    23 sections
├── snippets/
└── templates/
```

## 2. Connect the theme

Shopify admin → **Online Store → Themes → Add theme → Connect from GitHub**
→ repository `Divercitieslb/bob-music-store` → branch **`main`**.

Shopify then tracks `main`; every push to it updates the theme.

Two things that will bite if they are wrong:

- **Branch must be `main`, not `catalogue`.** Pointing Shopify at `catalogue`
  hands it 124 MB and it will refuse with *"Theme is too large."*
- **The Shopify GitHub App needs access to this repo.** If the picker greys it
  out with *"No access to this repository"*, open
  [github.com/settings/installations](https://github.com/settings/installations)
  → Shopify → *Repository access* → add `bob-music-store`.

## 3. Import the products

### 3a. Image URLs — already done

All 300 image URLs already point at the `catalogue` branch:

```
https://cdn.jsdelivr.net/gh/Divercitieslb/bob-music-store@catalogue/import/images/…
```

**The repository must be public** — jsDelivr will not serve a private one.
Settings → General → Danger Zone → *Change repository visibility* → Public.

Check it is serving before you import:

```bash
curl -I https://cdn.jsdelivr.net/gh/Divercitieslb/bob-music-store@catalogue/import/images/OUD-07-01.jpg
```

`HTTP/2 200` means all 300 will resolve. Allow a couple of minutes after
making the repo public — jsDelivr caches a new repo on first request.

If you ever move or rename the repo, re-stamp with:

```bash
python scripts/set-image-urls.py NEW-OWNER NEW-REPO catalogue
```

### 3b. Run the import

Shopify admin → **Products → Import** → upload
`import/bob-music-products.csv` → **Upload and continue**.

Shopify downloads each photograph from jsDelivr and re-hosts it on its own CDN,
so the GitHub repo is only needed at import time.

*Expect the import to take 10–20 minutes for 300 images.*

### 3c. Create the collections

`import/collections.csv` lists all 43 collections and the single smart rule each
one needs. For every row, in **Products → Collections → Create collection**:

- Title: the **Title** column
- Collection type: **Smart** (automated)
- Condition: **Product tag** — **is equal to** — the **Title** value

Every product is already tagged with each collection it belongs to, so the
collections fill themselves.

### 3d. Build the menu

**Online Store → Navigation → Main menu.** Add the seven families as top-level
items, each linking to its collection, with its sub-collections nested beneath.
The header renders a mega menu from whatever nesting it finds:

| Top level | Sub-items |
|---|---|
| Guitars & Bass | Acoustic, Classical, Electric, Bass, Kids' Guitars |
| Oud | Oud |
| Percussion | Darbuka, Riq & Frame Drums, Tabl & Bass Drums, Drum Kits & Bongos, Drum Heads |
| Accordions | Piano Accordions, Button Accordions |
| Violins & Wind | Violins, Electric Violins, Flutes & Ney, Recorders, Saxophones & Brass |
| Audio & Studio | Microphones, Amplifiers, Speakers & PA, Effects Pedals, Studio & Recording, MIDI Controllers, Footswitches |
| Strings & Accessories | Guitar Strings, Oud & Saz Strings, Violin & Bass Strings, Straps, Stands, Tuners & Pickups, Cases & Care |

Also create a `footer` and a `footer-help` menu — the footer reads those.

---

## 4. Prices — the one thing still outstanding

**Every product currently imports at `0.00`.** The original export had no prices
and inventing them for a live shop is not something to guess at.

Until a product has a price, the storefront shows **“Price on request”** with a
WhatsApp / email enquiry button instead of *Add to cart*. Nothing looks broken
and nothing sells for nothing.

To price the catalogue:

1. Open `import/price-sheet.csv` — one row per product, with SKU, title, type,
   vendor and the collections it sits in.
2. Fill the **Price (USD)** column (and *Compare at* / *Cost* if you want them).
3. Re-import that file through **Products → Import**, ticking
   **“Overwrite any current products that have the same handle.”**

You can also flip the whole shop to enquiry-only at any time:
**Customize → Theme settings → Selling mode → Enquiry-only mode.**

---

## 5. Theme settings to fill in

**Customize → Theme settings:**

- **Shop details** — street, city, phone, email, and the **WhatsApp number**
  in international format (e.g. `9613123456`). The WhatsApp number powers every
  enquiry button; leave it blank and those buttons are hidden.
- **Social** — Instagram, Facebook, TikTok.
- **Brand** — a favicon and a 1200×630 social sharing image, if you have them.

---

## 6. What was done to the product photographs

All 300 images were rebuilt from the originals through
`_work/retouch.py`:

- background lifted to **pure white** by flooding in from the frame edge, so
  the fill can never punch a hole inside the instrument
- cast shadows and stray marks on the sweep removed
- **TikTok watermarks removed** from the oud photographs — both the text lying
  on the white sweep and the glyphs lying on the instrument body
- elongated instruments **deskewed** to vertical where they were leaning
- every product **cropped to its own bounds and rescaled** so it fills the same
  85.5% of the frame — this is what makes the collection grids look ordered
- gentle per-image levels, saturation and unsharp
- output **2048×2048 JPEG**, sRGB, quality 90, progressive

Three photographs could not be fully rescued and are worth re-shooting when
convenient: `DRM-49` (glockenspiel, photographed bagged on a shop floor),
`DRM-18` and `DRM-24` (darbukas cropped at the foot in the original frame).

---

## 7. Notes on the catalogue

- **66 products were added** from the WhatsApp photo drop, after removing 123
  photographs that duplicated items already listed. Five more photographs were
  attached as extra angles to products that already existed.
- Microphone listings that arrive in **SONY / BOSE / YAMAHA branded boxes** are
  deliberately listed as unbranded “Dynamic Vocal Microphone”. The packaging
  does not match anything those manufacturers make, and naming them would be a
  trademark problem. Leave them as they are.
- Weights are estimates by product type, good enough for Shopify to quote a
  shipping rate. Correct any that matter.

---

## 8. Local development

```bash
npm install -g @shopify/cli @shopify/theme
shopify theme dev --store your-store.myshopify.com
```

To re-run any of the build steps, everything lives in `_work/`:

| Script | What it does |
|---|---|
| `retouch.py` | rebuilds every product image from `_work/raw/` |
| `dedup.py` → `newset.py` | matches a new photo drop against the catalogue |
| `build_csv.py` | regenerates the import CSV, price sheet and collections |
| `make_preview.py` | regenerates the static design proofs |
| `make_mark.py` | regenerates the vector riq mark and favicon |

`_work/` and everything else non-theme lives on the `catalogue` branch, so it
never reaches Shopify.

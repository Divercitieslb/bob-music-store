# November keyboard intake — 12 products

17 photographs came in. They are **12 products**, not 17:

| Product | Photographs |
|---|---|
| Ketron VEGA | 6 and 14 are the **same unit**, two different edits |
| Alesis Vortex Wireless 2 | 5, 8, 9, 10 and 11 are **one product** — 8 and 9 are the unit in its opened box, 5/10/11 are the printed carton |
| the other ten | one photograph each |

Of the five Alesis frames, two of the carton shots (5 and 10) were dropped as
redundant; the listing keeps the two unit shots and one carton shot.

**One photograph arrived mirrored.** The Yamaha's badge read "AHAMAY" and the
model number ran backwards — taken or exported through a front-camera flip. It
has been corrected, which matters beyond looks: the listing copy is read off
that panel.

---

## What to do

### 1. Import the products

Online Store is not involved — this is Products.

**Products → Import → `import/keyboards-products.csv`**

15 rows: 12 products plus 3 extra-image rows. Every price is `0.00`, so they
behave like the rest of the catalogue and show **Price on request** until you
set real prices.

### 2. Create the five new collections

There is no keyboards collection in the store today. The 42 that exist cover
guitars, oud, percussion, accordions, winds, audio and accessories — eleven of
these twelve products have nowhere to go.

**Import `import/keyboards-collections.csv`** (Matrixify), or create them by
hand as smart collections with the rule *Product tag — is equal to — the
collection's own title*:

```
Keyboards & Synths
  ├─ Arranger Keyboards
  ├─ Synthesizers
  ├─ Workstations
  └─ Portable Keyboards
```

> **Set the handle explicitly** on each one (Edit website SEO → URL handle) to
> the lower-cased hyphenated title: `keyboards-synths`, `arranger-keyboards`,
> `synthesizers`, `workstations`, `portable-keyboards`. If a handle is left to
> generate itself and one already exists, Shopify appends a suffix and every
> link in the theme stops resolving. That has already happened once to this
> store — the 42 live collections are all named `-copy`.

### 3. Add Keyboards & Synths to the menu

Navigation → Main menu → add **Keyboards & Synths** with the four children
under it. The header nav wraps to a second line and still fits.

### 4. Set the prices

All twelve are at 0.00. Seven are second-hand and one-of-a-kind, so they need
your number, not a formula.

---

## What the descriptions do and do not claim

Panel features, control names, style and voice lists are **read off the
photographs** — the Ketron's Oriental Scale row, the GEM's Arabic scale
section, the Yamaha's Khaligi and Maghrebi styles, the Korg PS60's six sound
families. Key counts are given only where the model has exactly one size.

Nothing claims polyphony, voice counts, sample memory or year **except** the
MK-821 and the Alesis, where the numbers are printed on the carton and quoted
as such.

Condition is stated plainly and is not flattering where the photograph is not:
the KingKORG's panel is described as marked and discoloured, the PS60's and the
Ringway's keys as yellowed, the Ketron's speaker grille as marked. The
photographs have not been retouched to hide any of it.

**Please read the twelve descriptions before importing.** Second-hand gear
varies unit to unit, and a few lines rest on what is visible in one photograph.

---

## Inventory

Every product imports at **quantity 1**. That is right for the second-hand
instruments. If you have more than one of the MK-821 or the Alesis, change the
quantity after import.

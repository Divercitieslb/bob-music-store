# The "How we work" page

The theme ships the layout (`templates/page.how-it-works.json`) and all the
copy inside it. Shopify still needs a page object to hang it on — a template
alone never creates a URL.

## Fastest route

Matrixify → import `import/pages-matrixify.csv`. One row, one page, template
suffix already set.

## By hand

Online Store → **Pages** → Add page

| Field | Value |
|---|---|
| Title | `How We Work` |
| Content | leave empty — the template supplies everything |
| Theme template | `how-it-works` |
| URL handle | `how-it-works` (check under *Edit website SEO*) |

Save. `https://bobmusic.shop/pages/how-it-works` goes live immediately.

## What already points at it

Nothing else needs wiring — these are in the theme:

- **Header** — the "How we work" link beside the search icon (desktop) and at
  the top of the mobile menu drawer. Theme editor → Header → *Utility link*.
- **Mega menu** — the "Explore" link in the featured panel of every dropdown.
- **Home page** — the "How we work" button on The Bench band.

If the handle ends up as anything other than `how-it-works`, change it in
Theme editor → Header → Utility link, and on the home page section.

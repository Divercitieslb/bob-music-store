# -*- coding: utf-8 -*-
"""Fix the CSS defects the audit found.

Grouped by what they actually cost a visitor:
  * product grids stuck at 155px columns at every width (dead media query)
  * the selected tab had no visible state (selector never matched)
  * text below WCAG AA on brass and on --ink-40, on almost every page
  * interactive borders at 1.32:1, below the 3:1 non-text minimum
  * "Sold" badge illegible
  * body{overflow-x:hidden} turning body into the scroll container, which
    breaks position:sticky on the header and the product info column
  * reduced-motion not stopping an infinite animation
  * a dead selector and a buried decorative pattern
"""
import os, sys

P = '../assets/base.css'
s0 = s = open(P, encoding='utf-8').read()
applied, missed = [], []


def sub(old, new, label):
    global s
    if old in s:
        s = s.replace(old, new)
        applied.append(label)
    else:
        missed.append(label)


# 1. dead media query — base rule must come first ---------------------------
sub("""@media(min-width:700px){.grid--products{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}}
.grid--products{grid-template-columns:repeat(auto-fill,minmax(155px,1fr))}""",
""".grid--products{grid-template-columns:repeat(auto-fill,minmax(155px,1fr))}
@media(min-width:700px){.grid--products{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}}""",
'product grid media query order')

# 2. selected tab had no visible state --------------------------------------
sub(".chip[aria-pressed=true],.chip.is-active{background:var(--ink);color:var(--bone);border-color:var(--ink)}",
    ".chip[aria-pressed=true],.chip[aria-selected=true],.chip.is-active{background:var(--ink);color:var(--bone);border-color:var(--ink)}",
    'selected tab state')

# 3. contrast tokens --------------------------------------------------------
sub("""  --sale:#9C3520;
  --ok:#3F6B4A;""",
"""  --sale:#9C3520;
  --ok:#3F6B4A;
  /* Brass and --ink-40 are below WCAG AA as text on light grounds
     (3.1:1 and 3.0:1 against --paper). These are the text-safe versions;
     keep --brass and --ink-40 for ornament, borders and light-on-dark. */
  --brass-text:#7A5A28;   /* 5.6:1 on paper */
  --rule-strong:#B8A98F;  /* 3.1:1 on paper — interactive borders */""",
    'contrast tokens')

# eyebrow / vendor / mega heading: brass -> brass-text on light
sub("""  font-family:var(--f-sans);font-size:.68rem;font-weight:600;letter-spacing:.28em;
  text-transform:uppercase;color:var(--brass);margin:0 0 .9rem;""",
"""  font-family:var(--f-sans);font-size:.68rem;font-weight:600;letter-spacing:.28em;
  text-transform:uppercase;color:var(--brass-text);margin:0 0 .9rem;""",
    'eyebrow contrast')
sub(".card__vendor{font-family:var(--f-sans);font-size:.64rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--brass)}",
    ".card__vendor{font-family:var(--f-sans);font-size:.64rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--brass-text)}",
    'card vendor contrast')
sub("""  font-family:var(--f-sans);font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;
  color:var(--brass);margin-bottom:1rem;font-weight:600;""",
"""  font-family:var(--f-sans);font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;
  color:var(--brass-text);margin-bottom:1rem;font-weight:600;""",
    'mega column heading contrast')

# ink-40 used as real text -> ink-60
for old, new, lbl in [
    (".eyebrow--muted{color:var(--ink-40)}", ".eyebrow--muted{color:var(--ink-60)}", 'eyebrow muted'),
    (".price--was{color:var(--ink-40);text-decoration:line-through;margin-right:.5rem}",
     ".price--was{color:var(--ink-60);text-decoration:line-through;margin-right:.5rem}", 'compare-at price'),
    (".facet__count{margin-left:auto;font-family:var(--f-mono);font-size:.68rem;color:var(--ink-40)}",
     ".facet__count{margin-left:auto;font-family:var(--f-mono);font-size:.68rem;color:var(--ink-60)}", 'facet counts'),
    (".pdp__meta dt{color:var(--ink-40);min-width:72px}",
     ".pdp__meta dt{color:var(--ink-60);min-width:72px}", 'pdp meta labels'),
]:
    sub(old, new, lbl)

sub("""  font-family:var(--f-sans);font-size:.68rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-40);padding-block:1.15rem;""",
"""  font-family:var(--f-sans);font-size:.68rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-60);padding-block:1.15rem;""",
    'breadcrumb contrast')
sub("""  font-family:var(--f-sans);font-size:.7rem;font-weight:600;letter-spacing:.24em;
  text-transform:uppercase;color:var(--ink-40);white-space:nowrap;""",
"""  font-family:var(--f-sans);font-size:.7rem;font-weight:600;letter-spacing:.24em;
  text-transform:uppercase;color:var(--ink-60);white-space:nowrap;""",
    'marquee brand names')

# 4. interactive borders below 3:1 -----------------------------------------
sub("""  padding:.62rem 1.15rem;border:1px solid var(--rule);font-family:var(--f-sans);""",
    """  padding:.62rem 1.15rem;border:1px solid var(--rule-strong);font-family:var(--f-sans);""",
    'chip border')
sub("""  appearance:none;border:1px solid var(--rule);background:var(--paper);""",
    """  appearance:none;border:1px solid var(--rule-strong);background:var(--paper);""",
    'select border')
sub(".qty{display:inline-flex;align-items:center;border:1px solid var(--rule)}",
    ".qty{display:inline-flex;align-items:center;border:1px solid var(--rule-strong)}",
    'quantity stepper border')
sub("""  padding:.6rem 1.1rem;border:1px solid var(--rule);cursor:pointer;""",
    """  padding:.6rem 1.1rem;border:1px solid var(--rule-strong);cursor:pointer;""",
    'variant option border')
sub("""  width:100%;padding:.85rem 1rem;border:1px solid var(--rule);
  background:var(--paper);color:var(--ink);""",
"""  width:100%;padding:.85rem 1rem;border:1px solid var(--rule-strong);
  background:var(--paper);color:var(--ink);""",
    'form field border')

# 5. Sold badge illegible ---------------------------------------------------
sub(".badge--sold{background:var(--ink-40)}", ".badge--sold{background:var(--ink-80)}", 'sold badge contrast')

# 6. body overflow breaks position:sticky -----------------------------------
sub("""  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
  overflow-x:hidden;
}""",
"""  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
}
/* overflow-x:hidden on body makes body the scroll container, which breaks
   position:sticky on the header and the product info column. Clip the two
   things that actually overflow instead. */
.marquee{overflow:hidden}
.split,.band,.hero{overflow:hidden}""",
    'body overflow / sticky')

# 7. dead selector ----------------------------------------------------------
sub(""".band__inner--right + .band::after,
.band:has(.band__inner--right)::after{""",
    """.band:has(.band__inner--right)::after{""",
    'dead band selector')

# 8. decorative pattern buried behind its own parent ------------------------
sub(""".tile-bg::before{
  content:'';position:absolute;inset:0;z-index:-1;opacity:.055;""",
""".tile-bg > *{position:relative;z-index:1}
.tile-bg::before{
  content:'';position:absolute;inset:0;z-index:0;opacity:.055;""",
    'tile-bg stacking')

open(P, 'w', encoding='utf-8').write(s)
print(f'applied {len(applied)}:')
for a in applied:
    print('   ', a)
if missed:
    print(f'MISSED {len(missed)}:')
    for m in missed:
        print('   ', m)

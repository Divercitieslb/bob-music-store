# -*- coding: utf-8 -*-
"""Retune base.css to the logo's Levantine language:
small structural labels move from monospace to wide-tracked Karla, monospace is
kept only for genuine numerals (price, SKU), and the greys become warm."""
P = '../assets/base.css'
s = open(P, encoding='utf-8').read()
before = s

R = [
# --- buttons, nav, labels: mono -> tracked sans -----------------------------
("""  padding:.95rem 2rem;font-family:var(--f-mono);font-size:.75rem;
  letter-spacing:.16em;text-transform:uppercase;border:1px solid var(--ink);""",
 """  padding:.95rem 2rem;font-family:var(--f-sans);font-size:.72rem;font-weight:600;
  letter-spacing:.2em;text-transform:uppercase;border:1px solid var(--ink);"""),

("""  display:inline-flex;align-items:center;gap:.55rem;font-family:var(--f-mono);
  font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;""",
 """  display:inline-flex;align-items:center;gap:.55rem;font-family:var(--f-sans);
  font-size:.72rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;"""),

("""  background:var(--ink);color:var(--bone);font-family:var(--f-mono);
  font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;""",
 """  background:var(--ink);color:var(--bone);font-family:var(--f-sans);
  font-size:.68rem;font-weight:500;letter-spacing:.18em;text-transform:uppercase;"""),

("""  display:flex;align-items:center;gap:.4rem;padding:1.6rem 0;
  font-family:var(--f-mono);font-size:.74rem;letter-spacing:.13em;
  text-transform:uppercase;white-space:nowrap;position:relative;""",
 """  display:flex;align-items:center;gap:.4rem;padding:1.75rem 0;
  font-family:var(--f-sans);font-size:.73rem;font-weight:600;letter-spacing:.17em;
  text-transform:uppercase;white-space:nowrap;position:relative;"""),

("""  font-family:var(--f-mono);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;
  color:var(--ink-40);margin-bottom:1rem;font-weight:400;""",
 """  font-family:var(--f-sans);font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;
  color:var(--brass);margin-bottom:1rem;font-weight:600;"""),

("""  padding:1.05rem .25rem;font-family:var(--f-mono);font-size:.8rem;
  letter-spacing:.1em;text-transform:uppercase;""",
 """  padding:1.05rem .25rem;font-family:var(--f-sans);font-size:.78rem;font-weight:600;
  letter-spacing:.16em;text-transform:uppercase;"""),

("""  font-family:var(--f-mono);font-size:.6rem;letter-spacing:.13em;text-transform:uppercase;
  background:var(--ink);color:var(--bone);""",
 """  font-family:var(--f-sans);font-size:.6rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;
  background:var(--ink);color:var(--bone);"""),

("""  padding:.6rem 1.1rem;border:1px solid var(--rule);font-family:var(--f-mono);
  font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;""",
 """  padding:.62rem 1.15rem;border:1px solid var(--rule);font-family:var(--f-sans);
  font-size:.68rem;font-weight:600;letter-spacing:.17em;text-transform:uppercase;"""),

("""  padding:.65rem 2.4rem .65rem 1rem;font-family:var(--f-mono);font-size:.72rem;
  letter-spacing:.1em;text-transform:uppercase;cursor:pointer;""",
 """  padding:.68rem 2.4rem .68rem 1rem;font-family:var(--f-sans);font-size:.7rem;font-weight:600;
  letter-spacing:.15em;text-transform:uppercase;cursor:pointer;"""),

("""  font-family:var(--f-mono);font-size:.72rem;letter-spacing:.13em;
  text-transform:uppercase;padding-bottom:.85rem;""",
 """  font-family:var(--f-sans);font-size:.7rem;font-weight:600;letter-spacing:.17em;
  text-transform:uppercase;padding-bottom:.85rem;"""),

("""  font-family:var(--f-mono);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;
  color:var(--bone);margin-bottom:1.1rem;font-weight:400;""",
 """  font-family:var(--f-sans);font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;
  color:var(--bone);margin-bottom:1.1rem;font-weight:600;"""),

("""  font-family:var(--f-mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-40);padding-block:1.15rem;""",
 """  font-family:var(--f-sans);font-size:.68rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-40);padding-block:1.15rem;"""),

("""  font-family:var(--f-mono);font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;
}
.acc__body""",
 """  font-family:var(--f-sans);font-size:.72rem;font-weight:600;letter-spacing:.17em;text-transform:uppercase;
}
.acc__body"""),

(""".opt__label{font-family:var(--f-mono);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-60)}""",
 """.opt__label{font-family:var(--f-sans);font-size:.68rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--ink-60)}"""),

("""  font-family:var(--f-mono);font-size:.72rem;letter-spacing:.1em;transition:all var(--t-fast);
}
.opt__values input:checked+label""",
 """  font-family:var(--f-sans);font-size:.72rem;font-weight:600;letter-spacing:.12em;transition:all var(--t-fast);
}
.opt__values input:checked+label"""),

(""".card__vendor{font-family:var(--f-mono);font-size:.65rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-40)}""",
 """.card__vendor{font-family:var(--f-sans);font-size:.64rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--brass)}"""),

(""".card__title{font-size:.95rem;font-weight:500;line-height:1.35;letter-spacing:-.01em}""",
 """.card__title{font-family:var(--f-display);font-size:1.14rem;font-weight:600;line-height:1.24}"""),

(""".tile__label h3{font-size:1.1rem;letter-spacing:-.01em}""",
 """.tile__label h3{font-size:1.5rem;font-weight:600}"""),

(""".tile__label span{font-family:var(--f-mono);font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;opacity:.75}""",
 """.tile__label span{font-family:var(--f-sans);font-size:.64rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;opacity:.8}"""),

("""  font-family:var(--f-mono);font-size:.72rem;letter-spacing:.2em;
  text-transform:uppercase;color:var(--ink-40);white-space:nowrap;""",
 """  font-family:var(--f-sans);font-size:.7rem;font-weight:600;letter-spacing:.24em;
  text-transform:uppercase;color:var(--ink-40);white-space:nowrap;"""),

(""".stock{display:inline-flex;align-items:center;gap:.5rem;font-family:var(--f-mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase}""",
 """.stock{display:inline-flex;align-items:center;gap:.5rem;font-family:var(--f-sans);font-size:.7rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase}"""),

(""".pdp__meta{display:grid;gap:.45rem;font-family:var(--f-mono);font-size:.72rem;letter-spacing:.08em;color:var(--ink-60);text-transform:uppercase}""",
 """.pdp__meta{display:grid;gap:.5rem;font-family:var(--f-sans);font-size:.72rem;letter-spacing:.1em;color:var(--ink-60);text-transform:uppercase}"""),

("""  font-family:var(--f-mono);font-size:.68rem;letter-spacing:.08em;
}""",
 """  font-family:var(--f-sans);font-size:.68rem;letter-spacing:.12em;
}"""),

(""".cart-summary__row{display:flex;justify-content:space-between;font-family:var(--f-mono);font-size:.8rem;letter-spacing:.05em}""",
 """.cart-summary__row{display:flex;justify-content:space-between;font-family:var(--f-sans);font-size:.82rem;letter-spacing:.06em}"""),

("""  border:1px solid var(--rule);font-family:var(--f-mono);font-size:.78rem;
}""",
 """  border:1px solid var(--rule);font-family:var(--f-sans);font-size:.78rem;font-weight:600;
}"""),

# --- warm the greys ---------------------------------------------------------
(""".section--ink{background:var(--ink);color:var(--bone)}""",
 """.section--ink{background:var(--ink);color:var(--bone)}
.section--espresso{background:var(--espresso);color:var(--bone)}
.section--espresso .eyebrow{color:var(--brass)}"""),
(""".section--ink .lede{color:#C9C1B7}""", """.section--ink .lede,.section--espresso .lede{color:#CFC3B0}"""),
(""".footer{background:var(--ink);color:#C9C1B7;""", """.footer{background:var(--ink);color:#BFB2A0;"""),
(""".footer a{color:#C9C1B7;""", """.footer a{color:#BFB2A0;"""),
(""".hero .lede{color:#D6CFC5;""", """.hero .lede{color:#DACFBE;"""),
("""background:linear-gradient(105deg,rgba(20,17,15,.92) 0%,rgba(20,17,15,.66) 42%,rgba(20,17,15,.15) 100%);""",
 """background:linear-gradient(102deg,rgba(20,16,12,.95) 0%,rgba(20,16,12,.72) 44%,rgba(20,16,12,.18) 100%);"""),
("""box-shadow:0 24px 48px -24px rgba(20,17,15,.22);""", """box-shadow:0 26px 52px -26px rgba(58,38,22,.28);"""),
("""background:rgba(20,17,15,.45);""", """background:rgba(20,16,12,.5);"""),
("""background:linear-gradient(to top,rgba(20,17,15,.86),rgba(20,17,15,0));""",
 """background:linear-gradient(to top,rgba(20,16,12,.9),rgba(20,16,12,0));"""),
("""  border:1px solid rgba(244,240,233,.22);""", """  border:1px solid rgba(239,230,214,.24);"""),
("""  border-top:1px solid rgba(244,240,233,.14);""", """  border-top:1px solid rgba(239,230,214,.16);"""),
("""  flex:1;min-width:180px;padding:.85rem 1rem;background:transparent;
  border:1px solid rgba(244,240,233,.28);color:var(--bone);""",
 """  flex:1;min-width:180px;padding:.85rem 1rem;background:transparent;
  border:1px solid rgba(239,230,214,.3);color:var(--bone);"""),
(""".newsletter input::placeholder{color:rgba(201,193,183,.6)}""",
 """.newsletter input::placeholder{color:rgba(191,178,160,.68)}"""),
(""".btn--outline-light{background:transparent;border-color:rgba(244,240,233,.5);color:var(--bone)}""",
 """.btn--outline-light{background:transparent;border-color:rgba(239,230,214,.55);color:var(--bone)}"""),
(""".announce a{border-bottom:1px solid rgba(244,240,233,.4)}""",
 """.announce a{border-bottom:1px solid rgba(239,230,214,.42)}"""),
]

missed = []
for old, new in R:
    if old in s:
        s = s.replace(old, new)
    else:
        missed.append(old.strip().split('\n')[0][:64])

open(P, 'w', encoding='utf-8').write(s)
print('replacements applied:', len(R) - len(missed), '/', len(R))
for m in missed:
    print('  MISSED:', m)
print('remaining var(--f-mono) refs:', s.count('var(--f-mono)'))
print('changed:', s != before)

# -*- coding: utf-8 -*-
"""Header: two rows on desktop, and a nav that can never overlap the icons.

The single-row header put `.header__nav{flex:1}` between the logo and the
actions, with `white-space:nowrap` on every link. With nine mega-menu triggers
the nav simply ran underneath the search/account/cart icons. Rebuilt as a grid
where the actions column is fixed and the nav lives on its own full-width row.
"""
P = '../assets/base.css'
s = open(P, encoding='utf-8').read()

OLD = """.header__bar{
  display:flex;align-items:center;gap:clamp(1rem,2.5vw,2.5rem);
  min-height:var(--header-h);
}
.header__logo{display:flex;align-items:center;flex-shrink:0}
.header__logo svg,.header__logo img{width:clamp(146px,15vw,208px);height:auto}
.header__nav{display:none;flex:1;min-width:0}
.header__actions{display:flex;align-items:center;gap:.35rem;margin-left:auto}"""

NEW = """.header__bar{
  display:grid;
  grid-template-columns:auto 1fr auto;   /* burger | logo | actions */
  align-items:center;gap:clamp(.5rem,2vw,1.5rem);
  min-height:var(--header-h);
}
.header__logo{display:flex;align-items:center;justify-self:start}
.header__logo img{width:clamp(132px,13vw,186px);height:auto}
.header__actions{
  display:flex;align-items:center;gap:.2rem;
  justify-self:end;flex-shrink:0;          /* never yields space to the nav */
}

/* The nav gets its own full-width row, so nine mega-menu triggers have room
   and can never collide with the icons. */
.header__nav{display:none;border-top:1px solid var(--rule-soft)}
.header__nav .wrap{display:flex;justify-content:center}"""
assert OLD in s
s = s.replace(OLD, NEW)

OLD2 = """.nav{display:flex;align-items:center;gap:clamp(.75rem,1.8vw,2rem);margin:0;padding:0;list-style:none}
.nav__item{position:static}
.nav__link{
  display:flex;align-items:center;gap:.4rem;padding:1.75rem 0;
  font-family:var(--f-sans);font-size:.73rem;font-weight:600;letter-spacing:.17em;
  text-transform:uppercase;white-space:nowrap;position:relative;
}"""
NEW2 = """.nav{
  display:flex;align-items:center;gap:clamp(.6rem,1.6vw,1.9rem);
  margin:0;padding:0;list-style:none;max-width:100%;
}
.nav__item{position:static}
.nav__link{
  display:flex;align-items:center;gap:.35rem;padding:1.05rem 0;
  font-family:var(--f-sans);font-size:.71rem;font-weight:600;letter-spacing:.15em;
  text-transform:uppercase;white-space:nowrap;position:relative;
}"""
assert OLD2 in s
s = s.replace(OLD2, NEW2)

s = s.replace(""".nav__link::after{
  content:'';position:absolute;left:0;right:0;bottom:1.15rem;height:1px;""",
""".nav__link::after{
  content:'';position:absolute;left:0;right:0;bottom:.55rem;height:1px;""")

OLD3 = """@media(min-width:1100px){
  .header__nav{display:block}
  .header__burger{display:none}
}"""
NEW3 = """@media(min-width:1080px){
  .header__nav{display:block}
  .header__burger{display:none}
  .header__bar{grid-template-columns:1fr auto 1fr}
  .header__logo{justify-self:start;grid-column:1}
  .header__actions{grid-column:3}
}
/* Last-resort guard: if a menu ever grows past the viewport the nav scrolls
   sideways rather than breaking the header. */
@media(min-width:1080px) and (max-width:1420px){
  .header__nav .wrap{justify-content:flex-start;overflow-x:auto;scrollbar-width:none}
  .header__nav .wrap::-webkit-scrollbar{display:none}
}"""
assert OLD3 in s
s = s.replace(OLD3, NEW3)

open(P, 'w', encoding='utf-8').write(s)
print('header CSS rebuilt')

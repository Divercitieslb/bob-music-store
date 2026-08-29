# -*- coding: utf-8 -*-
"""Remaining section fixes from the audit."""
import os

R = '..'
log = []


def patch(rel, pairs):
    p = os.path.join(R, rel)
    if not os.path.exists(p):
        log.append((rel, 'MISSING'))
        return
    s0 = s = open(p, encoding='utf-8').read()
    miss = []
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new, 1)
        else:
            miss.append(old.strip().splitlines()[0][:60])
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s)
    log.append((rel, f'{len(pairs)-len(miss)}/{len(pairs)}' + (f' MISS {miss}' if miss else '')))


# --- cart: subtotal was printing the total; no way to update without JS -----
patch('sections/main-cart.liquid', [
    ("""            <div class="cart-summary__row">
              <span>Subtotal</span><span class="num">{{ cart.total_price | money }}</span>
            </div>""",
     """            <div class="cart-summary__row">
              <span>Subtotal</span><span class="num">{{ cart.items_subtotal_price | money }}</span>
            </div>"""),
    ("""            <button type="submit" name="checkout" class="btn btn--full">Checkout</button>""",
     """            {%- comment -%}
              Update must precede Checkout: it is the form's first submit button,
              so pressing Enter in a quantity field updates the cart instead of
              jumping to checkout. theme.js clicks it on change; without JS it is
              the visible way to apply a quantity edit.
            {%- endcomment -%}
            <button type="submit" name="update" class="btn btn--ghost btn--full">Update cart</button>
            <button type="submit" name="checkout" class="btn btn--full">Checkout</button>"""),
    ("""                <a class="cart-line__media" href="{{ item.url }}" tabindex="-1" aria-hidden="true">""",
     """                {%- comment -%} aria-hidden must never sit on a focusable element; the
                     title beside this is already a link to the same product. {%- endcomment -%}
                <div class="cart-line__media">"""),
    ("""                </a>

                <div>
                  <h2 class="h3" style="font-size:1.1rem">""",
     """                </div>

                <div>
                  <h2 class="h3" style="font-size:1.1rem">"""),
    ("""                    <a href="{{ item.url_to_remove }}" class="mono" style="color:var(--ink-40)">Remove</a>""",
     """                    {%- comment -%} A POST button, not a GET link: link prefetchers and
                         crawlers can follow a GET and silently empty a shopper's cart. {%- endcomment -%}
                    <button type="submit" name="updates[]" value="0" class="mono"
                            style="color:var(--ink-60);text-decoration:underline"
                            aria-label="Remove {{ item.product.title | escape }}">Remove</button>"""),
])

# --- login: recovery form was unreachable without JS ------------------------
patch('sections/main-login.liquid', [
    ("""  <div id="recover" style="display:none">""",
     """  {%- comment -%}
    :target drives this without JS — "Forgotten your password?" is a real
    #recover link, so the form opens on a plain anchor jump. The .js rules only
    take over once scripting is available.
  {%- endcomment -%}
  <style>
    #recover{display:block}
    .js #recover{display:none}
    .js #recover:target,.js #recover.is-shown{display:block}
    .js #login.is-hidden{display:none}
    #recover:target ~ #login{display:none}
  </style>
  <div id="recover">"""),
    ("""      var show = a.getAttribute('data-show');
      document.getElementById('login').style.display = show === 'login' ? '' : 'none';
      document.getElementById('recover').style.display = show === 'recover' ? '' : 'none';""",
     """      var show = a.getAttribute('data-show');
      document.getElementById('login').classList.toggle('is-hidden', show !== 'login');
      document.getElementById('recover').classList.toggle('is-shown', show === 'recover');"""),
])

# --- marquee: WCAG 2.2.2 needs a real pause control -------------------------
patch('sections/brand-marquee.liquid', [
    ("""  <div class="marquee__track" aria-hidden="true">""",
     """  <button class="marquee__pause" type="button" data-marquee-pause
          aria-pressed="false" aria-label="Pause the scrolling brand list">
    <span class="marquee__pause-icon" aria-hidden="true"></span>
  </button>
  <div class="marquee__track" aria-hidden="true">"""),
    ("""<section class="marquee {{ section.settings.bg }}" aria-label="{{ section.settings.label }}">""",
     """{%- comment -%}
  WCAG 2.2.2: motion that starts automatically and runs beyond five seconds
  needs a mechanism to pause it. prefers-reduced-motion does not satisfy this.
{%- endcomment -%}
<style>
  .marquee{position:relative}
  .marquee__pause{
    position:absolute;top:.5rem;right:.75rem;z-index:2;
    width:26px;height:26px;display:grid;place-items:center;
    border:1px solid var(--rule-strong);background:var(--paper);opacity:.55;
    transition:opacity var(--t-fast);
  }
  .marquee__pause:hover,.marquee__pause:focus-visible{opacity:1}
  .marquee__pause-icon{
    width:8px;height:9px;border-left:2.5px solid var(--ink);border-right:2.5px solid var(--ink);
  }
  .marquee__pause[aria-pressed=true] .marquee__pause-icon{
    width:0;height:0;border:0;
    border-left:8px solid var(--ink);border-top:5px solid transparent;border-bottom:5px solid transparent;
  }
  .marquee__track.is-paused{animation-play-state:paused}
  .marquee:hover .marquee__track{animation-play-state:paused}
  .marquee.section--ink .marquee__pause{background:var(--ink);border-color:rgba(239,230,214,.3)}
  .marquee.section--ink .marquee__pause-icon{border-color:var(--bone)}
</style>
<section class="marquee {{ section.settings.bg }}" aria-label="{{ section.settings.label }}">"""),
    ("""  <span class="visually-hidden">{{ section.settings.brands }}</span>
</section>""",
     """  <span class="visually-hidden">{{ section.settings.brands }}</span>
</section>

<script>
  (function () {
    var s = document.currentScript && document.currentScript.previousElementSibling;
    var sec = document.querySelector('.marquee');
    if (!sec) return;
    var btn = sec.querySelector('[data-marquee-pause]');
    var track = sec.querySelector('.marquee__track');
    if (!btn || !track) return;
    btn.addEventListener('click', function () {
      var paused = track.classList.toggle('is-paused');
      btn.setAttribute('aria-pressed', String(paused));
      btn.setAttribute('aria-label', paused ? 'Resume the scrolling brand list'
                                            : 'Pause the scrolling brand list');
    });
  })();
</script>"""),
])

# --- footer: a menu that does not exist left a stranded heading -------------
patch('sections/footer.liquid', [
    ("""          {%- when 'menu' -%}
            <div {{ block.shopify_attributes }}>
              <h4>{{ block.settings.heading }}</h4>
              <ul>
                {%- for link in linklists[block.settings.menu].links -%}
                  <li><a href="{{ link.url }}">{{ link.title }}</a></li>
                {%- endfor -%}
              </ul>
            </div>""",
     """          {%- when 'menu' -%}
            {%- comment -%} A menu handle that was never created would otherwise
                 render a heading above an empty list on every page. {%- endcomment -%}
            {%- assign fmenu = linklists[block.settings.menu] -%}
            {%- if fmenu.links.size > 0 -%}
              <div {{ block.shopify_attributes }}>
                <h4>{{ block.settings.heading }}</h4>
                <ul>
                  {%- for link in fmenu.links -%}
                    <li><a href="{{ link.url }}">{{ link.title }}</a></li>
                  {%- endfor -%}
                </ul>
              </div>
            {%- endif -%}"""),
])

# --- /collections must paginate; the products query per row was gratuitous --
patch('sections/main-list-collections.liquid', [
    ("""  <div class="grid grid--3">
    {%- for col in collections -%}""",
     """  {%- paginate collections by 24 -%}
  <div class="grid grid--3">
    {%- for col in collections -%}"""),
    ("""          {%- elsif col.products.first.featured_media -%}
            <img src="{{ col.products.first.featured_media | image_url: width: 700 }}" alt="{{ col.title | escape }}"
                 width="700" height="875" loading="lazy">
""", ""),
    ("""  </div>
</div>

{% schema %}""",
     """  </div>

  {%- if paginate.pages > 1 -%}
    <nav class="pagination" aria-label="Pagination">
      {%- for part in paginate.parts -%}
        {%- if part.is_link -%}<a href="{{ part.url }}">{{ part.title }}</a>
        {%- else -%}<span class="is-current">{{ part.title }}</span>{%- endif -%}
      {%- endfor -%}
    </nav>
  {%- endif -%}
  {%- endpaginate -%}
</div>

{% schema %}"""),
])

for rel, msg in log:
    print(f'  {rel:42} {msg}')

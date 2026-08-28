/* Bob Music Store — theme behaviour.
   Small, dependency-free, progressive: every interaction here has a working
   no-JS fallback (real links, real form submits). */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------------------ drawers -- */
  var lastFocus = null;

  function openDrawer(id) {
    var d = document.getElementById(id);
    if (!d) return;
    lastFocus = document.activeElement;
    d.classList.add('is-open');
    d.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    var f = d.querySelector('input,button,a[href]');
    if (f) setTimeout(function () { f.focus(); }, 60);
  }

  function closeDrawer(d) {
    if (!d) return;
    d.classList.remove('is-open');
    d.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (lastFocus) { lastFocus.focus(); lastFocus = null; }
  }

  document.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-open]');
    if (opener) {
      var id = opener.getAttribute('data-open');
      // the cart icon is a real link; only intercept when the drawer exists
      if (document.getElementById(id)) { e.preventDefault(); openDrawer(id); }
      return;
    }
    var closer = e.target.closest('[data-close]');
    if (closer) { e.preventDefault(); closeDrawer(closer.closest('.drawer')); }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = $('.drawer.is-open');
    if (open) closeDrawer(open);
  });

  // keep focus inside an open drawer
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab') return;
    var d = $('.drawer.is-open');
    if (!d) return;
    var f = $$('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])', d)
      .filter(function (el) { return el.offsetParent !== null; });
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* --------------------------------------------------------------- tabs -- */
  $$('[data-tabs]').forEach(function (root) {
    var tabs = $$('[data-tab]', root);
    var panels = $$('[data-panel]', root);
    if (tabs.length < 2) return;
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t, j) { t.setAttribute('aria-selected', String(i === j)); });
        panels.forEach(function (p, j) { p.hidden = i !== j; });
      });
      tab.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var n = (i + d + tabs.length) % tabs.length;
        tabs[n].focus(); tabs[n].click();
      });
    });
  });

  /* ------------------------------------------------------ product gallery */
  var main = $('[data-gallery-main]');
  if (main) {
    $$('[data-gallery-thumb]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var img = main.querySelector('img');
        if (!img) return;
        img.src = btn.getAttribute('data-full');
        img.removeAttribute('srcset');
        img.alt = btn.getAttribute('data-alt') || '';
        $$('[data-gallery-thumb]').forEach(function (b) { b.setAttribute('aria-current', String(b === btn)); });
      });
    });
  }

  /* --------------------------------------------------------- quantity ---- */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-qty],[data-cart-qty]');
    if (!b) return;
    var step = parseInt(b.getAttribute('data-qty') || b.getAttribute('data-cart-qty'), 10);
    var input = b.parentNode.querySelector('input');
    if (!input) return;
    var min = parseInt(input.getAttribute('min') || '0', 10);
    input.value = Math.max(min, (parseInt(input.value, 10) || 0) + step);
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });

  // cart quantity change submits the real form (no-JS parity)
  $$('[data-cart-input]').forEach(function (input) {
    input.addEventListener('change', function () {
      var form = input.closest('form');
      if (form) form.submit();
    });
  });

  /* ------------------------------------------------------------- sorting - */
  var sort = $('[data-sort]');
  if (sort) {
    sort.addEventListener('change', function () {
      var u = new URL(window.location.href);
      u.searchParams.set('sort_by', sort.value);
      u.searchParams.delete('page');
      window.location.href = u.toString();
    });
  }

  /* -------------------------------------------------------------- facets - */
  var facetForm = $('[data-facet-form]');
  if (facetForm) {
    facetForm.addEventListener('change', function () {
      var u = new URL(window.location.href);
      // wipe existing filter params, then rewrite from the form
      Array.from(u.searchParams.keys()).forEach(function (k) {
        if (k.indexOf('filter.') === 0) u.searchParams.delete(k);
      });
      $$('input', facetForm).forEach(function (el) {
        if (el.type === 'checkbox' && el.checked) u.searchParams.append(el.name, el.value);
        if (el.type === 'number' && el.value) u.searchParams.set(el.name, el.value);
      });
      u.searchParams.delete('page');
      window.location.href = u.toString();
    });
  }

  /* --------------------------------------------------- predictive search - */
  var sInput = $('[data-search-input]');
  var sOut = $('[data-search-results]');
  if (sInput && sOut && window.Shop && window.Shop.routes.predictive) {
    var t = null;
    sInput.addEventListener('input', function () {
      clearTimeout(t);
      var q = sInput.value.trim();
      if (q.length < 2) { sOut.innerHTML = ''; return; }
      t = setTimeout(function () {
        var url = window.Shop.routes.predictive +
          '?q=' + encodeURIComponent(q) +
          '&resources[type]=product&resources[limit]=6&section_id=predictive-search';
        fetch(url)
          .then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); })
          .then(function (html) {
            var doc = new DOMParser().parseFromString(html, 'text/html');
            var grid = doc.querySelector('[data-predictive-grid]');
            sOut.innerHTML = grid ? grid.innerHTML : '';
          })
          .catch(function () { sOut.innerHTML = ''; });
      }, 220);
    });
  }

  /* ------------------------------------------------------ sticky header -- */
  var header = $('[data-header]');
  if (header) {
    var last = 0;
    window.addEventListener('scroll', function () {
      var y = window.scrollY;
      header.style.boxShadow = y > 8 ? '0 1px 0 rgba(20,16,12,.08)' : '';
      last = y;
    }, { passive: true });
  }
})();

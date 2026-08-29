/* Bob Music Store — theme behaviour.
   Small, dependency-free, progressive: every interaction here has a working
   no-JS fallback (real links, real form submits).

   Two rules that shape the structure:

   1. Per-section wiring lives in initSection(root) and is re-run on
      shopify:section:load. The theme editor destroys and re-inserts a
      section's DOM on every settings change, so anything bound once at parse
      time goes dead the first time a merchant edits that section.
   2. Anything that hides content is done HERE, never in Liquid. The markup
      ships visible so a visitor with JS off loses nothing; JS adds the hidden
      state only once it has taken over the behaviour. */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------------------ drawers -- */
  var lastFocus = null;
  var lastOpener = null;

  function openDrawer(id, opener) {
    var d = document.getElementById(id);
    if (!d) return;
    lastFocus = document.activeElement;
    lastOpener = opener || null;
    d.classList.add('is-open');
    d.setAttribute('aria-hidden', 'false');
    if (lastOpener) lastOpener.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    var f = d.querySelector('input,button,a[href]');
    if (f) setTimeout(function () { f.focus(); }, 60);
  }

  function closeDrawer(d) {
    if (!d) return;
    d.classList.remove('is-open');
    d.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    // reset every trigger for this drawer, not just the one that opened it
    $$('[data-open="' + d.id + '"]').forEach(function (b) {
      b.setAttribute('aria-expanded', 'false');
    });
    lastOpener = null;
    if (lastFocus) { lastFocus.focus(); lastFocus = null; }
  }

  document.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-open]');
    if (opener) {
      var id = opener.getAttribute('data-open');
      // the cart icon is a real link; only intercept when the drawer exists
      if (document.getElementById(id)) { e.preventDefault(); openDrawer(id, opener); }
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

  /* ------------------------------------------------------------ quantity -- */
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

  /* ------------------------------------------------- per-section wiring --- */
  var searchCtrl = null;

  function initTabs(root) {
    $$('[data-tabs]', root).forEach(function (wrap) {
      if (wrap.dataset.tabsReady) return;
      wrap.dataset.tabsReady = '1';

      var tabs = $$('[data-tab]', wrap);
      var panels = $$('[data-panel]', wrap);
      if (tabs.length < 2 || !panels.length) return;

      // The panels ship visible so no-JS sees every tab's products. Now that
      // JS is running, collapse to the selected one.
      function select(i) {
        tabs.forEach(function (t, j) {
          t.setAttribute('aria-selected', String(i === j));
          t.tabIndex = i === j ? 0 : -1;
        });
        panels.forEach(function (p, j) { p.hidden = i !== j; });
      }
      select(0);

      tabs.forEach(function (tab, i) {
        tab.addEventListener('click', function () { select(i); });
        tab.addEventListener('keydown', function (e) {
          var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
          if (!d) return;
          e.preventDefault();
          var n = (i + d + tabs.length) % tabs.length;
          tabs[n].focus();
          select(n);
        });
      });
    });
  }

  function initGallery(root) {
    var main = $('[data-gallery-main]', root);
    if (!main || main.dataset.galleryReady) return;
    main.dataset.galleryReady = '1';
    var thumbs = $$('[data-gallery-thumb]', root);
    thumbs.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var img = main.querySelector('img');
        if (!img) return;
        var full = btn.getAttribute('data-full');
        if (full) { img.src = full; img.removeAttribute('srcset'); }
        img.alt = btn.getAttribute('data-alt') || '';
        thumbs.forEach(function (b) { b.setAttribute('aria-current', String(b === btn)); });
      });
    });
  }

  function initCart(root) {
    $$('[data-cart-input]', root).forEach(function (input) {
      if (input.dataset.cartReady) return;
      input.dataset.cartReady = '1';
      input.addEventListener('change', function () {
        var form = input.closest('form');
        if (!form) return;
        // submit through the update button so Shopify does not read this as a
        // checkout click (the checkout button is the form's default submitter)
        var upd = form.querySelector('[name="update"]');
        if (upd) { upd.click(); } else { form.submit(); }
      });
    });
  }

  function initSort(root) {
    var sort = $('[data-sort]', root);
    if (!sort || sort.dataset.sortReady) return;
    sort.dataset.sortReady = '1';
    sort.addEventListener('change', function () {
      var u = new URL(window.location.href);
      u.searchParams.set('sort_by', sort.value);
      u.searchParams.delete('page');
      window.location.href = u.toString();
    });
  }

  function initFacets(root) {
    var form = $('[data-facet-form]', root);
    if (!form || form.dataset.facetReady) return;
    form.dataset.facetReady = '1';
    form.addEventListener('change', function () {
      var u = new URL(window.location.href);
      Array.from(u.searchParams.keys()).forEach(function (k) {
        if (k.indexOf('filter.') === 0) u.searchParams.delete(k);
      });
      $$('input', form).forEach(function (el) {
        if (el.type === 'checkbox' && el.checked) u.searchParams.append(el.name, el.value);
        if (el.type === 'number' && el.value) u.searchParams.set(el.name, el.value);
      });
      u.searchParams.delete('page');
      window.location.href = u.toString();
    });
  }

  function initSearch(root) {
    var sInput = $('[data-search-input]', root);
    var sOut = $('[data-search-results]', root);
    if (!sInput || !sOut || sInput.dataset.searchReady) return;
    if (!window.Shop || !window.Shop.routes || !window.Shop.routes.predictive) return;
    sInput.dataset.searchReady = '1';

    var t = null;
    sInput.addEventListener('input', function () {
      clearTimeout(t);
      var q = sInput.value.trim();
      if (q.length < 2) {
        if (searchCtrl) { searchCtrl.abort(); searchCtrl = null; }
        sOut.innerHTML = '';
        sInput.setAttribute('aria-expanded', 'false');
        return;
      }
      t = setTimeout(function () {
        // abort the in-flight request so a slow early reply cannot overwrite
        // a fast later one
        if (searchCtrl) searchCtrl.abort();
        searchCtrl = new AbortController();
        var url = window.Shop.routes.predictive +
          '?q=' + encodeURIComponent(q) +
          '&resources[type]=product&resources[limit]=6&section_id=predictive-search';
        fetch(url, { signal: searchCtrl.signal })
          .then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); })
          .then(function (html) {
            var doc = new DOMParser().parseFromString(html, 'text/html');
            var grid = doc.querySelector('[data-predictive-grid]');
            sOut.innerHTML = grid ? grid.innerHTML : '';
            sInput.setAttribute('aria-expanded', sOut.innerHTML ? 'true' : 'false');
          })
          .catch(function (err) {
            if (err && err.name === 'AbortError') return;
            sOut.innerHTML = '';
          });
      }, 220);
    });
  }

  function initSection(root) {
    initTabs(root);
    initGallery(root);
    initCart(root);
    initSort(root);
    initFacets(root);
    initSearch(root);
  }

  /* ----------------------------------------------------- header height ---- */
  /* Condense-on-scroll and the progress rail belong to sections/header.liquid,
     which owns its own listener. All that is needed here is the true header
     height: --header-h is the sticky offset for .pdp__info and for
     scroll-margin, and the real header is the announcement bar plus the logo
     row plus the nav row — around 186px on desktop, not the 82px placeholder
     in :root. Measure it rather than guess. */
  var header = $('[data-header]');

  function publishHeaderHeight() {
    if (!header) return;
    document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  }

  /* ---------------------------------------------------------------- boot -- */
  function boot() {
    initSection(document);
    publishHeaderHeight();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  window.addEventListener('resize', publishHeaderHeight, { passive: true });

  // the theme editor replaces a section's DOM wholesale on every edit
  document.addEventListener('shopify:section:load', function (e) {
    initSection(e.target);
    publishHeaderHeight();
  });
  document.addEventListener('shopify:section:unload', function () {
    if (searchCtrl) { searchCtrl.abort(); searchCtrl = null; }
  });
})();

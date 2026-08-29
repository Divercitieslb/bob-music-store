/* Bob Music Store — motion layer.
   Pairs with assets/motion.css. Vanilla, no dependencies, no build step.

   Ground rules held throughout this file:
   - Nothing here is load-bearing for content. CSS starts every effect from its
     finished state; JS only ever adds the "hidden" step and then removes it.
   - One rAF loop drives everything scroll-driven. One passive scroll listener.
   - Reads are batched before writes inside a frame — never interleaved.
   - Reduced motion is checked once AND re-checked on change, because a .01ms
     animation-duration (base.css) stops neither a rAF loop nor a delay. */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  var supportsIO = 'IntersectionObserver' in window;

  var mqReduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var mqFine = window.matchMedia('(hover: hover) and (pointer: fine)');
  var reduced = mqReduce.matches;

  /* ------------------------------------------------------ shared rAF loop -- */
  var frameId = 0;
  var lastTs = 0;
  var scrollY = window.pageYOffset || 0;
  var velocity = 0;              // px/frame, smoothed — drives the marquee
  var viewH = window.innerHeight || 0;

  var parallaxItems = [];        // {el, speed, shift}
  var counters = [];             // {el, from, to, dur, start, prefix, suffix, decimals}
  var marquees = [];             // {track, x, half, base} — a page may hold several

  function needsFrame() {
    return !reduced && (parallaxItems.length > 0 || counters.length > 0 || marquees.length > 0);
  }

  function requestLoop() {
    if (!frameId && needsFrame()) frameId = requestAnimationFrame(frame);
  }

  function frame(ts) {
    frameId = 0;
    var dt = lastTs ? Math.min(ts - lastTs, 64) : 16.7;  // clamp: a backgrounded tab must not lurch
    lastTs = ts;

    var y = window.pageYOffset || 0;
    var delta = y - scrollY;
    scrollY = y;
    // exponential smoothing so a single flick does not spike the marquee
    velocity += (Math.abs(delta) - velocity) * 0.12;
    if (velocity < 0.05) velocity = 0;

    /* --- read phase: measure everything before touching a single style --- */
    var i, it;
    for (i = 0; i < parallaxItems.length; i++) {
      it = parallaxItems[i];
      var rect = it.el.getBoundingClientRect();
      if (rect.bottom < -200 || rect.top > viewH + 200) { it.shift = null; continue; }
      // distance of the element's centre from the viewport centre, scaled
      var centre = rect.top + rect.height / 2;
      it.shift = (viewH / 2 - centre) * it.speed;
    }

    /* --- write phase --- */
    for (i = 0; i < parallaxItems.length; i++) {
      it = parallaxItems[i];
      if (it.shift === null) continue;
      it.el.style.transform = 'translate3d(0,' + it.shift.toFixed(2) + 'px,0)';
    }

    stepCounters(ts);
    stepMarquees(dt);

    if (needsFrame()) requestLoop();
  }

  function onScroll() { requestLoop(); }
  function onResize() { viewH = window.innerHeight || 0; measureMarquees(); requestLoop(); }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize, { passive: true });

  /* -------------------------------------------------------- 1. reveal ------ */
  var revealIO = null;

  function initReveal(scope) {
    var nodes = $$('[data-reveal]', scope).filter(function (n) { return !n.__bmReveal; });
    if (!nodes.length) return;

    // stagger: a parent marks a group, its children arrive one beat apart.
    // Capped with i % 4 so the tail of a long list is not left a second behind.
    $$('[data-reveal-stagger]', scope).forEach(function (parent) {
      var step = parseFloat(parent.getAttribute('data-reveal-stagger')) || 60;
      $$('[data-reveal]', parent).forEach(function (child, i) {
        child.style.transitionDelay = ((i % 4) * step / 1000) + 's';
      });
    });

    if (reduced || !supportsIO) {
      nodes.forEach(function (n) { n.__bmReveal = true; n.classList.add('is-in'); });
      return;
    }

    if (!revealIO) {
      revealIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          revealIO.unobserve(e.target);   // fire once; never re-animate on scroll-up
        });
      }, {
        threshold: 0.12,
        // the -8% inset stops an element firing the instant one pixel clears
        // the fold, which reads as premature
        rootMargin: '0px 0px -8% 0px'
      });
    }

    nodes.forEach(function (n) { n.__bmReveal = true; revealIO.observe(n); });
  }

  /* ---------------------------------------------------- 2. split headline -- */
  function initSplit(scope) {
    $$('[data-split]', scope).forEach(function (el) {
      if (el.__bmSplit) return;
      el.__bmSplit = true;

      var text = (el.textContent || '').replace(/\s+/g, ' ').trim();
      // Only split plain text. A heading carrying <em>, <a> or <br> keeps its
      // markup and simply reveals as a block — losing the effect beats losing
      // the link.
      if (!text || el.children.length) { el.setAttribute('data-reveal', ''); return; }

      el.setAttribute('aria-label', text);   // the accessible name stays whole
      var step = parseFloat(el.getAttribute('data-split')) || 55;
      var frag = doc.createDocumentFragment();
      var words = text.split(' ');

      words.forEach(function (word, i) {
        var line = doc.createElement('span');
        line.className = 'split-line';
        line.setAttribute('aria-hidden', 'true');   // spans are decoration only
        var inner = doc.createElement('span');
        inner.className = 'split-word';
        inner.textContent = word;
        inner.style.transitionDelay = (i * step / 1000) + 's';
        line.appendChild(inner);
        frag.appendChild(line);
        if (i < words.length - 1) frag.appendChild(doc.createTextNode(' '));
      });

      el.textContent = '';
      el.appendChild(frag);

      if (reduced || !supportsIO) { el.classList.add('is-in'); return; }
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          io.unobserve(e.target);
        });
      }, { threshold: 0.2, rootMargin: '0px 0px -6% 0px' });
      io.observe(el);
    });
  }

  /* --------------------------------------------------------- 3. parallax --- */
  function initParallax(scope) {
    if (reduced || !mqFine.matches) return;   // coarse pointers: scroll is already kinetic
    $$('[data-parallax]', scope).forEach(function (el) {
      if (el.__bmParallax) return;
      // reveal writes transform from CSS; parallax writes it inline. One
      // element cannot do both — the inline value would win and freeze it.
      if (el.hasAttribute('data-reveal')) return;
      var speed = parseFloat(el.getAttribute('data-parallax'));
      if (!isFinite(speed) || speed === 0) return;
      // clamp: anything past .35 detaches the image from the page
      speed = Math.max(-0.35, Math.min(0.35, speed));
      el.__bmParallax = true;
      parallaxItems.push({ el: el, speed: speed, shift: 0 });
    });
    requestLoop();
  }

  function teardownParallax() {
    parallaxItems.forEach(function (it) { it.el.style.transform = ''; it.el.__bmParallax = false; });
    parallaxItems.length = 0;
  }

  /* -------------------------------------------------------- 4. magnetic ---- */
  function initMagnetic(scope) {
    if (reduced || !mqFine.matches) return;
    $$('[data-magnetic]', scope).forEach(function (el) {
      if (el.__bmMagnetic) return;
      el.__bmMagnetic = true;

      var strength = parseFloat(el.getAttribute('data-magnetic')) || 0.28;
      var box = null;   // measured once on enter, so pointermove never reads layout

      el.addEventListener('pointerenter', function () {
        if (reduced) return;
        box = el.getBoundingClientRect();
        el.classList.add('is-magnetised');
      });

      el.addEventListener('pointermove', function (e) {
        if (reduced || !box) return;
        var dx = (e.clientX - (box.left + box.width / 2)) * strength;
        var dy = (e.clientY - (box.top + box.height / 2)) * strength;
        var cap = 14;   // px — a nudge, not a drag
        el.style.setProperty('--mx', Math.max(-cap, Math.min(cap, dx)).toFixed(1) + 'px');
        el.style.setProperty('--my', Math.max(-cap, Math.min(cap, dy)).toFixed(1) + 'px');
      });

      var release = function () {
        box = null;
        el.classList.remove('is-magnetised');
        el.style.setProperty('--mx', '0px');
        el.style.setProperty('--my', '0px');
      };
      el.addEventListener('pointerleave', release);
      el.addEventListener('pointercancel', release);
      el.addEventListener('blur', release);
    });
  }

  /* --------------------------------------------------- 5. hover image ------ */
  var follower = null;
  var followRaf = 0;
  var followX = 0, followY = 0;

  function initHoverImage(scope) {
    if (reduced || !mqFine.matches) return;
    var links = $$('[data-hover-image]', scope).filter(function (n) { return !n.__bmHover; });
    if (!links.length) return;

    if (!follower) {
      follower = doc.createElement('div');
      follower.className = 'hover-follow';
      follower.setAttribute('aria-hidden', 'true');
      follower.appendChild(doc.createElement('img'));
      doc.body.appendChild(follower);
    }
    var img = follower.querySelector('img');

    function place() {
      followRaf = 0;
      follower.style.transform = 'translate3d(' + followX + 'px,' + followY + 'px,0) scale(1)';
    }

    links.forEach(function (link) {
      link.__bmHover = true;
      var src = link.getAttribute('data-hover-image');
      if (!src) return;

      link.addEventListener('pointerenter', function (e) {
        if (reduced) return;
        if (img.getAttribute('src') !== src) {
          img.setAttribute('src', src);
          img.setAttribute('alt', '');
          img.setAttribute('loading', 'lazy');
          img.setAttribute('decoding', 'async');
        }
        followX = e.clientX; followY = e.clientY;
        place();
        follower.classList.add('is-visible');
      });

      link.addEventListener('pointermove', function (e) {
        if (reduced) return;
        followX = e.clientX; followY = e.clientY;
        if (!followRaf) followRaf = requestAnimationFrame(place);   // one write per frame
      });

      link.addEventListener('pointerleave', function () {
        follower.classList.remove('is-visible');
      });
    });
  }

  /* --------------------------------------------------------- 6. count-up --- */
  function initCounters(scope) {
    var nodes = $$('[data-count-to]', scope).filter(function (n) { return !n.__bmCount; });
    if (!nodes.length) return;

    nodes.forEach(function (el) {
      el.__bmCount = true;
      var to = parseFloat(el.getAttribute('data-count-to'));
      if (!isFinite(to)) return;

      var decimals = (el.getAttribute('data-count-to').split('.')[1] || '').length;
      var conf = {
        el: el,
        from: parseFloat(el.getAttribute('data-count-from')) || 0,
        to: to,
        dur: parseFloat(el.getAttribute('data-count-duration')) || 1600,
        prefix: el.getAttribute('data-count-prefix') || '',
        suffix: el.getAttribute('data-count-suffix') || '',
        decimals: decimals,
        start: 0
      };

      // Reduced motion (or no observer): print the final value and stop.
      if (reduced || !supportsIO) { paintCount(conf, conf.to); return; }

      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          io.unobserve(e.target);
          conf.start = 0;
          counters.push(conf);
          requestLoop();
        });
      }, { threshold: 0.4 });
      io.observe(el);
    });
  }

  function paintCount(c, value) {
    var parts = value.toFixed(c.decimals).split('.');
    // group the integer part only — a naive global regex would comma the decimals too
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    c.el.textContent = c.prefix + parts.join('.') + c.suffix;
  }

  function stepCounters(ts) {
    for (var i = counters.length - 1; i >= 0; i--) {
      var c = counters[i];
      if (!c.start) c.start = ts;
      var p = Math.min(1, (ts - c.start) / c.dur);
      var eased = 1 - Math.pow(1 - p, 3);          // cubic ease-out, matches --e-out closely enough
      paintCount(c, c.from + (c.to - c.from) * eased);
      if (p >= 1) counters.splice(i, 1);
    }
  }

  /* ---------------------------------------------------- 7. marquee speed --- */
  function initMarquee(scope) {
    if (reduced) return;
    // a page can hold more than one (header strip + a section band), so take
    // over every track, not just the first
    $$('.marquee__track', scope).forEach(function (track) {
      if (track.__bmMarquee) return;
      var m = { track: track, x: 0, half: 0, base: 0 };
      measureOne(m);
      if (!m.half) return;                    // nothing measurable — leave CSS in charge
      track.__bmMarquee = true;
      track.classList.add('is-jsdriven');
      marquees.push(m);
    });
    requestLoop();
  }

  function measureOne(m) {
    // the CSS keyframe translates -50%, which means the content is duplicated;
    // half the scroll width is therefore one full, seamless cycle
    m.half = m.track.scrollWidth / 2;
    // match base.css's 42s-per-cycle feel exactly, whatever the content width
    m.base = m.half / 42000;
  }

  function measureMarquees() { marquees.forEach(measureOne); }

  function stepMarquees(dt) {
    // scroll velocity nudges the rate between 1× and ~1.5×. Tasteful means the
    // viewer should feel it, not catch it.
    var rate = 1 + Math.min(velocity / 55, 0.5);
    for (var i = 0; i < marquees.length; i++) {
      var m = marquees[i];
      if (!m.half) continue;
      // The section renders a pause control (WCAG 2.2.2). Once this driver has
      // taken the track over, animation-play-state no longer applies to it, so
      // the class has to be honoured here or the button does nothing.
      if (m.track.classList.contains('is-paused')) continue;
      m.x -= m.base * dt * rate;
      if (m.x <= -m.half) m.x += m.half;
      m.track.style.transform = 'translate3d(' + m.x.toFixed(2) + 'px,0,0)';
    }
  }

  function teardownMarquees() {
    marquees.forEach(function (m) {
      m.track.classList.remove('is-jsdriven');
      m.track.style.transform = '';
      m.track.__bmMarquee = false;
    });
    marquees.length = 0;
  }

  /* ------------------------------------------- 8. illustration animation ---
     snippets/illustration.liquid documents two opt-in hooks — .is-in draws the
     rosette, .is-playing runs the equaliser — and nothing in the theme had ever
     added either class, so both drawings shipped frozen. One observer, shared
     by both, adding the class once when the drawing scrolls into view.
     ------------------------------------------------------------------------ */
  var illIO = null;

  function initIllustrations(scope) {
    var nodes = $$('.ill-rosette, .ill-eq', scope).filter(function (n) { return !n.__bmIll; });
    if (!nodes.length) return;

    function light(n) {
      n.classList.add(n.classList.contains('ill-eq') ? 'is-playing' : 'is-in');
    }

    /* Reduced motion still gets the finished drawing — the rosette's resting
       state is an undrawn outline, which would read as a rendering fault. The
       snippet kills the equaliser keyframe itself under the same query. */
    if (reduced || !supportsIO) {
      nodes.forEach(function (n) { n.__bmIll = true; light(n); });
      return;
    }

    if (!illIO) {
      illIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          light(e.target);
          illIO.unobserve(e.target);
        });
      }, { rootMargin: '0px 0px -12% 0px', threshold: 0.2 });
    }
    nodes.forEach(function (n) { n.__bmIll = true; illIO.observe(n); });
  }

  /* ------------------------------------------------------- 9. curtain ------ */
  function riqMark() {
    // The logo mark, reduced to its geometry: two rings and eight jingles.
    var jingles = '';
    for (var k = 0; k < 8; k++) {
      var a = (k * 45 + 22.5) * Math.PI / 180;
      jingles += '<circle cx="' + (100 + 89 * Math.cos(a)).toFixed(2) +
                 '" cy="' + (100 + 89 * Math.sin(a)).toFixed(2) +
                 '" r="10" fill="#B0854A"/>';
    }
    return '<svg class="curtain__mark" viewBox="0 0 200 200" aria-hidden="true" focusable="false">' +
      jingles +
      '<circle cx="100" cy="100" r="76" fill="none" stroke="#6C4824" stroke-width="14"/>' +
      '<circle cx="100" cy="100" r="58" fill="none" stroke="#B0854A" stroke-width="2"/>' +
      '</svg>';
  }

  function initCurtain() {
    if (reduced) return;
    // First view of the session only. Private-mode storage throws — treat a
    // throw as "already seen" so the curtain can never appear on every click.
    try {
      if (sessionStorage.getItem('bm:curtain')) return;
      sessionStorage.setItem('bm:curtain', '1');
    } catch (err) { return; }

    // If we are already past load, the page is on screen: a curtain now would
    // be a flash of hiding, which is worse than no curtain at all.
    if (doc.readyState === 'complete') return;

    var el = doc.createElement('div');
    el.className = 'curtain';
    el.setAttribute('aria-hidden', 'true');
    el.innerHTML = riqMark();
    doc.body.appendChild(el);

    // Hard budget: inert at 300ms, gone at 700ms, regardless of load state.
    setTimeout(function () { el.classList.add('is-inert', 'is-out'); }, 300);
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 720);
  }

  /* ------------------------------------------------------------- wiring ---- */
  function init(scope) {
    initReveal(scope);
    initSplit(scope);
    initParallax(scope);
    initMagnetic(scope);
    initHoverImage(scope);
    initCounters(scope);
    initMarquee(scope);
    initIllustrations(scope);
  }

  // Reduced motion can be switched mid-session. Honour it immediately.
  function onReduceChange() {
    reduced = mqReduce.matches;
    if (reduced) {
      teardownParallax();
      teardownMarquees();
      counters.forEach(function (c) { paintCount(c, c.to); });
      counters.length = 0;
      if (follower) follower.classList.remove('is-visible');
      $$('[data-reveal]').forEach(function (n) { n.classList.add('is-in'); });
      $$('[data-split]').forEach(function (n) { n.classList.add('is-in'); });
      if (frameId) { cancelAnimationFrame(frameId); frameId = 0; }
    } else {
      init(doc);
    }
  }
  if (mqReduce.addEventListener) mqReduce.addEventListener('change', onReduceChange);
  else if (mqReduce.addListener) mqReduce.addListener(onReduceChange);

  function boot() {
    initCurtain();
    init(doc);
  }

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot);
  else boot();

  // Fonts landing late change the marquee's width; re-measure once they do.
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(measureMarquees).catch(function () {});

  // Theme editor: sections are swapped in without a reload. Drop any track the
  // swap detached — writing transforms to an orphan node forever is a leak —
  // then scan the new markup.
  doc.addEventListener('shopify:section:load', function (e) {
    var scope = e.target && e.target.nodeType === 1 ? e.target : doc;
    for (var i = marquees.length - 1; i >= 0; i--) {
      if (!marquees[i].track.isConnected) marquees.splice(i, 1);
    }
    for (var j = parallaxItems.length - 1; j >= 0; j--) {
      if (!parallaxItems[j].el.isConnected) parallaxItems.splice(j, 1);
    }
    init(scope);
  });

  window.BobMotion = { refresh: function (scope) { init(scope || doc); } };
})();

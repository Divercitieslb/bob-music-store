/* Bob Music Store — live Google Business Profile data.

   One request per visitor per day fills in the rating, review count, address,
   phone, hours, reviews and photos wherever the theme asks for them. Nothing
   here is required: every target ships with the value typed under Theme
   settings → Shop details already rendered, and this only replaces it once
   Google has answered. If the key is missing, the quota is spent, or the
   network is down, the page is exactly what Liquid rendered.

   WHY AN API AND NOT SCRAPING. Reading the public Maps page for reviews is
   against Google's terms and breaks the first time they change their markup.
   The Places API is the sanctioned route, and it is the only one that keeps
   the numbers current on its own.

   WHAT IT CANNOT DO. Place Details returns AT MOST FIVE reviews and you do not
   get to choose which five — there is no endpoint that returns all of them.
   The section links out to the full list on Google for the rest.

   CACHING AND COST. Place Details with reviews is a billable SKU. The answer is
   cached in localStorage for 24 hours, so a returning visitor costs nothing and
   a busy day costs roughly one call per new visitor. Google's Maps Platform
   terms permit caching place content for up to 30 days; 24 hours keeps "new
   review appears on the site within a day" true without paying per page view.

   ATTRIBUTION. Google requires the reviewer's name and photo, the link to the
   review, and photo author attribution. All of it is rendered — do not strip
   it to tidy the design. */
(function () {
  'use strict';

  var cfg = window.BOB_GOOGLE_PLACE;
  if (!cfg || !cfg.placeId || !cfg.key) return;

  var CACHE_KEY = 'bm-gp:' + cfg.placeId;
  var TTL = 24 * 60 * 60 * 1000;

  var FIELDS = [
    'displayName',
    'formattedAddress',
    'shortFormattedAddress',
    'nationalPhoneNumber',
    'internationalPhoneNumber',
    'rating',
    'userRatingCount',
    'googleMapsUri',
    'regularOpeningHours.weekdayDescriptions',
    'regularOpeningHours.openNow',
    'reviews',
    'photos'
  ].join(',');

  var $$ = function (s, r) {
    return Array.prototype.slice.call((r || document).querySelectorAll(s));
  };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function read() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var box = JSON.parse(raw);
      if (!box || (Date.now() - box.t) > TTL) return null;
      return box.d;
    } catch (e) { return null; }
  }

  function write(d) {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify({ t: Date.now(), d: d })); }
    catch (e) { /* private mode, quota — the fetch still worked */ }
  }

  /* ------------------------------------------------------------- painting -- */

  function stars(rating) {
    // Five glyphs, the last one clipped to the fraction. A width-clipped
    // overlay rather than half-star characters, which no brand face has.
    var pct = Math.max(0, Math.min(100, (rating / 5) * 100));
    return '<span class="gstars" role="img" aria-label="' + rating.toFixed(1) +
           ' out of 5">' +
           '<span class="gstars__bg">★★★★★</span>' +
           '<span class="gstars__fg" style="width:' + pct.toFixed(1) + '%">★★★★★</span>' +
           '</span>';
  }

  function paintScalars(d) {
    if (typeof d.rating === 'number') {
      $$('[data-gp="rating"]').forEach(function (el) {
        el.textContent = d.rating.toFixed(1);
      });
      $$('[data-gp="stars"]').forEach(function (el) {
        el.innerHTML = stars(d.rating);
      });
    }
    if (typeof d.userRatingCount === 'number') {
      $$('[data-gp="count"]').forEach(function (el) {
        el.textContent = String(d.userRatingCount);
      });
    }
    if (d.formattedAddress) {
      $$('[data-gp="address"]').forEach(function (el) {
        el.textContent = d.formattedAddress;
      });
    }
    var phone = d.nationalPhoneNumber || d.internationalPhoneNumber;
    if (phone) {
      $$('[data-gp="phone"]').forEach(function (el) {
        el.textContent = phone;
        if (el.tagName === 'A') el.href = 'tel:' + phone.replace(/[^\d+]/g, '');
      });
    }
    if (d.googleMapsUri) {
      $$('[data-gp="maps"]').forEach(function (el) { el.href = d.googleMapsUri; });
    }
    var hours = d.regularOpeningHours && d.regularOpeningHours.weekdayDescriptions;
    if (hours && hours.length) {
      $$('[data-gp="hours"]').forEach(function (el) {
        el.innerHTML = hours.map(function (line) {
          return '<span class="ghours__row">' + esc(line) + '</span>';
        }).join('');
      });
    }
    if (d.regularOpeningHours && typeof d.regularOpeningHours.openNow === 'boolean') {
      $$('[data-gp="open-now"]').forEach(function (el) {
        el.textContent = d.regularOpeningHours.openNow ? 'Open now' : 'Closed now';
        el.classList.toggle('is-open', d.regularOpeningHours.openNow);
        el.hidden = false;
      });
    }
    // Reveal anything that only makes sense once real numbers exist.
    $$('[data-gp-needs-data]').forEach(function (el) { el.hidden = false; });
  }

  function initials(name) {
    return String(name || '?').trim().charAt(0).toUpperCase();
  }

  function paintReviews(d, host) {
    var list = (d.reviews || []).filter(function (r) {
      return r.text && r.text.text && r.text.text.trim().length > 0;
    });
    var min = parseInt(host.getAttribute('data-min-rating') || '0', 10);
    if (min) list = list.filter(function (r) { return (r.rating || 0) >= min; });
    if (!list.length) return;

    host.innerHTML = list.map(function (r) {
      var a = r.authorAttribution || {};
      var body = r.text.text.trim();
      // Google returns the full review; a wall of one long one next to four
      // short ones reads badly, so long ones are clamped in CSS, not truncated
      // here — truncating would misrepresent what somebody wrote.
      return '' +
        '<article class="grev">' +
          '<div class="grev__head">' +
            (a.photoUri
              ? '<img class="grev__avatar" src="' + esc(a.photoUri) + '" alt="" width="36" height="36" loading="lazy" referrerpolicy="no-referrer">'
              : '<span class="grev__avatar grev__avatar--letter" aria-hidden="true">' + esc(initials(a.displayName)) + '</span>') +
            '<div class="grev__who">' +
              '<p class="grev__name">' + esc(a.displayName || 'A Google user') + '</p>' +
              '<p class="grev__when">' + esc(r.relativePublishTimeDescription || '') + '</p>' +
            '</div>' +
          '</div>' +
          (typeof r.rating === 'number' ? stars(r.rating) : '') +
          '<blockquote class="grev__text">' + esc(body) + '</blockquote>' +
          (a.uri ? '<a class="grev__link" href="' + esc(a.uri) + '" target="_blank" rel="noopener nofollow">Read on Google</a>' : '') +
        '</article>';
    }).join('');
    host.hidden = false;
    var sec = host.closest('[data-gp-section]');
    if (sec) sec.classList.add('has-reviews');
  }

  function paintPhotos(d, host) {
    var max = parseInt(host.getAttribute('data-max') || '8', 10);
    var skip = parseInt(host.getAttribute('data-skip') || '0', 10);
    var photos = (d.photos || []).slice(skip, skip + max);
    if (!photos.length) return;

    host.innerHTML = photos.map(function (p) {
      var url = 'https://places.googleapis.com/v1/' + p.name +
                '/media?maxHeightPx=800&maxWidthPx=800&key=' + encodeURIComponent(cfg.key);
      var att = (p.authorAttributions || [])[0] || {};
      return '' +
        '<figure class="gshot">' +
          '<img src="' + esc(url) + '" alt="" loading="lazy" decoding="async" width="400" height="400">' +
          (att.displayName
            ? '<figcaption class="gshot__by">' + esc(att.displayName) + '</figcaption>'
            : '') +
        '</figure>';
    }).join('');
    host.hidden = false;

    /* A photo request can fail on its own — the key may not have the Places
       Photos SKU enabled, or a referrer rule may cover the page but not the
       media host. Without this a failure leaves an empty grey square, which
       reads as a broken shop rather than a missing photo. Drop the frame; drop
       the whole strip if none of them arrive. */
    Array.prototype.forEach.call(host.querySelectorAll('img'), function (img) {
      img.addEventListener('error', function () {
        var fig = img.closest('.gshot');
        if (fig) fig.remove();
        if (!host.querySelector('.gshot')) {
          host.hidden = true;
          var wrap = host.closest('.gshots');
          if (wrap) wrap.hidden = true;
        }
      });
    });
  }

  function paint(d) {
    if (!d) return;
    paintScalars(d);
    $$('[data-gp-reviews]').forEach(function (h) { paintReviews(d, h); });
    $$('[data-gp-photos]').forEach(function (h) { paintPhotos(d, h); });
  }

  /* --------------------------------------------------------------- fetch -- */

  function load() {
    var cached = read();
    if (cached) { paint(cached); return; }

    fetch('https://places.googleapis.com/v1/places/' + encodeURIComponent(cfg.placeId), {
      headers: {
        'X-Goog-Api-Key': cfg.key,
        'X-Goog-FieldMask': FIELDS
      }
    })
      .then(function (r) {
        if (!r.ok) throw new Error('Places API ' + r.status);
        return r.json();
      })
      .then(function (d) { write(d); paint(d); })
      .catch(function (err) {
        // Deliberately quiet on the page: the Liquid fallback is already on
        // screen and a broken key is the merchant's problem, not the visitor's.
        if (window.console && console.warn) {
          console.warn('[bob] Google Place lookup failed — showing the values from Theme settings instead.', err);
        }
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', load);
  } else {
    load();
  }
})();

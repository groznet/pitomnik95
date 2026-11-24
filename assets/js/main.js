/* Pitomnik95 — main.js
 * Scroll reveals, soft parallax, count-up stats, Alpine components.
 * Everything respects prefers-reduced-motion.
 */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Scroll reveal ---------- */
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (reduce || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Parallax: background moves slower than foreground ---------- */
  function initParallax() {
    if (reduce) return; // preference is read once; reload applies a changed setting
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
    if (!items.length) return;
    var ticking = false;
    function update() {
      var vh = window.innerHeight;
      items.forEach(function (el) {
        var host = el.parentElement || el;
        var r = host.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var speed = parseFloat(el.getAttribute('data-parallax')) || 0.2;
        var center = r.top + r.height / 2 - vh / 2;
        el.style.transform = 'translate3d(0,' + (center * speed * -1).toFixed(1) + 'px,0)';
      });
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------- Count-up numbers ---------- */
  function initCounters() {
    var els = document.querySelectorAll('[data-count]');
    if (!els.length) return;
    function run(el) {
      var target = parseInt(el.getAttribute('data-count'), 10);
      var suffix = el.getAttribute('data-suffix') || '';
      if (reduce) { el.textContent = target + suffix; return; }
      var start = null, dur = 1800;
      function step(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased) + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { run(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.4 });
    els.forEach(function (el) { io.observe(el); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initReveal(); initParallax(); initCounters();
  });

  /* ---------- Alpine components ---------- */
  document.addEventListener('alpine:init', function () {
    // Sticky header: transparent over hero, solid after scroll
    Alpine.data('siteHeader', function () {
      return {
        scrolled: false, mobile: false, open: null,
        init: function () {
          var self = this;
          var on = function () { self.scrolled = window.scrollY > 40; };
          on(); window.addEventListener('scroll', on, { passive: true });
          this.$watch('mobile', function (v) { document.documentElement.style.overflow = v ? 'hidden' : ''; });
        }
      };
    });

    // Before / after slider
    Alpine.data('beforeAfter', function (start) {
      return { pos: start || 50 };
    });

    // Generic filter (catalog, gallery)
    Alpine.data('filterable', function (initial) {
      return {
        active: initial || 'all',
        set: function (v) { this.active = v; },
        show: function (cat) { return this.active === 'all' || this.active === cat; }
      };
    });

    // Gallery = filter + lightbox
    Alpine.data('gallery', function () {
      return {
        active: 'all', open: false, src: '', alt: '',
        set: function (v) { this.active = v; },
        show: function (cat, src, alt) {
          if (src === undefined) return this.active === 'all' || this.active === cat;
          this.src = src; this.alt = alt || ''; this.open = true; document.documentElement.style.overflow = 'hidden';
        },
        close: function () { this.open = false; document.documentElement.style.overflow = ''; }
      };
    });

    // Product detail: gallery + size picker + WhatsApp order link
    Alpine.data('product', function (cfg) {
      return {
        images: cfg.images, thumbs: cfg.thumbs, name: cfg.name, wa: cfg.wa, sizes: cfg.sizes,
        i: 0, size: 0, lb: false,
        get href() {
          var s = this.sizes[this.size];
          var t = 'Здравствуйте! Хочу заказать: ' + this.name + (s ? ' (' + s.label + ')' : '');
          return this.wa + '?text=' + encodeURIComponent(t);
        },
        get price() {
          var s = this.sizes[this.size];
          return s && s.price ? Number(s.price).toLocaleString('ru-RU') + ' ₽' : 'Цена по запросу';
        },
        fmt: function (p) { return p ? Number(p).toLocaleString('ru-RU') + ' ₽' : 'по запросу'; },
        next: function () { this.i = (this.i + 1) % this.images.length; },
        prev: function () { this.i = (this.i - 1 + this.images.length) % this.images.length; },
        openLb: function () { this.lb = true; document.documentElement.style.overflow = 'hidden'; },
        closeLb: function () { this.lb = false; document.documentElement.style.overflow = ''; }
      };
    });

    // Catalog: sidebar filters (height / light / frost zone, AND logic) + category pills + mobile drawer
    Alpine.data('catalogFilter', function (initialCat) {
      var HEIGHTS = [[0, 0.5], [0.5, 1], [1, 3], [3, 10], [10, Infinity]];
      var ZONES = [[3, 4], [5, 5], [6, 7]];
      return {
        cat: initialCat || 'all', heights: [], lights: [], zones: [], drawer: false, items: [], shown: 0,
        init: function () {
          var self = this;
          this.items = Array.prototype.map.call(document.querySelectorAll('[data-card]'), function (el) { return el.dataset; });
          this.recount();
          ['cat', 'heights', 'lights', 'zones'].forEach(function (k) { self.$watch(k, function () { self.recount(); }); });
          this.$watch('drawer', function (v) { document.body.classList.toggle('overflow-hidden', v); });
        },
        get active() { return this.heights.length + this.lights.length + this.zones.length; },
        setCat: function (c) { this.cat = c; },
        ok: function (d) {
          if (this.cat !== 'all' && d.cat !== this.cat) return false;
          if (this.heights.length) {
            var lo = parseFloat(d.hmin), hi = parseFloat(d.hmax);
            if (isNaN(lo) || isNaN(hi)) return false;
            if (!this.heights.some(function (i) { var b = HEIGHTS[i]; return lo < b[1] && hi > b[0]; })) return false;
          }
          if (this.lights.length) {
            var l = (d.light || '').split('/');
            if (!this.lights.some(function (x) { return l.indexOf(x) !== -1; })) return false;
          }
          if (this.zones.length) {
            var z = parseInt(d.zone, 10);
            if (isNaN(z) || !this.zones.some(function (i) { return z >= ZONES[i][0] && z <= ZONES[i][1]; })) return false;
          }
          return true;
        },
        recount: function () { var self = this; this.shown = this.items.filter(function (d) { return self.ok(d); }).length; },
        reset: function () { this.heights = []; this.lights = []; this.zones = []; }
      };
    });

    // Lightbox
    Alpine.data('lightbox', function () {
      return {
        open: false, src: '', alt: '',
        show: function (src, alt) { this.src = src; this.alt = alt || ''; this.open = true; document.documentElement.style.overflow = 'hidden'; },
        close: function () { this.open = false; document.documentElement.style.overflow = ''; }
      };
    });
  });
})();

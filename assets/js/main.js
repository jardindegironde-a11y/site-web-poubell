/* ==========================================================================
   BACNIFIQUE — main.js
   Scène produit pilotée au scroll + interactions du site
   ========================================================================== */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function clamp(v, min, max) { return v < min ? min : (v > max ? max : v); }
  function smoothstep(edge0, edge1, x) {
    var t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
    return t * t * (3 - 2 * t);
  }

  /* ---------- Header : état au scroll + menu mobile ---------- */
  var header = document.getElementById('siteHeader');
  var navToggle = document.getElementById('navToggle');
  var mobileNav = document.getElementById('mobileNav');

  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', function () {
      var open = mobileNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Modal de contact ---------- */
  var modal = document.getElementById('contactModal');
  var modalClose = document.getElementById('modalClose');
  var lastFocused = null;

  function openModal(e) {
    if (e) e.preventDefault();
    lastFocused = document.activeElement;
    modal.hidden = false;
    document.body.classList.add('modal-open');
    if (modalClose) modalClose.focus();
  }
  function closeModal() {
    modal.hidden = true;
    document.body.classList.remove('modal-open');
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  if (modal && modalClose) {
    document.querySelectorAll('[data-modal-trigger]').forEach(function (trigger) {
      trigger.addEventListener('click', openModal);
    });
    modalClose.addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hidden) closeModal();
    });
  }

  /* ---------- Comparateurs avant / après ---------- */
  document.querySelectorAll('[data-ba-slider]').forEach(function (slider) {
    var before = slider.querySelector('.ba-img-before');
    var handle = slider.querySelector('.ba-handle');
    var range = slider.querySelector('.ba-range');
    if (!before || !handle || !range) return;

    function update(value) {
      before.style.clipPath = 'inset(0 ' + (100 - value) + '% 0 0)';
      handle.style.left = value + '%';
    }
    range.addEventListener('input', function () { update(Number(range.value)); });
    update(Number(range.value));
  });

  /* ---------- Révélation des blocs au scroll ---------- */
  var revealEls = document.querySelectorAll('[data-reveal]');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    revealEls.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ==========================================================================
     Scène produit : séquence d'images dessinée sur canvas, pilotée au scroll
     ========================================================================== */
  var stage = document.getElementById('stage');
  var canvas = document.getElementById('binCanvas');
  var dirtyImg = document.getElementById('productDirty');

  if (!stage || !canvas) return;

  var FRAME_COUNT = 72;
  var isSmall = window.matchMedia('(max-width: 900px)').matches;
  var frameDir = isSmall ? 'assets/img/seq-m/' : 'assets/img/seq-d/';

  function framePath(i) {
    return frameDir + String(i).padStart(3, '0') + '.webp';
  }

  var frames = new Array(FRAME_COUNT);
  var loadedCount = 0;
  var ctx = canvas.getContext('2d', { alpha: true });
  var currentIndex = -1;

  /* --- dimensionnement du canvas --- */
  var cssSize = 0;
  function sizeCanvas() {
    var rect = canvas.getBoundingClientRect();
    if (!rect.width) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cssSize = rect.width;
    canvas.width = Math.round(rect.width * dpr);
    canvas.height = Math.round(rect.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    currentIndex = -1; // force un redraw
  }

  /* --- dessine la frame la plus proche disponible --- */
  function drawFrame(index) {
    var img = frames[index];
    if (!img || !img.complete || !img.naturalWidth) {
      var found = null;
      for (var d = 1; d < FRAME_COUNT; d++) {
        var a = frames[index - d], b = frames[index + d];
        if (a && a.complete && a.naturalWidth) { found = a; break; }
        if (b && b.complete && b.naturalWidth) { found = b; break; }
      }
      if (!found) return;
      img = found;
    }
    var rect = canvas.getBoundingClientRect();
    ctx.clearRect(0, 0, rect.width, rect.height);
    ctx.drawImage(img, 0, 0, rect.width, rect.height);
    currentIndex = index;
  }

  /* --- chargement progressif : quelques frames clés, puis le reste --- */
  function loadFrame(i) {
    if (frames[i]) return frames[i];
    var img = new Image();
    img.decoding = 'async';
    img.src = framePath(i);
    img.onload = function () {
      loadedCount++;
      if (currentIndex === -1) drawFrame(0);
    };
    img.onerror = function () { loadedCount++; };
    frames[i] = img;
    return img;
  }

  // priorité : la première frame, puis un échantillon réparti, puis tout le reste
  loadFrame(0);
  for (var s = 0; s < FRAME_COUNT; s += 8) loadFrame(s);

  function loadRemaining() {
    var i = 0;
    (function next() {
      while (i < FRAME_COUNT && frames[i]) i++;
      if (i >= FRAME_COUNT) return;
      var img = loadFrame(i);
      if (img.complete) { next(); return; }
      img.addEventListener('load', next, { once: true });
      img.addEventListener('error', next, { once: true });
    })();
  }
  if ('requestIdleCallback' in window) {
    window.requestIdleCallback(loadRemaining, { timeout: 2500 });
  } else {
    setTimeout(loadRemaining, 900);
  }

  /* --- mode replié : pas d'animation liée au scroll --- */
  if (reduceMotion) {
    stage.classList.add('is-static');
    sizeCanvas();
    var firstImg = frames[0];
    if (firstImg.complete && firstImg.naturalWidth) drawFrame(0);
    else firstImg.addEventListener('load', function () { sizeCanvas(); drawFrame(0); }, { once: true });
    window.addEventListener('resize', function () { sizeCanvas(); drawFrame(currentIndex < 0 ? 0 : currentIndex); });
    return;
  }

  /* --- panneaux, points de progression, indice de scroll --- */
  var panels = Array.prototype.slice.call(stage.querySelectorAll('.panel'));
  var dots = Array.prototype.slice.call(stage.querySelectorAll('.stage-progress .dot'));
  var scrollHint = document.getElementById('scrollHint');
  var productFrame = stage.querySelector('.product-frame');

  // fenêtre d'affichage de chaque panneau, en progression 0 → 1
  var PANEL_WINDOWS = [
    [0.00, 0.14],
    [0.20, 0.42],
    [0.46, 0.68],
    [0.74, 1.00]
  ];

  var stageTop = 0;
  var scrollRange = 1;
  var ticking = false;

  function measure() {
    stageTop = stage.offsetTop;
    scrollRange = Math.max(stage.offsetHeight - window.innerHeight, 1);
    sizeCanvas();
  }

  function render() {
    ticking = false;
    var progress = clamp((window.scrollY - stageTop) / scrollRange, 0, 1);

    // rotation du produit : démarre après la révélation du nettoyage
    var spin = smoothstep(0.06, 1, progress);
    var index = Math.min(FRAME_COUNT - 1, Math.round(spin * (FRAME_COUNT - 1)));
    if (index !== currentIndex) drawFrame(index);

    // révélation « sale → propre »
    if (dirtyImg) dirtyImg.style.opacity = String(1 - smoothstep(0.015, 0.10, progress));

    // léger recul du produit pour la profondeur
    if (productFrame) {
      var depth = 1 - 0.07 * smoothstep(0, 0.55, progress);
      productFrame.style.transform = 'scale(' + depth.toFixed(4) + ')';
    }

    // panneaux
    var active = -1;
    for (var i = 0; i < panels.length; i++) {
      var w = PANEL_WINDOWS[i];
      var on = w && progress >= w[0] && progress <= w[1];
      panels[i].classList.toggle('is-active', !!on);
      if (on) active = i;
    }
    for (var d = 0; d < dots.length; d++) {
      dots[d].classList.toggle('is-on', d === active);
    }

    if (scrollHint) scrollHint.classList.toggle('is-hidden', progress > 0.04);
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 12);
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(render);
      ticking = true;
    }
  }

  measure();
  render();

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { measure(); render(); });
  window.addEventListener('load', function () { measure(); render(); });
})();

(function () {
  'use strict';

  /* ---------- Header: scrolled state + mobile nav ---------- */
  var header = document.getElementById('siteHeader');
  var navToggle = document.getElementById('navToggle');
  var mobileNav = document.getElementById('mobileNav');

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

  document.getElementById('year').textContent = new Date().getFullYear();

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Smooth anchor navigation (kept separate from scroll-linked
     hero animation, which needs raw/instant scroll positions to stay in sync) ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var id = link.getAttribute('href').slice(1);
      var target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
      history.pushState(null, '', '#' + id);
    });
  });

  /* ---------- Scroll-linked bin animation ---------- */
  var hero = document.getElementById('hero');
  var binScene = document.getElementById('binScene');
  var lowPower = (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2) ||
                 (navigator.deviceMemory && navigator.deviceMemory <= 2);

  function supportsWebGL() {
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
    } catch (e) {
      return false;
    }
  }

  if (reduceMotion || lowPower) {
    hero.classList.add('is-simplified');
  } else if (supportsWebGL()) {
    binScene.classList.add('is-3d');
    initWebglBin();
  } else {
    initSvgScrollBin();
  }

  function makeScrollProgress(callback) {
    var ticking = false;
    var heroTop = 0;
    var scrollRange = 1;

    function measure() {
      heroTop = hero.offsetTop;
      scrollRange = Math.max(hero.offsetHeight - window.innerHeight, 1);
    }

    function tick() {
      ticking = false;
      var progress = Math.max(0, Math.min(1, (window.scrollY - heroTop) / scrollRange));
      callback(progress);
    }

    function onScroll() {
      if (!ticking) {
        window.requestAnimationFrame(tick);
        ticking = true;
      }
    }

    measure();
    tick();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () {
      measure();
      tick();
    });

    return { measure: measure, tick: tick };
  }

  function bindHeadlineAndCta(progress) {
    var dirtyOpacity = 1 - smoothstepJs(0.34, 0.5, progress);
    var cleanOpacity = smoothstepJs(0.44, 0.6, progress);
    var headlineDirty = document.querySelector('.headline-dirty');
    var headlineClean = document.querySelector('.headline-clean');
    var heroCta = document.getElementById('heroCta');
    headlineDirty.style.opacity = String(dirtyOpacity);
    headlineDirty.style.transform = 'translateY(' + (-14 * (1 - dirtyOpacity)) + 'px)';
    headlineClean.style.opacity = String(cleanOpacity);
    headlineClean.style.transform = 'translateY(' + (14 * (1 - cleanOpacity)) + 'px)';

    var ctaOpacity = smoothstepJs(0.5, 0.68, progress);
    heroCta.style.opacity = String(ctaOpacity);
    heroCta.style.transform = 'translateY(' + (16 * (1 - ctaOpacity)) + 'px)';
    heroCta.style.pointerEvents = ctaOpacity > 0.5 ? 'auto' : 'none';
  }

  function smoothstepJs(edge0, edge1, x) {
    var t = Math.max(0, Math.min(1, (x - edge0) / (edge1 - edge0)));
    return t * t * (3 - 2 * t);
  }

  function initWebglBin() {
    var canvas = document.getElementById('binCanvas');

    import('./bin-scene.js').then(function (mod) {
      var scene = mod.initBinScene(canvas);
      var container = binScene;

      function resize() {
        var rect = container.getBoundingClientRect();
        scene.resize(rect.width, rect.height);
      }
      resize();
      window.addEventListener('resize', resize);

      makeScrollProgress(function (progress) {
        scene.render(progress);
        bindHeadlineAndCta(progress);
      });
    }).catch(function () {
      binScene.classList.remove('is-3d');
      initSvgScrollBin();
    });
  }

  function initSvgScrollBin() {
    var grime = document.getElementById('binGrime');
    var foam = document.getElementById('foamGroup');
    var water = document.getElementById('waterGroup');
    var sparkle = document.getElementById('sparkleGroup');
    var shine = document.getElementById('shineSweep');
    var lid = document.getElementById('binLid');

    function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
    function triangle(x, start, peak, end) {
      if (x <= start || x >= end) return 0;
      if (x <= peak) return (x - start) / (peak - start);
      return 1 - (x - peak) / (end - peak);
    }

    makeScrollProgress(function (progress) {
      grime.style.opacity = String(clamp(1 - progress * 1.7, 0, 1));
      foam.style.opacity = String(triangle(progress, 0.08, 0.38, 0.78));
      water.style.opacity = String(smoothstepJs(0.45, 0.85, progress));
      sparkle.style.opacity = String(smoothstepJs(0.68, 0.98, progress));
      shine.style.opacity = String(smoothstepJs(0.6, 0.92, progress) * 0.9);

      var lidAngle = -18 * smoothstepJs(0.78, 1, progress);
      lid.style.transform = 'rotate(' + lidAngle + 'deg)';

      bindHeadlineAndCta(progress);
    });
  }

  /* ---------- Booking form: live price + submit ---------- */
  var form = document.getElementById('bookingForm');
  var binCount = document.getElementById('binCount');
  var priceTotal = document.getElementById('priceTotal');
  var formStatus = document.getElementById('formStatus');
  var submitBtn = document.getElementById('submitBtn');
  var formWrap = document.querySelector('.booking-form-wrap');

  var PRICE_PER_BIN = 25;

  function updatePrice() {
    var count = parseInt(binCount.value, 10) || 1;
    priceTotal.textContent = (count * PRICE_PER_BIN) + ' €';
  }
  binCount.addEventListener('change', updatePrice);
  updatePrice();

  var dateInput = document.getElementById('date');
  var today = new Date().toISOString().split('T')[0];
  dateInput.setAttribute('min', today);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    formStatus.textContent = '';

    if (!form.reportValidity()) return;

    var honeypot = form.querySelector('.hp-field').value;
    if (honeypot) return;

    var data = {
      fullName: form.fullName.value.trim(),
      phone: form.phone.value.trim(),
      address: form.address.value.trim(),
      postalCode: form.postalCode.value.trim(),
      city: form.city.value.trim(),
      binCount: form.binCount.value,
      date: form.date.value,
      timeSlot: form.timeSlot.value,
      notes: form.notes.value.trim(),
      total: (parseInt(form.binCount.value, 10) || 1) * PRICE_PER_BIN
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'Envoi en cours...';

    fetch('send.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (res) { return res.json().catch(function () { return { success: res.ok }; }); })
      .then(function (json) {
        if (json && json.success) {
          formWrap.classList.add('is-success');
          formWrap.querySelector('.booking-success').scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
          throw new Error(json && json.message ? json.message : 'Erreur inconnue');
        }
      })
      .catch(function () {
        formStatus.textContent = "Une erreur est survenue. Merci de réessayer ou de nous appeler directement.";
        submitBtn.disabled = false;
        submitBtn.textContent = 'Confirmer ma demande de rendez-vous';
      });
  });
})();

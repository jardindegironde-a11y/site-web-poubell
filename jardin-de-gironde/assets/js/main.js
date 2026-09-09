/* =========================================================
   Jardin de Gironde — interactions
   Aucune dépendance. Chargé en `defer`.
   ========================================================= */
(function () {
  'use strict';

  /* -------------------------------------------------------
     CONFIGURATION — à ajuster après création des actions de
     conversion dans Google Ads (voir README.md).
     ------------------------------------------------------- */
  var CONFIG = {
    // Identifiant Google Ads (déjà présent dans le <head> de chaque page)
    adsId: 'AW-18308555635',
    // Libellés des actions de conversion Google Ads.
    // Format attendu : 'AW-18308555635/AbC-D_efGhIjKlMnOp'
    conversions: {
      devis: '',   // envoi du formulaire de devis (déclenché sur merci.html)
      appel: ''    // clic sur un numéro de téléphone
    },
    // Points d'envoi essayés dans l'ordre, jusqu'au premier qui répond.
    //   send.php ............ hébergement mutualisé Hostinger (PHP + e-mail)
    //   /hcgi/platform/... .. base Hostinger Horizons (collection devis_requests)
    endpoints: [
      'send.php',
      '/hcgi/platform/api/collections/devis_requests/records'
    ],
    // Adresse de repli si l'endpoint n'est pas joignable.
    fallbackEmail: 'jardindegironde@gmail.com',
    thanksUrl: 'merci.html'
  };

  var d = document;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function on(el, ev, fn) { if (el) el.addEventListener(ev, fn); }
  function all(sel, root) { return Array.prototype.slice.call((root || d).querySelectorAll(sel)); }

  /* ---------- Entête : bordure au défilement ---------- */
  var header = d.getElementById('siteHeader');
  var actionBar = d.querySelector('.action-bar');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('is-stuck', y > 8);
    if (actionBar) actionBar.classList.toggle('show', y > 420);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Menu mobile ---------- */
  var toggle = d.getElementById('navToggle');
  var mobileNav = d.getElementById('mobileNav');
  on(toggle, 'click', function () {
    var open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    if (mobileNav) mobileNav.classList.toggle('open', !open);
  });
  all('#mobileNav a').forEach(function (a) {
    on(a, 'click', function () {
      if (toggle) toggle.setAttribute('aria-expanded', 'false');
      if (mobileNav) mobileNav.classList.remove('open');
    });
  });

  /* ---------- Apparitions au défilement ---------- */
  var revealables = all('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Vidéo : lecture seulement quand elle est visible ---------- */
  all('video[data-lazy]').forEach(function (video) {
    if (!('IntersectionObserver' in window)) { video.play().catch(function () {}); return; }
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          video.muted = true;
          if (!video.getAttribute('src') && video.dataset.src) {
            // La source n'est chargée qu'à l'approche de la section : le play()
            // doit attendre que le navigateur ait de quoi lire.
            video.setAttribute('src', video.dataset.src);
            video.load();
            video.addEventListener('canplay', function () {
              if (!reduced) video.play().catch(function () {});
            }, { once: true });
          } else if (!reduced) {
            video.play().catch(function () {});
          }
        } else if (!video.paused) {
          video.pause();
        }
      });
    }, { threshold: 0.25 });
    vio.observe(video);
  });

  /* ---------- Suivi Google Ads ---------- */
  function track(name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
  }
  function conversion(key, params) {
    var label = CONFIG.conversions[key];
    if (!label || typeof window.gtag !== 'function') return;
    var payload = { send_to: label };
    for (var k in params) payload[k] = params[k];
    window.gtag('event', 'conversion', payload);
  }

  // Clic sur un numéro de téléphone = conversion « appel »
  all('a[href^="tel:"]').forEach(function (a) {
    on(a, 'click', function () {
      track('clic_telephone', { emplacement: a.dataset.loc || 'page' });
      conversion('appel', { value: 1.0, currency: 'EUR' });
    });
  });

  /* ---------- Paramètres de campagne (gclid, UTM) ---------- */
  var CAMPAIGN_KEYS = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  function readCampaign() {
    var stored = {};
    try { stored = JSON.parse(sessionStorage.getItem('jdg_campagne') || '{}'); } catch (e) { stored = {}; }
    var params = new URLSearchParams(window.location.search);
    var found = false;
    CAMPAIGN_KEYS.forEach(function (k) {
      var v = params.get(k);
      if (v) { stored[k] = v; found = true; }
    });
    if (found) {
      stored.arrivee = stored.arrivee || new Date().toISOString();
      stored.page_entree = stored.page_entree || window.location.pathname;
      try { sessionStorage.setItem('jdg_campagne', JSON.stringify(stored)); } catch (e) {}
    }
    return stored;
  }
  var campaign = readCampaign();

  function campaignSummary() {
    var parts = [];
    CAMPAIGN_KEYS.forEach(function (k) { if (campaign[k]) parts.push(k + '=' + campaign[k]); });
    if (campaign.page_entree) parts.push('page_entree=' + campaign.page_entree);
    return parts.join(' | ');
  }

  /* ---------- Formulaire de devis ---------- */
  all('form[data-devis]').forEach(function (form) {
    var statusEl = form.querySelector('.form-status');
    var submitBtn = form.querySelector('button[type="submit"]');
    var origin = form.dataset.origine || d.title;

    on(form, 'submit', function (e) {
      e.preventDefault();

      // Pot de miel anti-robot
      if (form.querySelector('[name="site"]') && form.querySelector('[name="site"]').value) return;

      if (!form.checkValidity()) { form.reportValidity(); return; }

      var data = {
        nom: form.nom.value.trim(),
        email: form.email.value.trim(),
        telephone: form.telephone.value.trim(),
        ville: form.ville ? form.ville.value.trim() : '',
        service: form.service ? form.service.value : '',
        message: form.message ? form.message.value.trim() : ''
      };

      // Les infos de campagne sont ajoutées au message : elles arrivent
      // dans la demande même si la base ne possède pas de champ dédié.
      var meta = ['Origine : ' + origin];
      var camp = campaignSummary();
      if (camp) meta.push('Campagne : ' + camp);
      data.message = (data.message ? data.message + '\n\n' : '') + '— ' + meta.join(' — ');
      CAMPAIGN_KEYS.forEach(function (k) { if (campaign[k]) data[k] = campaign[k]; });
      data.origine = origin;

      if (statusEl) { statusEl.textContent = ''; statusEl.classList.remove('error'); }
      if (submitBtn) { submitBtn.disabled = true; submitBtn.dataset.label = submitBtn.textContent; submitBtn.textContent = 'Envoi en cours…'; }

      track('demande_devis', { service: data.service, origine: origin });

      // Essaie chaque point d'envoi, du premier au dernier.
      function send(index) {
        if (index >= CONFIG.endpoints.length) return Promise.reject(new Error('aucun endpoint'));
        return fetch(CONFIG.endpoints[index], {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        }).then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res;
        }).catch(function (err) {
          if (index + 1 < CONFIG.endpoints.length) return send(index + 1);
          throw err;
        });
      }

      send(0)
        .then(function () {
          try { sessionStorage.setItem('jdg_devis_ok', '1'); } catch (err) {}
          window.location.href = CONFIG.thanksUrl;
        })
        .catch(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitBtn.dataset.label || 'Recevoir mon devis gratuit'; }
          if (statusEl) {
            statusEl.classList.add('error');
            statusEl.innerHTML = 'L\'envoi a échoué. Appelez-nous au <a href="tel:+33630644709">06 30 64 47 09</a> ' +
              'ou écrivez à <a href="mailto:' + CONFIG.fallbackEmail + '">' + CONFIG.fallbackEmail + '</a>.';
          }
        });
    });
  });

  /* ---------- Conversion sur la page de remerciement ---------- */
  if (d.body.dataset.page === 'merci') {
    conversion('devis', {
      value: 1.0,
      currency: 'EUR',
      transaction_id: 'devis_' + Date.now()
    });
    track('devis_envoye', {});
  }

  /* ---------- Année du copyright ---------- */
  all('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();

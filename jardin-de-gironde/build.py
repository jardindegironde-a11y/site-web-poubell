#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du site Jardin de Gironde.

Toutes les pages HTML du dossier sont produites par ce script à partir du
contenu défini ci-dessous. Pour modifier un texte, un service ou une FAQ :
éditez ce fichier puis relancez `python3 build.py`.

    cd jardin-de-gironde && python3 build.py
"""

import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))

# =====================================================================
#  Identité
# =====================================================================
SITE = "Jardin de Gironde"
BASE_URL = "https://www.jardindegironde.fr"
PHONE_DISPLAY = "06 30 64 47 09"
PHONE_HREF = "tel:+33630644709"
EMAIL = "jardindegironde@gmail.com"
ADS_ID = "AW-18308555635"
ZONE = "Toute la Gironde"
HOURS = "Lun – Sam, 8 h – 19 h"

VILLES = [
    "Bordeaux", "Mérignac", "Pessac", "Talence", "Bègles", "Villenave-d'Ornon",
    "Gradignan", "Cestas", "Canéjan", "Le Haillan", "Le Bouscat", "Bruges",
    "Eysines", "Saint-Médard-en-Jalles", "Léognan", "Cadaujac", "La Brède",
    "Martillac", "Créon", "Libourne", "Arcachon", "Andernos-les-Bains",
]

SERVICES_FORM = [
    "Entretien de jardins", "Tonte de pelouse", "Taille de haies et arbustes",
    "Débroussaillage", "Désherbage", "Création d'espaces verts",
    "Plantation de végétaux", "Engazonnement", "Nettoyage haute pression",
    "Nettoyage de toiture et gouttières", "Autre",
]

# =====================================================================
#  Icônes (SVG inline, trait 1.7)
# =====================================================================
def icon(name, cls="", size=None):
    paths = {
        "check": '<path d="M20 6 9 17l-5-5"/>',
        "check-circle": '<circle cx="12" cy="12" r="9"/><path d="M8.5 12.2l2.5 2.5 4.6-5"/>',
        "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M3 7l9 6 9-6"/>',
        "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.3 2"/>',
        "arrow": '<path d="M5 12h13"/><path d="M12.5 5.5 19 12l-6.5 6.5"/>',
        "shield": '<path d="M12 3l7.5 3v5.5c0 4.7-3.2 8.2-7.5 9.5-4.3-1.3-7.5-4.8-7.5-9.5V6z"/><path d="M9 12l2.2 2.2L15.3 10"/>',
        "leaf": '<path d="M20 4C10 4 4 9 4 16c0 2.2.7 3.4.7 3.4S9 12 17 9.5C12.8 12.2 9 15.5 7.4 20"/>',
        "euro": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.8A4.3 4.3 0 0 0 9 11.2m6.5 4A4.3 4.3 0 0 1 9 12.8M6.8 11h6m-6 2.6h6"/>',
        "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3.5v3m8-3v3"/>',
        "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 1-5.9L3.5 9.7l5.9-.8z"/>',
    }
    s = size or 20
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


# =====================================================================
#  Logo — reproduction vectorielle de l'écusson Jardin de Gironde
# =====================================================================
# Si vous déposez votre fichier de logo dans assets/img/ (logo.png, logo.webp
# ou logo.svg), il est utilisé automatiquement à la place de la reproduction
# vectorielle ci-dessous. Relancez simplement `python3 build.py`.
LOGO_FILE = next(
    (f"assets/img/{n}" for n in ("logo.svg", "logo.png", "logo.webp", "logo-jdg.svg")
     if os.path.exists(os.path.join(HERE, "assets/img", n))),
    None,
)


def logo_svg(height=46, cls="brand-logo"):
    if LOGO_FILE:
        return (f'<img class="{cls}" src="{LOGO_FILE}" alt="{SITE}" '
                f'height="{height}" decoding="async">')
    return f'''<svg class="{cls}" viewBox="0 0 560 480" height="{height}" role="img" aria-label="{SITE}">
  <path d="M26 104c0-14 6-23 19-27C160 42 400 42 515 77c13 4 19 13 19 27v238c0 12-5 20-15 27L297 462c-10 7-24 7-34 0L41 369c-10-7-15-15-15-27z" fill="#17662C"/>
  <path d="M50 116c0-10 5-17 15-20C173 64 387 64 495 96c10 3 15 10 15 20v226c0 9-4 15-12 21L292 434c-8 5-16 5-24 0L62 363c-8-6-12-12-12-21z" fill="none" stroke="#ffffff" stroke-width="10"/>
  <text class="logo-word" x="280" y="222" text-anchor="middle" fill="#ffffff"
        textLength="424" lengthAdjust="spacingAndGlyphs">JARDIN</text>
  <path d="M78 262h128M354 262h128" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
  <text class="logo-script" x="280" y="276" text-anchor="middle" fill="#ffffff"
        textLength="78" lengthAdjust="spacingAndGlyphs">de</text>
  <text class="logo-word" x="280" y="360" text-anchor="middle" fill="#ffffff"
        textLength="430" lengthAdjust="spacingAndGlyphs">GIRONDE</text>
</svg>'''


LOGO_CSS = """
.brand-logo { height: 50px; width: auto; }
.site-footer .brand-logo, .thanks .brand-logo { height: 76px; }
@media (min-width: 700px) { .brand-logo { height: 62px; } }
"""


# =====================================================================
#  Blocs communs
# =====================================================================
def head(title, description, canonical, preload_img=None, extra_css="", noindex=False):
    robots = "noindex, nofollow" if noindex else "index, follow"
    preload = ""
    if preload_img:
        name, widths, psizes = preload_img
        srcset = ", ".join(f"assets/img/{name}-{w}.webp {w}w" for w in widths)
        preload = ('\n<link rel="preload" as="image" fetchpriority="high" '
                   f'href="assets/img/{name}-{widths[0]}.webp" '
                   f'imagesrcset="{srcset}" imagesizes="{psizes}">')
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#17662C">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}/assets/img/creation-jardin-1000.webp">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script>document.documentElement.className+=" js";</script>
<link rel="stylesheet" href="assets/css/style.css">{preload}
<style>{LOGO_CSS}{extra_css}</style>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ADS_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ADS_ID}');
</script>
'''


def local_business_jsonld():
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "%(base)s/#organisation",
  "name": "%(site)s",
  "url": "%(base)s/",
  "image": "%(base)s/assets/img/creation-jardin-1000.webp",
  "telephone": "+33630644709",
  "email": "%(email)s",
  "description": "Entreprise d'entretien et de création de jardins en Gironde : tonte de pelouse, taille de haies, débroussaillage, désherbage, engazonnement et aménagement paysager.",
  "priceRange": "€€",
  "areaServed": { "@type": "AdministrativeArea", "name": "Gironde" },
  "address": { "@type": "PostalAddress", "addressRegion": "Gironde", "addressCountry": "FR" },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    "opens": "08:00", "closes": "19:00"
  }]
}
</script>''' % {"base": BASE_URL, "site": SITE, "email": EMAIL}


def faq_jsonld(items):
    entries = []
    for q, a in items:
        entries.append(
            '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
            % (_json_str(q), _json_str(a))
        )
    return ('<script type="application/ld+json">\n'
            '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}\n'
            '</script>' % ",".join(entries))


def _json_str(text):
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'


NAV_ITEMS = [
    ("Services", "index.html#services"),
    ("Réalisations", "index.html#realisations"),
    ("Crédit d'impôt", "index.html#credit-impot"),
    ("Contact", "index.html#devis"),
]


def header(minimal=False, home=False):
    """minimal=True : entête épurée pour les pages de campagne Google Ads."""
    prefix = "" if home else ""
    nav = ""
    mobile = ""
    if not minimal:
        links = "".join(
            f'<a href="{"#" + h.split("#")[1] if home and "#" in h else h}">{l}</a>'
            for l, h in NAV_ITEMS
        )
        nav = f'<nav class="main-nav" aria-label="Navigation principale">{links}</nav>'
        mobile = f'''
  <div class="mobile-nav" id="mobileNav">
    <div class="container mobile-nav-inner">
      {links}
      <a href="{"#devis" if home else "index.html#devis"}" class="btn btn-primary">Devis gratuit</a>
    </div>
  </div>'''
    toggle = "" if minimal else '''<button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="mobileNav" aria-label="Ouvrir le menu">
        <span></span><span></span><span></span>
      </button>'''
    cta_href = "#devis" if home or minimal else "index.html#devis"
    return f'''<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="site-header" id="siteHeader">
  <div class="container header-inner">
    <a class="brand" href="{'#top' if home else 'index.html'}" aria-label="{SITE} — accueil">
      {logo_svg()}
    </a>
    {nav}
    <div class="header-actions">
      <a class="header-tel" href="{PHONE_HREF}" data-loc="entete">{icon('phone', size=16)} {PHONE_DISPLAY}</a>
      <a class="btn btn-primary header-cta" href="{cta_href}">Devis gratuit</a>
      {toggle}
    </div>
  </div>{mobile}
</header>{prefix}'''


def action_bar(devis_href="#devis"):
    return f'''<div class="action-bar">
  <a class="btn btn-ghost" href="{PHONE_HREF}" data-loc="barre-mobile">{icon('phone', size=16)} Appeler</a>
  <a class="btn btn-primary" href="{devis_href}">Devis gratuit</a>
</div>'''


def footer(home=False):
    p = "" if home else "index.html"
    services = [
        ("Entretien de jardins", "entretien-jardins.html"),
        ("Tonte de pelouse", "tonte-pelouse.html"),
        ("Taille de haies et arbustes", "taille-haies.html"),
        ("Débroussaillage", "debroussaillage.html"),
        ("Création d'espaces verts", "creation-espaces-verts.html"),
        ("Nettoyage haute pression", "nettoyage-haute-pression.html"),
        ("Toitures et gouttières", "nettoyage-toiture-gouttiere.html"),
    ]
    svc = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in services)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="{p or '#top'}" aria-label="{SITE}">{logo_svg(66)}</a>
        <p>Entretien et création d'espaces verts en Gironde. Une équipe locale,
           un travail soigné, des devis clairs — pour les particuliers comme
           pour les professionnels.</p>
      </div>
      <div>
        <h4>Prestations</h4>
        <ul>{svc}</ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="{PHONE_HREF}" data-loc="pied-de-page">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ZONE}</li>
          <li>{HOURS}</li>
        </ul>
      </div>
      <div>
        <h4>Informations</h4>
        <ul>
          <li><a href="{p}#credit-impot">Crédit d'impôt 50 %</a></li>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><a href="politique-confidentialite.html">Politique de confidentialité</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span data-year></span> {SITE} — Services à la personne.</p>
      <p>Site conçu pour être simple, rapide et honnête.</p>
    </div>
  </div>
</footer>'''


def scripts():
    return '<script src="assets/js/main.js" defer></script>'


def form_card(origine, titre="Recevoir mon devis gratuit", service_default="Entretien de jardins"):
    options = "".join(
        f'<option value="{html.escape(s)}"{" selected" if s == service_default else ""}>{html.escape(s)}</option>'
        for s in SERVICES_FORM
    )
    return f'''<div class="form-card">
  <h2 class="h3">{titre}</h2>
  <p class="small muted" style="margin-top:8px">Réponse sous 24 h ouvrées. Sans engagement.</p>
  <form class="form-grid" data-devis data-origine="{html.escape(origine)}" style="margin-top:22px" novalidate>
    <input type="text" name="site" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="field-split">
      <div class="field">
        <label for="nom-{_slug(origine)}">Nom et prénom</label>
        <input id="nom-{_slug(origine)}" name="nom" type="text" required autocomplete="name" placeholder="Marie Dupont">
      </div>
      <div class="field">
        <label for="tel-{_slug(origine)}">Téléphone</label>
        <input id="tel-{_slug(origine)}" name="telephone" type="tel" required autocomplete="tel" placeholder="06 12 34 56 78">
      </div>
    </div>
    <div class="field-split">
      <div class="field">
        <label for="mail-{_slug(origine)}">E-mail</label>
        <input id="mail-{_slug(origine)}" name="email" type="email" required autocomplete="email" placeholder="marie@exemple.fr">
      </div>
      <div class="field">
        <label for="ville-{_slug(origine)}">Ville</label>
        <input id="ville-{_slug(origine)}" name="ville" type="text" autocomplete="address-level2" placeholder="Bordeaux, Mérignac…">
      </div>
    </div>
    <div class="field">
      <label for="svc-{_slug(origine)}">Prestation souhaitée</label>
      <select id="svc-{_slug(origine)}" name="service">{options}</select>
    </div>
    <div class="field">
      <label for="msg-{_slug(origine)}">Votre projet <span class="muted small">(facultatif)</span></label>
      <textarea id="msg-{_slug(origine)}" name="message" rows="4" placeholder="Surface du terrain, fréquence souhaitée, délais…"></textarea>
    </div>
    <button type="submit" class="btn btn-primary btn-lg btn-block">Recevoir mon devis gratuit</button>
    <p class="form-status" role="status" aria-live="polite"></p>
    <p class="form-consent">En envoyant ce formulaire, vous acceptez d'être recontacté au sujet de votre demande.
      Vos données ne sont ni revendues ni utilisées à d'autres fins — voir la
      <a href="politique-confidentialite.html">politique de confidentialité</a>.</p>
  </form>
</div>'''


def _slug(text):
    out = []
    for ch in text.lower():
        out.append(ch if ch.isalnum() else "-")
    return "".join(out).strip("-")[:24]


def picture(name, widths, alt, ratio=None, sizes="(min-width: 900px) 50vw, 100vw",
            eager=False, cls=""):
    """<img> responsive en WebP."""
    srcset = ", ".join(f"assets/img/{name}-{w}.webp {w}w" for w in widths)
    big = widths[0]
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    style = f' style="aspect-ratio:{ratio}"' if ratio else ""
    return (f'<img class="{cls}" src="assets/img/{name}-{big}.webp" srcset="{srcset}" '
            f'sizes="{sizes}" alt="{html.escape(alt)}" {loading} decoding="async"{style}>')


def trust_row(items=None):
    items = items or [
        ("calendar", "Devis gratuit sous 24 h"),
        ("euro", "Crédit d'impôt de 50 %"),
        ("shield", "Entreprise déclarée services à la personne"),
        ("pin", ZONE),
    ]
    lis = "".join(f'<li>{icon(i)} {t}</li>' for i, t in items)
    return f'<ul class="trust-row">{lis}</ul>'


def facts_block(pairs):
    cells = "".join(f'<div><dt>{d}</dt><dd>{t}</dd></div>' for d, t in pairs)
    return f'<dl class="facts reveal">{cells}</dl>'


def check_list(items):
    lis = "".join(f'<li>{icon("check-circle")}<span>{i}</span></li>' for i in items)
    return f'<ul class="check-list">{lis}</ul>'


def credit_section(anchor="credit-impot", note=True):
    return f'''<section id="{anchor}" class="section bg-surface">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">Avantage fiscal</p>
      <h2 class="h2" style="margin-top:14px">Vous ne payez réellement que la moitié</h2>
      <p class="lead" style="margin-top:20px">
        L'entretien courant du jardin relève des services à la personne : il ouvre droit
        à un crédit d'impôt de 50 % pour les particuliers. Une prestation facturée
        100 € ne vous coûte réellement que 50 €.
      </p>
      <div style="margin-top:30px">
        {check_list([
          "Attestation fiscale fournie chaque année",
          "Valable même si vous n'êtes pas imposable",
          "Plafond de 5 000 € de travaux par an et par foyer",
        ])}
      </div>
      {'<p class="small muted" style="margin-top:26px">Le crédit d’impôt s’applique aux petits travaux d’entretien courant (tonte, taille, débroussaillage, désherbage), selon les conditions d’éligibilité en vigueur. Les travaux de création et d’aménagement n’y ouvrent pas droit.</p>' if note else ''}
    </div>
    <div class="calc-card reveal" style="--d:1">
      <p class="eyebrow">Exemple concret</p>
      <div style="margin-top:18px">
        <div class="calc-row"><span>Entretien facturé</span><strong>100 €</strong></div>
        <div class="calc-row"><span>Crédit d'impôt (50 %)</span><strong style="color:var(--green-700)">− 50 €</strong></div>
        <div class="calc-total"><span>Coût réel pour vous</span><strong>50 €</strong></div>
      </div>
      <a class="btn btn-primary btn-block" style="margin-top:26px" href="#devis">Estimer mon coût réel</a>
    </div>
  </div>
</section>'''


def faq_section(items, title="Questions fréquentes"):
    body = "".join(
        f'<details><summary>{html.escape(q)}</summary><p>{a}</p></details>'
        for q, a in items
    )
    return f'''<section class="section" id="faq">
  <div class="container container-narrow">
    <div class="section-head reveal">
      <p class="eyebrow">Bon à savoir</p>
      <h2 class="h2">{title}</h2>
    </div>
    <div class="faq reveal">{body}</div>
  </div>
</section>'''


def zone_section():
    villes = " · ".join(VILLES)
    return f'''<section class="section-sm bg-soft" id="zone">
  <div class="container reveal">
    <p class="eyebrow">Zone d'intervention</p>
    <h2 class="h3" style="margin-top:12px">Nous intervenons partout en Gironde</h2>
    <p class="muted" style="margin-top:14px; max-width:70ch">{villes}, et l'ensemble des communes du département.</p>
  </div>
</section>'''


def devis_section(origine, titre="Demandez votre devis gratuit",
                  texte="Décrivez votre projet : nous vous répondons sous 24 h avec une estimation claire et sans engagement.",
                  service_default="Entretien de jardins"):
    return f'''<section id="devis" class="section bg-green">
  <div class="container split split-form">
    <div class="reveal">
      <p class="eyebrow">Contact</p>
      <h2 class="h2" style="margin-top:14px">{titre}</h2>
      <p style="margin-top:20px; font-size:19px; color:rgba(255,255,255,.85); max-width:32em">{texte}</p>
      <ul class="contact-list">
        <li>{icon('phone')}<a href="{PHONE_HREF}" data-loc="section-devis">{PHONE_DISPLAY}</a></li>
        <li>{icon('mail')}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{icon('pin')}<span>{ZONE}</span></li>
        <li>{icon('clock')}<span>{HOURS}</span></li>
      </ul>
    </div>
    <div class="reveal" style="--d:1">{form_card(origine, service_default=service_default)}</div>
  </div>
</section>'''


# =====================================================================
#  Données : services
# =====================================================================
SERVICES = [
    {
        "slug": "entretien-jardins",
        "titre": "Entretien de jardins",
        "court": "Un suivi régulier pour un jardin toujours impeccable, saison après saison.",
        "img": "debroussaillage",
        "img_w": [1200, 800, 500],
        "alt": "L'équipe de Jardin de Gironde en intervention d'entretien",
        "meta": "Entretien de jardins en Gironde : suivi régulier, taille, désherbage et soin de votre jardin à Bordeaux et partout en Gironde. Devis sous 24 h.",
        "long": "L'entretien d'un jardin demande du temps, du savoir-faire et une présence "
                "régulière. Jardin de Gironde prend en charge l'ensemble des travaux "
                "nécessaires au bon état de votre jardin : désherbage, taille, tonte, "
                "ramassage de feuilles, arrosage et entretien des massifs. Nous intervenons "
                "à la fréquence que vous choisissez, tout au long de l'année.",
        "benefices": [
            "Désherbage, tonte et taille inclus selon la saison",
            "Entretien des massifs et plantations existantes",
            "Ramassage des feuilles et nettoyage automnal",
            "Contrat d'entretien mensuel ou saisonnier disponible",
            "Rapport d'intervention et conseils personnalisés",
        ],
        "credit": True,
    },
    {
        "slug": "tonte-pelouse",
        "titre": "Tonte de pelouse",
        "court": "Une pelouse dense, nette et parfaitement rasée à la fréquence idéale.",
        "img": "tonte-pelouse",
        "img_w": [1086, 800, 500],
        "alt": "Pelouse fraîchement tondue au bord d'une terrasse en bois",
        "meta": "Tonte de pelouse en Gironde : pelouse nette et dense, tonte régulière, résultat impeccable à Bordeaux et partout en Gironde.",
        "long": "Notre équipe intervient sur tous types de terrains en Gironde pour assurer "
                "une tonte régulière et soignée de votre pelouse. Nous adaptons la hauteur "
                "de coupe et la fréquence de passage selon la saison, la nature de votre "
                "gazon et vos préférences. Le résultat : un gazon uniforme, sain et "
                "visuellement impeccable toute l'année.",
        "benefices": [
            "Tonte à la bonne hauteur selon la saison et la variété de gazon",
            "Ramassage des tontes inclus sur demande",
            "Matériel professionnel silencieux et précis",
            "Intervention ponctuelle ou contrat d'entretien régulier",
        ],
        "credit": True,
    },
    {
        "slug": "taille-haies",
        "titre": "Taille de haies et arbustes",
        "court": "Des haies structurées et des arbustes en pleine santé, taillés avec précision.",
        "img": "taille-haies",
        "img_w": [941, 800, 500],
        "alt": "Taille d'une haie au taille-haie thermique en Gironde",
        "meta": "Taille de haies et arbustes en Gironde : haies structurées, arbustes sains et bien formés à Bordeaux et en Gironde. Devis gratuit.",
        "long": "La taille de haies et d'arbustes demande rigueur et connaissance des espèces "
                "végétales. Notre équipe intervient au bon moment de l'année pour favoriser "
                "une repousse saine et donner à vos haies et arbustes un aspect soigné et "
                "structuré. Nous travaillons aussi bien sur les petits jardins que sur les "
                "grandes propriétés en Gironde.",
        "benefices": [
            "Taille adaptée à chaque espèce végétale",
            "Respect des périodes de taille pour protéger la flore",
            "Lignes nettes et formes régulières garanties",
            "Évacuation des déchets verts incluse",
            "Intervention ponctuelle ou planifiée",
        ],
        "credit": True,
    },
    {
        "slug": "debroussaillage",
        "titre": "Débroussaillage",
        "court": "Nettoyage des terrains envahis, mise aux normes et sécurité incendie.",
        "img": "debroussaillage",
        "img_w": [1200, 800, 500],
        "alt": "Équipe de débroussaillage de Jardin de Gironde sur un terrain",
        "meta": "Débroussaillage professionnel en Gironde : nettoyage de terrains envahis, mise aux normes et sécurité incendie à Bordeaux et en Gironde.",
        "long": "En Gironde, le débroussaillage est souvent une obligation légale, notamment "
                "pour les propriétés situées en zone à risque incendie. Notre équipe prend "
                "en charge le nettoyage complet de vos terrains : élimination des ronces, "
                "broussailles, herbes hautes et végétation envahissante. Nous vous aidons "
                "à remettre votre espace en ordre, en toute sécurité.",
        "benefices": [
            "Débroussaillage manuel et mécanique selon le terrain",
            "Mise aux normes réglementaires (obligations légales de débroussaillement)",
            "Nettoyage de terrains en friche, talus et lisières",
            "Évacuation ou broyage des végétaux sur place",
            "Intervention rapide sur devis",
        ],
        "credit": True,
    },
    {
        "slug": "creation-espaces-verts",
        "titre": "Création d'espaces verts",
        "court": "Conception sur mesure de jardins qui vous ressemblent, de A à Z.",
        "img": "creation-jardin",
        "img_w": [1448, 1000, 640],
        "alt": "Jardin créé par Jardin de Gironde : gazon neuf, clôture et massifs",
        "meta": "Création d'espaces verts sur mesure en Gironde : conception et aménagement de jardins à Bordeaux et partout en Gironde.",
        "long": "Nous concevons et aménageons vos espaces verts selon vos goûts, votre terrain "
                "et votre budget. De la création d'une pelouse à l'aménagement complet d'un "
                "jardin paysager, notre équipe vous accompagne à chaque étape : conseil, plan, "
                "plantation, mise en place de massifs, allées et structures végétales. Chaque "
                "réalisation est unique et pensée pour durer.",
        "benefices": [
            "Étude personnalisée de votre projet et de votre terrain",
            "Sélection d'espèces adaptées au climat girondin",
            "Plantation, engazonnement et création de massifs",
            "Aménagement d'allées, bordures et structures paysagères",
            "Suivi post-création disponible",
        ],
        "credit": False,
        "partenariat": True,
    },
    {
        "slug": "nettoyage-toiture-gouttiere",
        "titre": "Nettoyage de toitures et gouttières",
        "court": "Toitures démoussées et gouttières dégagées, avant que l'eau ne fasse des dégâts.",
        "img": None,
        "img_w": None,
        "alt": "",
        "meta": "Nettoyage de toiture et de gouttières en Gironde : démoussage, "
                "curage des chéneaux et descentes, à Bordeaux et partout en Gironde.",
        "long": "Une gouttière bouchée déborde, et c'est la façade, les fondations ou la "
                "charpente qui prennent l'eau. Nous curons les chéneaux et les descentes, "
                "retirons feuilles, mousses et dépôts, et vérifions l'écoulement avant de "
                "partir. Sur la toiture, nous procédons au démoussage et au nettoyage des "
                "tuiles. Deux passages par an, à l'automne et au printemps, suffisent "
                "généralement à éviter les mauvaises surprises.",
        "benefices": [
            "Curage complet des gouttières, chéneaux et descentes",
            "Démoussage de toiture et nettoyage des tuiles",
            "Contrôle de l'écoulement après intervention",
            "Évacuation des déchets retirés",
            "Intervention sécurisée, matériel adapté à la hauteur",
        ],
        "credit": False,
    },
    {
        "slug": "nettoyage-haute-pression",
        "titre": "Nettoyage haute pression",
        "court": "Terrasses, allées et murets retrouvent leur éclat d'origine.",
        "img": "nettoyage-haute-pression",
        "img_w": [1600, 1000, 640],
        "alt": "Avant / après : bassin nettoyé au karcher par Jardin de Gironde",
        "meta": "Nettoyage haute pression en Gironde : terrasses, allées, murets et façades nettoyés en profondeur à Bordeaux et en Gironde.",
        "long": "Le nettoyage haute pression est la solution la plus efficace pour redonner "
                "leur aspect d'origine à vos surfaces extérieures. Mousses, algues, taches "
                "et salissures incrustées disparaissent en quelques passages. Nous "
                "intervenons sur terrasses en bois ou béton, allées pavées, murets, "
                "clôtures et façades. Résultat immédiat et durable.",
        "benefices": [
            "Élimination des mousses, algues et taches tenaces",
            "Traitement des terrasses bois, béton et pierre",
            "Nettoyage des allées, murets et clôtures",
            "Matériel professionnel haute performance",
        ],
        "credit": False,
    },
]


def services_grid():
    cards = []
    for i, s in enumerate(SERVICES):
        cards.append(f'''<a class="service-card reveal" style="--d:{i % 3}" href="{s['slug']}.html">
      <div class="service-media illus"><img src="assets/img/illus/{s['slug']}.svg" alt=""
           width="120" height="120" loading="lazy" decoding="async"></div>
      <div class="service-body">
        <h3>{s['titre']}</h3>
        <p>{s['court']}</p>
        <span class="link-arrow">En savoir plus {icon('arrow', size=15)}</span>
      </div>
    </a>''')
    return '<div class="service-grid">' + "".join(cards) + '</div>'


def partenariat_section(video_first=False):
    return f'''<section class="section bg-surface" id="partenariat">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">Partenariat commercial</p>
      <h2 class="h2" style="margin-top:14px">Un partenariat de confiance avec Villaverde Cestas</h2>
      <p class="lead" style="margin-top:20px">
        Grâce à ce partenariat, les clients qui passent par Jardin de Gironde
        bénéficient de prix préférentiels sur les plantes du magasin.
      </p>
      <a class="btn btn-ghost" style="margin-top:28px" href="#devis">Demander un devis {icon('arrow', 'ico', 16)}</a>
    </div>
    <div class="video-frame reveal" style="--d:1">
      <span class="video-tag">Villaverde Cestas</span>
      <video data-lazy data-src="assets/video/villaverde-cestas.mp4"
             poster="assets/img/villaverde-poster.webp"
             muted loop playsinline preload="none"
             title="Partenariat entre Jardin de Gironde et Villaverde Cestas"></video>
    </div>
  </div>
</section>'''


def realisations_section():
    works = [
        ("taille-haies", [941, 800, 500], "Taille de haies", "Précision & finition",
         "Taille de haie réalisée par Jardin de Gironde", False),
        ("creation-jardin", [1448, 1000, 640], "Création d'un jardin", "Sur mesure, de A à Z",
         "Création d'un jardin avec gazon neuf et clôture bois", True),
        ("nettoyage-haute-pression", [1600, 1000, 640], "Nettoyage haute pression", "Avant / après",
         "Avant après d'un nettoyage haute pression", True),
    ]
    figs = []
    for i, (name, widths, titre, sur, alt, wide) in enumerate(works):
        cls = "work work-wide reveal" if wide else "work reveal"
        figs.append(f'''<figure class="{cls}" style="--d:{i}">
      {picture(name, widths, alt, sizes="(min-width: 900px) 33vw, (min-width: 600px) 50vw, 100vw")}
      <figcaption><span>{sur}</span><b>{titre}</b></figcaption>
    </figure>''')
    return f'''<section class="section" id="realisations">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Réalisations</p>
      <h2 class="h2">Le travail parle de lui-même</h2>
      <p class="lead">Des chantiers réels, photographiés sur le terrain, en Gironde.
         Pas d'images de synthèse : ce que vous voyez est ce que nous faisons.</p>
    </div>
    <div class="works">{"".join(figs)}</div>
  </div>
</section>'''


def steps_section(title, eyebrow, steps):
    body = "".join(
        f'''<div class="step reveal" style="--d:{i}">
      <b>Étape {i + 1}</b><h3>{t}</h3><p>{d}</p>
    </div>''' for i, (t, d) in enumerate(steps)
    )
    return f'''<section class="section bg-surface" id="deroulement">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">{eyebrow}</p>
      <h2 class="h2">{title}</h2>
    </div>
    <div class="steps">{body}</div>
  </div>
</section>'''


def write(filename, content):
    path = os.path.join(HERE, filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("  ✓ %-34s %6d octets" % (filename, len(content.encode("utf-8"))))


# =====================================================================
#  FAQ
# =====================================================================
FAQ_ENTRETIEN = [
    ("Comment fonctionne le crédit d'impôt de 50 % ?",
     "Nos prestations d'entretien courant du jardin relèvent des services à la personne. "
     "Vous réglez la facture normalement, nous vous remettons une attestation fiscale en "
     "début d'année suivante, et 50 % du montant vous est restitué par l'administration — "
     "que vous soyez imposable ou non. Le plafond est de 5 000 € de travaux par an et par foyer."),
    ("Suis-je obligé de signer un contrat à l'année ?",
     "Non. Vous pouvez faire appel à nous pour une intervention ponctuelle. Le contrat "
     "d'entretien régulier existe pour ceux qui préfèrent ne plus y penser, mais il n'a "
     "jamais rien d'obligatoire."),
    ("Dois-je être présent pendant l'intervention ?",
     "Ce n'est pas nécessaire dès lors que nous avons accès au terrain. Beaucoup de nos "
     "clients nous confient l'entretien pendant leurs absences ; nous vous envoyons un "
     "compte-rendu après le passage."),
    ("Que faites-vous des déchets verts ?",
     "L'évacuation est comprise dans nos prestations de taille et de débroussaillage. "
     "Les végétaux sont apportés en déchèterie ou broyés sur place selon le volume et "
     "votre préférence."),
    ("Sous quel délai intervenez-vous ?",
     "Vous recevez votre devis sous 24 h ouvrées. La première intervention a généralement "
     "lieu dans la semaine, selon la saison et la charge de travail en cours."),
]

FAQ_CREATION = [
    ("Combien coûte la création d'un jardin ?",
     "Tout dépend de la surface, de l'état du terrain et des aménagements souhaités. "
     "C'est pour cela que nous nous déplaçons avant de chiffrer : le devis est gratuit, "
     "détaillé poste par poste, et vous n'avez aucun engagement."),
    ("Le crédit d'impôt de 50 % s'applique-t-il aux travaux de création ?",
     "Non, et nous préférons le dire clairement. Le crédit d'impôt services à la personne "
     "concerne l'entretien courant du jardin (tonte, taille, débroussaillage, désherbage). "
     "Les travaux de création et d'aménagement paysager n'y ouvrent pas droit — en revanche, "
     "l'entretien qui suivra, oui."),
    ("Fournissez-vous les végétaux ?",
     "Oui. Grâce à notre partenariat avec Villaverde Cestas, nos clients bénéficient de "
     "prix préférentiels sur les plantes du magasin. Nous sélectionnons des espèces "
     "adaptées au climat girondin, pour qu'elles tiennent dans le temps."),
    ("Quel délai entre le devis et le chantier ?",
     "Le devis vous parvient sous 24 h ouvrées après notre visite. Le démarrage du chantier "
     "dépend de son ampleur et de la saison de plantation ; nous vous donnons une date "
     "ferme au moment de la signature."),
    ("Reprenez-vous un jardin existant à remettre en état ?",
     "C'est une grande partie de notre travail : terrains laissés à l'abandon, pelouses à "
     "refaire, massifs à restructurer. Nous partons de l'existant plutôt que de tout raser."),
]

FAQ_HOME = FAQ_ENTRETIEN[:3] + FAQ_CREATION[1:3]


# =====================================================================
#  Page d'accueil
# =====================================================================
def page_index():
    hero_img = picture("creation-jardin", [1448, 1000, 640],
                       "Jardin créé par Jardin de Gironde : pelouse neuve, clôture bois et massifs",
                       sizes="(min-width: 900px) 46vw, 92vw", eager=True)
    return (
        head(
            "Jardin de Gironde — Entretien et création de jardins en Gironde",
            "Entretien de jardin, tonte, taille de haies, débroussaillage et création "
            "d'espaces verts partout en Gironde. Devis gratuit sous 24 h, crédit d'impôt "
            "de 50 % sur l'entretien.",
            BASE_URL + "/",
            preload_img=("creation-jardin", [1448, 1000, 640], "(min-width: 900px) 46vw, 92vw"),
        )
        + local_business_jsonld() + faq_jsonld(FAQ_HOME) + '''
</head>
<body>
''' + header(home=True) + '''
<main id="contenu">

  <section class="hero" id="top">
    <div class="container hero-grid">
      <div class="reveal in">
        <p class="eyebrow">Entretien &amp; création de jardins en Gironde</p>
        <h1 class="h1">Des espaces verts qui respirent le soin.</h1>
        <p class="lead">Une équipe locale, un travail régulier et des devis clairs.
           Vous nous confiez votre jardin : vous n'avez plus à y penser.</p>
        <div class="hero-actions">
          <a class="btn btn-primary btn-lg" href="#devis">Demander un devis gratuit ''' + icon('arrow', 'ico', 16) + '''</a>
          <a class="btn btn-ghost btn-lg" href="''' + PHONE_HREF + '''" data-loc="hero">''' + icon('phone', 'ico', 16) + ''' ''' + PHONE_DISPLAY + '''</a>
        </div>
        ''' + trust_row() + '''
      </div>
      <div class="hero-media reveal in" style="--d:1">''' + hero_img + '''</div>
    </div>
  </section>

  <section class="section-sm">
    <div class="container">
      ''' + facts_block([
          ("Réponse à votre demande", "Sous 24 h"),
          ("Crédit d'impôt sur l'entretien", "50 %"),
          ("Zone d'intervention", "Toute la Gironde"),
          ("Devis", "Gratuit, sans engagement"),
      ]) + '''
    </div>
  </section>

  <section class="section bg-soft" id="services">
    <div class="container">
      <div class="section-head reveal">
        <p class="eyebrow">Nos prestations</p>
        <h2 class="h2">Tout ce dont votre jardin a besoin</h2>
        <p class="lead">De la tonte hebdomadaire à la création complète d'un espace vert,
           avec le même soin du détail.</p>
      </div>
      ''' + services_grid() + '''
    </div>
  </section>

''' + credit_section() + realisations_section() + partenariat_section()
        + zone_section() + faq_section(FAQ_HOME) + devis_section("Accueil") + '''
</main>
''' + footer(home=True) + action_bar() + scripts() + '''
</body>
</html>
''')


# =====================================================================
#  Pages de campagne Google Ads
# =====================================================================
def landing(slug, title, description, origine, eyebrow, h1, lead, usps, checklist,
            checklist_title, steps, faq, service_default, photo, photo_w, photo_alt,
            with_credit, with_partenariat, form_titre):
    usp_html = "".join(f'''<div class="usp reveal" style="--d:{i}">
        <span class="illus-badge"><img src="assets/img/illus/{ic}.svg" alt="" width="120" height="120" loading="lazy"></span>
        <div><h3>{t}</h3><p>{d}</p></div>
      </div>''' for i, (ic, t, d) in enumerate(usps))

    return (
        head(title, description, f"{BASE_URL}/{slug}.html",
             preload_img=(photo, photo_w, "(min-width: 900px) 46vw, 92vw"))
        + local_business_jsonld() + faq_jsonld(faq) + '''
</head>
<body>
''' + header(minimal=True, home=True) + '''
<main id="contenu">

  <section class="hero" id="top">
    <div class="container hero-grid split-form">
      <div class="reveal in">
        <p class="eyebrow">''' + eyebrow + '''</p>
        <h1 class="h1">''' + h1 + '''</h1>
        <p class="lead">''' + lead + '''</p>
        <div class="hero-actions">
          <a class="btn btn-primary btn-lg" href="#devis">Obtenir mon devis gratuit ''' + icon('arrow', 'ico', 16) + '''</a>
          <a class="btn btn-ghost btn-lg" href="''' + PHONE_HREF + '''" data-loc="hero-lp">''' + icon('phone', 'ico', 16) + ''' ''' + PHONE_DISPLAY + '''</a>
        </div>
        ''' + trust_row() + '''
      </div>
      <div class="reveal in" style="--d:1">''' + form_card(origine, titre=form_titre, service_default=service_default) + '''</div>
    </div>
  </section>

  <section class="section bg-soft">
    <div class="container">
      <div class="section-head reveal">
        <p class="eyebrow">Pourquoi nous</p>
        <h2 class="h2">Ce que vous obtenez</h2>
      </div>
      <div class="usp-grid">''' + usp_html + '''</div>
    </div>
  </section>

  <section class="section">
    <div class="container split">
      <div class="reveal">
        <p class="eyebrow">Prestations incluses</p>
        <h2 class="h2" style="margin-top:14px">''' + checklist_title + '''</h2>
        <div style="margin-top:28px">''' + check_list(checklist) + '''</div>
        <a class="btn btn-primary" style="margin-top:30px" href="#devis">Demander mon devis ''' + icon('arrow', 'ico', 16) + '''</a>
      </div>
      <div class="hero-media reveal" style="--d:1">'''
        + picture(photo, photo_w, photo_alt, sizes="(min-width: 900px) 46vw, 92vw") + '''</div>
    </div>
  </section>

''' + steps + (credit_section("credit-impot") if with_credit else "")
        + (partenariat_section() if with_partenariat else "")
        + realisations_section() + zone_section() + faq_section(faq)
        + devis_section(origine, service_default=service_default) + '''
</main>
''' + footer() + action_bar() + scripts() + '''
</body>
</html>
''')


def page_lp_entretien():
    return landing(
        slug="entretien-jardin",
        title="Entretien de jardin en Gironde — Devis gratuit sous 24 h | Jardin de Gironde",
        description="Jardinier en Gironde : tonte, taille de haies, débroussaillage et "
                    "désherbage. Devis gratuit sous 24 h et crédit d'impôt de 50 %. "
                    "Bordeaux et toute la Gironde.",
        origine="Campagne Ads — Entretien / jardinage",
        eyebrow="Jardinier en Gironde",
        h1="Un jardin entretenu toute l'année, sans y penser.",
        lead="Tonte, taille de haies, débroussaillage, désherbage. Une équipe locale qui "
             "passe à la fréquence que vous choisissez — et 50 % du montant vous revient "
             "en crédit d'impôt.",
        usps=[
            ("tonte-pelouse", "Un passage régulier, à votre rythme",
             "Hebdomadaire, mensuel ou ponctuel : c'est vous qui décidez. Nous adaptons la "
             "fréquence à la saison et à votre terrain."),
            ("entretien-jardins", "Une seule entreprise pour tout le jardin",
             "Tonte, taille, désherbage, ramassage des feuilles, entretien des massifs : "
             "vous n'avez qu'un interlocuteur."),
            ("taille-haies", "Du matériel professionnel, un travail net",
             "Des lignes droites, des finitions propres, et l'évacuation des déchets verts "
             "comprise dans la prestation."),
            ("debroussaillage", "Crédit d'impôt de 50 %",
             "Attestation fiscale fournie chaque année. Une prestation de 100 € vous "
             "revient réellement à 50 €, imposable ou non."),
        ],
        checklist_title="Ce que comprend l'entretien de votre jardin",
        checklist=[
            "Tonte de pelouse à la bonne hauteur selon la saison",
            "Taille des haies, arbustes et massifs au bon moment de l'année",
            "Débroussaillage des terrains envahis et mise aux normes",
            "Désherbage des allées, bordures et massifs",
            "Ramassage des feuilles et nettoyage automnal",
            "Nettoyage des toitures et curage des gouttières",
            "Évacuation des déchets verts incluse",
            "Compte-rendu après chaque intervention",
        ],
        steps=steps_section(
            "Comment ça se passe", "Déroulement",
            [("Vous décrivez votre jardin",
              "Par téléphone ou via le formulaire. Surface approximative, fréquence "
              "souhaitée, contraintes d'accès."),
             ("Nous chiffrons sous 24 h",
              "Un devis clair, détaillé, sans engagement — avec le montant après crédit "
              "d'impôt indiqué noir sur blanc."),
             ("Nous intervenons",
              "Vous n'avez pas besoin d'être présent. Nous arrivons avec notre matériel et "
              "repartons avec les déchets verts."),
             ("Vous recevez votre attestation",
              "Chaque début d'année, l'attestation fiscale à joindre à votre déclaration "
              "pour récupérer 50 %.")]),
        faq=FAQ_ENTRETIEN,
        service_default="Entretien de jardins",
        photo="taille-haies", photo_w=[941, 800, 500],
        photo_alt="Jardinier de Jardin de Gironde taillant une haie en Gironde",
        with_credit=True, with_partenariat=False,
        form_titre="Recevoir mon devis d'entretien",
    )


def page_lp_creation():
    return landing(
        slug="creation-paysagisme",
        title="Paysagiste en Gironde — Création et aménagement de jardin | Jardin de Gironde",
        description="Paysagiste en Gironde : conception et création de jardins sur mesure, "
                    "engazonnement, massifs, allées et clôtures. Devis gratuit et détaillé "
                    "sous 24 h à Bordeaux et en Gironde.",
        origine="Campagne Ads — Paysagisme / création",
        eyebrow="Paysagiste en Gironde",
        h1="Votre jardin, conçu et réalisé sur mesure.",
        lead="Conception, engazonnement, massifs, allées, clôtures. Nous partons de votre "
             "terrain et de vos envies, puis nous réalisons — avec des végétaux choisis "
             "pour tenir dans le climat girondin.",
        usps=[
            ("creation-espaces-verts", "Un projet pensé pour votre terrain",
             "Exposition, nature du sol, usage réel de l'espace : le plan part de ce que "
             "vous avez, pas d'un catalogue."),
            ("entretien-jardins", "Des végétaux adaptés au climat girondin",
             "Sélectionnés avec notre partenaire Villaverde Cestas, à prix préférentiel "
             "pour nos clients."),
            ("nettoyage-haute-pression", "De la remise en état à la finition",
             "Débroussaillage, terrassement léger, engazonnement, massifs, allées, "
             "bordures et nettoyage de fin de chantier."),
            ("taille-haies", "Un devis détaillé, poste par poste",
             "Vous savez exactement ce que vous payez, et ce qui peut attendre une "
             "seconde phase si le budget l'impose."),
        ],
        checklist_title="Nos prestations de création et d'aménagement",
        checklist=[
            "Étude du terrain et proposition d'aménagement",
            "Préparation du sol, terrassement léger et remise à niveau",
            "Engazonnement : semis ou gazon en plaques",
            "Création de massifs, plantation d'arbustes et de vivaces",
            "Allées, bordures, pas japonais et structures paysagères",
            "Pose de clôtures, palissades et brise-vues",
            "Nettoyage complet en fin de chantier",
        ],
        steps=steps_section(
            "Du premier échange au jardin fini", "Déroulement",
            [("Visite et écoute",
              "Nous venons voir le terrain, comprendre l'usage que vous en faites et "
              "ce que vous voulez y changer."),
             ("Plan et devis détaillé",
              "Une proposition d'aménagement et un devis poste par poste, sous 24 h "
              "après la visite."),
             ("Réalisation",
              "Préparation du sol, plantations, engazonnement, structures. Un chantier "
              "tenu propre du début à la fin."),
             ("Suivi et entretien",
              "Nous restons disponibles pour la reprise des végétaux, et pour l'entretien "
              "régulier si vous le souhaitez.")]),
        faq=FAQ_CREATION,
        service_default="Création d'espaces verts",
        photo="creation-jardin", photo_w=[1448, 1000, 640],
        photo_alt="Création d'un jardin en Gironde : gazon neuf, clôture bois et massifs",
        with_credit=False, with_partenariat=True,
        form_titre="Recevoir mon devis de création",
    )


# =====================================================================
#  Pages de service
# =====================================================================
def page_service(s):
    autres = [x for x in SERVICES if x["slug"] != s["slug"]][:3]
    cards = "".join(f'''<a class="service-card reveal" style="--d:{i}" href="{o['slug']}.html">
      <div class="service-media illus"><img src="assets/img/illus/{o['slug']}.svg" alt="" width="120" height="120" loading="lazy"></div>
      <div class="service-body"><h3>{o['titre']}</h3><p>{o['court']}</p>
        <span class="link-arrow">En savoir plus {icon('arrow', size=15)}</span></div>
    </a>''' for i, o in enumerate(autres))

    return (
        head(f"{s['titre']} en Gironde — {SITE}", s["meta"],
             f"{BASE_URL}/{s['slug']}.html",
             preload_img=((s["img"], s["img_w"], "(min-width: 900px) 70vw, 92vw")
                          if s["img"] else None))
        + local_business_jsonld() + '''
</head>
<body>
''' + header() + '''
<main id="contenu">

  <section class="page-hero">
    <div class="container">
      <p class="breadcrumb"><a href="index.html">Accueil</a> &nbsp;/&nbsp; ''' + s["titre"] + '''</p>
      <div style="display:flex; gap:22px; align-items:center; margin-top:22px; flex-wrap:wrap">
        <span class="illus-badge"><img src="assets/img/illus/''' + s["slug"] + '''.svg" alt="" width="120" height="120"></span>
        <h1 class="h1" style="margin:0; flex:1; min-width:260px">''' + s["titre"] + ''' en Gironde</h1>
      </div>
      <p class="lead" style="max-width:52ch">''' + s["court"] + '''</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#devis">Demander un devis gratuit ''' + icon('arrow', 'ico', 16) + '''</a>
        <a class="btn btn-ghost" href="''' + PHONE_HREF + '''" data-loc="page-service">''' + icon('phone', 'ico', 16) + ''' ''' + PHONE_DISPLAY + '''</a>
      </div>
      <div class="page-media reveal in">'''
        + (picture(s["img"], s["img_w"], s["alt"], sizes="(min-width: 900px) 70vw, 92vw", eager=True)
           if s["img"] else
           f'''<div class="page-illus"><img src="assets/img/illus/{s["slug"]}.svg" alt=""
                width="200" height="200" loading="eager"></div>''') + '''</div>
    </div>
  </section>

  <section class="section-sm">
    <div class="container split">
      <div class="prose reveal">
        <h2 class="h2">''' + s["titre"] + '''</h2>
        <p style="margin-top:20px">''' + s["long"] + '''</p>
      </div>
      <div class="reveal" style="--d:1">
        <p class="eyebrow">Ce qui est compris</p>
        <div style="margin-top:22px">''' + check_list(s["benefices"]) + '''</div>
      </div>
    </div>
  </section>

''' + (credit_section("credit-impot") if s["credit"] else "")
        + (partenariat_section() if s.get("partenariat") else "") + '''

  <section class="section bg-soft">
    <div class="container">
      <div class="section-head reveal">
        <p class="eyebrow">Aussi</p>
        <h2 class="h2">Nos autres prestations</h2>
      </div>
      <div class="service-grid">''' + cards + '''</div>
    </div>
  </section>

''' + zone_section() + devis_section(s["titre"], service_default=s["titre"]) + '''
</main>
''' + footer() + action_bar() + scripts() + '''
</body>
</html>
''')


# =====================================================================
#  Page de remerciement (conversion Google Ads)
# =====================================================================
def page_merci():
    return (
        head("Merci pour votre demande — " + SITE,
             "Votre demande de devis a bien été reçue. Nous vous recontactons sous 24 h ouvrées.",
             BASE_URL + "/merci.html", noindex=True)
        + '''
</head>
<body data-page="merci">
''' + header(minimal=True) + '''
<main id="contenu">
  <div class="container thanks">
    <div>
      <svg class="thanks-mark" viewBox="0 0 48 48" fill="none" stroke="currentColor"
           stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="24" cy="24" r="20"/><path d="M15 24.5l6.5 6.5L33 18"/>
      </svg>
      <h1 class="h2">Merci, votre demande est bien arrivée.</h1>
      <p class="lead">Nous revenons vers vous <strong>sous 24 h ouvrées</strong> avec un
         devis gratuit et détaillé. Si votre demande est urgente, appelez-nous directement.</p>
      <div class="contact-card">
        <a href="''' + PHONE_HREF + '''" data-loc="merci">''' + PHONE_DISPLAY + '''</a>
        <a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a>
        <p class="small muted">''' + ZONE + ''' — ''' + HOURS + '''</p>
      </div>
      <a class="btn btn-ghost" style="margin-top:30px" href="index.html">Retour à l'accueil</a>
    </div>
  </div>
</main>
''' + footer() + scripts() + '''
</body>
</html>
''')


# =====================================================================
#  Pages légales
# =====================================================================
def legal_page(slug, title, description, body):
    return (
        head(f"{title} — {SITE}", description, f"{BASE_URL}/{slug}.html")
        + '''
</head>
<body>
''' + header() + '''
<main id="contenu">
  <section class="section">
    <div class="container container-narrow prose">
      <h1 class="h2">''' + title + '''</h1>
      ''' + body + '''
    </div>
  </section>
</main>
''' + footer() + scripts() + '''
</body>
</html>
''')


MENTIONS = f'''
<p style="margin-top:26px"><strong>Éditeur du site</strong><br>
{SITE} — entreprise d'entretien et de création d'espaces verts intervenant en Gironde.<br>
Téléphone : <a href="{PHONE_HREF}">{PHONE_DISPLAY}</a><br>
Courriel : <a href="mailto:{EMAIL}">{EMAIL}</a><br>
Zone d'intervention : {ZONE}.</p>

<p><strong>Informations légales</strong><br>
Forme juridique, numéro SIRET, adresse du siège social et numéro de TVA
intracommunautaire : à compléter avant la mise en ligne.
Déclaration d'activité de services à la personne : numéro à compléter.</p>

<p><strong>Directeur de la publication</strong><br>
Le représentant légal de {SITE}.</p>

<p><strong>Hébergement</strong><br>
Le site est hébergé par Hostinger International Ltd., 61 Lordou Vironos Street,
6023 Larnaca, Chypre.</p>

<p><strong>Propriété intellectuelle</strong><br>
L'ensemble des textes, photographies et illustrations présents sur ce site est la
propriété de {SITE}. Toute reproduction, même partielle, est interdite sans
autorisation écrite préalable.</p>

<p><strong>Photographies</strong><br>
Les photographies publiées sur ce site sont des prises de vue réelles de chantiers
réalisés par {SITE}. Aucune image de synthèse n'est utilisée pour illustrer nos
réalisations.</p>

<p><strong>Médiation de la consommation</strong><br>
Conformément à l'article L.612-1 du Code de la consommation, le consommateur peut
recourir gratuitement à un médiateur de la consommation en cas de litige.
Coordonnées du médiateur : à compléter.</p>
'''

CONFIDENTIALITE = f'''
<p style="margin-top:26px">La présente politique explique quelles données personnelles
sont collectées sur ce site, pourquoi, et quels sont vos droits.</p>

<p><strong>Responsable du traitement</strong><br>
{SITE} — <a href="mailto:{EMAIL}">{EMAIL}</a> — <a href="{PHONE_HREF}">{PHONE_DISPLAY}</a>.</p>

<p><strong>Données collectées</strong><br>
Via le formulaire de demande de devis : nom et prénom, numéro de téléphone, adresse
e-mail, ville, prestation souhaitée et description de votre projet. Sont également
enregistrés, le cas échéant, les paramètres de la campagne publicitaire par laquelle
vous êtes arrivé sur le site (identifiant de clic Google Ads, source, campagne).</p>

<p><strong>Finalités et base légale</strong><br>
Ces données servent uniquement à vous recontacter, à établir votre devis et à assurer
le suivi de votre demande. La base légale est votre consentement, matérialisé par
l'envoi du formulaire, ainsi que l'exécution de mesures précontractuelles.</p>

<p><strong>Durée de conservation</strong><br>
Les demandes de devis sont conservées trois ans à compter du dernier contact, puis
supprimées. Les documents comptables liés à une prestation réalisée sont conservés
dix ans, conformément aux obligations légales.</p>

<p><strong>Destinataires</strong><br>
Vos données sont traitées par {SITE} et par son hébergeur Hostinger, qui assure le
stockage technique. Elles ne sont ni vendues, ni louées, ni transmises à des tiers à
des fins commerciales.</p>

<p><strong>Mesure d'audience et publicité</strong><br>
Ce site utilise Google Ads (balise Google, gtag.js) afin de mesurer l'efficacité de nos
campagnes publicitaires. Ces outils peuvent déposer des cookies sur votre terminal.
Vous pouvez vous y opposer via les paramètres de votre navigateur ou via les
<a href="https://adssettings.google.com" rel="nofollow noopener" target="_blank">paramètres
des annonces Google</a>.</p>

<p><strong>Vos droits</strong><br>
Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition
et de portabilité de vos données. Pour l'exercer, écrivez à
<a href="mailto:{EMAIL}">{EMAIL}</a>. Vous pouvez également introduire une réclamation
auprès de la CNIL (<a href="https://www.cnil.fr" rel="nofollow noopener" target="_blank">cnil.fr</a>).</p>
'''


# =====================================================================
#  Fichiers techniques
# =====================================================================
def sitemap():
    pages = ["", "entretien-jardin.html", "creation-paysagisme.html"] + \
            [s["slug"] + ".html" for s in SERVICES] + \
            ["mentions-legales.html", "politique-confidentialite.html"]
    urls = "".join(
        f"  <url><loc>{BASE_URL}/{p}</loc><changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if p == '' else '0.8'}</priority></url>\n" for p in pages)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n'
            .replace("sitemap.org", "sitemaps.org") + urls + "</urlset>\n")


def robots():
    return (f"User-agent: *\nAllow: /\nDisallow: /merci.html\n\n"
            f"Sitemap: {BASE_URL}/sitemap.xml\n")


# =====================================================================
#  Génération
# =====================================================================
def main():
    print("Génération du site %s" % SITE)
    write("index.html", page_index())
    write("entretien-jardin.html", page_lp_entretien())
    write("creation-paysagisme.html", page_lp_creation())
    for s in SERVICES:
        write(s["slug"] + ".html", page_service(s))
    write("merci.html", page_merci())
    write("mentions-legales.html", legal_page(
        "mentions-legales", "Mentions légales",
        "Mentions légales du site Jardin de Gironde.", MENTIONS))
    write("politique-confidentialite.html", legal_page(
        "politique-confidentialite", "Politique de confidentialité",
        "Politique de confidentialité et traitement des données personnelles "
        "du site Jardin de Gironde.", CONFIDENTIALITE))
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
    print("Terminé.")


if __name__ == "__main__":
    main()

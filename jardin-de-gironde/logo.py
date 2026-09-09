#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère assets/img/logo-jdg.svg — reproduction vectorielle de l'écusson
Jardin de Gironde.

Le texte est converti en courbes : le fichier ne dépend d'aucune police,
pèse ~6 Ko et reste net à toutes les tailles.

Prérequis : les deux polices, à récupérer une fois dans /tmp/fonts/
    Oswald 700     https://fonts.google.com/specimen/Oswald
    Kaushan Script https://fonts.google.com/specimen/Kaushan+Script

    pip install fonttools && python3 logo.py

Si vous disposez du fichier d'origine du logo, inutile de lancer ce script :
déposez-le dans assets/img/ sous le nom logo.png, logo.webp ou logo.svg,
build.py le détecte et l'utilise en priorité.
"""

import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

GREEN = "#1E7A34"

def load(path):
    f = TTFont(path)
    return f, f.getGlyphSet(), f['head'].unitsPerEm, f['cmap'].getBestCmap()

def glyph_paths(font, gs, cmap, text):
    out = []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[name].draw(pen)
        out.append((pen.getCommands(), gs[name].width))
    return out

def straight(fontfile, text, size, cx, baseline, target_w):
    f, gs, upem, cmap = load(fontfile)
    gl = glyph_paths(f, gs, cmap, text)
    s = size / upem
    raw = sum(w for _, w in gl) * s
    n = len(gl)
    space = (target_w - raw) / (n - 1) if n > 1 else 0
    x = cx - target_w / 2
    parts = []
    for d, w in gl:
        if d:
            parts.append(f'<path d="{d}" transform="translate({x:.1f} {baseline:.1f}) '
                         f'scale({s:.5f} {-s:.5f})" fill="#ffffff"/>')
        x += w * s + space
    return "\n  ".join(parts)

def arched(fontfile, text, size, cx, baseline, target_w, rise):
    """Texte cintré : chaque lettre suit un arc de cercle."""
    f, gs, upem, cmap = load(fontfile)
    gl = glyph_paths(f, gs, cmap, text)
    s = size / upem
    raw = sum(w for _, w in gl) * s
    n = len(gl)
    space = (target_w - raw) / (n - 1) if n > 1 else 0
    R = (target_w ** 2) / (8 * rise) + rise / 2
    total = target_w + 0  # longueur de corde
    half = math.asin((target_w / 2) / R)          # demi-angle
    cy = baseline - rise + R                       # centre du cercle
    parts = []
    pos = 0.0
    for d, w in gl:
        adv = w * s
        mid = pos + adv / 2
        # position angulaire du centre de la lettre
        theta = (mid / (target_w)) * (2 * half) - half
        gx = cx + R * math.sin(theta)
        gy = cy - R * math.cos(theta)
        if d:
            ang = math.degrees(theta)
            parts.append(
                f'<path d="{d}" transform="translate({gx:.1f} {gy:.1f}) rotate({ang:.2f}) '
                f'translate({-adv/2:.1f} 0) scale({s:.5f} {-s:.5f})" fill="#ffffff"/>')
        pos += adv + space
    return "\n  ".join(parts)

OSW = '/tmp/fonts/Oswald700.ttf'
KAU = '/tmp/fonts/Kaushan.ttf'

# Les flancs restent verticaux jusqu'aux trois quarts de la hauteur : c'est ce
# qui laisse la place à GIRONDE avant que l'écusson ne se referme en pointe.
shield_outer = ("M 26 124 C 26 109 33 100 47 96 C 173 60 387 60 513 96 "
                "C 527 100 534 109 534 124 L 534 368 L 296 457 "
                "C 286 462 274 462 264 457 L 26 368 Z")
shield_inner = ("M 47 133 C 47 122 52 116 63 113 C 179 81 381 81 497 113 "
                "C 508 116 513 122 513 133 L 513 357 L 291 440 "
                "C 284 443 276 443 269 440 L 47 357 Z")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 480" role="img" aria-label="Jardin de Gironde">
  <title>Jardin de Gironde</title>
  <path d="{shield_outer}" fill="{GREEN}"/>
  <path d="{shield_inner}" fill="none" stroke="#ffffff" stroke-width="10"/>
  {arched(OSW, "JARDIN", 124, 280, 226, 416, 24)}
  <path d="M 74 258 C 134 251 180 249 218 250 C 180 254 134 257 74 262 Z" fill="#ffffff"/>
  <path d="M 486 258 C 426 251 380 249 342 250 C 380 254 426 257 486 262 Z" fill="#ffffff"/>
  {straight(KAU, "de", 84, 280, 274, 68)}
  {straight(OSW, "GIRONDE", 100, 280, 342, 424)}
</svg>
'''
open('assets/img/logo-jdg.svg', 'w', encoding='utf-8').write(svg)
print("écrit :", len(svg), "octets")

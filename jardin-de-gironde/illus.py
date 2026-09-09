#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Illustrations des prestations — style sérigraphie, une seule couleur.

Chaque membre est dessiné en « tube » : un trait épais vert par-dessus lequel
on repasse un trait plus fin de la couleur du fond. On obtient un contour
régulier, et l'ordre de tracé gère naturellement les recouvrements.

    cd jardin-de-gironde && python3 illus.py
"""

import os

GREEN = "#17662C"
BG = "#F7F5EE"          # doit correspondre au fond de la tuile (.service-media.illus)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/img/illus")

W = 3.0                  # épaisseur du contour


def tube(d, thickness):
    """Membre contouré : épaisseur = largeur visible du membre."""
    return (f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{thickness + 2 * W}"'
            f' stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{BG}" stroke-width="{thickness}"'
            f' stroke-linecap="round" stroke-linejoin="round"/>')


def shape(d, fill=BG):
    return f'<path d="{d}" fill="{fill}" stroke="{GREEN}" stroke-width="{W}" stroke-linejoin="round"/>'


def line(d, w=W):
    return (f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{w}"'
            f' stroke-linecap="round" stroke-linejoin="round"/>')


def dot(cx, cy, r=2.4):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GREEN}"/>'


def circle(cx, cy, r, fill=BG):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{GREEN}" stroke-width="{W}"/>'


def head(cx, cy, r=18, dir=1):
    """Tête + casquette + visage. dir = 1 regarde à droite, -1 à gauche."""
    s = [circle(cx, cy, r)]
    # casquette
    s.append(shape(f"M {cx - r - 1} {cy - 4} a {r + 1} {r + 1} 0 0 1 {2 * (r + 1)} 0 z"))
    # visière
    bx = cx + dir * (r - 3)
    s.append(shape(f"M {bx} {cy - 5} c {dir*11} 1 {dir*19} -1 {dir*23} -5 "
                   f"c {dir*-6} -4 {dir*-15} -5 {dir*-22} -4 z"))
    # visage
    s.append(dot(cx + dir * 7, cy + 1, 2.3))
    s.append(line(f"M {cx + dir * 1} {cy + 8} q {dir*5} 4 {dir*9} -1", 2.6))
    return "".join(s)


def ground(y=182, x0=14, x1=186):
    return line(f"M {x0} {y} H {x1}", 3.4)


def grass(xs, y=182):
    out = []
    for x in xs:
        out.append(line(f"M {x-5} {y} c 0 -6 1 -9 3 -12", 2.6))
        out.append(line(f"M {x} {y} c 1 -7 1 -11 0 -14", 2.6))
        out.append(line(f"M {x+5} {y} c 0 -6 -1 -9 -3 -12", 2.6))
    return "".join(out)


def svg(alt, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" '
            f'height="200" role="img" aria-label="{alt}">\n{body}\n</svg>\n')


SCENES = {}


def legs(cx, y_hip=120, y_foot=168, back=(-8, -15, -3), front=(9, 16, 30), t=13):
    """Les deux jambes, tracées avant le torse. Le segment horizontal final
    fait office de pied."""
    bx, bk, bt = back
    fx, fk, ft = front
    return (tube(f"M {cx+bx} {y_hip} C {cx+bk} {y_hip+18} {cx+bk-2} {y_foot-8} "
                 f"{cx+bk} {y_foot} L {cx+bt} {y_foot}", t)
            + tube(f"M {cx+fx} {y_hip} C {cx+fk} {y_hip+18} {cx+fk+1} {y_foot-8} "
                   f"{cx+fk} {y_foot} L {cx+ft} {y_foot}", t))


def torso(cx, y_top=86, y_bot=114, t=34):
    return tube(f"M {cx} {y_top} L {cx+2} {y_bot}", t)


# ------------------------------------------------------------------ tonte
CX = 62
_lg = legs(CX)
SCENES["tonte-pelouse"] = ("Jardinier poussant une tondeuse", "".join([
    ground(180), grass([24]),
    tube(f"M {CX-6} 94 C {CX+16} 100 {CX+26} 106 {CX+32} 112", 11),   # bras arrière
    _lg,
    torso(CX),
    tube(f"M {CX+12} 90 C {CX+26} 92 {CX+36} 96 {CX+42} 100", 12),    # bras avant
    head(CX, 54, 17),
    circle(CX+34, 113, 6), circle(CX+45, 101, 6),                     # mains
    line("M 100 104 L 140 146", 5),                                   # timon
    line("M 92 96 L 112 114", 5),                                     # traverse
    shape("M 138 140 h 44 a 10 10 0 0 1 10 10 v 14 a 10 10 0 0 1 -10 10 h -44 "
          "a 10 10 0 0 1 -10 -10 v -14 a 10 10 0 0 1 10 -10 z"),
    shape("M 152 140 v -10 a 4 4 0 0 1 4 -4 h 11 a 4 4 0 0 1 4 4 v 10 z"),
    line("M 170 160 h 13", 3.2),
    circle(140, 174, 8), circle(178, 174, 8), dot(140, 174, 2), dot(178, 174, 2),
]))

# ------------------------------------------------------------- taille haies
CX = 58
_lg = legs(CX)
SCENES["taille-haies"] = ("Jardinier taillant une haie", "".join([
    ground(180),
    shape("M 122 180 v -40 c 0 -17 13 -26 27 -24 c 6 -10 20 -11 26 -3 "
          "c 8 -5 21 -1 21 9 v 58 z"),
    line("M 142 178 v -30", 2.6), line("M 160 178 v -34", 2.6), line("M 178 178 v -28", 2.6),
    tube(f"M {CX-6} 96 C {CX+14} 104 {CX+26} 110 {CX+32} 114", 11),
    _lg,
    torso(CX),
    tube(f"M {CX+12} 90 C {CX+26} 92 {CX+36} 94 {CX+42} 98", 12),
    head(CX, 54, 17),
    circle(CX+34, 115, 6), circle(CX+45, 99, 6),
    shape("M 104 88 h 26 a 9 9 0 0 1 9 9 v 12 a 9 9 0 0 1 -9 9 h -26 z"),
    shape("M 139 96 h 44 a 6 6 0 0 1 0 12 h -44 z"),
    line("M 146 108 v 7 M 157 108 v 7 M 168 108 v 7 M 179 108 v 7", 2.8),
    shape("M 150 76 c 7 -2 11 2 10 8 c -6 3 -11 -1 -10 -8 z"),
    shape("M 172 66 c 7 -2 11 2 10 8 c -6 3 -11 -1 -10 -8 z"),
    shape("M 186 84 c 7 -2 11 2 10 8 c -6 3 -11 -1 -10 -8 z"),
]))

# ---------------------------------------------------------------- entretien
CX = 56
_lg = legs(CX)
SCENES["entretien-jardins"] = ("Jardinier arrosant une jeune plante", "".join([
    ground(180),
    tube(f"M {CX-6} 96 C {CX+12} 104 {CX+22} 110 {CX+28} 114", 11),
    _lg,
    torso(CX),
    tube(f"M {CX+12} 90 C {CX+26} 92 {CX+34} 96 {CX+40} 100", 12),
    head(CX, 54, 17),
    circle(CX+30, 115, 6), circle(CX+43, 101, 6),
    shape("M 104 110 L 101 142 a 9 9 0 0 0 9 9 h 22 a 9 9 0 0 0 9 -9 L 138 110 z"),
    line("M 99 110 h 42", 3.4),
    shape("M 112 110 c 1 -15 17 -15 18 0"),
    shape("M 140 120 L 163 105 L 172 116 L 145 133 Z"),
    line("M 160 122 c 4 9 5 15 5 21", 3),
    line("M 168 120 c 3 8 4 13 4 18", 3),
    line("M 176 178 V 152", 3.4),
    shape("M 176 160 c -14 1 -20 -7 -19 -15 c 12 -3 20 4 19 15 z"),
    shape("M 176 149 c 14 1 20 -7 19 -15 c -12 -3 -20 4 -19 15 z"),
]))

# ----------------------------------------------------------- débroussaillage
CX = 54
_lg = legs(CX)
SCENES["debroussaillage"] = ("Jardinier débroussaillant un terrain", "".join([
    ground(180),
    line("M 108 178 c 2 -15 10 -21 19 -22", 3),
    line("M 126 178 c -2 -13 5 -19 14 -20", 3),
    tube(f"M {CX-6} 94 C {CX+14} 96 {CX+26} 98 {CX+34} 100", 11),
    _lg,
    torso(CX),
    tube(f"M {CX+12} 90 C {CX+28} 96 {CX+40} 104 {CX+48} 110", 12),
    head(CX, 54, 17),
    shape("M 84 74 h 28 a 9 9 0 0 1 9 9 v 12 a 9 9 0 0 1 -9 9 h -28 z"),
    line("M 92 74 v -7 h 10 v 7", 3),
    line("M 116 102 L 152 148", 5.5),
    circle(CX+36, 101, 6), circle(CX+50, 112, 6),
    circle(157, 155, 14),
    line("M 157 155 l 11 -3 M 157 155 l -3 11 M 157 155 l -9 -8", 2.8),
    line("M 133 142 a 28 28 0 0 1 15 -13", 3),
    line("M 182 168 a 28 28 0 0 0 -16 -15", 3),
    line("M 140 122 l 10 -5 M 152 132 l 10 -4", 2.8),
]))

# ------------------------------------------------------------------ création
CX = 54
_lg = legs(CX, front=(9, 16, 32))
SCENES["creation-espaces-verts"] = ("Jardinier plantant un jeune arbre", "".join([
    ground(180),
    line("M 24 178 c 16 -18 40 -22 60 -22 c 20 0 44 4 60 22", 3.2),
    tube(f"M {CX-6} 94 C {CX+12} 100 {CX+22} 106 {CX+28} 112", 11),
    _lg,
    torso(CX),
    tube(f"M {CX+12} 90 C {CX+30} 88 {CX+44} 88 {CX+56} 92", 12),
    head(CX, 54, 17),
    circle(CX+30, 113, 6), circle(CX+58, 93, 6),
    shape("M 104 46 h 26 c 0 9 -6 14 -13 14 s -13 -5 -13 -14 z"),
    line("M 117 60 L 113 158", 5),
    shape("M 103 158 h 20 l -3 15 c -1 6 -6 9 -7 9 s -6 -3 -7 -9 z"),
    line("M 168 178 V 112", 4),
    shape("M 168 144 c -19 1 -27 -9 -26 -20 c 16 -4 27 5 26 20 z"),
    shape("M 168 129 c 19 1 27 -9 26 -20 c -16 -4 -27 5 -26 20 z"),
    shape("M 168 114 c -11 -7 -12 -19 -5 -27 c 11 5 13 19 5 27 z"),
]))

# ------------------------------------------------------------ haute pression
CX = 54
_lg = legs(CX)
SCENES["nettoyage-haute-pression"] = ("Jardinier nettoyant une terrasse au nettoyeur haute pression", "".join([
    ground(180),
    shape("M 118 156 h 72 v 22 h -72 z"),
    line("M 142 156 v 22 M 166 156 v 22", 2.8),
    line("M 125 166 h 5 M 133 172 h 5 M 150 164 h 4", 2.6),
    tube(f"M {CX-6} 96 C {CX+14} 104 {CX+26} 110 {CX+32} 114", 11),
    _lg,
    torso(CX),
    tube(f"M {CX+12} 90 C {CX+26} 92 {CX+34} 94 {CX+40} 96", 12),
    head(CX, 54, 17),
    circle(CX+34, 115, 6), circle(CX+43, 97, 6),
    shape("M 100 88 h 38 a 7 7 0 0 1 0 14 h -38 a 7 7 0 0 1 0 -14 z"),
    line("M 106 102 l -5 14", 3.4),
    line("M 138 92 l 22 5 a 3.5 3.5 0 0 1 0 5 l -22 5", 3.4),
    line("M 164 98 c 11 9 17 20 20 33", 3),
    line("M 163 105 c 8 11 11 22 11 32", 3),
    line("M 160 111 c 4 12 4 23 2 32", 3),
    line("M 180 62 l 3.5 8 8 3.5 -8 3.5 -3.5 8 -3.5 -8 -8 -3.5 8 -3.5 z", 2.8),
    line("M 158 76 l 2.5 6 6 2.5 -6 2.5 -2.5 6 -2.5 -6 -6 -2.5 6 -2.5 z", 2.8),
]))

# --------------------------------------------------------- toiture/gouttière
SCENES["nettoyage-toiture-gouttiere"] = ("Jardinier nettoyant une gouttière depuis une échelle", "".join([
    ground(180),
    shape("M 96 74 L 200 34 L 200 46 L 96 86 Z"),                  # pan de toit
    shape("M 92 86 h 108 v 17 h -108 z"),                          # gouttière
    shape("M 124 108 c 0 4 -3 5 -3 8 a 3 3 0 0 0 6 0 c 0 -3 -3 -4 -3 -8 z"),
    shape("M 168 110 c 0 4 -3 5 -3 8 a 3 3 0 0 0 6 0 c 0 -3 -3 -4 -3 -8 z"),
    line("M 30 180 L 72 44", 4.5),                                 # montants
    line("M 56 182 L 98 46", 4.5),
    line("M 66 64 L 92 66 M 61 84 L 87 86 M 56 104 L 82 106 "
         "M 51 124 L 77 126 M 46 144 L 72 146 M 41 164 L 67 166", 3.4),
    legs(88, y_hip=118, y_foot=150, back=(-8, -14, -2), front=(9, 15, 28)),
    torso(88, 84, 112),
    tube("M 76 92 C 66 100 62 110 62 118", 11),
    tube("M 100 88 C 118 84 132 80 142 76", 12),
    head(88, 52, 17),
    circle(146, 78, 6),
    shape("M 152 60 c 8 -2 12 2 11 9 c -7 3 -12 -2 -11 -9 z"),     # feuilles retirées
    shape("M 172 46 c 8 -2 12 2 11 9 c -7 3 -12 -2 -11 -9 z"),
    shape("M 132 52 c 8 -2 12 2 11 9 c -7 3 -12 -2 -11 -9 z"),
]))


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (alt, body) in SCENES.items():
        path = os.path.join(OUT, name + ".svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg(alt, body))
        print("  \u2713 %-34s %5d octets" % (name + ".svg", os.path.getsize(path)))


if __name__ == "__main__":
    main()

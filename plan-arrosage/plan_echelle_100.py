"""Plan d'arrosage a l'echelle 1/100 (1 cm = 1 m) - format A3 paysage.
Imprimer a 100 % / taille reelle (sans "ajuster a la page")."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrow

CM = 1 / 2.54
PW, PH = 42.0, 29.7            # A3 paysage (cm)
X0, X1, Y0, Y1 = -8.5, 23.5, -13.5, 3.5   # zone dessinee (m) -> 32 x 17 cm
AX_L, AX_B = 2.0, 10.0          # position du cadre sur la feuille (cm)

# ---------- Geometrie (m), x = le long de la rue des Colombes, y vers le haut ----------
ex = np.array([1.0, 0.0])
def arc(center, r, a0, a1, n=60):
    t = np.linspace(a0, a1, n)
    return np.c_[center[0] + r*np.cos(t), center[1] + r*np.sin(t)]

A = np.array([0.0, 0.0])
B = A + 21.628 * ex
# Angle coin arrondi (tangent rue / avenue), arc = 5,6271 m
u = np.array([0.265, 0.964]); u /= np.linalg.norm(u)      # direction P->Q (avenue)
theta = np.arccos(u @ ex)
R = 5.6271 / theta
O = A + np.array([0, -R])
coin = arc(O, R, np.pi/2 + theta, np.pi/2)                 # de Q vers A
Q = coin[0]
P = Q - 6.1264 * u
H4 = P + 6.6323 * ex
H1 = H4 + np.array([0, 5.4129])
H2 = H1 + 15.0847 * ex
F = H2 + np.array([0, -6.4244])
C = B + 4.9841 * np.array([0.057, -0.998]) / np.linalg.norm([0.057, -0.998])
dCD = np.array([-4.53, -2.13]); D = C + 5.0571 * dCD / np.linalg.norm(dCD)
E = np.array([17.88, -9.23])
# arc C->D (quart de cercle, concave)
mid, ch = (C + D) / 2, D - C
nrm = np.array([ch[1], -ch[0]]) / np.linalg.norm(ch)
Oc = mid - nrm * np.linalg.norm(ch) / 2
rc = np.linalg.norm(C - Oc)
a0, a1 = np.arctan2(*(C - Oc)[::-1]), np.arctan2(*(D - Oc)[::-1])
if a1 - a0 > np.pi: a1 -= 2*np.pi
if a0 - a1 > np.pi: a1 += 2*np.pi
arcCD = arc(Oc, rc, a0, a1)
W = np.array([-6.56, -11.93])   # arrivee eau de ville (position approx.)

massif = np.vstack([coin, B, arcCD, E, F, H2, H1, H4, P])

# ---------- Figure ----------
fig = plt.figure(figsize=(PW*CM, PH*CM))
ax = fig.add_axes([AX_L/PW, AX_B/PH, (X1-X0)/PW, (Y1-Y0)/PH])
ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for x in np.arange(np.ceil(X0), X1 + .01): ax.axvline(x, color="#e6e6e6", lw=.3, zorder=0)
for y in np.arange(np.ceil(Y0), Y1 + .01): ax.axhline(y, color="#e6e6e6", lw=.3, zorder=0)

# Maison
maison = np.array([H1, H2, [H2[0], Y0], [H1[0], Y0]])
ax.add_patch(Polygon(maison, closed=True, fc="#eeeeee", ec="#999999", lw=.8, ls="--", zorder=1))
ax.text(8.5, -6.0, "MAISON", ha="center", va="center", fontsize=16, color="#777", weight="bold")

# Massif a arroser
ax.add_patch(Polygon(massif, closed=True, fc="#dff0d0", ec="#d00000", lw=1.6, zorder=2))

# Mur exterieur blanc
mur = np.vstack([P, coin, B, C])
ax.plot(*mur.T, color="#333", lw=3.2, zorder=3, solid_capstyle="butt")
# Goutte-a-goutte (decale 30 cm a l'interieur)
def offset(poly, d):
    out = []
    for i, p in enumerate(poly):
        a = poly[max(i-1, 0)]; b = poly[min(i+1, len(poly)-1)]
        t = (b - a) / np.linalg.norm(b - a); out.append(p + d*np.array([t[1], -t[0]]))
    return np.array(out)
gag = offset(mur, 0.35)
ax.plot(*gag.T, color="#0066cc", lw=1.6, ls=(0, (4, 2)), zorder=4)

# Rues
ax.text(10.5, 2.0, "RUE DES COLOMBES", ha="center", va="center", fontsize=13, color="#555", weight="bold")
ax.text(-7.9, -4.0, "AV. DE L'ÎLE DE FRANCE", rotation=np.degrees(np.arctan2(u[1], u[0])),
        ha="center", va="center", fontsize=11, color="#555", weight="bold")

# Arrivee eau
ax.plot(*W, marker="s", ms=11, mfc="#0066cc", mec="k", zorder=6)
ax.annotate("ARRIVÉE EAU DE VILLE\n(regard compteur, position approx.)", W, xytext=(W[0]+2.2, W[1]-0.4),
            fontsize=8, va="center", arrowprops=dict(arrowstyle="-", lw=.6), zorder=6)

# Cotes (valeurs relevees, en cm)
def cote(p, q, txt, off):
    p, q = np.asarray(p), np.asarray(q); t = (q - p) / np.linalg.norm(q - p); n = np.array([-t[1], t[0]])
    a, b = p + off*n, q + off*n
    ax.annotate("", a, b, arrowprops=dict(arrowstyle="<->", lw=.7, color="#3344aa", shrinkA=0, shrinkB=0), zorder=7)
    for s, e in ((p, a), (q, b)): ax.plot(*np.c_[s, e + .15*np.sign(off)*n], color="#3344aa", lw=.4, zorder=7)
    m = (a + b) / 2 + 0.35*np.sign(off)*n
    ang = np.degrees(np.arctan2(t[1], t[0]))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    ax.text(*m, txt, rotation=ang, ha="center", va="center", fontsize=8.5, color="#3344aa", weight="bold",
            bbox=dict(fc="white", ec="none", pad=.5), zorder=8)
cote(A, B, "2162,80", 0.9)
cote(B, C, "498,41", 0.8)
cote(C, D, "505,71", 0.6)
cote(H2, F, "642,44", 0.7)
cote(H1, H2, "1508,47", -0.7)
cote(H1, H4, "541,29", 0.7)
cote(P, H4, "663,23", 0.7)
cote(P, Q, "612,64", 0.8)
mc = coin[len(coin)//2]; dirn = (mc - O) / np.linalg.norm(mc - O)
ax.text(*(mc + 1.1*dirn), "562,71\n(arrondi)", ha="center", va="center", fontsize=8.5, color="#3344aa", weight="bold")

# Nord (photo satellite orientee nord en haut)
nd = np.array([0.41, 0.91]); base = np.array([21.5, -12.0])
ax.add_patch(FancyArrow(*base, *(1.6*nd), width=.12, head_width=.5, head_length=.6, color="k", zorder=9))
ax.text(*(base + 2.6*nd), "N", ha="center", va="center", fontsize=12, weight="bold")

# Barre d'echelle 0-5 m
sb = np.array([-7.5, 2.2])
for i in range(5):
    ax.add_patch(plt.Rectangle(sb + [i, 0], 1, .25, fc="k" if i % 2 == 0 else "white", ec="k", lw=.6, zorder=9))
for i in range(6): ax.text(sb[0] + i, sb[1] + .55, f"{i} m", ha="center", fontsize=7)

# ---------- Cartouche ----------
def ft(x, y, s, **k): fig.text(x/PW, y/PH, s, **k)
ft(2.0, 28.2, "PLAN D'ARROSAGE AUTOMATIQUE — JARDIN", fontsize=18, weight="bold", va="center")
ft(2.0, 27.4, "Angle Rue des Colombes / Av. de l'Île de France", fontsize=11, va="center", color="#444")
ft(40.0, 28.2, "ÉCHELLE 1/100  —  1 cm = 1 m", fontsize=16, weight="bold", ha="right", va="center", color="#c00000")
ft(40.0, 27.4, "Format A3 paysage — imprimer à 100 % (taille réelle)", fontsize=9.5, ha="right", va="center")

leg = fig.add_axes([2/PW, 1.5/PH, 18/PW, 7.5/PH]); leg.axis("off"); leg.set_xlim(0, 18); leg.set_ylim(0, 7.5)
leg.text(0, 7.0, "LÉGENDE", fontsize=11, weight="bold")
leg.add_patch(Polygon([[0, 5.6], [1.2, 5.6], [1.2, 6.2], [0, 6.2]], fc="#dff0d0", ec="#d00000", lw=1.4))
leg.text(1.6, 5.9, "Massif / zone plantée à arroser", va="center", fontsize=9)
leg.plot([0, 1.2], [4.8, 4.8], color="#333", lw=3.2); leg.text(1.6, 4.8, "Mur extérieur blanc", va="center", fontsize=9)
leg.plot([0, 1.2], [3.8, 3.8], color="#0066cc", lw=1.6, ls=(0, (4, 2)))
leg.text(1.6, 3.8, "Ligne goutte-à-goutte le long du mur (≈ 40 m linéaires)", va="center", fontsize=9)
leg.plot(0.6, 2.8, marker="s", ms=10, mfc="#0066cc", mec="k"); leg.text(1.6, 2.8, "Arrivée eau de ville (regard rectangle verre)", va="center", fontsize=9)
leg.add_patch(Polygon([[0, 1.5], [1.2, 1.5], [1.2, 2.1], [0, 2.1]], fc="#eeeeee", ec="#999", ls="--"))
leg.text(1.6, 1.8, "Maison (non arrosée)", va="center", fontsize=9)
leg.text(0, 0.7, "Cotes en centimètres (relevé client). Quadrillage léger = 1 m.", fontsize=8.5, color="#3344aa")

nt = fig.add_axes([21.5/PW, 1.5/PH, 18.5/PW, 7.5/PH]); nt.axis("off"); nt.set_xlim(0, 18.5); nt.set_ylim(0, 7.5)
nt.add_patch(plt.Rectangle((0, 0), 18.5, 7.5, fill=False, lw=1))
nt.text(0.4, 6.9, "BESOINS / REMARQUES", fontsize=11, weight="bold", va="center")
for i, s in enumerate([
        "• Arrivée d'eau : eau de ville (regard rectangle à couvercle verre,",
        "   côté Av. de l'Île de France, en bas à gauche du plan).",
        "• Arrosage alimenté sur l'eau de ville.",
        "• Goutte-à-goutte tout le long du mur extérieur blanc : ≈ 40 m linéaires",
        "   (Av. de l'Île de France + arrondi + Rue des Colombes + retour).",
        "• Surface du massif : ≈ %.0f m²." % (0.5*abs(np.dot(massif[:,0], np.roll(massif[:,1],1)) - np.dot(massif[:,1], np.roll(massif[:,0],1)))),
        "• Contrôle d'impression : la barre 0–5 m doit mesurer 5 cm à la règle."]):
    nt.text(0.4, 6.0 - i*0.8, s, fontsize=9, va="center")

for ext in ("pdf", "png"):
    fig.savefig(f"plan-arrosage/plan_arrosage_echelle_1-100_A3.{ext}", dpi=200)
print("R coin = %.2f m, lg mur = %.2f m" % (R, 6.1264 + 5.6271 + 21.628 + 4.9841))

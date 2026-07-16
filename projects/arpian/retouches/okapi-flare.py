#!/usr/bin/env python3
"""Retouche flare — okapi-elastique.jpeg (Chalet Arpian).

Corrections :
1. Voile lumineux diagonal (dehaze local, rendu naturel) :
   - Zone A (sapins + mains de l'adulte) : le voile est estimé comme champ
     lisse par canal à partir du plancher local (érosion) des pixels sombres,
     étendu par inpainting sur les zones claires — fonctionne bien car le
     fond (sapins) est uniformément sombre. Ciel exclu par masque.
   - Zone B (nappe claire bas-droite) : le fond y est hétérogène (herbe,
     gonflables, tente), un champ estimé crée des taches ; on modélise donc
     le voile MANUELLEMENT : somme de gaussiennes 2D placées sur la nappe,
     couleur du voile mesurée (herbe voilée vs herbe propre).
   - Zone E (tapis du trampoline) : champ estimé (fond sombre uniforme),
     dosage léger.
2. Arc-en-ciel de flare : aplatissement de chrominance ciblé (a/b LAB tirés
   vers leur médiane locale k=61), luminance et texture herbe conservées.

Sortie : okapi-elastique-retouchee.jpeg (qualité 92).
"""

import cv2
import numpy as np
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "okapi-elastique.jpeg")
DST = os.path.join(HERE, "okapi-elastique-retouchee.jpeg")

img = cv2.imread(SRC).astype(np.float32)
H, W = img.shape[:2]  # 3672 x 2066


# ---------------------------------------------------------------- utilities
def feathered_rect(x1, y1, x2, y2, sigma):
    m = np.zeros((H, W), np.float32)
    m[y1:y2, x1:x2] = 1.0
    k = int(sigma * 3) | 1
    return cv2.GaussianBlur(m, (k, k), sigma)


def estimate_veil_field(dark_thresh=125):
    """Champ de voile par canal (B,G,R) au 1/4 de résolution, remonté."""
    scale = 0.25
    small = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    dmin = small.min(axis=2)
    invalid = (dmin > dark_thresh).astype(np.uint8)
    invalid = cv2.dilate(invalid, np.ones((5, 5), np.uint8))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    fields = []
    for c in range(3):
        floor = cv2.erode(small[:, :, c], ker)
        floor8 = np.clip(floor, 0, 255).astype(np.uint8)
        filled = cv2.inpaint(floor8, invalid, 7, cv2.INPAINT_TELEA).astype(np.float32)
        filled = cv2.GaussianBlur(filled, (0, 0), 15)
        fields.append(cv2.resize(filled, (W, H), interpolation=cv2.INTER_LINEAR))
    return np.stack(fields, axis=2)


def sky_protection():
    b, r = img[:, :, 0], img[:, :, 2]
    sky = ((b - r > 18) & (b > 125)).astype(np.float32)
    sky = cv2.GaussianBlur(sky, (0, 0), 4)
    return 1.0 - np.clip(sky * 1.4, 0, 1)


def gaussian_blob(cx, cy, sx, sy, amp):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return amp * np.exp(-(((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2) / 2.0)


def apply_field_zone(out, veil, no_sky, rect, feather, strength):
    x1, y1, x2, y2 = rect
    w = feathered_rect(x1, y1, x2, y2, feather) * no_sky
    core = w > 0.6
    for c in range(3):
        anchor = np.percentile(veil[:, :, c][core], 8)
        excess = np.maximum(veil[:, :, c] - anchor, 0)
        out[:, :, c] -= strength * excess * w
    return out


def flatten_chroma(out, x1, y1, x2, y2, sigma_mask, keep, ksize=61,
                   lo=15.0, hi=35.0, exclude=None):
    """Désaturation ciblée : a/b LAB tirés vers leur médiane locale.

    Seuil doux par pixel : les déviations chromatiques modérées (arc-en-ciel,
    tinte de flare) sont aplaties (facteur `keep`), les fortes (bords d'objets
    réellement colorés, ex. panneau rouge) sont conservées (rampe lo→hi).
    `exclude` : liste de rects (x1,y1,x2,y2) adoucis à retirer du masque
    (ex. bord du trampoline).
    """
    m = 90
    cx1, cy1 = max(x1 - m, 0), max(y1 - m, 0)
    cx2, cy2 = min(x2 + m, W), min(y2 + m, H)
    crop = np.clip(out[cy1:cy2, cx1:cx2], 0, 255).astype(np.uint8)
    lab = cv2.cvtColor(crop, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    med_a = cv2.medianBlur(a, ksize).astype(np.float32)
    med_b = cv2.medianBlur(b, ksize).astype(np.float32)
    af, bf = a.astype(np.float32), b.astype(np.float32)
    dev = np.sqrt((af - med_a) ** 2 + (bf - med_b) ** 2)
    t = np.clip((dev - lo) / (hi - lo), 0, 1)
    t = t * t * (3 - 2 * t)  # smoothstep
    factor = keep + (1.0 - keep) * t  # fraction de déviation conservée
    mm = np.zeros(l.shape, np.float32)
    mm[y1 - cy1:y2 - cy1, x1 - cx1:x2 - cx1] = 1.0
    if exclude:
        for ex1, ey1, ex2, ey2 in exclude:
            gx1, gy1 = max(ex1 - cx1, 0), max(ey1 - cy1, 0)
            gx2, gy2 = min(ex2 - cx1, mm.shape[1]), min(ey2 - cy1, mm.shape[0])
            if gx2 > gx1 and gy2 > gy1:
                cut = np.zeros_like(mm)
                cut[gy1:gy2, gx1:gx2] = 1.0
                cut = cv2.GaussianBlur(cut, (0, 0), 25)
                mm *= (1.0 - np.clip(cut * 1.2, 0, 1))
    kk = int(sigma_mask * 3) | 1
    mm = cv2.GaussianBlur(mm, (kk, kk), sigma_mask)
    blend = mm * (1.0 - factor)  # 0 = inchangé, 1 = médiane
    af = af - blend * (af - med_a)
    bf = bf - blend * (bf - med_b)
    lab2 = cv2.merge([l, np.clip(af, 0, 255).astype(np.uint8),
                      np.clip(bf, 0, 255).astype(np.uint8)])
    out[cy1:cy2, cx1:cx2] = cv2.cvtColor(lab2, cv2.COLOR_LAB2BGR).astype(np.float32)
    return out


# ------------------------------------------------------- 1. voile lumineux
veil = estimate_veil_field()
no_sky = sky_protection()
out = img.copy()

# Zone A — traînées sur les sapins + mains/bras (champ estimé)
out = apply_field_zone(out, veil, no_sky, rect=(110, 1560, 740, 2470),
                       feather=50, strength=0.90)

# Zone E — voile doux sur le tapis du trampoline (champ estimé, dosage léger)
out = apply_field_zone(out, veil, no_sky, rect=(0, 3080, 1300, 3672),
                       feather=70, strength=0.70)

# Zone B — nappe claire bas-droite : voile modélisé (gaussiennes 2D, couleur
# par nappe). Couleur mesurée sur l'herbe : voilée (152,172,165) - propre
# (124,117,100) ≈ (B28,G55,R65) → voile chaud-laiteux (35,52,58) ; sur
# l'ombre de la tente un voile neutre évite une dominante violette.
WARM = np.array([35.0, 52.0, 58.0], np.float32)     # B, G, R
NEUTRE = np.array([45.0, 50.0, 54.0], np.float32)
GRIS = np.array([40.0, 40.0, 48.0], np.float32)
# Les nappes d'une même couleur sont combinées par MAX (pas de cumul aux
# recouvrements) puis bornées à 1.0. L'ombre de la tente est dosée léger :
# elle contient des ghosts clairs qu'une soustraction lisse ne peut pas
# enlever — mieux vaut la laisser doucement brumeuse que sombre et tachée.
GROUPES = [
    (WARM, [
        (1850, 3200, 340, 360, 0.85),   # nappe principale sur l'herbe
        (1420, 3030, 230, 200, 0.75),   # bande de l'arc-en-ciel (streaks)
        (1620, 3070, 150, 130, 0.50),   # suite des streaks vers la droite
        (1650, 3220, 140, 90, 0.35),    # patch chaud résiduel sur l'herbe
        (2050, 3300, 200, 350, 0.75),   # bord droit bas
        (1900, 3600, 300, 180, 0.50),   # coin bas-droite
    ]),
    (NEUTRE, [
        (1560, 2900, 300, 320, 0.55),   # ombre de la tente / ghosts
        (2000, 2780, 260, 260, 0.55),   # tente côté droit / haut
        (500, 2050, 100, 320, 0.40),    # bande résiduelle centre sapins
    ]),
    (GRIS, [
        (540, 2100, 45, 90, 0.50),      # petit ghost rose sur les sapins
    ]),
]
STRENGTH_B = 0.95
for col, blobs in GROUPES:
    w = np.zeros((H, W), np.float32)
    for cx, cy, sx, sy, amp in blobs:
        w = np.maximum(w, gaussian_blob(cx, cy, sx, sy, amp))
    w = np.clip(w, 0, 1.0) * no_sky
    out -= STRENGTH_B * w[:, :, None] * col[None, None, :]

# Luminance de l'arc-en-ciel : bande claire le long du trajet de l'arc
# (ombre de la tente → herbe), soustraite en blanc doux via une chaîne de
# petites gaussiennes (chrominance traitée séparément plus bas).
ARC_PTS = [(1400, 2465), (1520, 2530), (1620, 2610), (1700, 2700),
           (1760, 2800), (1800, 2900), (1830, 3000), (1850, 3100)]
w_arc = np.zeros((H, W), np.float32)
for ax, ay in ARC_PTS:
    w_arc = np.maximum(w_arc, gaussian_blob(ax, ay, 45, 45, 1.0))
out -= 0.55 * (w_arc * no_sky)[:, :, None] * np.float32(16.0)

out = np.clip(out, 0, 255)

# ------------------------------------------------------ 2. arc-en-ciel
# Zone C : tout le trajet de l'arc (herbe, chalet, tente, panneau rouge).
# Le seuil doux préserve les objets réellement colorés ; le bord du
# trampoline est exclu du masque (consigne : ne pas y toucher).
out = flatten_chroma(out, 1180, 2380, 2066, 3300, sigma_mask=45, keep=0.15,
                     exclude=[(1100, 3280, 1900, 3672)])
# Zone C3 : ghost rose résiduel sur les sapins
out = flatten_chroma(out, 480, 1990, 630, 2230, sigma_mask=25, keep=0.25)
# Zone D : petit arc résiduel au bord droit, sur l'herbe
out = flatten_chroma(out, 1900, 3280, 2066, 3620, sigma_mask=30, keep=0.30)
# Segment cyan résiduel de l'arc, près du sac sombre
out = flatten_chroma(out, 1790, 2860, 1910, 3060, sigma_mask=25, keep=0.25,
                     lo=8, hi=50)

# Panneau rouge (toboggan de la tente) : la bande de l'arc y crée des
# déviations trop fortes pour le seuil doux — on tire les pixels déviants
# (verdis ou jaunis) de l'intérieur du panneau vers sa chrominance médiane.
px1, py1, px2, py2 = 1705, 2620, 1785, 2890  # intérieur du panneau
crop = np.clip(out[py1:py2, px1:px2], 0, 255).astype(np.uint8)
lab = cv2.cvtColor(crop, cv2.COLOR_BGR2LAB).astype(np.float32)
med_a = float(np.median(lab[:, :, 1]))
med_b = float(np.median(lab[:, :, 2]))
shift = np.maximum(
    np.clip((med_a - 8.0 - lab[:, :, 1]) / 10.0, 0, 1),   # verdis
    np.clip((lab[:, :, 2] - med_b - 12.0) / 10.0, 0, 1))  # jaunis
mm = np.zeros(shift.shape, np.float32)
mm[8:-8, 8:-8] = 1.0
mm = cv2.GaussianBlur(mm, (0, 0), 6)
blend = 0.65 * shift * mm
lab[:, :, 1] += blend * (med_a - lab[:, :, 1])
lab[:, :, 2] += blend * (med_b - lab[:, :, 2])
out[py1:py2, px1:px2] = cv2.cvtColor(
    np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

cv2.imwrite(DST, out.astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
print("écrit :", DST)

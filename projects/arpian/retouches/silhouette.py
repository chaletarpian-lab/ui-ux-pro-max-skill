"""Ajoute une silhouette de dos (contre-jour, hors focus) devant la fenêtre,
même effet que la photo d'inspiration mymountainresort."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = 'fenetre-original.jpeg'
OUT = 'fenetre-silhouette.jpeg'

img = Image.open(SRC).convert('RGB')
W, H = img.size

# ---- proportions (unité = hauteur de tête) ----
CX = 0.435 * W           # axe vertical de la figure
HEAD_H = 0.074 * H       # hauteur de tête
HEAD_TOP = 0.268 * H
HEAD_RX = HEAD_H * 0.42
HEAD_CY = HEAD_TOP + HEAD_H / 2
HEAD_RY = HEAD_H / 2
NECK_Y = HEAD_TOP + HEAD_H * 1.02
SHOULDER_Y = HEAD_TOP + HEAD_H * 1.42
SHOULDER_HALF = HEAD_H * 1.12    # carrure
WAIST_Y = HEAD_TOP + HEAD_H * 3.3
WAIST_HALF = HEAD_H * 0.82
HIP_Y = HEAD_TOP + HEAD_H * 4.1
HIP_HALF = HEAD_H * 0.88
FEET_Y = HEAD_TOP + HEAD_H * 7.4
FEET_HALF = HEAD_H * 0.42
FADE_START = HEAD_TOP + HEAD_H * 4.6   # fondu des jambes dans l'ombre
FADE_END = FEET_Y
BLUR = 12

rng = np.random.default_rng(7)

def hair_wobble(n, amp):
    phase = rng.uniform(0, 2 * np.pi, 3)
    t = np.linspace(0, 2 * np.pi, n)
    w = (np.sin(3 * t + phase[0]) * 0.5 +
         np.sin(7 * t + phase[1]) * 0.3 +
         np.sin(13 * t + phase[2]) * 0.2)
    return w * amp

pts = []

# tête (par le haut, léger volume de cheveux à l'arrière-gauche)
n_head = 60
ang = np.linspace(np.pi, 0, n_head)
wob = hair_wobble(n_head, HEAD_RX * 0.05)
for i, a in enumerate(ang):
    r_x = HEAD_RX * (1 + 0.08 * np.sin(a) * np.cos(a * 0.7))
    x = CX + np.cos(a) * (r_x + wob[i])
    y = HEAD_CY - np.sin(a) * (HEAD_RY * 1.02 + wob[i])
    pts.append((x, y))

# côté droit : cheveux -> léger creux de nuque -> épaule
pts += [
    (CX + HEAD_RX * 1.00, HEAD_CY + HEAD_RY * 0.45),
    (CX + HEAD_RX * 0.80, NECK_Y),
    (CX + HEAD_RX * 0.85, NECK_Y + HEAD_H * 0.10),
    # trapèze puis épaule arrondie, ligne presque horizontale
    (CX + SHOULDER_HALF * 0.45, SHOULDER_Y - HEAD_H * 0.16),
    (CX + SHOULDER_HALF * 0.78, SHOULDER_Y - HEAD_H * 0.06),
    (CX + SHOULDER_HALF * 0.96, SHOULDER_Y + HEAD_H * 0.05),
    (CX + SHOULDER_HALF * 1.00, SHOULDER_Y + HEAD_H * 0.28),
]
# bras droit le long du corps -> taille -> hanche
pts += [
    (CX + SHOULDER_HALF * 0.98, SHOULDER_Y + HEAD_H * 0.9),
    (CX + WAIST_HALF * 1.04, WAIST_Y),
    (CX + HIP_HALF, HIP_Y),
]
# jambes (fondu dans l'ombre)
pts += [
    (CX + FEET_HALF * 1.3, FEET_Y - HEAD_H * 0.8),
    (CX + FEET_HALF, FEET_Y),
    (CX - FEET_HALF, FEET_Y),
    (CX - FEET_HALF * 1.3, FEET_Y - HEAD_H * 0.8),
]
# hanche -> taille -> bras gauche
pts += [
    (CX - HIP_HALF, HIP_Y),
    (CX - WAIST_HALF * 1.04, WAIST_Y),
    (CX - SHOULDER_HALF * 0.98, SHOULDER_Y + HEAD_H * 0.9),
]
# épaule gauche (à peine plus haute) -> nuque -> cheveux
pts += [
    (CX - SHOULDER_HALF * 1.00, SHOULDER_Y + HEAD_H * 0.24),
    (CX - SHOULDER_HALF * 0.95, SHOULDER_Y + HEAD_H * 0.02),
    (CX - SHOULDER_HALF * 0.76, SHOULDER_Y - HEAD_H * 0.10),
    (CX - SHOULDER_HALF * 0.44, SHOULDER_Y - HEAD_H * 0.19),
    (CX - HEAD_RX * 0.88, NECK_Y + HEAD_H * 0.08),
    (CX - HEAD_RX * 0.84, NECK_Y - HEAD_H * 0.02),
    (CX - HEAD_RX * 1.04, HEAD_CY + HEAD_RY * 0.40),
]

# ---- masque (supersampling x2 + flou de mise au point) ----
mask = Image.new('L', (W * 2, H * 2), 0)
d = ImageDraw.Draw(mask)
d.polygon([(x * 2, y * 2) for x, y in pts], fill=255)
mask = mask.resize((W, H), Image.LANCZOS)
mask = mask.filter(ImageFilter.GaussianBlur(BLUR))

# fondu vertical des jambes dans l'ombre du sol
m = np.asarray(mask, dtype=np.float32) / 255.0
ys = np.arange(H, dtype=np.float32)
ramp = np.clip((FADE_END - ys) / (FADE_END - FADE_START), 0, 1)
ramp = ramp ** 1.4
m *= ramp[:, None]

# ---- composite ----
sil_color = np.array([13, 12, 14], dtype=np.float32)
base = np.asarray(img, dtype=np.float32)
a = (m * 0.985)[..., None]
out = base * (1 - a) + sil_color * a
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(OUT, quality=93)
print('saved', OUT)

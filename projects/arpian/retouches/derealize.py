"""Post-traitement « photo réelle » pour images générées par IA :
grain capteur, aberration chromatique, vignettage, tons imparfaits,
pipeline de netteté façon smartphone."""
import numpy as np
import cv2

def process(src, dst, *, desat=0.92, black_lift=5, glow_cut=0.0,
            grain=4.2, chroma_noise=1.4, ca_px=1.4, vignette=0.10,
            seed=1):
    rng = np.random.default_rng(seed)
    img = cv2.imread(src).astype(np.float32)
    h, w = img.shape[:2]

    # 1) micro-resample : casse la texture trop uniforme du rendu IA
    img = cv2.resize(img, (int(w * 0.88), int(h * 0.88)), interpolation=cv2.INTER_AREA)
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)

    # 2) tons : désaturation légère, voile réduit, noirs relevés, épaule douce
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] *= desat
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    if glow_cut > 0:            # récupère du contraste dans le voile lumineux
        mean = cv2.GaussianBlur(img, (0, 0), 60)
        img = np.clip(img + glow_cut * (img - mean), 0, 255)
    x = img / 255.0
    x = x + (black_lift / 255.0) * (1 - x) ** 2          # noirs légèrement laiteux
    x = np.where(x > 0.82, 0.82 + (x - 0.82) * 0.82, x)  # épaule sur les hautes lumières
    img = x * 255.0

    # 3) aberration chromatique radiale (bords)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    scale = ca_px * r ** 2
    map_out_x = xx + (xx - cx) / cx * scale
    map_out_y = yy + (yy - cy) / cy * scale
    map_in_x = xx - (xx - cx) / cx * scale
    map_in_y = yy - (yy - cy) / cy * scale
    img[:, :, 2] = cv2.remap(img[:, :, 2], map_out_x, map_out_y, cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)
    img[:, :, 0] = cv2.remap(img[:, :, 0], map_in_x, map_in_y, cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)

    # 4) vignettage doux
    vig = 1 - vignette * r ** 2
    img *= vig[..., None]

    # 5) grain : bruit de luminance dominant en basses lumières + bruit chroma fin
    lum = img.mean(axis=2, keepdims=True) / 255.0
    strength = grain * (1.15 - 0.7 * lum)
    noise_l = rng.normal(0, 1, (h, w, 1)).astype(np.float32)
    noise_l = cv2.GaussianBlur(noise_l, (0, 0), 0.6)[..., None]
    noise_c = rng.normal(0, chroma_noise, (h, w, 3)).astype(np.float32)
    img = img + noise_l * strength + noise_c

    # 6) accentuation légère façon pipeline smartphone
    blur = cv2.GaussianBlur(img, (0, 0), 1.2)
    img = np.clip(img + 0.35 * (img - blur), 0, 255)

    cv2.imwrite(dst, img.astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print('saved', dst)

# photo 1 : saturation chaude marquée -> désaturation un peu plus forte
process('enfants-lit-01-ia.jpeg', 'enfants-lit-01-realiste.jpeg',
        desat=0.90, black_lift=5, glow_cut=0.06, grain=4.4, seed=11)

# photo 2 : voile lumineux prononcé -> dehaze plus fort, grain un peu plus visible
process('enfants-lit-02-ia.jpeg', 'enfants-lit-02-realiste.jpeg',
        desat=0.91, black_lift=4, glow_cut=0.14, grain=4.8, seed=22)

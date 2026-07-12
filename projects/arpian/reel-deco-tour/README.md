# Reel Instagram — « Le tour déco » (Chalet Arpian)

Reel vertical 1080 × 1920 (~48 s, 30 fps) : visite déco du chalet pièce par pièce,
23 scènes avec effet Ken Burns et fondus enchaînés, dans le design système Arpian
(`../design-system.md`) : palette crème / chocolat / or, Fraunces + Montserrat,
kickers « — 0X — LA PIÈCE », accents italiques or, clôture chocolat avec CTA.

## Fichiers

- `reel.html` — timeline des scènes (photos, textes, cadrages `pos`, durées) et
  fonction `window.seek(t)` déterministe pour le rendu image par image.
  Ouvrir dans un navigateur pour une prévisualisation en boucle.
- `render.mjs` — capture les frames via Playwright/Chromium puis assemble le MP4.
- `assets/photos/` — photos redimensionnées (hauteur max 2208 px pour l'overscan Ken Burns).
- `output/arpian-reel-deco-tour.mp4` — le Reel final.

## Régénérer

```bash
cd projects/arpian/reel-deco-tour
npm install playwright@1.56.1 --no-save
node render.mjs 30 ./frames [chemin-ffmpeg]   # ffmpeg avec libx264 requis
```

Pour modifier une scène (texte, cadrage, ordre), éditer le tableau `SCENES`
dans `reel.html` puis relancer le rendu.

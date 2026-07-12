# Production des slides Instagram (carrousels)

> Pour tout agent qui produit des visuels. Le design système complet est dans
> `projects/arpian/design-system.md` — le lire AVANT ce fichier.

## Rappel design système (résumé opérationnel)

- Format : **1080 × 1350** (portrait 4:5), HTML autonome → capture PNG.
- Couleurs : crème `#F3EEE5`, chocolat `#221A13`, or `#C2A279`.
  Scrims photo en `rgba(24,18,12,…)` (brun neutre, jamais bleu/noir pur).
- Fontes (locales, dans `instagram-carousel/assets/fonts/fonts.css`) :
  **Fraunces** 600 (titres, segment clé en *italique or*), Fraunces 400 (body),
  **Montserrat** 500/600 (kickers uppercase espacés, CTA, URL).
- Grammaire des slides : couverture centrée / slides contenu bas-gauche avec
  kicker « — 0X — TITRE » / clôture fond chocolat avec CTA or.
  Détails et exemples : `design-system.md` + slides HTML existantes.

## Pipeline technique

```bash
cd projects/arpian/instagram-carousel
npm install playwright@1.56.1 --no-save   # chromium déjà présent : /opt/pw-browsers/chromium
node screenshot.mjs                        # rend toutes les slides listées → output/
rm -rf node_modules package.json package-lock.json   # AVANT tout commit
```

- Chaque slide = un fichier `slide-XX-nom.html` ajouté à la liste de `screenshot.mjs`.
- Nouvelle photo : la copier dans `assets/` (jamais référencer les uploads).
- Google Fonts passe par le proxy (`SSL_CERT_FILE=/root/.ccr/ca-bundle.crt` en Python) ;
  toute nouvelle fonte doit être téléchargée en local et ajoutée à `fonts.css`.

## Contrôle qualité visuel (obligatoire avant livraison)

1. **Regarder chaque PNG rendu** (outil Read) — jamais livrer à l'aveugle.
2. Lisibilité : texte sur zone chargée → renforcer le scrim, pas la taille.
3. Cadrage : régler `object-position` pour garder les sujets (personnes, enseigne).
4. Vérifier retours à la ligne des titres (pas de mot isolé), pagination,
   orthographe (Okapi, Arpian), accents.
5. Crédit photo si la source l'exige (ex. « © OT Valmorel / Pierre Jacques »,
   vertical bord droit, Montserrat 16px, crème 55 %).

## Retouches photo (scripts dans `projects/arpian/retouches/`)

- `silhouette.py` : silhouette humaine paramétrable (contre-jour, flou).
- `derealize.py` : rendre une image IA photographique (grain, désat, CA, vignette).
- Suppression d'objets : privilégier le **clonage par bandes** en respectant les
  lignes de structure (crêtes, horizon) ; inpainting Telea uniquement sur petites
  zones sombres homogènes, loin des zones claires (il bave).
- Toujours travailler sur une copie ; garder l'original dans le dossier.
- Itérer : rendre → regarder le crop en pleine résolution → corriger.

## Prompts pour IA génératives (GPT Image, etc.)

- Contraintes de préservation EN PREMIER : « TÂCHE D'ÉDITION, PAS DE NOUVELLE
  SCÈNE », cadrage/format verrouillés, liste des éléments à garder pixel-identiques.
- Description des sujets COURTE (une description riche fait recadrer le modèle).
- Style enfants : « bon chic bon genre » (velours côtelé, col claudine, maille,
  nœuds), pas de logos. Exiger : « clearly airborne », « candid unposed expressions ».
- Livrer FR + EN. Rappeler le tag « créé avec l'IA » de Meta pour la publication.
- Après génération : passer `derealize.py` pour le rendu photo.

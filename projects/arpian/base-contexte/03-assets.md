# Inventaire des assets

> Chemins relatifs à `projects/arpian/`. Tenir ce fichier à jour à chaque ajout.

## Identité

| Asset | Chemin | Notes |
|---|---|---|
| Logo blanc (fond sombre) | `instagram-carousel/assets/arpian-logo-blanc.png` | 600×230, PNG alpha. Couverture : centré bas ~320px ; slides contenu : haut-gauche ~210px |
| Fontes locales | `instagram-carousel/assets/fonts/fonts.css` | Fraunces, Montserrat, Cormorant Garamond, Great Vibes (woff2 locaux) |

## Photos prêtes à l'emploi

| Photo | Chemin | Usage |
|---|---|---|
| Okapi (retouchée, sans grue) | `instagram-carousel/assets/okapi-day.jpeg` | Trampolines en journée, enfant au centre |
| Family room néon (soir) | `instagram-carousel/assets/family-room-night.jpeg` | Enfants en pyjama, enseigne néon |
| Valmorel village été | `instagram-carousel/assets/valmorel-summer.webp` | Panorama. **Crédit obligatoire : © OT Valmorel / Pierre Jacques** |
| Fenêtre + personne assise (sans lampadaire) | `retouches/fenetre-assise-sans-lampadaire.jpeg` | Contemplative, luge, sommets. Générée IA puis retouchée |
| Fenêtre vide (original) | `retouches/fenetre-original.jpeg` | Base pour éditions IA |
| Enfants sautant sur lits ×2 (IA, réalisées) | `retouches/enfants-lit-0{1,2}-realiste.jpeg` | Post-traitées grain/désat. Tag IA Meta à la publication |
| Couloir + bambin au caddie | `instagram-carousel/assets/couloir-enfant.jpeg` | Moment volé, enfant au fond du couloir |
| Élastique Okapi (retouchée, sans flare) | `instagram-carousel/assets/okapi-elastique.jpeg` | Enfant en plein vol, Crêt du Niélard. Original + script : `retouches/okapi-*` |

## Bannières (`banniere/`)

| Bannière | Fichier | Notes |
|---|---|---|
| LinkedIn « Votre tribu, votre chalet, votre rythme. » | `banniere-linkedin.html` → `output/banniere-linkedin-arpian.png` | 1584×396 @2x, photo `assets/salon-vue.jpeg`, rendu via `screenshot-banniere.mjs` ; référence d'origine : `reference-banniere.png` |

## Slides produites (HTML + PNG dans `instagram-carousel/`)

| Slide | Fichier | Statut |
|---|---|---|
| Couverture panorama « activité phare » | `slide-00-intro.html` | Alternative |
| Couverture Okapi « Le paradis des enfants, à Valmorel. » | `slide-00-intro-okapi.html` | **Choix actuel** |
| Contenu 01 Okapi « le paradis des enfants. » | `slide-01-okapi.html` | Redondante si couverture Okapi |
| Contenu 02 Family room « leur paradis du soir. » | `slide-02-family-room.html` | OK |
| Clôture « Des vacances au paradis, ça se réserve. » | `slide-03-cloture.html` | OK |
| Post « Adults only ou kids friendly ? » | `slide-post-adults-kids.html` | Chute « vos réveils », or clair #D8BC94 sur zone claire |
| Post « Ici, les enfants touchent le ciel. » | `slide-post-okapi-ciel.html` | Bloc texte centré dans le ciel |

## Légendes validées (historique des livrables texte)

- Carrousel « deux paradis » : accroche « Le paradis des enfants, à Valmorel. »
- Photo bar/pièce à vivre : « Le cœur battant du chalet. » (bar vestige de
  l'ancien restaurant, bardage Samuel ébéniste)
- Dortoir en suite : « Les quartiers des enfants. » (2 dortoirs, salle d'eau chacun)
- Reel activités sportives : accroche « Si pour vous, vacances à la montagne rime
  avec vacances sportives, vous serez servis à Valmorel. »
- Dortoir SDB intégrée : « Dans chaque dortoir, une salle d'eau. La leur. »
- Terrasse été (bain non chauffé) : « Le paradis des grands existe aussi. »
- Post couloir : « Adults only ou kids friendly : à l'Arpian, c'est vous qui
  choisissez. Vos réveils aussi. » (+ concept « vos propres hôtes »)
- Post élastique Okapi : « Ici, les enfants touchent le ciel. » (Crêt du Niélard)

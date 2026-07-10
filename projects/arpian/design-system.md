# Design Système — Chalet Arpian (Valmorel)

Identité dérivée de l'enseigne néon de la Family Room : « CHALET ARPIAN — *Valmorel* »
(bleu électrique + script rose néon sur bois de mélèze), esprit chalet alpin premium & familial.

## Couleurs

| Token | Hex | Usage |
|---|---|---|
| `--nuit-alpine` | `#0B1030` | Fond profond, scrims, textes sur clair |
| `--neon-glacier` | `#5B8CFF` | Accent néon bleu (enseigne), soirée |
| `--neon-valmorel` | `#FF5C8A` | Accent script rose néon, soirée |
| `--melze` | `#D9A05B` | Bois chaud, filets, détails |
| `--soleil-altitude` | `#FFC145` | Accent journée (soleil, énergie) |
| `--neige` | `#FBF7F0` | Texte principal sur photo/scrim |

Dualité jour/nuit : accent **soleil-altitude** en journée, accents **néon glacier + valmorel**
(avec glow `text-shadow`) en soirée. Le scrim `nuit-alpine` unifie les deux.

## Typographie

| Rôle | Fonte | Usage |
|---|---|---|
| Display | Cormorant Garamond 600/700 | Titres — élégance hôtelière |
| Script | Great Vibes | Mots accent — écho du « Valmorel » néon |
| Label/Body | Montserrat 500/600 | Kickers uppercase (letter-spacing 0.3em), sous-titres |

## Grille slide Instagram (1080 × 1350)

- Photo plein cadre (`object-fit: cover`), scrim dégradé transparent → nuit-alpine.
- Barre de marque en haut : filets `melze` + « CHALET ARPIAN · VALMOREL ».
- Bloc texte bas : kicker uppercase accent → titre serif `neige` → ligne script accent → sous-titre Montserrat.
- Pied : points de pagination + indication de swipe / handle.

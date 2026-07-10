# Design Système — Chalet Arpian (Valmorel)

Style « éditorial alpin » : photos plein cadre, serif à fort contraste, accent italique doré,
palette crème / chocolat / or. Référence : carrousel été (`arpianete01…06`) réalisé dans Claude design.

## Couleurs

| Token | Hex | Usage |
|---|---|---|
| `--creme` | `#F3EEE5` | Texte sur photo/sombre, fond des slides claires |
| `--chocolat` | `#221A13` | Fond des slides de clôture, texte sur crème |
| `--or` | `#C2A279` | Accent : kickers, mots en italique, CTA, étoiles |

Scrims photo : dégradés de `rgba(24,18,12,…)` (brun neutre, jamais bleu).

## Typographie

| Rôle | Fonte | Usage |
|---|---|---|
| Display | Fraunces 600 | Titres ; le mot/segment clé passe en *italique doré* |
| Body | Fraunces 400 | Sous-titres et légendes, interlignage 1.55–1.6 |
| Label | Montserrat 500/600 | Kickers uppercase (letter-spacing 0.16–0.32em), CTA, URL |

## Grammaire des slides (1080 × 1350)

- **Couverture** : kicker or centré « VALMOREL · SAVOIE · … », titre centré crème dont la
  dernière ligne est en italique or, sous-titre serif 2 lignes, étoiles « ✦ ✦ ✦ » or,
  logo blanc centré en bas.
- **Slides contenu** : petit logo blanc en haut à gauche ; bloc texte bas-gauche :
  kicker « — 0X — TITRE » or, titre crème + ligne italique or, body serif crème 2 lignes.
- **Clôture** (fond chocolat) : étoiles or en haut, titre italique centré (fin en or),
  signature « Une tribu. Un chalet. Arpian. » en or, bandeau CTA or (texte chocolat,
  Montserrat uppercase, une seule ligne), logo centré, « ARPIAN-VALMOREL.COM » espacé.
- Crédit photo éventuel : vertical sur le bord droit, Montserrat 16px, crème 55 %.

## Régénérer les PNG

```bash
cd projects/arpian/instagram-carousel
npm install playwright@1.56.1 --no-save
node screenshot.mjs   # écrit dans output/
```

# Carrousel LinkedIn — Chalet Arpian (Valmorel)

Dossier autonome : tout ce qu'il faut pour modifier et regénérer le carrousel
dans n'importe quelle session Claude Code (ou en local).

## Contenu

- `slides.html` — la source des 11 slides (1080 × 1350, format 4:5 LinkedIn).
  Chemins **relatifs** vers `assets/` : le fichier s'ouvre aussi dans un navigateur.
- `assets/` — photos recadrées du chalet, portraits partenaires, logo Arpian
  (`logo_arpian.png`, fond transparent), polices Lora + Outfit (`assets/fonts/`).
- `build.py` — regénère les PNG des slides et le PDF final.
- `slide_01.png` … `slide_11.png` — le dernier rendu.
- `CarrouselLinkedInArpian.pdf` — **le fichier à publier sur LinkedIn**
  (post → « Ajouter un document »).

## Regénérer après modification

```bash
pip install playwright pillow
playwright install chromium        # inutile si Chromium déjà fourni
python3 build.py
# Claude Code web : python3 build.py --chromium /opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

## Structure des slides

| # | id HTML | Contenu |
|---|---------|---------|
| 1 | `s1` | Couverture — « Un chalet rien que pour votre tribu. » |
| 2 | `s2` | L'extérieur (chalet sous la neige) |
| 3 | `s3` | Le salon — 100 m² de vie commune |
| 4 | `s4` | La salle à manger — bar en bois sculpté |
| 5 | `s5` | La cuisine — chef privé + équipements |
| 6 | `s6` | Les chambres — literie 5 étoiles + appartement |
| 7 | `s7` | Family room — discothèque & cinéma privé |
| 8 | `s7b` | Coin gaming — baby-foot & borne d'arcade |
| 9 | `s8` | Bain nordique — 8 places, sauna |
| 10 | `s9` | Nos partenaires — Sam, Saro, Nathan + options |
| 11 | `s10` | Slide de fin — « Une tribu. Un chalet. Arpian. » |

## Identité graphique

- Fond `#1C140D`, crème `#F4F1EA`, doré `#C4A57B`, texte discret `#B8A895`
  (variables CSS `:root` en tête de `slides.html`).
- Titres : Lora Bold, partie dorée en Lora Bold Italic (`<span class="it">`).
- Eyebrows / puces / boutons : Outfit, majuscules espacées.
- La bannière LinkedIn assortie est dans `../banners/BanniereLinkedInArpian.png`
  (titre Lora Bold 90 px, sous-titre Lora Bold Italic, même doré).

## Modifier

- Textes : directement dans `slides.html` (entités HTML pour les accents).
- Photos : remplacer le fichier dans `assets/` ou changer `src` ;
  le cadrage se règle avec `object-position` sur l'`<img>`.
- Ajouter une slide : dupliquer un bloc `<div class="slide" id="...">`,
  ajouter l'id dans `SLIDE_IDS` de `build.py`, mettre à jour les `pagenum`.

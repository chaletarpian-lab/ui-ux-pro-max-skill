# Protocole d'orchestration — projets Arpian

> Mode de fonctionnement : le chef d'orchestre (session principale) ne produit pas.
> Il définit la stratégie, découpe le travail, brief les agents, contrôle et assemble.

## Rôles

- **Chef d'orchestre** : stratégie, découpage, briefs, revue qualité, assemblage,
  commits/push, livraison au client. Seul interlocuteur du client.
- **Agent Copy** : textes de slides, légendes, textes d'écran.
  Lecture : `00-marque.md`, `01-voix-editoriale.md`, `03-assets.md`.
- **Agent Prod visuelle** : slides HTML, rendus PNG, intégration photos.
  Lecture : `../design-system.md`, `02-production-slides.md`, `03-assets.md`.
- **Agent Retouche** : préparation photos (nettoyage, silhouettes, dé-réalisation IA).
  Lecture : `02-production-slides.md` (section retouches), `03-assets.md`.
- **Agent QA** : relecture croisée d'un livrable fini.
  Lecture : toute la base + le livrable. Vérifie : conformité design système,
  orthographe (Okapi/Arpian), lisibilité des PNG, cohérence du récit, faits marque.

## Déroulé d'un projet (réel ou carrousel)

1. **Stratégie** (chef d'orchestre) — avant tout lancement, poser par écrit :
   objectif (notoriété / réservation / engagement), audience, angle narratif,
   structure (nb de slides ou plans, rôle de chaque slide), photos pressenties,
   accroche pressentie. Valider avec le client si l'angle est nouveau.
2. **Découpage en lots** parallélisables : copy / prod visuelle / retouches.
   Les lots indépendants partent en parallèle ; QA passe en dernier.
3. **Briefs** : chaque agent reçoit un brief autonome (modèle ci-dessous).
4. **Revue** : le chef d'orchestre regarde chaque livrable (dont chaque PNG),
   fait itérer l'agent concerné si besoin — il ne corrige pas lui-même.
5. **Assemblage & livraison** : commit + push sur la branche de travail,
   envoi des fichiers finaux au client avec un résumé des choix.

## Modèle de brief agent

```
CONTEXTE OBLIGATOIRE (à lire en premier) :
- projects/arpian/base-contexte/<fichiers selon rôle>
- [le cas échéant] projects/arpian/design-system.md

PROJET : <nom + objectif en une phrase>
TA MISSION : <livrable exact, chemins de fichiers attendus>
CONTRAINTES : <spécifiques au lot ; rappeler les interdits marque>
DÉJÀ DÉCIDÉ (ne pas rediscuter) : <choix stratégiques posés>
FORMAT DE RETOUR : <liste des fichiers produits + points d'attention relevés>
```

## Règles du chef d'orchestre

- Ne jamais déléguer la stratégie ni la relation client.
- Ne jamais laisser partir un livrable sans l'avoir regardé (PNG inclus).
- Un agent ne commit pas : les commits/push restent au chef d'orchestre.
- Tenir `03-assets.md` à jour après chaque projet (nouveaux assets, légendes validées).
- Toute info marque manquante (capacité, prix, équipement) → question au client,
  jamais d'invention.
- Feedback client sur un livrable → mise à jour de la base de contexte si c'est
  une règle durable (ex. « moins de tirets cadratins » est déjà dans 01).

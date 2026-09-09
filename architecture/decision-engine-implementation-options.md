# Decision Engine — options d'implémentation

Le modèle de décision de ce dépôt reste **vendor-neutral**. Les politiques et contrats doivent pouvoir être portés sur plusieurs technologies.

## Option A — moteur de règles applicatif

Approche retenue pour le POC portable :

- règles versionnées dans Git ;
- moteur Python simple ;
- reason codes explicites ;
- tests unitaires ;
- aucune dépendance propriétaire.

**Avantage** : léger, transparent, facile à tester.

**Limite** : gouvernance métier et authoring moins riches qu'une plateforme dédiée.

## Option B — IBM ODM

IBM ODM peut être évalué comme implémentation d'entreprise lorsque les besoins incluent :

- authoring et gouvernance de règles métier ;
- séparation cycle de vie règles / code applicatif ;
- versioning et promotion de Decision Services ;
- audit et explicabilité de politiques déterministes.

Dans ce dépôt, ODM reste **une option d'implémentation**, pas une dépendance obligatoire. Le dépôt ODM/IARD séparé porte l'apprentissage approfondi de cette technologie.

## Option C — moteur DMN / règles open source ou plateforme cloud

Une implémentation DMN/rules compatible avec les contraintes de l'entreprise peut également porter ces politiques, à condition de conserver :

- versioning ;
- tests ;
- traçabilité ;
- reason codes ;
- séparation recommandation/exécution ;
- portabilité des contrats.

## Critères de choix

- gouvernance des règles ;
- compétences disponibles ;
- intégration OpenShift/Azure ;
- sécurité ;
- audit ;
- coût/licence ;
- performance ;
- résilience ;
- facilité de CI/CD et GitOps.

# MayaBank Carbon-Aware Decision Architecture

Référentiel d’architecture et laboratoire pédagogique pour concevoir une plateforme de **décision de décarbonation des infrastructures de paiement**, dans un contexte fictif et anonymisé.

## Positionnement

**Architecte Solution — Green IT / Carbon-Aware Architecture / AI / GreenOps — Payment Infrastructure**

Le dépôt montre comment relier :

```text
Infrastructure de paiement
  -> inventaire / CMDB / observabilité
  -> CPU / RAM / JVM / stockage / DB / énergie / coût
  -> calcul carbone
  -> AI / ML pour prévoir et optimiser
  -> Decision Engine pour appliquer les politiques
  -> MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW
  -> OpenShift / Cloud / ITSM / GitOps
```

## Cas d’usage fil rouge

Plateforme fictive **MayaBank Payment Platform** :

- modernisation middleware vers OpenShift ;
- right-sizing CPU/RAM ;
- rationalisation VM/JVM ;
- optimisation stockage et sauvegarde ;
- consolidation bases de données ;
- arrêt ou réduction des environnements non critiques ;
- comparaison de scénarios d’architecture selon carbone, coût, performance, sécurité et résilience.

## Principe architectural

L’AI cherche, prévoit et optimise. Le Decision Engine vérifie les contraintes de l’entreprise.

```text
Metrics / CMDB / Cost / Carbon
            |
            v
         AI / ML
  prediction / anomaly / optimization
            |
            v
      Decision Engine
  policy / SLA / RTO / security / budget
            |
            v
MIGRATE / RIGHTSIZE / KEEP / REVIEW
```

Le moteur de décision reste **vendor-neutral** dans ce dépôt. IBM ODM pourra être évalué comme une implémentation possible, sans transformer ce dépôt en second dépôt ODM.

## Règles du dépôt

- aucun nom, donnée, architecture interne ou chiffre attribuable à une entreprise réelle ;
- tous les scénarios utilisent **MayaBank Payment Platform** ;
- données de démonstration synthétiques uniquement ;
- distinguer mesure, calcul, hypothèse et prédiction ;
- ne jamais présenter un gain carbone estimé comme une mesure réelle ;
- chaque recommandation doit pouvoir expliquer ses critères ;
- chaque itération doit être récupérable, documentée et testable indépendamment.

## État

**Itération 0 — Initialisation et cadrage : TERMINÉE**

Voir `docs/iteration-00/README.md`.

## Roadmap

Voir `docs/00-roadmap.md`.

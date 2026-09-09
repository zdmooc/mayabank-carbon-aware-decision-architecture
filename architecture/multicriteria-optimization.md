# Architecture — Optimisation multi-critères GreenOps

## But

Comparer plusieurs options d'architecture sans réduire la décision à un seul KPI.

```text
Decision Engine candidates
        ↓
Hard policy gate
        ↓
Eligible architecture options
        ↓
Multicriteria Engine
  carbon / cost / performance
  availability / risk
        ↓
Pareto front
        ↓
Preference profile
        ↓
Recommended option + alternatives
        ↓
Human review / ITSM / future GitOps
```

## Séparation essentielle

### Contraintes dures

Avant tout scoring :
- sécurité ;
- RTO/RPO ;
- conformité ;
- dépendance bloquante ;
- qualité minimale des données ;
- budget obligatoire si nécessaire.

Une option rejetée par une contrainte dure ne peut pas être « sauvée » par un bon score carbone.

### Critères d'arbitrage

Une fois l'option éligible :
- carbone ;
- coût ;
- performance ;
- disponibilité ;
- risque.

Les poids sont versionnés séparément de la logique du Decision Engine.

## Pourquoi Pareto

Une moyenne pondérée unique peut cacher des compromis importants. Le front de Pareto conserve les options non dominées afin qu'un architecte puisse voir :
- l'option la plus conservatrice ;
- l'option la plus sobre ;
- l'option la moins coûteuse ;
- l'option au meilleur compromis selon le profil choisi.

## Sortie cible

Chaque analyse expose :
- `candidateId` ;
- `profileVersion` ;
- `recommendedOption` ;
- `recommendedAction` ;
- `recommendedUtilityScore` ;
- `paretoOptions[]` ;
- score détaillé de chaque option ;
- `autoApplyAllowed=false`.

## Gouvernance

- changement de poids = changement de policy versionné ;
- aucune optimisation n'est auto-appliquée ;
- les alternatives Pareto restent visibles ;
- les données synthétiques et poids de lab ne sont jamais présentés comme politiques réelles ;
- une option peut revenir en `REVIEW` dans le futur si une contrainte transverse change.

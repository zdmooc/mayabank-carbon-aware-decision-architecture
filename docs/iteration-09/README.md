# Itération 9 — Optimisation multi-critères & Pareto

## Statut

**TERMINÉE — comparaison carbone/coût/performance/risque/disponibilité, front de Pareto et recommandation explicable livrés.**

## Objectif

Éviter qu'une décision GreenOps soit réduite à un seul indicateur carbone ou coût.

```text
Options d'architecture
  KEEP / RIGHTSIZE / MIGRATE / ...
          ↓
Hard policy gates
          ↓
Carbone / Coût / Performance
Risque / Disponibilité
          ↓
Pareto dominance
          ↓
Options non dominées
          ↓
Weighted preference profile
          ↓
Recommended option + alternatives
```

## Principe

Le moteur distingue deux étapes :

1. **contraintes dures** : une option non éligible selon sécurité, SLA, RTO/RPO ou policy n'entre pas dans l'optimisation ;
2. **arbitrage multi-critères** : les options restantes sont comparées sans supposer qu'un critère domine tous les autres.

## Critères v1

À maximiser :
- réduction carbone ;
- réduction de coût ;
- performance ;
- disponibilité.

À minimiser :
- risque.

## Pareto

Une option est dominée lorsqu'une autre option est au moins aussi bonne sur tous les critères et strictement meilleure sur au moins un.

Le front de Pareto est conservé pour montrer les compromis possibles avant application d'un profil de préférences.

## Profil de préférences v1

Poids synthétiques et versionnés :
- carbone : 30 % ;
- coût : 20 % ;
- performance : 15 % ;
- disponibilité : 15 % ;
- risque : 20 %.

Ces poids ne représentent aucune politique d'entreprise réelle. Ils servent uniquement au laboratoire.

## Livrables

- `optimization/weights.json` ;
- `optimization/pareto.py` ;
- `data/synthetic/multicriteria-options.csv` ;
- `tests/test_multicriteria.py` ;
- `architecture/multicriteria-optimization.md`.

## Exécution

```bash
python optimization/pareto.py
python optimization/pareto.py --json
python -m unittest tests/test_multicriteria.py
```

## Critères de sortie

- [x] carbone pris en compte ;
- [x] coût pris en compte ;
- [x] performance prise en compte ;
- [x] risque pris en compte ;
- [x] disponibilité prise en compte ;
- [x] contraintes dures séparées des préférences ;
- [x] front de Pareto calculé ;
- [x] option dominée détectée ;
- [x] recommandation pondérée explicable ;
- [x] alternatives Pareto conservées ;
- [x] aucune exécution automatique d'un changement.

## Prochaine étape

**Itération 10 — API & Event-Driven : Recommendation API, OpenAPI, événements RecommendationGenerated/DecisionApproved/ChangeApplied, AsyncAPI, correlation ID et audit.**

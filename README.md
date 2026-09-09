# MayaBank Carbon-Aware Decision Architecture

Référentiel d’architecture et laboratoire pédagogique pour concevoir une plateforme de **décision de décarbonation des infrastructures de paiement**, dans un contexte fictif et anonymisé.

## Positionnement

**Architecte Solution — Green IT / Carbon-Aware Architecture / AI / GreenOps — Payment Infrastructure**

Le dépôt relie :

```text
Infrastructure / CMDB / observabilité
  -> Carbon Engine
  -> Right-Sizing / Modernisation / Storage
  -> AI / ML
  -> Decision Engine
  -> Optimisation multi-critères / Pareto
  -> Recommendation API / Event-Driven
  -> OpenShift / Azure / GitOps / ITSM
```

## Principe architectural

**L’AI/ML prévoit et priorise ; le Decision Engine applique les contraintes dures ; l’optimisation multi-critères compare les options éligibles ; l’humain approuve les changements sensibles ; l’API n’applique aucun changement automatiquement.**

## Cas d’usage fil rouge

Plateforme fictive **MayaBank Payment Platform** : modernisation middleware, right-sizing CPU/RAM, rationalisation VM/JVM, optimisation stockage/backup, consolidation DB, réduction non-prod et comparaison carbone/coût/performance/risque/disponibilité.

## Modules livrés

### I2 — Carbon Engine

```bash
python carbon-engine/engine.py --scenario optimized
python -m unittest tests/test_carbon_engine.py
```

### I3–I6 — Observabilité / Right-Sizing / Modernisation / Storage

```bash
python observability/normalize_metrics.py
python rightsizing/recommend.py
python modernization/assess.py
python storage/assess.py
```

### I7 — AI / ML GreenOps

Forecast CPU/power, consommation, anomalies, ranking, `confidenceScore` et fallback. L’AI/ML ne déclenche aucun changement.

### I8 — Decision Engine

Le moteur vérifie qualité, confiance ML, criticité, SLA/RTO/RPO, sécurité, budget et dépendances. Décisions : `MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW`.

`autoApplyAllowed=false` pour toutes les décisions.

### I9 — Optimisation multi-critères

Carbone, coût, performance, disponibilité, risque, hard gates, front de Pareto, poids versionnés et alternatives non dominées.

```bash
python optimization/pareto.py
python -m unittest tests/test_multicriteria.py
```

### I10 — Recommendation API & Event-Driven

L’API réutilise directement le Decision Engine :

- `POST /v1/recommendations/evaluate` ;
- `POST /v1/recommendations/{recommendationId}/approve` ;
- OpenAPI 3.1 ;
- `X-Correlation-Id` ;
- audit JSONL ;
- `policyVersion` et `reasonCodes` conservés ;
- aucune duplication de la politique dans l’API.

Événements AsyncAPI 3.1 :

- `RecommendationGenerated` ;
- `DecisionApproved` ;
- `ChangeApplied`.

`ChangeApplied` appartient au processus de changement externe contrôlé. L’appel `/approve` retourne toujours :

```text
autoApplyAllowed=false
changeApplied=false
```

Validation portable :

```bash
python -m unittest tests/test_recommendation_api.py
python api/reference_recommendation_api.py
```

Le fichier `data/synthetic/recommendation-events.jsonl` montre la chaîne complète de façon synthétique et explicitement non réelle.

## Stratégie de déploiement

1. **OpenShift Local / CRC** — prochaine étape I11.
2. **Azure AKS** — cible Kubernetes Azure de référence.
3. **ARO** — option entreprise si OpenShift managé sur Azure est requis.

## Règles du dépôt

- aucun nom, chiffre ou architecture attribuable à une entreprise réelle ;
- données synthétiques uniquement ;
- distinguer mesure, calcul, hypothèse et prédiction ;
- ne jamais présenter un gain estimé comme une mesure réelle ;
- chaque recommandation doit expliquer ses critères ;
- aucun hard gate ne peut être compensé par une pondération ;
- approbation et exécution sont deux étapes distinctes ;
- aucune recommandation n’est auto-appliquée ;
- éviter tout fork fonctionnel entre OpenShift Local et Azure.

## État

- **I0 à I10 : TERMINÉES**
- **Prochaine : I11 — OpenShift Local / CRC**

Voir `docs/iteration-10/README.md`, `docs/00-roadmap.md` et `docs/BACKLOG.md`.

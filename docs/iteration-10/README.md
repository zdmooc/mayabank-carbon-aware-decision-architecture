# Itération 10 — Recommendation API & Event-Driven

## Statut

**TERMINÉE — Recommendation API, OpenAPI, AsyncAPI, correlation ID, audit et séparation approbation/exécution livrés.**

## Objectif

Exposer les décisions GreenOps de manière gouvernée et traçable sans permettre à l'API d'appliquer automatiquement un changement d'infrastructure.

```text
Metrics / Carbon / AI-ML
        ↓
Decision Engine
        ↓
Recommendation API
        ↓
RecommendationGenerated
        ↓
Human approval
        ↓
DecisionApproved
        ↓
ITSM / GitOps / Change process
        ↓
ChangeApplied
```

## API v1

Endpoints :

- `POST /v1/recommendations/evaluate` ;
- `POST /v1/recommendations/{recommendationId}/approve` ;
- `GET /health/live` ;
- `GET /health/ready`.

Le endpoint `evaluate` réutilise directement `decision-engine/engine.py` et ses politiques versionnées. Les règles ne sont pas dupliquées dans la couche API.

## Gouvernance

- `X-Correlation-Id` propagé ;
- `recommendationId` généré par l'API ;
- `policyVersion` exposée ;
- `reasonCodes` conservés ;
- `humanApprovalRequired` conservé ;
- `autoApplyAllowed=false` ;
- l'approbation humaine enregistre une intention approuvée mais n'exécute aucun changement ;
- `changeApplied=false` après l'appel `/approve`.

## Événements v1

Topics logiques :

- `mayabank.greenops.recommendation.generated.v1` ;
- `mayabank.greenops.decision.approved.v1` ;
- `mayabank.greenops.change.applied.v1`.

Événements :

- `RecommendationGenerated` ;
- `DecisionApproved` ;
- `ChangeApplied`.

Le dernier événement est émis uniquement par le processus de changement contrôlé après exécution réelle. **La Recommendation API ne génère jamais `ChangeApplied` automatiquement.**

## Audit

Le serveur de référence écrit ses événements dans un journal JSONL local, configurable avec :

```bash
EVENT_AUDIT_PATH=/tmp/greenops-events.jsonl
```

Un journal de démonstration synthétique est fourni dans :

`data/synthetic/recommendation-events.jsonl`

## Livrables

- `api/recommendation-api.openapi.yaml` ;
- `api/recommendation-events.asyncapi.yaml` ;
- `api/reference_recommendation_api.py` ;
- `data/synthetic/recommendation-events.jsonl` ;
- `tests/test_recommendation_api.py`.

## Validation portable

```bash
python -m unittest tests/test_recommendation_api.py
python api/reference_recommendation_api.py
```

Serveur local par défaut :

`http://127.0.0.1:8090`

## Critères de sortie

- [x] Recommendation API ;
- [x] OpenAPI 3.1 ;
- [x] réutilisation du Decision Engine existant ;
- [x] événements RecommendationGenerated / DecisionApproved / ChangeApplied définis ;
- [x] AsyncAPI 3.1 ;
- [x] correlation ID ;
- [x] audit JSONL ;
- [x] sécurité logique : contrainte non satisfaite -> REVIEW ;
- [x] séparation recommandation / approbation / exécution ;
- [x] aucun changement auto-appliqué.

## Prochaine étape

**Itération 11 — OpenShift Local / CRC : containerisation et déploiement Carbon Engine / Recommendation API / AI-ML / Decision Engine, Services/Routes, ConfigMaps/Secrets, quotas/policies, observabilité locale et E2E.**

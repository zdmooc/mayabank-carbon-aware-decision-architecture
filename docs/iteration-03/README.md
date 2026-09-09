# Itération 3 — Observabilité, inventaire et qualité des données

## Statut

**TERMINÉE — pipeline synthétique d’ingestion/normalisation, corrélation et tests de qualité livrés.**

## Objectif

Préparer des données d’observabilité fiables avant tout right-sizing ou recommandation carbone.

Le Carbon Engine ne doit pas consommer aveuglément une métrique. Il doit connaître :

- sa source ;
- sa date ;
- sa fraîcheur ;
- sa complétude ;
- l’actif auquel elle appartient ;
- l’application et l’environnement associés ;
- les anomalies ou informations manquantes.

## Chaîne de traitement

```text
Sources synthétiques
Grafana-like / APM-like / Prometheus-like
             ↓
      observability-raw.csv
             ↓
   normalize_metrics.py
             ↓
Correlation avec inventory.csv
             ↓
Freshness + Completeness + Warnings
             ↓
GOOD / WARN / INVALID / QUARANTINE
             ↓
Future Right-Sizing / Carbon Engine / Decision Engine
```

## Règles v1

### Fraîcheur

Pour rendre les tests déterministes, l’Itération 3 utilise un instant de référence synthétique fixe :

`2026-09-01T12:00:00Z`

Seuil : **60 minutes**.

- âge <= 60 min : `FRESH` ;
- âge > 60 min : `STALE` + warning `STALE_METRIC`.

### Corrélation

Une métrique dont `asset_id` n’existe pas dans l’inventaire est placée en quarantaine :

`UNKNOWN_ASSET`

Elle ne doit pas alimenter un calcul carbone ou une recommandation.

### Données manquantes

- CPU et RAM sont obligatoires pour la normalisation v1 ;
- power manquant -> `WARN`, car un calcul carbone direct serait incomplet ;
- heap JVM manquant sur un actif JVM -> `WARN` ;
- aucune valeur manquante n’est remplacée silencieusement.

## Livrables

- `data/synthetic/observability-raw.csv` ;
- `observability/normalize_metrics.py` ;
- `tests/test_observability_pipeline.py`.

## Exécution locale

```bash
python observability/normalize_metrics.py
```

Tests :

```bash
python -m unittest tests/test_observability_pipeline.py
```

## Cas couverts

- actif connu et métriques fraîches ;
- métrique stale ;
- métrique power manquante ;
- métrique JVM avec heap ;
- actif inconnu mis en quarantaine ;
- corrélation asset -> application -> environnement.

## Principe d’architecture

**Pas de décision GreenOps fiable sans qualité et provenance des données.**

Le futur Decision Engine pourra refuser ou dégrader une recommandation quand :

- la donnée est trop ancienne ;
- une métrique requise manque ;
- l’actif n’est pas inventorié ;
- la provenance ou la confiance sont insuffisantes.

## Critères de sortie

- [x] ingestion synthétique CPU/RAM/JVM ;
- [x] corrélation application -> infrastructure ;
- [x] fraîcheur calculée explicitement ;
- [x] données manquantes visibles ;
- [x] actif inconnu mis en quarantaine ;
- [x] qualité et warnings exposés ;
- [x] tests de non-régression fournis ;
- [x] aucune donnée d’entreprise réelle.

## Prochaine étape

**Itération 4 — Right-Sizing : détection de sous-utilisation, recommandations requests/limits, capacité N+1, garde-fous SLA et explication de décision.**

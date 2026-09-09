# Itération 1 — Modèle de données Carbon & Infrastructure

## Statut

**TERMINÉE — modèle, dictionnaire, données synthétiques et validateur livrés.**

## Objectif

Construire le modèle de données minimal nécessaire pour comparer des scénarios d’infrastructure de paiement selon :

- capacité ;
- utilisation réelle ;
- coût ;
- énergie ;
- carbone ;
- criticité ;
- résilience ;
- qualité/provenance des données.

## Principe

Avant de faire de l’AI ou d’appliquer des règles de décision, il faut pouvoir distinguer clairement :

```text
INVENTAIRE
  application / environnement / actif
        ↓
MESURE
  CPU / RAM / stockage / énergie
        ↓
FACTEUR
  intensité carbone / période / zone
        ↓
CALCUL
  estimation carbone
        ↓
PRÉDICTION
  AI / ML (itérations futures)
        ↓
DÉCISION
  Decision Engine (itérations futures)
```

## Entités v1

- `Application` ;
- `Environment` ;
- `ComputeAsset` ;
- `MetricObservation` ;
- `CarbonFactor` ;
- `CostObservation` ;
- `DataProvenance`.

## Identifiants

Tous les jeux de données utilisent des identifiants fictifs stables :

- application : `APP-*` ;
- actif : `ASSET-*` ;
- observation : horodatage ISO-8601 ;
- facteur carbone : `CF-*`.

## Données de démonstration

Les données de `data/synthetic/` sont **entièrement synthétiques**. Elles ne reproduisent aucun chiffre, inventaire ou nom d’une entreprise réelle.

## Livrables

- `docs/iteration-01/data-dictionary.md` ;
- `schemas/carbon-infra-record.schema.json` ;
- `data/synthetic/inventory.csv` ;
- `data/synthetic/metrics.csv` ;
- `data/synthetic/carbon-factors.csv` ;
- `tools/validate_iteration_01.py`.

## Critères de sortie

- [x] modèle application/environnement/actif défini ;
- [x] CPU/RAM/stockage représentés ;
- [x] métriques séparées de l’inventaire ;
- [x] facteurs carbone séparés des mesures ;
- [x] provenance/qualité prévues ;
- [x] données synthétiques fournies ;
- [x] validateur sans dépendance externe fourni ;
- [x] aucune donnée client réelle.

## Exécution locale

Depuis la racine du dépôt :

```bash
python tools/validate_iteration_01.py
```

Résultat attendu :

```text
Iteration 01 data validation: OK
```

## Prochaine étape

**Itération 2 — Carbon Engine : calcul reproductible AS-IS / TO-BE, hypothèses explicites et tests de cohérence.**

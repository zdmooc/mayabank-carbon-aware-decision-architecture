# Itération 6 — Data & Storage / consolidation / rétention

## Statut

**TERMINÉE — modèle stockage, tiers HOT/WARM/COLD, rétention, backup, consolidation DB et comparaison coût/carbone livrés.**

## Objectif

Étendre la démarche Carbon-Aware aux données et au stockage sans optimiser uniquement sur le coût ou le carbone.

```text
Data / DB / Storage inventory
          ↓
Criticité + RTO + rétention + usage DB
          ↓
Storage Assessment Engine
          ↓
Tier HOT / WARM / COLD
TTL / Retention / Backup
DB Consolidation Candidate
          ↓
Cost + Carbon + Risk
          ↓
KEEP / OPTIMIZE / REVIEW
```

Toutes les données, coefficients et coûts utilisés ici sont synthétiques.

## Principes

- les données critiques transactionnelles restent sur un tier compatible avec le RTO ;
- aucune réduction de rétention n’est appliquée à une donnée supposée réglementaire/audit sans règle explicite ;
- les environnements non-prod peuvent avoir des TTL plus courts ;
- les backups sont dimensionnés selon criticité et besoin de reprise ;
- une consolidation DB n’est recommandée que si l’utilisation synthétique est faible et si la criticité le permet ;
- carbone, coût, RTO et risque sont évalués ensemble.

## Coefficients v1

Les coefficients de coût et carbone sont **fictifs** et versionnés dans le moteur. Ils servent à tester la méthode :

- HOT : coût/carbone les plus élevés ;
- WARM : intermédiaire ;
- COLD : coût/carbone les plus faibles mais accès plus lent.

Aucun coefficient n’est présenté comme une valeur fournisseur réelle.

## Livrables

- `data/synthetic/storage-assets.csv` ;
- `storage/assess.py` ;
- `tests/test_storage_assessment.py` ;
- `architecture/data-storage-optimization.md`.

## Exécution

```bash
python storage/assess.py
python storage/assess.py --json
python -m unittest tests/test_storage_assessment.py
```

## Critères de sortie

- [x] inventaire synthétique DB/stockage ;
- [x] tiers HOT/WARM/COLD ;
- [x] rétention / TTL ;
- [x] backups ;
- [x] candidats à consolidation DB ;
- [x] garde-fous criticité/RTO ;
- [x] comparaison coût/carbone ;
- [x] recommandations explicables ;
- [x] aucune donnée d’entreprise réelle.

## Prochaine étape

**Itération 7 — AI / ML : prévision de charge, anomalies, prévision de consommation, ranking des candidats et confidence score.**

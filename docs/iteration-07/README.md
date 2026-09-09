# Itération 7 — AI / ML pour GreenOps

## Statut

**TERMINÉE — prévision de charge/consommation, anomalies, ranking, confiance et fallback livrés.**

## Objectif

Ajouter une couche AI/ML d’aide à l’optimisation sans lui donner l’autorité d’exécuter un changement d’infrastructure.

```text
Historical Metrics
 CPU / Power / Quality
        ↓
 AI / ML Engine
 forecast / anomaly / ranking
 confidenceScore
        ↓
 Candidate Recommendations
        ↓
 Future Decision Engine
 SLA / RTO / security / budget / criticality
        ↓
 Human approval / GitOps
```

## Fonctions v1

- prévision simple de CPU ;
- prévision de puissance ;
- estimation de consommation annuelle ;
- détection d’anomalie sur le dernier point ;
- ranking des candidats à optimisation ;
- `confidenceScore` ;
- fallback si historique insuffisant.

## Méthode de laboratoire

Le moteur est volontairement transparent et sans dépendance externe :

- tendance linéaire simple pour le prochain point ;
- statistique moyenne/écart-type pour l’anomalie ;
- score de ranking combinant sous-utilisation et puissance ;
- confiance dépendant du nombre de points et de la qualité des données.

Il ne s’agit pas d’un modèle de production ni d’un benchmark fournisseur.

## Règles de confiance

- 6 points de bonne qualité -> confiance élevée ;
- moins de 4 points -> `FALLBACK_INSUFFICIENT_HISTORY` ;
- une donnée de qualité dégradée réduit la confiance ;
- une anomalie ne doit pas être interprétée automatiquement comme opportunité de réduction.

## Livrables

- `data/synthetic/ml-workload-history.csv` ;
- `ai-ml/greenops_model.py` ;
- `tests/test_greenops_ml.py`.

## Exécution

```bash
python ai-ml/greenops_model.py
python ai-ml/greenops_model.py --json
python -m unittest tests/test_greenops_ml.py
```

## Gouvernance

Le moteur AI/ML fournit seulement des signaux :

- prévision ;
- anomalie ;
- score de priorité ;
- niveau de confiance.

Le futur Decision Engine devra encore vérifier SLA, RTO/RPO, criticité, sécurité, coûts, dépendances et qualité avant toute recommandation finale.

## Critères de sortie

- [x] prévision de charge ;
- [x] détection d’anomalie ;
- [x] prévision de consommation ;
- [x] ranking des candidats ;
- [x] confidence score ;
- [x] fallback sans historique suffisant ;
- [x] tests de non-régression ;
- [x] aucune exécution automatique d’un changement.

## Prochaine étape

**Itération 8 — Decision Engine : politiques Green IT, SLA/RTO/RPO/sécurité/budget/criticité et décisions gouvernées.**

# Itération 4 — Right-Sizing explicable

## Statut

**TERMINÉE — moteur de recommandation CPU/RAM, garde-fous criticité/SLA, contrôle de fraîcheur et tests livrés.**

## Objectif

Transformer les données d'observabilité de l'Itération 3 en recommandations de capacité prudentes et explicables.

```text
Inventory + Workload Summary + Data Quality
                    ↓
           Right-Sizing Engine
                    ↓
 Criticality Policy + Headroom + Max Reduction
                    ↓
      N+1 / Freshness / Quality Guardrails
                    ↓
 KEEP / RIGHTSIZE_DOWN / RIGHTSIZE_UP / REVIEW_DATA
```

## Principes

- utiliser des percentiles synthétiques de charge plutôt qu'une mesure instantanée seule ;
- ajouter une marge de sécurité dépendant de la criticité ;
- plafonner la réduction maximale ;
- ne jamais réduire automatiquement un actif sur donnée stale ou invalide ;
- signaler un besoin de capacité supplémentaire plutôt que masquer un risque de saturation ;
- exiger un garde-fou N+1 pour les actifs critiques de production.

## Livrables

- `data/synthetic/workload-summary.csv` ;
- `rightsizing/policies.csv` ;
- `rightsizing/recommend.py` ;
- `tests/test_rightsizing.py`.

## Exécution

```bash
python rightsizing/recommend.py
python rightsizing/recommend.py --json
python -m unittest tests/test_rightsizing.py
```

## Décisions v1

- `KEEP` : capacité cohérente avec la charge et les garde-fous ;
- `RIGHTSIZE_DOWN` : réduction possible dans les limites de sécurité ;
- `RIGHTSIZE_UP` : capacité cible supérieure à l'allocation courante ;
- `REVIEW_DATA` : qualité/fraîcheur insuffisante pour décider.

## Garde-fous

La recommandation est une **aide à la décision**, pas une exécution automatique. Le futur Decision Engine devra encore vérifier SLA, RTO/RPO, sécurité, dépendances et fenêtre de changement.

## Critères de sortie

- [x] sous-utilisation détectable ;
- [x] cible CPU/RAM calculée ;
- [x] marges selon criticité ;
- [x] réduction maximale contrôlée ;
- [x] N+1 exposé pour production critique ;
- [x] recommandation refusée si donnée stale/invalide ;
- [x] besoin de scale-up visible ;
- [x] explication et reason codes ;
- [x] tests de non-régression.

## Prochaine étape

**Itération 5 — Modernisation middleware vers OpenShift : modèle VM/JVM fictif, sizing pods/namespaces, stockage, HA et comparaison carbone/coût/risque.**

# Itération 8 — Decision Engine GreenOps

## Statut

**TERMINÉE — politiques Green IT, garde-fous SLA/RTO/RPO/sécurité/budget/criticité et décisions gouvernées livrés.**

## Objectif

Transformer les signaux des itérations précédentes en décisions d'architecture gouvernées et explicables.

```text
Observabilité / CMDB / Carbon Engine
Right-Sizing / Modernisation / Storage
AI-ML forecast / anomalies / ranking
                ↓
         Decision Engine
 policy / SLA / RTO-RPO / security
 budget / criticality / data quality
                ↓
 MIGRATE / RIGHTSIZE / CONSOLIDATE
 KEEP / RETIRE / REVIEW
                ↓
       Human approval / ITSM
```

## Principe d'architecture

**L'AI/ML propose ou priorise ; le Decision Engine applique les politiques ; l'humain approuve les changements sensibles.**

Le moteur reste vendor-neutral. IBM ODM est documenté comme option possible d'implémentation, mais aucune dépendance ODM n'est introduite dans ce dépôt.

## Garde-fous v1

Une recommandation devient `REVIEW` lorsque :

- qualité des données insuffisante ;
- confiance ML insuffisante pour un signal dépendant du ML ;
- contrainte sécurité ouverte ;
- budget non approuvé ;
- RTO/RPO incompatibles avec la cible ;
- criticité élevée avec risque non résolu ;
- dépendance bloquante non traitée.

## Décisions couvertes

- `MIGRATE` ;
- `RIGHTSIZE` ;
- `CONSOLIDATE` ;
- `KEEP` ;
- `RETIRE` ;
- `REVIEW`.

Aucune décision n'est auto-appliquée : `autoApplyAllowed=false`.

## Livrables

- `decision-engine/policies.json` ;
- `decision-engine/engine.py` ;
- `data/synthetic/decision-candidates.csv` ;
- `tests/test_decision_engine.py` ;
- `architecture/decision-engine.md` ;
- `architecture/decision-engine-implementation-options.md`.

## Exécution

```bash
python decision-engine/engine.py
python decision-engine/engine.py --json
python -m unittest tests/test_decision_engine.py
```

## Critères de sortie

- [x] politiques Green IT versionnées ;
- [x] SLA/RTO/RPO pris en compte ;
- [x] sécurité et budget pris en compte ;
- [x] criticité et qualité des données prises en compte ;
- [x] décisions MIGRATE/RIGHTSIZE/CONSOLIDATE/KEEP/RETIRE/REVIEW ;
- [x] règles explicables et reason codes ;
- [x] human review sur cas sensibles ;
- [x] IBM ODM évalué comme option sans dépendance obligatoire ;
- [x] aucune exécution automatique d'un changement.

## Prochaine étape

**Itération 9 — Optimisation multi-critères : carbone, coût, performance, risque, disponibilité et analyse Pareto.**

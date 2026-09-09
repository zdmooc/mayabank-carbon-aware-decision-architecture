# Itération 5 — Modernisation Middleware vers OpenShift

## Statut

**TERMINÉE — modèle AS-IS/TO-BE, sizing OpenShift, HA, stockage, comparaison carbone/coût/risque et décisions de migration livrés.**

## Objectif

Évaluer une modernisation fictive de workloads middleware VM/JVM vers OpenShift sans supposer qu'une migration est automatiquement bénéfique.

```text
AS-IS
VM / JVM / middleware
CPU / RAM / sessions / stockage / HA
              ↓
     Assessment Engine
              ↓
TO-BE OpenShift
Namespace / Pods / requests / limits
PDB / replicas / stockage / anti-affinity
              ↓
Carbone + coût + risque + résilience
              ↓
MIGRATE / KEEP / REVIEW
```

Toutes les données et coefficients sont synthétiques.

## Workloads fictifs

1. `payment-orchestrator` — production critique, stateless, bon candidat ;
2. `reconciliation-batch` — environnement non-prod, bon candidat ;
3. `legacy-session-service` — production avec état de session local, candidat conditionnel nécessitant une refonte/externalisation de session.

## Principes de sizing

La cible OpenShift décrit explicitement :

- namespace ;
- replicas minimum ;
- requests CPU/RAM ;
- limits CPU/RAM ;
- PodDisruptionBudget ;
- distribution multi-worker / anti-affinity pour les services critiques ;
- stratégie stockage ;
- dépendances bloquantes.

## Garde-fous

Une réduction de CPU/RAM n'est pas un objectif isolé. Le moteur doit également vérifier :

- criticité ;
- HA ;
- état de session ;
- persistance ;
- dépendances middleware ;
- observabilité ;
- capacité N+1 ;
- risque de migration.

Un workload avec état local ou dépendance non résolue retourne `REVIEW`, même si la cible semble meilleure en carbone ou en coût.

## Comparaison synthétique

Le calcul v1 compare :

- énergie opérationnelle modélisée ;
- émissions opérationnelles modélisées ;
- coût annuel synthétique ;
- score de risque de migration ;
- capacité HA cible.

Ces valeurs ne constituent ni un benchmark OpenShift, ni une mesure réelle d'un SI.

## Livrables

- `data/synthetic/middleware-source.csv` ;
- `data/synthetic/openshift-target.csv` ;
- `modernization/assess.py` ;
- `tests/test_modernization.py` ;
- `architecture/middleware-to-openshift.md`.

## Exécution

```bash
python modernization/assess.py
python modernization/assess.py --json
python -m unittest tests/test_modernization.py
```

## Critères de sortie

- [x] modèle VM/JVM fictif ;
- [x] modèle cible OpenShift ;
- [x] sizing pods/namespaces ;
- [x] stockage et état de session pris en compte ;
- [x] HA/PDB/replicas documentés ;
- [x] comparaison énergie/carbone/coût ;
- [x] score de risque synthétique ;
- [x] décision `MIGRATE / KEEP / REVIEW` explicable ;
- [x] aucune donnée d'entreprise réelle.

## Prochaine étape

**Itération 6 — Data & Storage : consolidation DB, tiers hot/warm/cold, rétention/TTL, backup et comparaison coût/carbone.**

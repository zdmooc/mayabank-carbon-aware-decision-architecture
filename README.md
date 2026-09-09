# MayaBank Carbon-Aware Decision Architecture

Référentiel d’architecture et laboratoire pédagogique pour concevoir une plateforme de **décision de décarbonation des infrastructures de paiement**, dans un contexte fictif et anonymisé.

## Positionnement

**Architecte Solution — Green IT / Carbon-Aware Architecture / AI / GreenOps — Payment Infrastructure**

Le dépôt montre comment relier :

```text
Infrastructure de paiement
  -> inventaire / CMDB / observabilité
  -> CPU / RAM / JVM / stockage / DB / énergie / coût
  -> Carbon Engine
  -> AI / ML pour prévoir et optimiser
  -> Decision Engine pour appliquer les politiques
  -> MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW
  -> OpenShift / Azure / ITSM / GitOps
```

## Cas d’usage fil rouge

Plateforme fictive **MayaBank Payment Platform** :

- modernisation middleware vers OpenShift ;
- right-sizing CPU/RAM ;
- rationalisation VM/JVM ;
- optimisation stockage et sauvegarde ;
- consolidation bases de données ;
- arrêt ou réduction des environnements non critiques ;
- comparaison de scénarios selon carbone, coût, performance, sécurité et résilience.

## Principe architectural

```text
Metrics / CMDB / Cost / Carbon Factors
            ↓
       Carbon Engine
            ↓
         AI / ML
 forecast / anomaly / ranking
            ↓
      Decision Engine
 policy / SLA / RTO-RPO / security
 budget / criticality / data quality
            ↓
MIGRATE / RIGHTSIZE / CONSOLIDATE
KEEP / RETIRE / REVIEW
            ↓
 Human approval / ITSM / GitOps
```

**L’AI/ML propose ou priorise ; le Decision Engine applique les politiques ; l’humain approuve les changements sensibles.**

## Carbon Engine v1

```bash
python carbon-engine/engine.py --scenario optimized
python -m unittest tests/test_carbon_engine.py
```

Les résultats sont entièrement synthétiques et servent uniquement à tester la méthode.

## Observabilité, Right-Sizing, Modernisation et Storage

```bash
python observability/normalize_metrics.py
python -m unittest tests/test_observability_pipeline.py
python rightsizing/recommend.py
python -m unittest tests/test_rightsizing.py
python modernization/assess.py
python -m unittest tests/test_modernization.py
python storage/assess.py
python -m unittest tests/test_storage_assessment.py
```

## AI / ML GreenOps v1

L’Itération 7 ajoute :

- forecast CPU/power ;
- estimation de consommation ;
- détection d’anomalies ;
- ranking des candidats ;
- `confidenceScore` ;
- fallback si historique insuffisant.

```bash
python ai-ml/greenops_model.py
python -m unittest tests/test_greenops_ml.py
```

L’AI/ML ne déclenche aucun changement.

## Decision Engine v1

L’Itération 8 ajoute un moteur de décision vendor-neutral qui vérifie :

- qualité des données ;
- confiance ML ;
- criticité ;
- SLA / RTO / RPO ;
- sécurité ;
- budget ;
- dépendances bloquantes.

Décisions :

- `MIGRATE` ;
- `RIGHTSIZE` ;
- `CONSOLIDATE` ;
- `KEEP` ;
- `RETIRE` ;
- `REVIEW`.

```bash
python decision-engine/engine.py
python decision-engine/engine.py --json
python -m unittest tests/test_decision_engine.py
```

Toutes les décisions exposent une version de politique et des reason codes. `autoApplyAllowed=false` : aucune décision n’est exécutée automatiquement.

IBM ODM est documenté comme **option d’implémentation possible**, sans dépendance obligatoire dans ce dépôt.

## Stratégie de déploiement

1. **OpenShift Local / CRC** — cible prioritaire des labs.
2. **Azure AKS** — cible Kubernetes Azure de référence.
3. **ARO** — option entreprise si OpenShift managé sur Azure est requis.

## Règles du dépôt

- aucun nom, chiffre ou architecture attribuable à une entreprise réelle ;
- données synthétiques uniquement ;
- distinguer mesure, calcul, hypothèse et prédiction ;
- ne jamais présenter un gain estimé comme une mesure réelle ;
- chaque recommandation doit expliquer ses critères ;
- aucune recommandation n’est auto-appliquée ;
- éviter tout fork fonctionnel entre OpenShift Local et Azure.

## État

- **I0 à I8 : TERMINÉES**
- **Prochaine : Itération 9 — Optimisation multi-critères**

Voir `docs/iteration-08/README.md`, `docs/00-roadmap.md` et `docs/BACKLOG.md`.

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

Plateforme fictive **MayaBank Payment Platform** : modernisation middleware, right-sizing, rationalisation VM/JVM, optimisation stockage/backup, consolidation DB et réduction raisonnée des environnements non critiques.

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
 SLA / RTO / security / budget
            ↓
MIGRATE / RIGHTSIZE / KEEP / REVIEW
```

Le moteur de décision reste **vendor-neutral**. IBM ODM pourra être évalué comme option d’implémentation sans transformer ce dépôt en second dépôt ODM.

## Carbon Engine v1

```bash
python carbon-engine/engine.py --scenario optimized
python carbon-engine/engine.py --scenario optimized --json
python -m unittest tests/test_carbon_engine.py
```

Résultats synthétiques du lab : énergie **−39.62 %**, émissions **−39.25 %**, coût annuel **−19.90 %**. Ils ne représentent aucune infrastructure réelle.

## Observabilité & qualité des données v1

```bash
python observability/normalize_metrics.py
python -m unittest tests/test_observability_pipeline.py
```

Une métrique stale, incomplète ou non corrélée ne doit jamais alimenter silencieusement une recommandation GreenOps.

## Right-Sizing v1

```bash
python rightsizing/recommend.py
python rightsizing/recommend.py --json
python -m unittest tests/test_rightsizing.py
```

Le moteur applique criticité, headroom, plafonds de réduction, capacité N+1 et blocage sur données insuffisantes.

## Modernisation middleware -> OpenShift v1

```bash
python modernization/assess.py
python modernization/assess.py --json
python -m unittest tests/test_modernization.py
```

Résultat logique : **2 candidats MIGRATE et 1 candidat REVIEW** tant que l’état de session local n’est pas externalisé.

## Data & Storage v1

```bash
python storage/assess.py
python storage/assess.py --json
python -m unittest tests/test_storage_assessment.py
```

Le ledger critique reste HOT ; les données historiques/non-prod peuvent être optimisées lorsque criticité et RTO le permettent.

## AI / ML GreenOps v1

L’Itération 7 ajoute :

- prévision CPU ;
- prévision puissance/consommation ;
- détection d’anomalies ;
- ranking des candidats à optimisation ;
- `confidenceScore` ;
- fallback si historique insuffisant.

```bash
python ai-ml/greenops_model.py
python ai-ml/greenops_model.py --json
python -m unittest tests/test_greenops_ml.py
```

Dans le dataset synthétique, l’UAT sous-utilisée remonte en tête du ranking, un pic PROD est marqué `ANOMALY_REVIEW`, et un historique trop court passe en `FALLBACK_INSUFFICIENT_HISTORY`.

Principe : **l’AI/ML fournit des signaux ; elle n’autorise ni n’exécute seule un changement d’infrastructure.**

## Stratégie de déploiement

1. **OpenShift Local / CRC — cible prioritaire des labs** ;
2. **Azure AKS — cible Kubernetes cloud de référence** ;
3. **ARO — option OpenShift managé entreprise**.

Principe : une seule logique fonctionnelle/décisionnelle, avec adaptations de plateforme via manifests/overlays/IaC.

## Règles du dépôt

- aucun nom, chiffre ou architecture interne attribuable à une entreprise réelle ;
- données synthétiques uniquement ;
- distinguer mesure, calcul, hypothèse et prédiction ;
- ne jamais présenter un gain estimé comme une mesure réelle ;
- aucune recommandation n’est auto-appliquée.

## État

- **I0 : TERMINÉE**
- **I1 : TERMINÉE**
- **I2 : TERMINÉE**
- **I3 : TERMINÉE**
- **I4 : TERMINÉE**
- **I5 : TERMINÉE**
- **I6 : TERMINÉE**
- **I7 : TERMINÉE**
- **Prochaine : Itération 8 — Decision Engine**

Voir `docs/iteration-07/README.md`.

## Roadmap

Voir `docs/00-roadmap.md` et `docs/BACKLOG.md`.

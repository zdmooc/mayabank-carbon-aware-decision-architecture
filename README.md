# MayaBank Carbon-Aware Decision Architecture

Référentiel d’architecture et laboratoire pédagogique pour concevoir une plateforme de **décision de décarbonation des infrastructures de paiement**, dans un contexte fictif et anonymisé.

## Positionnement

**Architecte Solution — Green IT / Carbon-Aware Architecture / AI / GreenOps — Payment Infrastructure**

Le dépôt relie :

```text
Infrastructure / CMDB / observabilité
  -> Carbon Engine
  -> Right-Sizing / Modernisation / Storage
  -> AI / ML
  -> Decision Engine
  -> Optimisation multi-critères / Pareto
  -> API / Event-Driven
  -> OpenShift / Azure / GitOps / ITSM
```

## Principe architectural

**L’AI/ML prévoit et priorise ; le Decision Engine applique les contraintes dures ; l’optimisation multi-critères compare les options éligibles ; l’humain approuve les changements sensibles.**

## Cas d’usage fil rouge

Plateforme fictive **MayaBank Payment Platform** :

- modernisation middleware vers OpenShift ;
- right-sizing CPU/RAM ;
- rationalisation VM/JVM ;
- optimisation stockage et sauvegarde ;
- consolidation bases de données ;
- réduction des environnements non critiques ;
- comparaison de scénarios carbone/coût/performance/risque/disponibilité.

## Modules livrés

### I2 — Carbon Engine

```bash
python carbon-engine/engine.py --scenario optimized
python -m unittest tests/test_carbon_engine.py
```

### I3–I6 — Observabilité / Right-Sizing / Modernisation / Storage

```bash
python observability/normalize_metrics.py
python rightsizing/recommend.py
python modernization/assess.py
python storage/assess.py
```

### I7 — AI / ML GreenOps

- forecast CPU/power ;
- consommation ;
- anomalies ;
- ranking ;
- `confidenceScore` ;
- fallback.

### I8 — Decision Engine

Le moteur vérifie :

- qualité des données ;
- confiance ML ;
- criticité ;
- SLA / RTO / RPO ;
- sécurité ;
- budget ;
- dépendances bloquantes.

Décisions : `MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW`.

`autoApplyAllowed=false` pour toutes les décisions.

### I9 — Optimisation multi-critères

L’Itération 9 ajoute :

- carbone ;
- coût ;
- performance ;
- disponibilité ;
- risque ;
- contraintes dures séparées des préférences ;
- front de Pareto ;
- profil de poids versionné ;
- recommandation pondérée ;
- conservation des alternatives non dominées.

```bash
python optimization/pareto.py
python optimization/pareto.py --json
python -m unittest tests/test_multicriteria.py
```

Le scénario synthétique recommande `OPT-MIGRATE` selon le profil de lab, tout en conservant `KEEP`, `RIGHTSIZE` et `SERVERLESS` comme alternatives Pareto. L’option agressive est détectée comme dominée et une option non éligible est exclue avant scoring.

Principe : **un bon score carbone ne peut jamais contourner une contrainte de sécurité, SLA, RTO/RPO ou policy.**

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
- aucun hard gate ne peut être compensé par une pondération ;
- aucune recommandation n’est auto-appliquée ;
- éviter tout fork fonctionnel entre OpenShift Local et Azure.

## État

- **I0 à I9 : TERMINÉES**
- **Prochaine : Itération 10 — API & Event-Driven**

Voir `docs/iteration-09/README.md`, `docs/00-roadmap.md` et `docs/BACKLOG.md`.

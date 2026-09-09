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
- comparaison de scénarios d’architecture selon carbone, coût, performance, sécurité et résilience.

## Principe architectural

L’AI cherche, prévoit et optimise. Le Decision Engine vérifie les contraintes de l’entreprise.

```text
Metrics / CMDB / Cost / Carbon Factors
            |
            v
       Carbon Engine
            |
            +----> AI / ML
            |      prediction / anomaly / optimization
            |
            v
      Decision Engine
  policy / SLA / RTO / security / budget
            |
            v
MIGRATE / RIGHTSIZE / KEEP / REVIEW
```

Le moteur de décision reste **vendor-neutral** dans ce dépôt. IBM ODM pourra être évalué comme une implémentation possible, sans transformer ce dépôt en second dépôt ODM.

## Carbon Engine v1

L’Itération 2 fournit un moteur reproductible, sans dépendance externe, qui compare des scénarios synthétiques `BASELINE` et `OPTIMIZED`.

```bash
python carbon-engine/engine.py --scenario optimized
python carbon-engine/engine.py --scenario optimized --json
python -m unittest tests/test_carbon_engine.py
```

Résultats de laboratoire actuellement verrouillés par les tests :

- énergie : **−39.62 %** ;
- émissions opérationnelles synthétiques : **−39.25 %** ;
- coût annuel synthétique : **−19.90 %**.

Ces valeurs servent uniquement à valider la méthode et ne représentent aucune infrastructure réelle.

## Observabilité & qualité des données v1

L’Itération 3 ajoute une chaîne d’ingestion synthétique avec :

- corrélation `asset -> application -> environnement` ;
- CPU / RAM / JVM heap / power ;
- contrôle de fraîcheur ;
- signalement des données manquantes ;
- quarantaine des actifs inconnus ;
- statuts de qualité et warnings explicites.

```bash
python observability/normalize_metrics.py
python -m unittest tests/test_observability_pipeline.py
```

Principe : **une métrique stale, incomplète ou non corrélée ne doit jamais alimenter silencieusement une recommandation GreenOps.**

## Stratégie de déploiement

Le projet doit être exécutable sur deux cibles complémentaires :

1. **OpenShift Local / CRC — cible prioritaire des labs locaux**
   - déployer Carbon Engine, API, AI/ML, Decision Engine et observabilité ;
   - expérimenter le right-sizing, les workloads conteneurisés, GitOps et les politiques GreenOps ;
   - conserver des preuves reproductibles avant de déclarer un lab exécuté.

2. **Azure — cible cloud alternative**
   - **AKS** comme cible Kubernetes Azure de référence pour les labs cloud ;
   - **ARO** comme option entreprise lorsqu’une cible OpenShift managée sur Azure est requise ;
   - intégrer progressivement Azure Monitor / Log Analytics / Cost Management et les sources de données utiles aux scénarios carbone ;
   - détruire les ressources de lab coûteuses après validation lorsque cela est possible.

Principe : **concevoir une seule architecture fonctionnelle et décisionnelle, avec des déploiements adaptés à Local/CRC et Azure**.

## Règles du dépôt

- aucun nom, donnée, architecture interne ou chiffre attribuable à une entreprise réelle ;
- tous les scénarios utilisent **MayaBank Payment Platform** ;
- données de démonstration synthétiques uniquement ;
- distinguer mesure, calcul, hypothèse et prédiction ;
- ne jamais présenter un gain carbone estimé comme une mesure réelle ;
- chaque recommandation doit pouvoir expliquer ses critères ;
- chaque itération doit être récupérable, documentée et testable indépendamment ;
- éviter tout fork fonctionnel entre OpenShift Local et Azure.

## État

- **Itération 0 — Initialisation et cadrage : TERMINÉE**
- **Itération 1 — Modèle de données Carbon & Infrastructure : TERMINÉE**
- **Itération 2 — Carbon Engine AS-IS / TO-BE : TERMINÉE**
- **Itération 3 — Observabilité, inventaire et qualité des données : TERMINÉE**
- **Prochaine : Itération 4 — Right-Sizing**

Voir `docs/iteration-03/README.md`.

## Validation I1

```bash
python tools/validate_iteration_01.py
```

## Roadmap

Voir `docs/00-roadmap.md` et `docs/BACKLOG.md`.

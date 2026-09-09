# Roadmap — Carbon-Aware Decision Architecture

## Objectif global

Construire progressivement une architecture de décision pour réduire l’empreinte carbone d’une infrastructure de paiement tout en respectant coût, performance, sécurité, criticité et résilience, avec une trajectoire de déploiement **OpenShift Local / CRC -> Azure**.

## Stratégie de déploiement transverse

- **OpenShift Local / CRC** : cible prioritaire des labs et validations locales.
- **Azure AKS** : cible cloud Kubernetes de référence.
- **Azure Red Hat OpenShift (ARO)** : option entreprise lorsque le besoin impose OpenShift managé sur Azure.
- Même logique Carbon/AI/Decision entre local et cloud.
- Différences de plateforme gérées par manifests, Helm/Kustomize, overlays et IaC.
- Les ressources Azure de lab doivent être arrêtées ou détruites après validation lorsque cela est possible.

## Itérations

### Itération 0 — Cadrage et gouvernance — TERMINÉE
- périmètre fictif MayaBank Payment Platform ;
- anonymisation ;
- séparation mesures / calculs / hypothèses / prédictions ;
- rôle AI / Decision Engine ;
- NFR ;
- stratégie CRC -> Azure.

### Itération 1 — Modèle de données Carbon & Infra — TERMINÉE
- application, environnement, serveur, VM, JVM, pod, cluster ;
- CPU, RAM, stockage, backup, DB ;
- énergie, facteurs carbone et coût ;
- criticité / RTO / RPO ;
- provenance et qualité des données ;
- dataset synthétique et validateur.

### Itération 2 — Carbon Engine AS-IS / TO-BE — TERMINÉE
- moteur de calcul reproductible ;
- hypothèses explicites ;
- scénarios BASELINE / OPTIMIZED ;
- énergie / kgCO2e / coût ;
- tests de non-régression ;
- comparaison documentée.

### Itération 3 — Observabilité & CMDB
- ingestion métriques CPU/RAM/JVM ;
- inventaire ;
- normalisation ;
- corrélation application-infrastructure ;
- qualité et fraîcheur des données.

### Itération 4 — Right-Sizing
- sous-utilisation ;
- requests/limits ;
- capacité N+1 ;
- scénarios de réduction CPU/RAM ;
- garde-fous de performance.

### Itération 5 — Modernisation Middleware -> OpenShift
- scénario VM/WebSphere-like vers conteneurs/OpenShift ;
- sizing ;
- dépendances ;
- stockage ;
- HA ;
- comparaison carbone/coût/risque.

### Itération 6 — Data & Storage
- consolidation DB ;
- stockage chaud/froid ;
- rétention ;
- backup ;
- coût et carbone.

### Itération 7 — AI / ML
- prévision de charge ;
- détection d’anomalies ;
- prévision de consommation ;
- classement des candidats à optimisation ;
- confiance et limites du modèle.

### Itération 8 — Decision Engine
- politiques Green IT ;
- SLA ;
- RTO/RPO ;
- sécurité ;
- budget ;
- criticité ;
- MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW.

### Itération 9 — Optimisation multi-critères
- carbone ;
- coût ;
- performance ;
- risque ;
- disponibilité ;
- arbitrage Pareto et recommandations explicables.

### Itération 10 — API & Event-Driven
- exposition des recommandations ;
- OpenAPI ;
- événements de décision ;
- audit et corrélation.

### Itération 11 — Déploiement OpenShift Local / CRC
- déploiement Carbon Engine, API, AI/ML et Decision Engine ;
- Services / Routes ;
- ConfigMaps / Secrets ;
- requests/limits, quotas et policies ;
- observabilité locale ;
- GitOps ;
- validation E2E avec données synthétiques et preuves.

### Itération 12 — Azure / GreenOps cloud
- portage vers AKS ;
- ARO documenté comme alternative OpenShift managée ;
- Azure Monitor / Log Analytics ;
- Cost Management et sources de métriques utiles ;
- IaC et destruction contrôlée des ressources de lab ;
- comparaison de parité fonctionnelle et de coûts Local/CRC vs Azure.

### Itération 13 — GitOps / ITSM
- recommandation -> changement contrôlé ;
- approbation humaine ;
- overlays local/Azure ;
- rollback ;
- preuves avant/après.

### Itération 14 — Observabilité carbone & FinOps
- dashboards ;
- indicateurs ;
- SLI/SLO ;
- budget carbone ;
- coût ;
- dérive.

### Itération 15 — Gouvernance / sécurité / audit
- traçabilité ;
- qualité des données ;
- séparation recommandation/exécution ;
- contrôles et responsabilités.

### Itération 16 — Soutenance Architecte Solution
- HLD ;
- ADR ;
- matrice de scénarios ;
- risques ;
- trajectoire ;
- comparaison OpenShift Local / AKS / ARO ;
- démonstration anonymisée.

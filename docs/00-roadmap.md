# Roadmap — Carbon-Aware Decision Architecture

## Objectif global

Construire progressivement une architecture de décision pour réduire l’empreinte carbone d’une infrastructure de paiement tout en respectant coût, performance, sécurité, criticité et résilience.

## Itérations

### Itération 0 — Cadrage et gouvernance
Statut : **TERMINÉE**

- définir le périmètre fictif MayaBank Payment Platform ;
- fixer les règles d’anonymisation ;
- distinguer mesures, calculs, hypothèses et prédictions ;
- définir le rôle de l’AI et du Decision Engine ;
- définir les NFR et critères de décision ;
- créer la roadmap.

### Itération 1 — Modèle de données Carbon & Infra
- application, environnement, serveur, VM, JVM, pod, cluster ;
- CPU, RAM, stockage, backup, DB ;
- consommation énergétique et facteurs carbone ;
- coût et criticité ;
- provenance et qualité des données.

### Itération 2 — Carbon Engine
- calculs reproductibles ;
- hypothèses explicites ;
- scénarios AS-IS / TO-BE ;
- tests de cohérence ;
- comparaison d’architectures.

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

### Itération 11 — OpenShift / Cloud / GreenOps
- intégration avec workloads ;
- scheduling ;
- scaling ;
- arrêt non-prod ;
- politiques d’exploitation.

### Itération 12 — GitOps / ITSM
- recommandation -> changement contrôlé ;
- approbation humaine ;
- GitOps ;
- rollback ;
- preuves avant/après.

### Itération 13 — Observabilité carbone & FinOps
- dashboards ;
- indicateurs ;
- SLI/SLO ;
- budget carbone ;
- coût ;
- dérive.

### Itération 14 — Gouvernance / sécurité / audit
- traçabilité ;
- qualité des données ;
- séparation recommandation/exécution ;
- contrôles et responsabilités.

### Itération 15 — Soutenance Architecte Solution
- HLD ;
- ADR ;
- matrice de scénarios ;
- risques ;
- trajectoire ;
- démonstration anonymisée.

# Roadmap — Carbon-Aware Decision Architecture

## Objectif global

Construire progressivement une architecture de décision pour réduire l’empreinte carbone d’une infrastructure de paiement tout en respectant coût, performance, sécurité, criticité et résilience, avec une trajectoire **OpenShift Local / CRC -> Azure**.

## Stratégie de déploiement transverse

- **OpenShift Local / CRC** : cible prioritaire des labs.
- **Azure AKS** : cible cloud Kubernetes de référence.
- **ARO** : option entreprise si OpenShift managé sur Azure est requis.
- Même logique Carbon/AI/Decision entre local et cloud.
- Aucun gain réel ni lab exécuté n’est revendiqué sans preuve.

## Itérations

### I0 — Cadrage et gouvernance — TERMINÉE
Périmètre fictif, anonymisation, séparation mesures/calculs/hypothèses/prédictions, NFR et stratégie CRC -> Azure.

### I1 — Modèle de données Carbon & Infra — TERMINÉE
Applications, environnements, compute, CPU/RAM/stockage/backup/DB, énergie, facteurs carbone, coût, criticité, RTO/RPO et provenance.

### I2 — Carbon Engine AS-IS / TO-BE — TERMINÉE
Calcul reproductible, hypothèses explicites, scénarios BASELINE/OPTIMIZED, énergie/kgCO2e/coût et tests.

### I3 — Observabilité & CMDB — TERMINÉE
Ingestion CPU/RAM/JVM, inventaire, normalisation, corrélation, fraîcheur et qualité.

### I4 — Right-Sizing — TERMINÉE
Sous-utilisation, cibles CPU/RAM, N+1, plafonds de réduction, garde-fous et recommandations explicables.

### I5 — Modernisation Middleware -> OpenShift — TERMINÉE
AS-IS VM/JVM, cible pods/namespaces, stockage, dépendances, HA/PDB, comparaison carbone/coût/risque et décisions MIGRATE/REVIEW.

### I6 — Data & Storage — TERMINÉE
Consolidation DB, HOT/WARM/COLD, rétention/TTL, backup, RTO/criticité et comparaison coût/carbone.

### I7 — AI / ML — TERMINÉE
Forecast de charge/consommation, anomalies, ranking, `confidenceScore` et fallback.

### I8 — Decision Engine — TERMINÉE
Politiques Green IT, qualité/confiance, SLA/RTO-RPO, sécurité, budget, criticité, dépendances et décisions gouvernées `MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW`.

### I9 — Optimisation multi-critères
- carbone ;
- coût ;
- performance ;
- risque ;
- disponibilité ;
- analyse Pareto ;
- explication du compromis retenu.

### I10 — API & Event-Driven
Recommendation API, OpenAPI, événements `RecommendationGenerated / DecisionApproved / ChangeApplied`, AsyncAPI, correlation ID et audit.

### I11 — OpenShift Local / CRC
Déploiement Carbon Engine, API, AI/ML et Decision Engine ; Services/Routes ; ConfigMaps/Secrets ; requests/limits/quotas/NetworkPolicy ; observabilité ; GitOps ; test E2E.

### I12 — Azure / GreenOps cloud
Portage AKS, ARO documenté, IaC, Azure Monitor/Log Analytics, Cost Management, identité/réseau/secrets, parité CRC/Azure et destroy contrôlé.

### I13 — GitOps / ITSM
Recommandation -> changement contrôlé, approbation humaine, Argo CD, overlays local/Azure, rollback et preuves avant/après.

### I14 — Observabilité carbone & FinOps
Dashboards carbone/coût, SLI/SLO, budget carbone, dérive/anomalies et historique des décisions.

### I15 — Gouvernance / sécurité / audit
Data lineage, traçabilité décision, séparation recommandation/exécution, IAM/RBAC, threat model et contrôles.

### I16 — Soutenance Architecte Solution
HLD, ADR, matrice AS-IS/scénarios/TO-BE, risques, arbitrages, diagrammes, démonstration et entretien.

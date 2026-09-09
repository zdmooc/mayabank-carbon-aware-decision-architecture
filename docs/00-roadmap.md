# Roadmap — Carbon-Aware Decision Architecture

## Objectif global

Construire progressivement une architecture de décision pour réduire l’empreinte carbone d’une infrastructure de paiement tout en respectant coût, performance, sécurité, criticité et résilience, avec une trajectoire de déploiement **OpenShift Local / CRC -> Azure**.

## Stratégie de déploiement transverse

- **OpenShift Local / CRC** : cible prioritaire des labs et validations locales.
- **Azure AKS** : cible cloud Kubernetes de référence.
- **Azure Red Hat OpenShift (ARO)** : option entreprise lorsque le besoin impose OpenShift managé sur Azure.
- Même logique Carbon/AI/Decision entre local et cloud.
- Différences de plateforme gérées par manifests, Helm/Kustomize, overlays et IaC.

## Itérations

### Itération 0 — Cadrage et gouvernance — TERMINÉE
- périmètre fictif ; anonymisation ; séparation mesures/calculs/hypothèses/prédictions ; NFR ; stratégie CRC -> Azure.

### Itération 1 — Modèle de données Carbon & Infra — TERMINÉE
- application/environnement/actifs ; CPU/RAM/stockage/DB ; énergie/facteurs carbone/coût ; criticité/RTO/RPO ; provenance/qualité.

### Itération 2 — Carbon Engine AS-IS / TO-BE — TERMINÉE
- calcul reproductible ; hypothèses explicites ; scénarios ; énergie/kgCO2e/coût ; tests.

### Itération 3 — Observabilité & CMDB — TERMINÉE
- ingestion CPU/RAM/JVM ; inventaire ; normalisation ; corrélation application-infrastructure ; qualité/fraîcheur.

### Itération 4 — Right-Sizing — TERMINÉE
- cibles CPU/RAM ; capacité N+1 ; plafonds de réduction ; garde-fous ; recommandations explicables.

### Itération 5 — Modernisation Middleware -> OpenShift — TERMINÉE
- AS-IS VM/JVM ; cible OpenShift ; dépendances ; stockage ; HA/PDB ; énergie/carbone/coût/risque ; MIGRATE/REVIEW.

### Itération 6 — Data & Storage — TERMINÉE
- consolidation DB ; HOT/WARM/COLD ; rétention/TTL ; backup ; garde-fous criticité/RTO ; coût/carbone.

### Itération 7 — AI / ML — TERMINÉE
- prévision de charge ; détection d’anomalies ; prévision de consommation ; ranking ; confidence score ; fallback sur historique insuffisant ; aucune exécution automatique.

### Itération 8 — Decision Engine
- politiques Green IT ;
- SLA ;
- RTO/RPO ;
- sécurité ;
- budget ;
- criticité ;
- règles versionnées ;
- MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW ;
- human review ;
- IBM ODM évalué comme option sans dépendance obligatoire.

### Itération 9 — Optimisation multi-critères
- carbone ; coût ; performance ; risque ; disponibilité ; Pareto ; explication du compromis.

### Itération 10 — API & Event-Driven
- Recommendation API ; OpenAPI ; événements ; AsyncAPI ; correlation ID ; audit.

### Itération 11 — Déploiement OpenShift Local / CRC
- Carbon Engine ; API ; AI/ML ; Decision Engine ; Services/Routes ; ConfigMaps/Secrets ; quotas/policies ; observabilité ; GitOps ; E2E.

### Itération 12 — Azure / GreenOps cloud
- AKS ; ARO alternatif ; Azure Monitor/Log Analytics ; Cost Management ; identité/réseau/secrets ; IaC ; destroy ; parité fonctionnelle.

### Itération 13 — GitOps / ITSM
- recommandation -> changement contrôlé ; approbation humaine ; Argo CD ; overlays ; rollback ; preuves avant/après.

### Itération 14 — Observabilité carbone & FinOps
- dashboards ; SLI/SLO ; budget carbone ; coût ; dérive ; historique des décisions.

### Itération 15 — Gouvernance / sécurité / audit
- lineage ; traçabilité ; séparation recommandation/exécution ; IAM/RBAC ; threat model ; contrôles.

### Itération 16 — Soutenance Architecte Solution
- HLD ; ADR ; matrice scénarios ; risques ; trajectoire ; comparaison CRC/AKS/ARO ; démonstration.

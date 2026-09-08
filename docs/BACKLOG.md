# Backlog — Carbon-Aware Decision Architecture / Infrastructure Paiement

## Objectif
Construire un POC démontrable de décision de décarbonation d’une infrastructure de paiement, combinant données infra, Carbon Engine, AI/ML, Decision Engine, OpenShift Local/CRC puis Azure.

## Priorités
- **P0** : indispensable au fil rouge et à la démonstration.
- **P1** : industrialisation et intégration.
- **P2** : approfondissement expert / entretien.

## Backlog par itération

### I0 — Cadrage et gouvernance — DONE
- [x] Contexte fictif MayaBank Payment Platform
- [x] Anonymisation et données synthétiques uniquement
- [x] Séparation Carbon Engine / AI / Decision Engine / humain
- [x] Architecture logique initiale
- [x] Roadmap
- [x] Cible OpenShift Local/CRC puis Azure AKS/ARO

### I1 — Modèle de données Carbon & Infra — P0
- [ ] Modéliser application / environnement / serveur / VM / JVM / pod / cluster
- [ ] CPU / RAM / stockage / backup / DB
- [ ] Énergie / facteur carbone / coût
- [ ] Criticité / SLA / RTO / RPO
- [ ] Provenance et fraîcheur des données
- [ ] Jeu de données synthétique versionné

**DoD** : un dataset synthétique complet permet de calculer au moins deux scénarios d’architecture.

### I2 — Carbon Engine — P0
- [ ] Calcul d’empreinte reproductible
- [ ] Facteurs carbone explicites
- [ ] Distinction mesure / calcul / hypothèse
- [ ] AS-IS / TO-BE
- [ ] Tests unitaires
- [ ] Rapport de comparaison

### I3 — Observabilité & inventaire — P0
- [ ] Ingestion métriques CPU/RAM/JVM
- [ ] Inventaire applicatif et infra
- [ ] Corrélation application -> infrastructure
- [ ] Gestion données manquantes
- [ ] Qualité / fraîcheur / source

### I4 — Right-Sizing — P0
- [ ] Détecter sous-utilisation
- [ ] Requests / limits cibles
- [ ] N+1 et garde-fous
- [ ] Comparer avant/après
- [ ] Refuser optimisation si SLA menacé
- [ ] Produire recommandation explicable

### I5 — Modernisation Middleware -> OpenShift — P0
- [ ] Modèle VM/WebSphere-like fictif
- [ ] Modèle cible conteneurs/OpenShift
- [ ] CPU/RAM/JVM -> pods/namespaces
- [ ] Stockage et dépendances
- [ ] HA
- [ ] Comparaison carbone / coût / risque
- [ ] Décision MIGRATE / KEEP / REVIEW

### I6 — Data & Storage — P1
- [ ] Consolidation DB
- [ ] Stockage hot/warm/cold
- [ ] Rétention / TTL
- [ ] Backup
- [ ] Comparaison coût / carbone

### I7 — AI / ML — P0
- [ ] Prévision de charge
- [ ] Détection d’anomalies
- [ ] Prévision de consommation
- [ ] Ranking des candidats à optimisation
- [ ] Confidence score
- [ ] Fallback sans modèle

### I8 — Decision Engine — P0
- [ ] Politiques Green IT
- [ ] Critères SLA / RTO/RPO / sécurité / budget / criticité
- [ ] Décisions MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW
- [ ] Règles versionnées
- [ ] Human review sur cas sensibles
- [ ] IBM ODM évalué comme option, sans dépendance obligatoire

### I9 — Optimisation multi-critères — P1
- [ ] Carbone
- [ ] Coût
- [ ] Performance
- [ ] Risque
- [ ] Disponibilité
- [ ] Analyse Pareto
- [ ] Explication du compromis retenu

### I10 — API & Event-Driven — P1
- [ ] Recommendation API
- [ ] OpenAPI
- [ ] Événements RecommendationGenerated / DecisionApproved / ChangeApplied
- [ ] AsyncAPI
- [ ] Correlation ID
- [ ] Audit

### I11 — OpenShift Local / CRC — P0
- [ ] Déployer Carbon Engine
- [ ] Déployer API
- [ ] Déployer AI/ML
- [ ] Déployer Decision Engine
- [ ] Services / Routes
- [ ] ConfigMaps / Secrets
- [ ] Requests / limits / quotas / NetworkPolicy
- [ ] Observabilité locale
- [ ] GitOps
- [ ] Test E2E automatisé

**DoD** : un scénario synthétique complet produit une décision explicable de bout en bout sur CRC.

### I12 — Azure / GreenOps Cloud — P1
- [ ] Portage AKS
- [ ] ARO documenté comme alternative
- [ ] IaC
- [ ] Azure Monitor / Log Analytics
- [ ] Cost Management
- [ ] Registry / identité / réseau / secrets
- [ ] Parité fonctionnelle avec CRC
- [ ] Destroy contrôlé des ressources de lab

### I13 — GitOps / ITSM — P1
- [ ] Recommandation -> changement contrôlé
- [ ] Human approval
- [ ] Argo CD
- [ ] Overlays local/Azure
- [ ] Rollback
- [ ] Preuve avant/après

### I14 — Observabilité carbone & FinOps — P1
- [ ] Dashboard carbone
- [ ] Dashboard coût
- [ ] SLI/SLO
- [ ] Budget carbone
- [ ] Dérive / anomalies
- [ ] Historique des décisions

### I15 — Gouvernance / sécurité / audit — P2
- [ ] Data lineage
- [ ] Traçabilité décision
- [ ] Séparation recommandation/exécution
- [ ] IAM / RBAC
- [ ] Threat model
- [ ] Contrôles / responsabilités

### I16 — Soutenance Architecte Solution — P2
- [ ] HLD
- [ ] ADR majeurs
- [ ] Matrice AS-IS / scénarios / TO-BE
- [ ] Risques et arbitrages
- [ ] Diagrammes finaux
- [ ] Demo script
- [ ] Questions/réponses entretien

## 3 passes de revue finale

### Revue R1 — Cohérence architecture
- [ ] Data / Carbon / AI / Decision / Human clairement séparés
- [ ] API / Event / Platform cohérents
- [ ] Aucun chiffre ou nom client réel
- [ ] Pas de doublon inutile avec les autres dépôts

### Revue R2 — Exécutabilité
- [ ] `git clone` propre
- [ ] Dataset synthétique fourni
- [ ] Calculs reproductibles
- [ ] Déploiement CRC reproductible
- [ ] Tests E2E verts
- [ ] GitOps opérationnel
- [ ] Portabilité Azure vérifiée

### Revue R3 — Niveau Architecte Solution
- [ ] HLD/ADR/NFR complets
- [ ] Sécurité/HA/PRA/observabilité/GreenOps traités
- [ ] Hypothèses et limites explicites
- [ ] README orienté recruteur/architecte
- [ ] Démo de 10–15 min
- [ ] Aucun gain carbone présenté comme réel sans preuve

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

### I1 — Modèle de données Carbon & Infra — DONE
- [x] Modéliser application / environnement / serveur / VM / JVM / pod / cluster
- [x] CPU / RAM / stockage / backup / DB
- [x] Énergie / facteur carbone / coût
- [x] Criticité / SLA / RTO / RPO
- [x] Provenance et fraîcheur des données
- [x] Jeu de données synthétique versionné

**DoD atteint** : modèle et dataset synthétiques versionnés, avec inventaire, métriques, facteurs carbone, coûts, diagramme de données et validateur `python tools/validate_iteration_01.py`.

### I2 — Carbon Engine — DONE
- [x] Calcul d’empreinte reproductible
- [x] Facteurs carbone explicites
- [x] Distinction mesure / calcul / hypothèse
- [x] AS-IS / TO-BE
- [x] Tests unitaires
- [x] Rapport de comparaison

**DoD atteint** : moteur sans dépendance externe, scénarios `baseline.csv` et `optimized.csv`, hypothèses versionnées, tests de non-régression et comparaison énergie / kgCO2e / coût. Les résultats sont synthétiques et ne représentent aucun environnement réel.

### I3 — Observabilité & inventaire — DONE
- [x] Ingestion métriques CPU/RAM/JVM
- [x] Inventaire applicatif et infra
- [x] Corrélation application -> infrastructure
- [x] Gestion données manquantes
- [x] Qualité / fraîcheur / source

**DoD atteint** : flux synthétique d’observabilité, corrélation asset/application, fraîcheur, complétude, warnings, quarantaine des actifs inconnus et tests `python -m unittest tests/test_observability_pipeline.py`.

### I4 — Right-Sizing — DONE
- [x] Détecter sous-utilisation
- [x] Requests / limits cibles
- [x] N+1 et garde-fous
- [x] Comparer avant/après
- [x] Refuser optimisation si SLA/qualité menacé
- [x] Produire recommandation explicable

**DoD atteint** : moteur `rightsizing/recommend.py`, politiques par criticité, charges p95 synthétiques, plafonds de réduction, garde-fou N+1, blocage sur données stale et tests `python -m unittest tests/test_rightsizing.py`. Aucune recommandation n’est auto-appliquée.

### I5 — Modernisation Middleware -> OpenShift — DONE
- [x] Modèle VM/WebSphere-like fictif
- [x] Modèle cible conteneurs/OpenShift
- [x] CPU/RAM/JVM -> pods/namespaces
- [x] Stockage et dépendances
- [x] HA
- [x] Comparaison carbone / coût / risque
- [x] Décision MIGRATE / KEEP / REVIEW

**DoD atteint** : modèle AS-IS VM/JVM, cible OpenShift avec namespaces/replicas/requests/limits/PDB, prise en compte du stockage et de l’état de session, assessment synthétique énergie/carbone/coût/risque et décisions explicables. Deux workloads de lab sont `MIGRATE`, un reste `REVIEW` tant que son état de session n’est pas externalisé.

### I6 — Data & Storage — DONE
- [x] Consolidation DB
- [x] Stockage hot/warm/cold
- [x] Rétention / TTL
- [x] Backup
- [x] Comparaison coût / carbone

**DoD atteint** : inventaire DB/stockage synthétique, politiques HOT/WARM/COLD, rétention/TTL, backups, candidats de consolidation DB, moteur `storage/assess.py`, garde-fous criticité/RTO et tests `python -m unittest tests/test_storage_assessment.py`. Les coefficients coût/carbone sont fictifs et aucune recommandation n’est auto-appliquée.

### I7 — AI / ML — DONE
- [x] Prévision de charge
- [x] Détection d’anomalies
- [x] Prévision de consommation
- [x] Ranking des candidats à optimisation
- [x] Confidence score
- [x] Fallback sans modèle

**DoD atteint** : moteur AI/ML transparent sans dépendance externe, forecast CPU/power, anomalies, ranking, `confidenceScore`, fallback si historique insuffisant et tests. L’AI fournit uniquement des signaux et ne déclenche aucun changement.

### I8 — Decision Engine — DONE
- [x] Politiques Green IT
- [x] Critères SLA / RTO/RPO / sécurité / budget / criticité
- [x] Décisions MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW
- [x] Règles versionnées
- [x] Human review sur cas sensibles
- [x] IBM ODM évalué comme option, sans dépendance obligatoire

**DoD atteint** : politiques `greenops-policy-v1`, Decision Engine vendor-neutral, reason codes, contrôle qualité/confiance/sécurité/budget/RTO-RPO/dépendances, human approval et tests. `autoApplyAllowed=false` pour toutes les décisions.

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

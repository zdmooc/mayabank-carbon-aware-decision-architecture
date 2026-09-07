# Itération 0 — Cadrage Carbon-Aware / Infrastructure Paiement

## Objectif

Définir le cadre du dépôt avant tout calcul carbone, entraînement de modèle ou automatisation.

## Contexte fictif

**MayaBank Payment Platform** exploite un patrimoine hybride composé d’applications de paiement, middleware, VM/JVM, bases de données, stockage et plateformes conteneurisées.

L’objectif est de comparer des scénarios de modernisation et d’optimisation selon plusieurs critères :

- empreinte carbone ;
- coût ;
- performance ;
- capacité ;
- criticité ;
- disponibilité ;
- sécurité ;
- RTO/RPO ;
- complexité de migration.

## Séparation des responsabilités

| Besoin | Composant privilégié |
|---|---|
| mesure/inventaire | observabilité / CMDB / sources infra |
| calcul d’empreinte | Carbon Engine |
| prévision / anomalie / optimisation | AI / ML |
| politique et arbitrage | Decision Engine |
| validation sensible | humain / workflow |
| exécution contrôlée | GitOps / ITSM / plateforme |

Principe : **l’AI recommande ; le Decision Engine vérifie les politiques ; l’humain garde le contrôle des changements sensibles.**

## NFR initiaux

- explicabilité des recommandations ;
- provenance des données ;
- distinction mesure/calcul/hypothèse/prédiction ;
- reproductibilité ;
- sécurité ;
- auditabilité ;
- réversibilité ;
- performance ;
- maîtrise des coûts ;
- absence de données client réelles.

## Architecture logique initiale

```text
Applications / Infrastructure
        |
        v
CMDB / Metrics / Cost / Carbon factors
        |
        v
     Carbon Engine
        |
        +----> AI / ML
        |      forecast / anomaly / optimization
        |
        v
   Decision Engine
 policy / SLA / RTO / security / budget
        |
        v
MIGRATE / RIGHTSIZE / CONSOLIDATE
KEEP / RETIRE / REVIEW
        |
        v
Human approval -> GitOps / ITSM / Platform
```

## Livrables de l’Itération 0

- README de positionnement ;
- roadmap ;
- contexte fictif ;
- séparation Carbon Engine / AI / Decision Engine / humain ;
- principes d’anonymisation ;
- NFR initiaux ;
- architecture logique initiale.

## Critères de sortie

- [x] aucun nom d’entreprise cliente réelle ;
- [x] aucune donnée réelle ou chiffre client ;
- [x] cas d’usage infrastructure de paiement clairement défini ;
- [x] rôle de l’AI séparé du moteur de décision ;
- [x] moteur de décision vendor-neutral ;
- [x] roadmap incrémentale créée ;
- [x] aucun gain carbone présenté comme réel sans mesure et preuve.

**Statut : TERMINÉE**

Prochaine étape : **Itération 1 — Modèle de données Carbon & Infrastructure.**

# Architecture initiale — MayaBank Carbon-Aware Payment Platform

## Vue logique

```mermaid
flowchart LR
    SRC[CMDB / Metrics / Cost / Carbon Factors] --> CE[Carbon Engine]
    CE --> AI[AI / ML\nForecast / Anomaly / Optimization]
    CE --> DE[Decision Engine]
    AI --> DE
    DE --> HR[Human Review]
    DE --> ACT[GitOps / ITSM / Platform]
    DE --> OBS[Audit / Observabilité]
    ACT --> OCP[OpenShift / Cloud / Infrastructure]
```

## Responsabilités

- **Sources** : inventaire, métriques, coûts, facteurs carbone et criticité.
- **Carbon Engine** : calculs reproductibles et scénarios AS-IS / TO-BE.
- **AI/ML** : prévision de charge, anomalies, classement et optimisation multi-critères.
- **Decision Engine** : appliquer politiques Green IT, SLA, RTO/RPO, sécurité, budget et criticité.
- **Human Review** : valider les changements sensibles ou à forte incertitude.
- **GitOps / ITSM** : exécuter uniquement les changements approuvés.
- **Audit/Observabilité** : conserver sources, hypothèses, modèle, règle et décision.

## Types de décisions cibles

- MIGRATE ;
- RIGHTSIZE ;
- CONSOLIDATE ;
- KEEP ;
- RETIRE ;
- REVIEW.

## Principe de gouvernance

Une recommandation AI n’est pas une décision d’exploitation. La décision finale doit pouvoir expliquer les données utilisées, les hypothèses, les règles, le niveau de confiance et les contraintes qui ont conduit au résultat.

## Cible d’industrialisation

À partir des itérations ultérieures : modèle de données carbone, API, événements, OpenShift, GitOps, ITSM, observabilité, FinOps/GreenOps, sécurité, audit et tests avant/après.

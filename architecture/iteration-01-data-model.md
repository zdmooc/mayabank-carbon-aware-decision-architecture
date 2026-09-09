# Architecture de données — Itération 1

```mermaid
erDiagram
    APPLICATION ||--o{ COMPUTE_ASSET : owns
    APPLICATION {
      string application_id PK
      string application_name
      string business_domain
      string criticality
      int rto_minutes
      int rpo_minutes
    }

    COMPUTE_ASSET ||--o{ METRIC_OBSERVATION : produces
    COMPUTE_ASSET ||--o{ COST_OBSERVATION : incurs
    COMPUTE_ASSET }o--|| CARBON_FACTOR : located_in

    COMPUTE_ASSET {
      string asset_id PK
      string application_id FK
      string environment
      string platform_type
      string hosting_target
      float vcpu_allocated
      float ram_gb_allocated
      float storage_gb
      string region
      boolean shutdown_allowed
    }

    METRIC_OBSERVATION {
      string asset_id FK
      datetime timestamp
      float cpu_utilization_pct
      float ram_utilization_pct
      float power_watts
      string measurement_type
      string source
      float confidence
    }

    COST_OBSERVATION {
      string asset_id FK
      string period
      float cost_eur
      string cost_type
      string source
      float confidence
    }

    CARBON_FACTOR {
      string carbon_factor_id PK
      string region
      date valid_from
      date valid_to
      float gco2e_per_kwh
      string source
      string factor_type
    }
```

## Lecture architecturale

1. L’**application** porte la criticité et les objectifs RTO/RPO.
2. Un ou plusieurs **actifs techniques** supportent l’application.
3. Les **métriques** sont temporelles et ne sont jamais confondues avec la capacité allouée.
4. Les **coûts** sont historisés par période.
5. Les **facteurs carbone** sont versionnés par région et période de validité.
6. Toute future recommandation devra conserver la provenance et le niveau de confiance des données utilisées.

## Préparation des itérations suivantes

Ce modèle permettra ensuite de calculer :

- taux de sous-utilisation ;
- énergie estimée ;
- empreinte carbone par actif/application ;
- coût par actif/application ;
- scénarios de right-sizing ;
- scénarios AS-IS / TO-BE OpenShift ;
- recommandations multi-critères Carbon + FinOps + résilience.

# Dictionnaire de données — Carbon & Infrastructure v1

## Application

| Champ | Type | Description |
|---|---|---|
| application_id | string | Identifiant fictif stable, ex. `APP-PAY-001` |
| application_name | string | Nom fictif de l’application |
| business_domain | string | Domaine, ex. `PAYMENT` |
| criticality | enum | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| rto_minutes | integer | RTO cible en minutes |
| rpo_minutes | integer | RPO cible en minutes |

## Environment

| Champ | Type | Description |
|---|---|---|
| environment | enum | `DEV`, `TEST`, `UAT`, `PROD` |
| service_window | string | Fenêtre de service descriptive |
| shutdown_allowed | boolean | Autorisation théorique d’arrêt planifié |

## ComputeAsset

| Champ | Type | Description |
|---|---|---|
| asset_id | string | Identifiant fictif stable |
| application_id | string | Application rattachée |
| environment | string | Environnement |
| platform_type | enum | `PHYSICAL`, `VM`, `JVM`, `POD`, `DB` |
| hosting_target | enum | `ON_PREM`, `OPENSHIFT_LOCAL`, `AKS`, `ARO` |
| vcpu_allocated | number | vCPU alloués |
| ram_gb_allocated | number | RAM allouée en Go |
| storage_gb | number | Stockage logique en Go |
| region | string | Zone fictive, ex. `FR-EAST` |

## MetricObservation

| Champ | Type | Description |
|---|---|---|
| asset_id | string | Actif observé |
| timestamp | datetime | Date/heure ISO-8601 |
| cpu_utilization_pct | number | Utilisation CPU en % |
| ram_utilization_pct | number | Utilisation RAM en % |
| power_watts | number/null | Puissance observée ou estimée si disponible |
| measurement_type | enum | `MEASURED`, `CALCULATED`, `ESTIMATED` |
| source | string | Source synthétique de la donnée |
| confidence | number | Confiance 0..1 |

## CarbonFactor

| Champ | Type | Description |
|---|---|---|
| carbon_factor_id | string | Identifiant du facteur |
| region | string | Zone concernée |
| valid_from | date | Début de validité |
| valid_to | date | Fin de validité |
| gco2e_per_kwh | number | Intensité carbone fictive en gCO2e/kWh |
| source | string | Source du facteur |
| factor_type | enum | `SYNTHETIC`, `EXTERNAL_REFERENCE` |

## CostObservation

Prévue pour les itérations suivantes afin de rapprocher FinOps et GreenOps.

Champs attendus :

- `asset_id` ;
- `period` ;
- `cost_eur` ;
- `cost_type` ;
- `source` ;
- `confidence`.

## DataProvenance

Chaque donnée utilisée pour une recommandation doit pouvoir répondre à :

- d’où vient-elle ?
- quand a-t-elle été observée ?
- est-elle mesurée, calculée, estimée ou prédite ?
- quelle est sa qualité/confiance ?
- quelle version de facteur ou de modèle a été utilisée ?

## Règle fondamentale

Une **mesure**, un **calcul**, une **hypothèse** et une **prédiction AI** ne doivent jamais être mélangés dans le même statut de donnée.

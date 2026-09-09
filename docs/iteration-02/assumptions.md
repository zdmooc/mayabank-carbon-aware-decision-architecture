# Hypothèses — Carbon Engine v1

Toutes les données et hypothèses de cette itération sont **synthétiques**.

## Formules

Pour un actif et un scénario :

```text
adjusted_power_w = observed_power_w × power_multiplier
energy_kwh_year = adjusted_power_w × active_hours_per_year / 1000
emissions_kgco2e_year = energy_kwh_year × gco2e_per_kwh / 1000
annual_cost_eur = monthly_cost_eur × 12 × cost_multiplier
```

## Ce que le moteur calcule

- énergie opérationnelle estimée ;
- émissions opérationnelles associées à l'électricité ;
- coût annuel de run simplifié ;
- écarts BASELINE / TO-BE.

## Ce qu'il ne calcule pas encore

- carbone de fabrication des équipements ;
- Scope 3 complet ;
- PUE détaillé du datacenter ;
- amortissement matériel ;
- réseau ;
- cycle de vie complet du stockage ;
- coûts de migration ;
- effets rebond.

Ces limites sont intentionnelles : l'Itération 2 valide d'abord un noyau de calcul simple, explicable et testable.

## Scénario BASELINE

- tous les actifs sont considérés actifs 8 760 h/an ;
- puissance observée/estimée conservée ;
- coût mensuel synthétique conservé ;
- région carbone inchangée.

## Scénario OPTIMIZED

Le scénario illustre uniquement des hypothèses d'architecture :

- right-sizing sur les workloads de production ;
- plages d'allumage réduites pour UAT/TEST/DEV lorsqu'elles sont autorisées ;
- réduction synthétique de puissance après optimisation ;
- réduction synthétique du coût de run.

Aucun de ces coefficients ne doit être interprété comme un gain réel mesuré.

## Gouvernance

Chaque scénario doit fournir explicitement :
- heures actives ;
- multiplicateur de puissance ;
- multiplicateur de coût ;
- éventuel changement de région ;
- type de changement ;
- hypothèse textuelle.

Une variation non documentée est considérée invalide.

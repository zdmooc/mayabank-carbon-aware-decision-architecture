# Itération 2 — Carbon Engine AS-IS / TO-BE

## Statut

**TERMINÉE — moteur de calcul, scénarios et tests de non-régression livrés.**

## Objectif

Construire un premier moteur carbone simple, explicable et reproductible à partir des données synthétiques de l'Itération 1.

Le moteur compare deux scénarios :

- `BASELINE` : situation synthétique de référence ;
- `OPTIMIZED` : hypothèses de right-sizing et réduction des plages d'allumage non-prod.

## Chaîne de calcul

```text
Inventory + Metrics + Costs + Carbon Factors
                    ↓
              Carbon Engine
                    ↓
        Scenario BASELINE / TO-BE
                    ↓
      Energy / kgCO2e / Annual Cost
                    ↓
          Delta + Reduction %
```

## Résultats synthétiques attendus

| Indicateur | BASELINE | OPTIMIZED | Réduction |
|---|---:|---:|---:|
| Énergie | 7 752.600 kWh/an | 4 680.975 kWh/an | 39.62 % |
| Émissions | 576.715 kgCO2e/an | 350.350 kgCO2e/an | 39.25 % |
| Coût | 72 240.00 €/an | 57 864.00 €/an | 19.90 % |

Ces valeurs sont **entièrement synthétiques** et servent uniquement à tester la méthode.

## Livrables

- `docs/iteration-02/assumptions.md` ;
- `carbon-engine/engine.py` ;
- `carbon-engine/scenarios/baseline.csv` ;
- `carbon-engine/scenarios/optimized.csv` ;
- `tests/test_carbon_engine.py`.

## Exécution

```bash
python carbon-engine/engine.py --scenario optimized
```

Sortie JSON détaillée :

```bash
python carbon-engine/engine.py --scenario optimized --json
```

Tests :

```bash
python -m unittest tests/test_carbon_engine.py
```

## Principes de gouvernance

- aucune hypothèse implicite ;
- tous les coefficients de scénario sont versionnés ;
- mesure, estimation, facteur et calcul restent séparés ;
- aucun gain synthétique n'est présenté comme un gain réel ;
- les limites méthodologiques sont documentées ;
- un scénario incomplet ou non documenté doit échouer.

## Critères de sortie

- [x] calcul d'énergie reproductible ;
- [x] calcul carbone reproductible ;
- [x] calcul coût simplifié ;
- [x] scénario AS-IS / BASELINE ;
- [x] scénario TO-BE / OPTIMIZED ;
- [x] hypothèses explicites ;
- [x] tests de non-régression ;
- [x] comparaison synthétique documentée.

## Prochaine étape

**Itération 3 — Observabilité & inventaire : ingestion, normalisation, corrélation application → infrastructure, qualité et fraîcheur des données.**

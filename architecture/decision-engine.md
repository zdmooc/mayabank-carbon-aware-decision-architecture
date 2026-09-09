# Architecture — GreenOps Decision Engine

## Positionnement

Le Decision Engine transforme des signaux techniques en décisions gouvernées.

```text
Data quality / CMDB / Observability
            +
Carbon Engine / Right-Sizing
Modernization / Storage / AI-ML
            ↓
      Decision Engine
            ↓
Policy checks + reason codes
            ↓
MIGRATE / RIGHTSIZE / CONSOLIDATE / KEEP / RETIRE / REVIEW
            ↓
Human Approval / ITSM / GitOps
```

## Responsabilités

### Sources

- mesurer ou estimer ;
- produire un signal technique ;
- exposer provenance, qualité et confiance.

### AI / ML

- prévoir ;
- détecter des anomalies ;
- classer les candidats ;
- fournir une confiance.

### Decision Engine

- appliquer les politiques Green IT ;
- vérifier SLA, RTO/RPO, sécurité, budget, criticité et dépendances ;
- produire une décision explicable ;
- orienter vers `REVIEW` si un garde-fou n'est pas satisfait.

### Humain / ITSM / GitOps

- approuver ;
- planifier ;
- exécuter le changement ;
- conserver la preuve avant/après.

## Anti-patterns évités

- AI qui applique directement un changement ;
- optimisation uniquement basée sur le carbone ;
- optimisation sur données de mauvaise qualité ;
- migration autorisée malgré dépendance bloquante ;
- réduction de capacité ignorant SLA/RTO/RPO ;
- décision non versionnée ou sans reason codes.

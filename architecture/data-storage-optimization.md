# Data & Storage Optimization — architecture cible

## Chaîne de décision

```text
Applications / Databases / Storage
              ↓
Inventory + Retention + Backup + RTO
              ↓
       Storage Assessment
              ↓
  HOT / WARM / COLD recommendation
  TTL / retention recommendation
  Backup recommendation
  DB consolidation candidate
              ↓
      Cost + Carbon + Risk
              ↓
        KEEP / OPTIMIZE
              ↓
        Human validation
```

## Principes

### HOT
Réservé aux données demandant faible latence ou RTO court, notamment les données transactionnelles critiques.

### WARM
Données encore régulièrement consultées mais pouvant accepter un stockage moins coûteux/énergivore.

### COLD
Données rarement consultées, historiques, logs ou archives lorsque le RTO l’autorise.

## Rétention / TTL

La politique de rétention doit provenir du besoin métier, réglementaire ou opérationnel. Une réduction de rétention n’est proposée automatiquement que pour les jeux synthétiques non-prod/logs dans le lab.

## Backup

Le nombre de copies et la rétention de backup doivent être cohérents avec criticité, RPO/RTO et stratégie de reprise. Le moteur I6 ne supprime jamais automatiquement un backup.

## Consolidation DB

Un candidat à consolidation doit présenter :

- plusieurs instances ;
- faible CPU/RAM synthétique ;
- criticité compatible ;
- capacité cible démontrée ;
- absence de dépendance bloquante.

La recommandation ne vaut pas changement automatique.

## Méthodologie carbone

Les coefficients HOT/WARM/COLD et DB sont fictifs. Ils permettent de tester une méthode comparative reproductible, pas de mesurer une infrastructure réelle.

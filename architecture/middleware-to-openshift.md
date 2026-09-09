# Architecture — Middleware VM/JVM vers OpenShift

## Vue logique

```text
AS-IS
+-------------------------------+
| VM / JVM / Middleware         |
| CPU / RAM surdimensionnés     |
| sessions locales possibles    |
| stockage partagé / local      |
+---------------+---------------+
                |
                v
+-------------------------------+
| Assessment / Right-Sizing     |
| - charge                      |
| - criticité                   |
| - état                        |
| - stockage                    |
| - HA                          |
| - coût / carbone              |
+---------------+---------------+
                |
                v
TO-BE OPENSHIFT
+-------------------------------+
| Namespace                     |
| Deployment / Pods             |
| requests / limits             |
| PDB                           |
| anti-affinity / topology      |
| Service / Route               |
| CSI / objet / ephemeral       |
+-------------------------------+
```

## Mapping de responsabilité

| Préoccupation | AS-IS | TO-BE |
|---|---|---|
| Processus Java | JVM sur VM | conteneur Java dans pod |
| Scalabilité | capacité VM | replicas / HPA futur |
| Réservation CPU/RAM | allocation VM | requests |
| Plafond CPU/RAM | configuration VM/JVM | limits selon politique |
| HA | VM / middleware | replicas + distribution + PDB |
| Configuration | fichiers / middleware | ConfigMap / Secret |
| Stockage | local / partagé | CSI / objet / ephemeral selon besoin |
| Déploiement | scripts/outils historiques | GitOps cible |
| Observabilité | agent/APM | metrics/logs/traces cloud-native |

## Règles d'architecture

### Stateless first

Un service réellement stateless est le meilleur candidat initial :

- pas de session locale indispensable ;
- fichiers temporaires non persistants ;
- état métier externalisé ;
- dépendances réseau connues.

### Session state

Une session locale dans une JVM crée un couplage avec l'instance. Avant une migration cloud-native, il faut choisir explicitement :

- session externe ;
- token/stateless ;
- cache distribué ;
- sticky session comme solution transitoire seulement si justifiée.

Le lab classe `legacy-session-service` en `REVIEW` tant que ce point n'est pas traité.

### HA

Pour un service critique :

- au moins 2 replicas, 3 dans le scénario de référence ;
- distribution multi-worker ;
- PodDisruptionBudget ;
- readiness/liveness probes dans une itération de déploiement ;
- capacité N+1 à démontrer avant production.

### Stockage

Le choix du stockage doit suivre la donnée, pas reproduire automatiquement le stockage VM :

- `EPHEMERAL` pour données recréables ;
- `CSI_SHARED` si persistance POSIX réellement requise ;
- stockage objet si le pattern fonctionnel s'y prête ;
- DB externe pour l'état transactionnel.

## Décision d'architecture

La recommandation n'est pas : « tout migrer vers OpenShift ».

Elle est :

```text
MIGRATE
  si bénéfice plausible + dépendances maîtrisées + HA cible cohérente

REVIEW
  si session/stockage/dépendance/risque bloque une migration directe

KEEP
  si une cible OpenShift n'apporte pas suffisamment de valeur ou augmente le risque
```

Les chiffres du dépôt sont synthétiques et ne servent qu'à démontrer le raisonnement d'architecture.

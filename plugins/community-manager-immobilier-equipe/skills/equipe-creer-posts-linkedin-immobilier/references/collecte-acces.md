# Choisir les accès et maîtriser les quotas LinkedIn

Appliquer cette fiche à toute collecte autorisée, ponctuelle ou récurrente, avec apprentissage.md et surveillance.md. Une modification du skill ne lance pas une collecte et ne change pas la cadence. Réutiliser les autorisations existantes dans leur portée.

## 1. Choisir la source pour chaque donnée

1. Identifier le profil personnel cible et les posts du lot à partir du registre. Ne pas substituer une page d'entreprise, un homonyme ou une autre connexion.
2. Découvrir les outils utiles et leurs paramètres. Distinguer lecture du post, statistiques personnelles, statistiques de page, compteurs de réactions/commentaires, texte des commentaires et réponses. Un droit de publier ne vaut pas droit de lire ; un outil présent au catalogue ne garantit pas l'accès du compte.
3. Réutiliser les capacités récemment vérifiées sans répéter une découverte et un test pour chaque post. En cas de doute, tester en lecture seule sur un post cible, avec une requête minimale. Consigner capacité, cible, résultat, date et limite ; revalider après changement de compte/droits, erreur ou doute pertinent sur la validité. Ne pas tester par une publication ou un commentaire.
4. Utiliser le connecteur pour chaque capacité effectivement disponible. S'il fournit les statistiques mais pas les commentaires, garder les statistiques et compléter les commentaires par le web ; faire l'inverse si nécessaire. Ne pas remplacer une mesure privée fiable par un compteur public moins précis.
5. Pour les éléments manquants, effectuer soi-même la consultation publique autorisée : recherche web ciblée, puis ouverture des liens de publications. Privilégier les URL du registre ; en cas d'échec du profil ou d'une URL de fil, chercher le nom, l'identifiant du profil, l'identifiant du post ou une phrase distinctive pour retrouver une page publique de publication. Vérifier auteur et correspondance avant rattachement. L'échec d'une URL ne prouve pas l'indisponibilité de toutes les pages publiques.
6. Utiliser le navigateur seulement selon les règles et capacités de l'environnement, si ce recours est nécessaire et autorisé. Respecter les restrictions d'accès et les parcours sécurisés de connexion ; ne pas contourner CAPTCHA, blocage ou contenu privé. Ne pas demander d'emblée au conseiller de copier ses posts lorsqu'une lecture publique reste possible.
7. Si aucune source ne permet de lire la cible après ces tentatives raisonnables, livrer le résultat partiel avec la liste des éléments manquants. Limiter la recherche de repli à quelques requêtes pertinentes et liens candidats ; ne pas boucler ni essayer des services au hasard. Une donnée inaccessible ne doit pas empêcher d'analyser les autres données vérifiées.

## 2. Rendre la couverture et les conclusions vérifiables

Pour chaque post, conserver avec le relevé : URL/identifiant vérifié, source de chaque famille de données, heure de consultation, fraîcheur connue ou inconnue et couverture des commentaires. Distinguer source API, page publique lue et contenu indexé/extrait de recherche. Une page renvoyée par un moteur peut être en cache : ne pas assimiler sa consultation à une actualisation certaine de ses compteurs. Si seule une version indexée est accessible, présenter son contenu comme tel, avec sa date connue et la limite de fraîcheur.

Ne pas déclarer vérifié un suivi de résultats actuels sur la seule lecture d'une ancienne version indexée. Garder les observations historiques exploitables, mais le statut du suivi doit refléter l'accès nécessaire à sa portée : accès non résolu = `blocked`, accès suffisant vérifié mais tâche non configurée = `pending_setup`. L'activation ne devient effective qu'après les vérifications de surveillance.md.

Réutiliser `audience_review.source`, `coverage` et `metrics` sans créer un second registre. Conserver les absences à `null`, jamais à zéro. Préciser le nombre de commentaires effectivement lus, les réponses incluses, le tri et les limites ; les compteurs d'un commentaire ne sont pas ceux du post. Des commentaires visibles ne prouvent pas que toute la discussion a été récupérée.

Ne jamais reconstituer impressions, portée, clics, visiteurs ou conversions à partir des likes, commentaires ou abonnés. Sans dénominateur disponible, ne pas calculer de taux par impression/portée. Des commentaires partiels peuvent éclairer les questions et objections observées ; ils ne mesurent pas l'opinion de toute l'audience ni la performance globale du post. Séparer faits, interprétations et recommandations, puis rattacher aux versions réellement diffusées selon apprentissage.md.

## 3. Distinguer permissions, quotas et services payants

| Situation constatée | Traitement |
| --- | --- |
| Permission LinkedIn refusée, notamment `403` | Identifier le droit et la capacité manquants ; utiliser les autres capacités et le public accessibles. Ne pas présenter un abonnement supérieur comme un remède garanti. |
| Limite de requêtes, notamment `429` | Identifier le fournisseur, la limite et le délai connu ; respecter `Retry-After` s'il existe, différer les appels concernés, garder les résultats acquis. Ne pas contourner le quota par rotation de comptes ou d'identités. |
| Quota Composio mensuel atteint | Distinguer les appels Composio des accès web directs ; utiliser les sources restantes autorisées et proposer une cadence moindre ou attendre la remise à zéro selon le besoin. |
| Portefeuille Composio Instant vide | Identifier l'outil tiers concerné, par exemple ScrapeCreators. Continuer à tester/utiliser les comptes connectés et la consultation publique directe : le solde Instant ne prouve pas leur blocage. |
| Outil de page d'entreprise ou création de commentaire disponible | Ne pas en déduire l'accès aux statistiques d'un profil personnel ni à la lecture des commentaires. |

Vérifier les tarifs officiels au moment d'une question de coût ou d'un choix payant : [Composio](https://composio.dev/pricing), [Instant](https://composio.dev/instant) et [limites LinkedIn](https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/rate-limits). Ne pas graver un quota commercial changeant dans une règle permanente. Distinguer quota général, sous-quota d'applications OAuth gérées par Composio, éventuels sous-quotas d'exécution, portefeuille Instant et limites propres à LinkedIn. Les quotas d'un espace ne sont pas automatiquement réservés à LinkedIn : tenir compte des autres usages Composio.

Privilégier les accès déjà autorisés et la lecture publique directe avant un service tiers facturé. N'utiliser un service payant que dans un budget explicitement autorisé, avec coût applicable identifié ; ne pas souscrire, recharger ou changer de forfait sur une simple demande de collecte. Un crédit absent ne justifie pas de demander une recharge avant d'avoir essayé les voies gratuites adaptées. Si le forfait exact, la consommation ou une limite d'application sont invisibles, le dire ; ne pas inventer le solde du compte ni déclarer sa compatibilité garantie.

## 4. Dimensionner et limiter les appels

Estimer à partir du rythme demandé : publications × appels nécessaires pour texte/média/vérification, plus passages de collecte × posts effectivement relus × appels par famille de données/page, plus les contrôles utiles et une marge de pagination/reprise. Une instruction en langage naturel ou un appel groupé peut exécuter plusieurs outils facturables. La préparation de texte et la recherche web directe ne consomment pas d'appels Composio lorsqu'elles n'utilisent pas Composio ; un passage quotidien du skill n'impose pas une collecte quotidienne.

Séparer estimation et consommation mesurée. Donner les hypothèses, une fourchette et le quota applicable vérifié ; partager les quotas avec les autres usages de l'espace. Actualiser l'estimation à partir des relevés d'usage s'ils sont accessibles, sans prétendre les avoir consultés autrement.

Conserver la fenêtre et le nombre de posts convenus, réutiliser les identifiants et observations, ne lire que les échéances dues et paginer dans une borne annoncée. Ne pas relire chaque jour les 365 posts accessibles au coach : cette profondeur de mémoire n'est pas une consigne de collecte quotidienne. Si une borne coupe la discussion, enregistrer la couverture partielle et la reprise utile. Ne pas multiplier les appels qui échouent pour la même permission. Un quota confortable ne résout pas un droit d'accès manquant.

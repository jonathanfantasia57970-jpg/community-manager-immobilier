# Mise à jour et personnalisation sans réinitialisation

## Deux espaces distincts

Le paquet contient les méthodes, outils, schémas de départ et le catalogue commun versionné. Il reste immuable pendant l’activité d’un conseiller. Le profil réel, ses préférences, contacts, comptes, mandats, contenus, médias, apprentissages, décisions, calendriers, réservations, reçus et historiques restent dans ses propres ressources persistantes, hors du paquet. Ni une réinstallation ni une nouvelle version n’autorisent leur suppression, remplacement ou transfert vers le créateur ou un autre conseiller.

Avant toute configuration, retrouver le profil par son propriétaire et ses références canoniques ; ne pas se fier seulement au nom. S’il existe, reprendre sa version actuelle. Ne créer un profil que si son absence a été établie. En cas d’accès impossible, ne pas conclure qu’il est absent et ne pas créer de doublon.

## Personnaliser la communication

Lire `editorial.communication`, `editorial.personal_rules`, les préférences du canal et les exemples approuvés/refusés, puis les dernières consignes applicables. Résoudre aussi langue, tutoiement/vouvoiement, niveau de formalité, rythme, longueur, humour, emojis, vocabulaire, questions finales, appels à l’action, voix, accent, présence à l’image et charte. Les exceptions par canal sont dans `communication.channel_overrides`. Leadership et recrutement restent deux choix indépendants, désactivés seulement au démarrage d’un nouveau profil.

La dernière demande explicite du conseiller prévaut dans sa portée ; puis ses préférences par canal ; puis son profil général ; enfin les valeurs de départ communes. Une nouvelle valeur de départ ne remplace jamais une préférence existante, y compris `false`, une liste vide ou un refus explicite. Les corrections ponctuelles ne deviennent pas des règles globales sans raison ou demande. Mettre à jour seulement les champs concernés, avec source et révision, en conservant les exemples et décisions antérieurs. Ne pas imposer un questionnaire à chaque reprise.

La personnalisation adapte l’expression, les thèmes et la présentation ; elle ne crée ni vécu, ni résultat, ni autorisation, et ne supprime pas les contrôles de fond, droits, fidélité ou relecture.

## Migration de profil

Une mise à jour du plugin seule ne touche à aucune ressource personnelle. Si une nouvelle fonction nécessite un champ : lire la version actuelle et vérifier le propriétaire ; établir une sauvegarde privée restaurable ; préparer la différence ; ajouter uniquement les clés absentes utiles ; préserver les champs inconnus, toutes les listes, valeurs existantes, références et états. Un `null` existant peut être un choix non renseigné : ne pas le remplacer automatiquement. Ne jamais remplacer un objet mal formé par un modèle vide ; signaler seulement l’incompatibilité concernée.

Relire juste avant écriture et utiliser le contrôle de version du stockage. Si la version change, relire et recalculer la fusion ; ne jamais forcer une ancienne copie. Vérifier après écriture le diff attendu et l’intégrité des valeurs protégées. Conserver le reçu de migration dans l’espace personnel. Une erreur de migration bloque seulement la fonction dépendante. Aucun retour arrière ne doit écraser des modifications ultérieures : restaurer dans une copie puis rapprocher les changements.

Pour un profil JSON local, `skills/equipe-configurer-espace/scripts/migrer_profil.py` prépare par défaut une fusion en lecture seule. L’application exige `--apply` et l’empreinte attendue `--expected-sha256`, crée une sauvegarde exclusive, verrouille les appels de cet outil et vérifie la source avant remplacement atomique. Ce verrou ne coordonne pas les autres éditeurs : employer le contrôle de version du stockage pour une source partagée ou distante. Ne jamais appliquer ce script à un export en prétendant avoir migré la source Notion. Ne jamais migrer les registres opérationnels avec ce script de profil.

## Catalogue commun et ajouts personnels

Conserver intégralement les 69 fiches et les 16 familles de sources embarquées. Pour un catalogue personnel, identifier les fiches par `(catalogue d’origine, identifiant stable)` ; ne pas dédupliquer par titre, ne pas renuméroter les ajouts du conseiller et ne pas écraser une fiche homonyme.

Une synchronisation conserve fichiers personnalisés, annotations, évaluations, usages, historiques, exclusions, favoris et fiches privées. Ajouter seulement les nouvelles références communes absentes. Une nouvelle version commune d’une fiche déjà adaptée devient une proposition liée à la même origine : conserver la version personnelle active et présenter les différences ; ne l’adopter que dans le mandat correspondant. Une fiche retirée du paquet n’est jamais supprimée du catalogue personnel. Garder journal d’import, version commune vue et correspondance d’identifiants afin qu’une relance soit idempotente.

Une première installation peut importer la base sans aucun historique du créateur. Une mise à jour reprend l’import existant ; elle ne réimporte pas les 69 fiches en bloc, ne vide pas les registres et ne recrée pas les bases, médias ou tâches.

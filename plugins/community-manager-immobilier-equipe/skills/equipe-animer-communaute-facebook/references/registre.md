# Registre Facebook et mémoire indépendante

## Sources canoniques

- Registre : `CONFIG_FACEBOOK_REGISTRY`, clé `CONFIG_FACEBOOK_KEY`.
- Coaching : `CONFIG_FACEBOOK_COACHING`, clé `CONFIG_FACEBOOK_COACHING_KEY`.
- Les identifiants persistants sont conservés dans `../assets/sources.json` après création confirmée. Utiliser le skill Library et ces identifiants ; ne pas recréer une base si elle est simplement inaccessible.

Ces fichiers sont propres à Facebook. Ne pas écrire dans le registre LinkedIn ou la veille éditoriale, ni recopier leurs performances comme observations Facebook. Initialement, aucune publication, action extérieure ou performance n'a été importée. Une base vide ne prouve pas un compte sans historique.

## Lecture progressive

Lire les versions actuelles, garder leurs identifiants et versions, puis filtrer localement avant de charger du texte dans le modèle. Consulter `channels`, `account` (héritage), `editorial_plan`, `preferences` et les actions ouvertes. Pour rédiger, utiliser `scripts/registre.py context CHEMIN_JSON` (20 fiches par défaut), puis `--query 'termes proches'` et `--ids ID1 ID2` pour les textes utiles. Ne pas charger les commentaires bruts.

Le coach accède aux **365 dernières fiches de posts**, par `created_at`, ou à toutes si moins nombreuses. Une fiche compte une fois, ses versions ne comptent pas comme de nouveaux posts. Utiliser `coach-context`, paginé avec `--limit 50 --offset 50`, puis suivre `next_offset`. Les recherches restent dans cette fenêtre ; les textes et observations complets restent accessibles par `--ids`. Une page ou une recherche ciblée ne constitue pas une analyse des 365 posts. Pour un bilan sur l'ensemble, parcourir les lots et annoncer la couverture réelle. Les comparaisons de résultats utilisent les dates de publication et d'observation vérifiées.

Consulter les suites avec `scripts/registre.py actions CHEMIN_JSON` ; elles ne sont pas limitées aux 365 posts. `--all` inclut les actions terminées ou annulées. Lire les entrées utiles au-delà des extraits si elles sont tronquées. La fenêtre de lecture n'efface aucun ancien post. Une consultation du registre ne lance aucune collecte sur le réseau.

## Structure du registre

Racine : `schema_version: 1`, `registry_key`, `revision`, `updated_on`, `account`, `editorial_plan`, `preferences`, `entries`, `actions`. Préserver les champs inconnus. `account` garde URL, type, identifiant, date et source de vérification ; valeurs inconnues = `null`. `editorial_plan` distingue hypothèses, décisions confirmées, disponibilité et cadence. Une configuration mémorisée ne supplante jamais les autorisations de la conversation.

Garder `editorial_plan.morning_workflow` pour la mission matinale et sa tâche réellement confirmée. Le lancement quotidien ne prouve pas une cadence de publications. Conserver désormais deux derniers passages dans `last_editorial_runs.page` et `.profile` (préserver `last_editorial_run` hérité pour traçabilité) : `run_key` (date dans le fuseau du profil, canal et cible), `local_date`, `started_at`, `completed_at` ou `null`, `decision` (`create`, `reuse`, `no_post`, `blocked`), `reason` bref, `entry_id` ou `null`, `state` (`in_progress`, `completed`, `blocked`). Ce suivi remplace le précédent sans créer un journal croissant.

Avant une génération matinale, retrouver la clé du jour et l'éventuelle entrée en cours. Réutiliser le post déjà prêt ou terminer sa version incomplète ; ne pas recommencer une création ou un média sur simple relance. Garder aussi `morning_run_key` dans l'entrée concernée pour réconcilier une interruption entre sauvegardes. Une issue `no_post` ne crée aucune fausse fiche de publication. En cas d'historique inaccessible, ne pas fabriquer de preuve d'absence de doublon ; signaler cette limite et éviter une répétition connue dans le contexte accessible.

Chaque post possède `id`, `created_at` avec fuseau, `version`, `status`, `scope`, `subject`, `text`, `media` ; ajouter objectif, public, pilier, angle, idées développées, sources, participation, feedback, versions antérieures et revue quand utiles. Une proposition de calendrier peut rester `planned` avec texte vide ; ne pas l'annoncer comme prête. Statuts : `planned`, `draft`, `incomplete`, `ready`, `approved`, `scheduled`, `published`, `rejected`, `cancelled`. Portées : `full`, `text_only`, `idea`, `brief`.

Pour les nouvelles productions, renseigner `audience_primary`, `audience_need` et une `editorial_fingerprint` compacte : `experience`, `participant_action`, `effort`, `emotional_register`, `hook_pattern`, `visual_treatment`, `distinctive_value`, `share_reason`. Garder chaque valeur courte et descriptive, sans score fictif. Sujet, angle et `ideas_developed` portent déjà le fond ; ne pas le recopier dans l'empreinte. `participation` détaille seulement les consignes et suites nécessaires. Ces champs sont projetés et recherchables par le script ; les anciennes fiches sans empreinte restent compatibles et leurs inconnues ne deviennent pas des faits. Ne pas créer un deuxième historique de diversité : l'analyse de la séquence est calculée à partir des fiches.

`media` contient au plus un objet : type `image` ou `video`, référence réelle `ref`, `verified`, provenance, durée si vidéo et vérifications utiles. Pour un post `full` prêt, exiger texte et un média final vérifié. Conserver une livraison partielle comme `incomplete`, pas comme un post complet. Restituer obligatoirement ce média final avec le texte dans le fil de livraison, même si la diffusion est automatique ou le statut reste `ready`. Pour un format différent explicitement demandé, adapter la procédure sans prétendre que le validateur actuel le prend déjà en charge.

Pour toute nouvelle publication complète, ajouter `creative_mechanism_review` : `consulted_at`, `concepts_examined` (noms et URLs), `selected_concept` avec son adaptation, ou `not_selected_reason`. Enregistrer aussi `content_structure` avec les quatre champs compacts `context`, `problem`, `solution`, `cta`. Ces champs permettent de vérifier le fond, la diversité et le choix de format ; ils ne remplacent jamais le texte exact du post.

Pour `approved`, garder `user_confirmation` avec portée et référence à l'instruction. Pour `scheduled` et les diffusions automatiques `published`, conserver `target_id`, `provider_result`, la date confirmée avec fuseau, et URL/identifiant si accessibles. Les confirmations manuelles du profil et les reçus fournisseur sans date suivent les exceptions explicites de page-profil.md ; ne pas inventer un reçu ni une date. Ne pas déduire une publication d'une approbation ou d'une programmation. Une différence avec le texte effectivement publié se conserve séparément dans `published_snapshot`.

Réserver `feedback` aux appréciations du conseiller ; `audience_review` porte la dernière observation du public selon coaching.md. Ne pas empiler les relevés et commentaires bruts. Enregistrer les productions effectivement livrées ou les idées de calendrier proposées avec leur état ; pas les candidats internes ni les fixtures de validation.

Une action possède `id`, `kind`, `description`, `post_id` si applicable, `external` booléen, `due_at` connu ou `null`, et `status` : `proposed`, `approved`, `completed`, `blocked`, `cancelled`. Garder `instruction_ref` pour un accord, `result` pour un achèvement ; pour une action externe effectuée, garder aussi `target_ref` et la confirmation du service. La création d'un brouillon de réponse n'est pas son envoi. Ces traces documentent l'action sans lui donner une autorisation autonome.

## Brief canonique avant production

Conserver les briefs dans `editorial_plan.editorial_briefs[brief_id]` du même registre, hors `entries`. Un brief porte notamment `brief_id`, `revision`, la destination Page/profil, le fond retenu, `decision_format` et les relais du contrat CM. Créer cette collection facultative seulement lors d'une écriture autorisée ; ne pas migrer les anciennes fiches. Les portées héritées `idea`/`brief` restent lisibles mais ne servent pas à enregistrer les nouvelles intentions : les fenêtres de posts ne doivent pas compter un brief comme une production.

Lier calendrier, passage et éventuelle entrée produite par `brief_id` ; ajouter `brief_revision` à la version du post soumise. Garder la révision du brief distincte de `version` du post. Le projet vidéo référence ce même objet et ne devient pas son propriétaire. Une adaptation Instagram possède un brief lié, avec sa destination propre, sans dupliquer le texte ni l'état Facebook. Relire versions et réservations avant mutation et préserver les champs inconnus.

## Enregistrer et nettoyer

Modifier seulement les champs concernés, incrémenter `revision` et actualiser `updated_on`. Valider avec `scripts/registre.py validate CHEMIN_JSON` ou `scripts/coaching.py CHEMIN_JSON`, puis remplacer le même fichier avec sa version attendue. Ces validateurs contrôlent la structure, pas la réalité d'un accord, la qualité d'un média ou la réussite d'une publication. En cas de conflit, relire et fusionner sans retirer la garde de version. Un seul rédacteur écrit ; les reviewers restent en lecture seule. Ne pas annoncer le succès avant la confirmation du service.

Effacer des posts sur demande n'efface pas la mémoire de coaching indépendante. Ne pas réimporter les posts supprimés ; marquer la traçabilité réduite des observations. Préserver les actions encore ouvertes sauf demande de les supprimer également, en signalant si leur post source n'est plus disponible. Ne pas fermer silencieusement un engagement au cours d'un nettoyage.

## Extension Page/profil

Garder le schéma 1 compatible et ajouter `channels.page` / `.profile` : destination, mode de publication, état, mandat, cadence et prochaine révision. `account` reste la destination héritée, pas une autorisation Page. Ajouter `channel` aux fiches dont l'attribution est prouvée ; laisser les autres inconnues. `context --channel page` ou `--channel profile` filtre avant pagination ; `coach-context` garde d'abord la fenêtre globale des 365 derniers posts puis filtre le canal. Une recherche sans filtre permet les rapprochements entre canaux.

Suivre page-profil.md pour `publication_attempt`, `publication_confirmation`, `delivered_at`, `published_on` et les deux passages quotidiens. Le script valide les confirmations manuelles sans exiger de reçu technique fictif ; il ne prouve ni le choix de cible ni la réalité de la diffusion. Les décisions opérationnelles de cadence sont bornées à la valeur actuelle, la précédente, la raison et la prochaine révision.

# Observations et coaching

## Collecte sur demande

Une demande de bilan des réactions ou de collecte autorise le périmètre correspondant. Une création, un conseil ou la consultation du registre n'en déclenche pas. Réutiliser la sélection du conseiller ; à défaut, retenir les publications confirmées de plus de cinq jours sans observation exploitable intégrée, dans la fenêtre des 365 derniers posts. Compter depuis `published_at`, jamais depuis la création du brouillon. Traiter un post plus récent ou un historique plus large si demandé, avec ses limites.

Vérifier compte, publication, version publiée et couverture d'accès. Découvrir les outils selon acces.md ; les statistiques ne donnent pas nécessairement les commentaires. Signaler toute couverture partielle ou blocage et poursuivre ce qui est accessible. Une demande « tous les posts » n'est pas silencieusement réduite à la fenêtre par défaut. Ne pas collecter ou importer d'autres historiques pour remplir une base vide.

Relever date, source, âge du post, réactions, commentaires, partages, impressions/portée si disponibles et texte des échanges accessibles. Valeur inconnue = `null`, pas zéro. Distinguer réponses du conseiller, participants distincts et contributions répétées. Pour un grand fil, indiquer échantillon, nombre lu, ordre et limites. Ne pas déduire profession, intérêt commercial ou résidence d'un nom ou d'une photo.

## Synthèse par post

Garder la dernière `audience_review` : `observation_id`, `observed_at`, `state` (`observed`, `partial`, `blocked`, `insufficient`), source, couverture, métriques et leurs définitions, âge du post, `summary` de 150 mots maximum, au plus trois hypothèses, `integration_state` (`pending`, `applied`), `applied_to_memory_revision` (`null` avant intégration). Ajouter identifiant/URL de publication et version réellement observée.

Séparer faits, interprétations et explications alternatives. Comparer des posts de contexte et d'ancienneté compatibles ; garder le même dénominateur pour les taux. Ne pas déduire confiance, intention d'achat ou conversion d'un compteur de likes. Un zéro réellement vérifié est un résultat ; un accès bloqué ne met pas à jour les enseignements.

Observer la diversité des participants, leurs retours, les réalisations partagées, les échanges entre membres, la compréhension du propos, les effets professionnels attestés et le coût réel de préparation/animation lorsqu'il est connu. Ne pas transformer un lecteur silencieux en personne désintéressée, ni une corrélation en causalité.

Évaluer selon le public et l'objectif du post : découverte (portée hors abonnés si disponible, partages et visites), relation (participants qui reviennent, échanges substantiels, créations), confiance (questions précises, retours explicites, recommandations) et résultats professionnels attestés (demandes immobilières, échanges de collaboration ou d'équipe). Garder ces signaux distincts ; les likes ne prouvent pas la confiance, un partage ne prouve pas que sa destination appartient à la cible. Ne pas ouvrir de messages privés ni enrichir les profils pour remplir ces mesures sans demande correspondante. Pour les vidéos, inclure rétention et durée de visionnage seulement si accessibles et comparables.

Comparer les contextes, pas uniquement les volumes : audience visée, format, âge, portée connue, publication organique ou soutenue, effort de participation. Un jeu très commenté hors cible ne doit pas éclipser un contenu professionnel utile. Proposer un essai avec une hypothèse, un changement identifiable et un critère d'évaluation adapté ; attendre le choix du conseiller. Conserver aussi les résultats contradictoires et les limites des petits échantillons.

Orienter prioritairement les conseils de progression vers la viralité auprès des cibles : examiner portée hors abonnés, partages rapportés à la portée lorsqu'elle est connue, puis capacité à retenir et faire participer de nouvelles personnes. Comparer à des publications du compte de contexte comparable ; préciser période, échantillon et dénominateur, sans seuil universel ni score inventé. Distinguer diffusion large et adéquation à la cible, qui peut rester inconnue. Lors d'un bilan demandé, dégager le levier de propagation le plus prometteur, proposer une amélioration concrète et la mesure qui permettra d'en juger. En l'absence de retours, présenter une hypothèse de conception, jamais une amélioration démontrée. Ce cap ne déclenche aucune collecte et ne vaut pas acceptation automatique des essais proposés.

## Concevoir et décider un essai

Pour une piste suivie, formuler une hypothèse précise, un changement identifiable, le public et le bénéfice visés, puis la période ou le nombre de publications proposé. Définir dans `evaluation` le contexte de comparaison, les données nécessaires et ce qui ferait poursuivre, ajuster ou arrêter. Utiliser les champs existants : pas de nouveau journal d'expériences ni de seuil universel. Sans données de référence, commencer par établir un repère ; ne pas promettre un gain chiffré.

Privilégier un changement principal lorsque l'objectif est d'en apprendre la cause. Si plusieurs éléments changent, évaluer le concept global sans attribuer le résultat à un seul. Comparer à ancienneté proche, distinguer organique et sponsorisé si connu, compter les participants distincts seulement si accessibles. Intégrer l'effort réel d'animation : une participation forte mais ingérable peut demander un format plus léger.

Lors du bilan demandé, recommander de poursuivre si le bénéfice recherché apparaît de façon suffisamment cohérente, d'ajuster si la participation ou la compréhension révèle un obstacle, ou d'arrêter si le contenu dessert la cible ou la confiance. Si l'échantillon est trop petit, les données absentes ou les résultats contradictoires, conclure « indéterminé » et expliquer quelle observation aiderait. Un essai accepté n'autorise pas la collecte automatique ; une réussite ne vaut ni règle permanente ni autorisation de prolonger sa portée.

## Mémoire compacte et choix

Utiliser le fichier indépendant du registre. Structure : `schema_version: 1`, `memory_key: CONFIG_FACEBOOK_COACHING_KEY`, `revision`, `updated_on`, `status` (`awaiting_requested_collection`, puis `has_observations`), `coverage`, `insights`, `experiments`, `last_batch`.

Limiter à **800 mots, 12 enseignements et 3 pistes suivies au total**. Pour un enseignement : `id`, `statement`, `scope`, `confidence` (`low`, `moderate`, `high`), `status` (`hypothesis`, `supported`, `contested`), `evidence` avec `period`, `note`, `distinct_posts` vérifié ou `null`, `refs` (cinq références maximum), `limits`, `updated_on`. Confirmer, nuancer, contredire, fusionner ou laisser inchangé selon les observations nouvelles. Ne pas recompter un post relu comme preuve indépendante ; ne pas affirmer un cumul exact après perte de traçabilité.

Les observations nourrissent des conseils visibles, jamais de nouvelles consignes implicites. Proposer quelques actions utiles et expliquer appui, bénéfice recherché, action et limites. Reconnaître aussi un point fort ou conseiller sur les réponses et la continuité. Aucun rapport ou conseil n'est obligatoire à chaque création.

Conserver les pistes utiles dans `experiments` : `id`, `proposal`, `basis`, `objective`, `evaluation`, `status` (`proposed`, `accepted`, `completed`, `declined`). Toute décision retenue ou refusée garde `user_confirmation` ; `accepted` et `completed` gardent aussi `scope`. Un accord ponctuel n'autorise pas les posts suivants. Vérifier que la portée est encore active ; si inconnue, ne pas appliquer la piste par défaut. `completed` signifie application achevée, sans prouver publication ou résultat ; préciser ce qui reste inconnu dans `evaluation`.

Un conseil sans données peut être suivi comme tel avant la première collecte, sans inventer de constat public. Une réussite ne rend pas une règle permanente. Proposer séparément toute modification du skill et attendre une demande explicite. Ne pas tirer de consigne rédactionnelle d'une proposition non retenue, même si son efficacité paraît probable.

## Sauvegarde sans double intégration

Sauvegarder les observations en `pending`, puis la mémoire avec une révision nouvelle et `last_batch` : `id`, `observed_at`, `applied_observations` (couples `entry_id`/`observation_id`, vingt maximum). Sauvegarder ensuite les marqueurs `applied` des posts. En cas d'interruption, réconcilier chaque couple avant un nouveau lot ; ne pas réappliquer une observation déjà présente dans le dernier lot confirmé. Pour un grand bilan, finir chaque sous-lot avant le suivant.

Une mise à jour d'un choix de coaching modifie seulement les champs concernés, date et révision ; elle ne crée ni observation, ni résultat, ni nouveau `last_batch`. Conserver limites et décisions encore utiles sans évincer une piste en cours pour un nouveau conseil. Valider avec `scripts/coaching.py`, puis sauvegarder avec la garde de version du registre.

Restituer la couverture réelle, les constats utiles, ce qui change dans la mémoire, les quelques conseils et les éventuelles limites de sauvegarde. Ce bilan ne publie pas de réponse et ne programme rien implicitement.

# Mémoire éditoriale persistante

## Source canonique

- Fichier : CONFIG_LINKEDIN_REGISTRY
- Library : CONFIG_PERSONAL_FILE_REFERENCE
- Clé interne : CONFIG_LINKEDIN_KEY ; schema_version : 1.
- Couverture initiale : productions de ce skill à partir du 22 octobre 2026 ; aucune publication antérieure importée. Une base vide n'atteste pas que le conseiller n'a rien publié.

Accéder à la version actuelle avec le skill Library avant chaque sélection ; conserver identifiants et version obtenus. Pour un registre volumineux, matérialiser puis filtrer localement avant de transmettre du texte au modèle. Ne pas utiliser une ancienne copie locale comme vérité. Ne pas recréer une base parallèle après un échec de lecture.

## Pilotage community manager

Conserver l'état de stratégie, calendrier glissant, actions ouvertes et passages dans l'objet facultatif `community_management` du même registre, selon [community-management.md](community-management.md#7-conserver-un-état-léger). Garder le schéma 1 et les entrées historiques. Les intentions de calendrier ne sont pas des posts produits : ne les ajouter à `entries` qu'après production effective. Ne pas dupliquer dans cet état les textes, médias ni la mémoire d'apprentissage. Une modification du seul pilotage ne crée pas de nouvelle version d'un texte. Le validateur existant accepte cet objet complémentaire mais n'en atteste pas la cohérence : vérifier liens aux entrées, dates, états, doublons et portée des autorisations avant sauvegarde.

Relier les recommandations choisies à `community_management.open_actions`, aux créneaux concernés et au champ facultatif `recommendation_applications` des entrées, selon [recommandations.md](recommandations.md). Une preuve doit préciser la version examinée ; après réécriture, conserver les preuves historiques et vérifier de nouveau l'application dans la nouvelle version. Les anciens posts sans ce champ ne sont ni réputés conformes ni réputés non conformes. Ne pas recopier les textes ou les commentaires dans les fiches d'action.

## Mémoire de coaching et lecture bornée

Conserver la configuration facultative de surveillance et les préférences de suggestion dans `community_management.audience_monitoring`, selon [surveillance.md](surveillance.md). Préserver ce champ lors d'une écriture éditoriale ou d'un nettoyage des posts ; ne pas transformer son absence en activation. Les observations restent dans les entrées, les enseignements dans la mémoire de coaching : la configuration ne les duplique pas.

La synthèse globale est indépendante : `CONFIG_LINKEDIN_LEARNING`, Library `CONFIG_PERSONAL_FILE_REFERENCE`, clé `CONFIG_LINKEDIN_LEARNING_KEY`. Son nom et sa clé restent stables ; elle sert de mémoire au coach. Lire sa version actuelle avant une création pour retrouver les pistes retenues encore applicables et, si utile, proposer un conseil séparé. Ses observations ne sont pas des instructions de rédaction. Son absence de résultats ne signifie pas absence de publications ; ne pas lancer une collecte pour la remplir. Si elle est inaccessible, le signaler brièvement et continuer avec les exigences éditoriales disponibles et les choix explicites de la conversation, sans inventer de consignes mémorisées ni recréer le fichier. Les modalités du coaching et de la collecte sont dans [apprentissage.md](apprentissage.md).

Pour rédiger, charger les 20 dernières fiches compactes, puis rechercher seulement les anciens sujets ou idées proches ; garder distincts ce contexte éditorial et la mémoire du coach. Employer `scripts/registre.py context CHEMIN_JSON`, `--query 'termes proches'` et, si nécessaire, `--offset 20` ; la recherche lexicale n'est pas une comparaison sémantique. Varier les termes à partir des idées développées, pas uniquement du titre. Relire les entrées retenues avec `--ids ID1 ID2` ; ne pas parcourir automatiquement tous les lots ni tous les commentaires. Si un extrait est tronqué ou un ancien index manque, consulter les textes candidats avant de conclure. Déclarer une couverture limitée si les données ne permettent pas la comparaison ; les fenêtres ci-dessous guident la recherche, pas un chargement exhaustif.

Une demande d'effacement des posts ou des sujets traités vise le registre, pas cette mémoire indépendante. Conserver la synthèse lors de ce nettoyage, sauf demande explicite de réinitialiser aussi l'apprentissage. Après suppression des sources, indiquer la traçabilité réduite et ne pas restaurer les posts effacés. La synthèse globale ne reconstitue pas à elle seule l'historique anti-répétition.

Un registre distinct existe pour la veille éditoriale : Registre-veille-editoriale.md, CONFIG_PERSONAL_FILE_REFERENCE. Ses entrées LinkedIn confirmées peuvent servir à un contrôle complémentaire en lecture seule. Ne pas le modifier ni y appliquer la règle d'enregistrement automatique de ce nouveau skill. Si ce contrôle est indisponible, ne pas prétendre couvrir cet historique.

## Historique accessible au coach

Donner au coach accès aux **365 dernières fiches de posts présentes dans le registre**, ou à toutes si elles sont moins nombreuses. Compter une fiche par post, sans compter ses versions comme des posts supplémentaires. La fenêtre est ordonnée par `created_at`, date de création de la fiche ; elle porte sur 365 posts, pas sur 365 jours. Conserver leurs statuts : un texte préparé ou refusé peut éclairer le coaching éditorial sans constituer une publication. Pour comparer les résultats du public, utiliser les dates de publication et d'observation vérifiées.

Utiliser `scripts/registre.py coach-context CHEMIN_JSON` pour un index paginé avec thèmes, idées, angles, retours du conseiller et synthèses des réactions disponibles. `--query 'termes proches'` recherche dans cette fenêtre ; `--limit 50 --offset 50` permet de la parcourir par lots, en suivant `next_offset`. Relire les textes et observations complets nécessaires avec `coach-context CHEMIN_JSON --ids ID1 ID2`. Une recherche ou un premier lot ne couvre pas les 365 posts : pour un bilan demandé sur l'ensemble, parcourir tous les lots de cette fenêtre et préciser la couverture réelle, les retours manquants et les extraits tronqués. Pour un conseil ponctuel, lire seulement les éléments utiles.

Cette consultation utilise les données déjà enregistrées et ne déclenche aucune collecte sur LinkedIn. Garder la mémoire globale courte : ne pas y recopier les 365 fiches ni les charger intégralement à chaque rédaction. Cette fenêtre n'est pas une règle d'effacement : conserver les entrées plus anciennes, et élargir la consultation si le conseiller le demande explicitement. Après un effacement demandé, exploiter les fiches restantes et la synthèse indépendante, sans reconstituer les posts supprimés ni prétendre disposer encore de leurs textes.

## Sélectionner sans répéter

Comparer lecteur, situation, problème, raisonnement, exemples, thèse et enseignement aux 20 dernières productions, aux 90 derniers jours et aux entrées plus anciennes proches par le thème **ou par l'idée**. Relire intégralement les textes proches. Chercher aussi les répétitions transversales : une idée secondaire, une chute ou le même motif concret peut revenir sous des thèmes différents. Distinguer changement de décor, d'accroche ou de vocabulaire et changement réel de raisonnement. Examiner les territoires peu explorés selon editorial.md sans déduire leur absence d'un index incomplet. Ces fenêtres sont des repères internes ajustables, sans délai minimum ni quota automatique.

Apprécier ensemble la récence, la fréquence, la place de l'idée dans les textes, les retours du conseiller et l'apport proposé. Sur un historique court, ne pas inventer de tendance. À qualité comparable, privilégier les idées et angles moins explorés. Une idée déjà utilisée reste disponible : approfondissement, autre cause, limite, conséquence, point de vue ou application qui change réellement la compréhension peuvent justifier son retour. Une reprise explicitement demandée ou un rappel utile restent possibles, même sans thèse nouvelle ; noter leur raison dans `novelty`, sans les présenter comme inédits. Ne pas forcer un angle artificiel pour satisfaire la diversité.

Avant livraison, refaire cette comparaison sur le texte final, car son développement peut revenir à une idée récurrente absente du brief. Pour une reprise proche sans apport ni raison identifiable, réorienter le développement ou préférer une autre piste. Ne pas bannir une idée parce qu'elle revient souvent ; distinguer lassitude liée à sa répétition et désaccord de fond. Conserver les refus avec leur portée, sans étendre un conseil rejeté à tout son thème. Après un effacement, utiliser les préférences et retours encore conservés comme limites qualitatives, sans restaurer les posts ni affirmer un décompte. Renseigner le lecteur dans audience et la comparaison utile dans novelty ; ne pas créer de registre ou de quota supplémentaires. Les notes internes ne prouvent pas la satisfaction du conseiller ; ses retours explicites sur la version concernée priment.

## Ce qui est mémorisé

Enregistrer les productions effectivement retenues et livrées, même non publiées, pour ne pas les reproposer sans raison. Ne pas enregistrer chaque idée explorée en interne. Conserver les rejets et corrections du conseiller avec leur motif. Ne jamais assimiler un post préparé, une approbation ou une image créée à une publication réelle.

Statuts autorisés :

| Valeur | Sens |
| --- | --- |
| prepared | Livrable relu et complet dans le périmètre demandé |
| incomplete | Élément requis manquant ou contrôle non terminé |
| approved | Version explicitement validée par le conseiller |
| published | Publication confirmée par le conseiller ou preuve lue dans un outil |
| rejected | Version ou sujet écarté par le conseiller |

Ne pas employer approved pour la note du reviewer. Lier toute confirmation à la version concernée ; une réécriture non encore approuvée revient à prepared ou incomplete, sans effacer les confirmations des versions antérieures.

## Structure d'une entrée

Champs obligatoires :

- id : identifiant stable unique, par exemple UUID ; created_at : date ISO avec fuseau.
- pillar, subject, scene, thesis, takeaway : pilier, sujet, situation, position et enseignement, chacun exprimé précisément.
- angle : point de vue précis et mécanisme choisis pour traiter le sujet ; ni simple titre ni nom de format.
- ideas_developed : liste des idées effectivement développées dans le texte final, sous la forme `{ "idea": "proposition précise", "role": "central|supporting|conclusion" }`. Retenir les idées significatives, y compris secondaires et de conclusion, sans quota et sans découper chaque phrase. Utiliser des formulations comparables d'un post à l'autre ; un mot-clé comme « autonomie » ne suffit pas. Une même idée centrale reprise en conclusion ne nécessite pas deux éléments.
- hook, text : accroche et texte réellement livré, conservés intégralement.
- status : valeur du tableau ; scope : full, text_only ou brief.
- visual : objet avec state = created, missing ou not_requested ; concept, prompt, alt_text et référence d'artefact disponible. Conserver aussi identité de référence et mode portrait/scène/métaphore.
- version : entier positif, initialement 1, incrémenté après correction ; versions : liste des versions antérieures. Avant une correction, y conserver une copie complète de la version précédente sans imbriquer son propre historique, avec date et motif.

Champs à renseigner selon le travail : updated_at, run_id pour reprise, audience, tension, format, sources, review, novelty, user_confirmation, publication_evidence, published_at, publication_url, feedback et metrics. review doit exister pour un livrable complet ; conserver le mode indépendant ou auto-relecture, la version revue, le verdict qualitatif, l'enjeu concret et la tension, l'apport identifié et les passages qui les portent, l'attente créée envers le conseiller, l'objection décisive, les corrections et les limites. Ne plus exiger de notes chiffrées ; préserver les anciennes comme historique sans les convertir artificiellement. novelty doit donner l'entrée la plus proche ou indiquer l'absence d'entrée, puis expliquer l'apport ou la raison de la reprise. Ajouter `compared_entries` (identifiants pertinents), `recurrence_assessment` (idées communes, récence, fréquence observée et différence d'angle) et `reuse_reason` lorsqu'une reprise est retenue. Ne pas revendiquer une nouveauté sur le seul changement de thème ou de scène.

Pour les anciennes entrées, préserver la compatibilité du schéma 1 : l'absence de `angle` ou `ideas_developed` signifie « non encore indexé », pas « idée jamais abordée ». Compléter ces champs seulement depuis le texte conservé réellement lu ; indiquer `idea_index_source` avec la version du texte, la date d'indexation et l'origine « analyse du texte conservé ». Ne pas restaurer un historique volontairement effacé. Cet enrichissement de métadonnées ne change ni le texte, ni sa version, ni son statut et ne vaut pas approbation du conseiller. Lors d'une réécriture, conserver l'ancien index avec l'ancienne version et indexer le nouveau texte.

Pour chaque source effectivement utilisée, conserver titre, auteurs ou organisme, date, URL, proposition soutenue, section consultée et limite de transposition, selon references/sources-fond.md. Ne pas enregistrer toute la bibliographie générale comme si elle avait été exploitée pour ce post.

Un rejet utilisateur invalide l'appréciation positive interne pour la version concernée. Conserver les anciennes revues et ajouter le retour qui les contredit ; ne pas effacer l'échec. Une mise à jour de statut ou de feedback sans réécriture ne crée pas une nouvelle version du texte. Les essais internes d'audit ne sont pas des productions éditoriales à enregistrer.

Pour les nouveaux visuels, ajouter `visual.direction` (brief retenu : accroche, moment, action, expression, intensité, regard, posture, cadrage) et `visual.observed` (caractéristiques réellement constatées après inspection). Conserver la comparaison aux visuels récents et les différences utiles dans `visual.variation_review`. Laisser les attributs anciens non observés inconnus ; ne pas les reconstruire depuis un prompt comme s'ils avaient été vérifiés. Distinguer dans les retours l'appréciation du texte et celle du couple image–accroche ; ne jamais valider l'ensemble sur la seule satisfaction concernant le texte.

Pour une production suivant le protocole critiques–décideur de relecture.md, conserver dans `review` les `critics` (rôle, agent, versions examinées, constats et preuves), l'`arbitration` (agent distinct, décision et traitement des remarques), les `cycles` et les limites éventuelles. Ces champs complètent le schéma existant ; préserver les revues historiques sans leur attribuer rétroactivement des contrôles non faits. Un retour utilisateur négatif prime sur les arbitrages internes, avec sa portée exacte ; ne pas transformer une demande d'amélioration du style en interdiction du thème.

Pour approved, conserver user_confirmation (texte, date, version concernée). Pour published, conserver aussi publication_evidence (confirmation ou URL et origine de la preuve). Un lien seul non consulté ne prouve pas le contenu publié. La date de publication peut rester inconnue ; ne pas utiliser celle de génération à sa place.

Pour un visuel généré dont aucun identifiant durable n'est exposé, conserver un null explicite avec la note « identifiant durable non exposé ». Ne pas inventer d'URL ni de fichier. Pour un brief demandé seul, state = not_requested. Pour une commande complète avec image manquante ou remise du fichier non résolue, status = incomplete.

Dans `visual.delivery`, séparer les faits de livraison : `render_state` (pending, emitted ou failed), `file_reference` (référence réellement obtenue, sinon null), `file_verified` (booléen), `final_link_included` (booléen), `user_reported_missing` (booléen) et, seulement si fournie, `user_receipt_confirmation`. Garder `visual.state = created` si l'image existe mais que la livraison a échoué. Un champ de planification n'est pas une preuve d'émission. Si la sauvegarde précède la réponse finale, laisser les champs non encore réalisés à leur état exact ; les réconcilier au prochain accès au registre à partir de la réponse effectivement envoyée, sans prétendre qu'ils ont déjà eu lieu. Un signalement d'absence reste non résolu jusqu'à la réparation effective de l'accès ; ne pas déduire la réception utilisateur d'un succès d'outil. Ajouter le retour à la même entrée sans perdre ses versions ni créer un nouveau post.

Pour un nouveau visuel composé, conserver dans `visual.typography` la référence de la preuve de composition et le résultat du vérificateur : empreintes du fichier final, de la charte et de la police. Relier ces éléments au fichier effectivement sauvegardé et livré. Distinguer assemblage vérifié, inspection visuelle et appréciation éditoriale ; aucun de ces contrôles ne prouve les autres. Dans la revue du texte, noter les qualités préservées lorsqu'une correction pouvait les affecter, sans ajouter de score ni de formulaire obligatoire.

metrics : données observées seulement, avec date, fenêtre et source ; laisser les valeurs absentes à null, jamais à zéro par défaut. Séparer appréciations qualitatives et compteurs. Ajouter les préférences explicites dans preferences avec leur source ; ne pas transformer une seule performance en règle définitive.

Réserver `feedback` aux retours éditoriaux existants, notamment ceux du conseiller ; enregistrer la dernière observation du public dans `audience_review` selon apprentissage.md. Ce champ n'entre pas dans le contexte ordinaire de rédaction. Une collecte ne change ni le texte livré ni sa version ; une différence avec la publication réelle se conserve séparément. Ne pas accumuler les commentaires bruts ou une liste illimitée de bilans dans chaque entrée.

## Brief canonique avant production

Pour un nouveau contenu autorisé, conserver le contrat du CM dans `community_management.editorial_briefs[brief_id]`, objet indexé par identifiant stable, dans ce même registre. Reprendre le modèle `assets/brief-editorial.json` du CM ; `brief_id` doit correspondre à la clé et `revision` est un entier positif. `entree_canonique` identifie le registre et l'emplacement du brief (identité Library et chemin JSON), avant comme après production. Ne pas créer d'entrée dans `entries` pour une simple intention. La révision du brief n'est pas la version du post.

Calendrier et consultations portent `brief_id` ; leurs résumés éventuels référencent la révision consultée, sans seconde autorité éditoriale. Lorsqu'une production existe réellement, son entrée conserve `brief_id` et `brief_revision`, révision dont elle est issue. Le brief reste au même emplacement ; `diffusion_registre_reference` peut alors référencer l'entrée et sa distribution. Le projet vidéo utilise ce même emplacement comme `editorial_brief.canonical_ref`, avec `revision_read` ; ni copie concurrente ni déplacement du brief.

Les états du brief (besoin, proposition, production, contrôle, prêt, report) décrivent le travail et ne deviennent pas des statuts de post. Un changement substantiel incrémente sa révision et invalide les contrôles affectés. Une production active restée sur une ancienne révision doit être rapprochée et marquée `incomplete` tant que sa concordance n'est pas établie ; préserver versions, approbations antérieures et reçus historiques. Une entrée déjà publiée demeure le témoignage de sa version réellement publiée : ne pas modifier son statut pour un nouveau brief ; conserver l'écart et reprendre par une adaptation distincte autorisée.

Le validateur vérifie les identifiants et révisions présents ; il n'atteste ni la qualité du fond, ni la réalité d'une consultation, ni la fermeture des réserves. L'ajout de cette extension au schéma 1 ne migre pas les anciennes entrées et n'autorise pas à réécrire le registre vivant pendant une maintenance de skill.

## Média vidéo dans une entrée

Pour une vidéo, conserver le champ historique `visual` pour une éventuelle couverture (`not_requested` si aucune) et ajouter `media` :
- `kind: video`, `state: created|missing` ;
- `file_reference`, `version` (chaîne stable), `project_reference` ;
- `duration_seconds` mesurée, ou null si non connue ;
- `review_reference` vers les rapports du fichier/version exacts ; `reviewed_version` égale à `version` seulement après les revues requises ;
- `delivery` pour les mêmes faits de remise que visual.delivery, appliqués au MP4.

Une production vidéo complète exige un fichier vidéo accessible et contrôlé, son projet, le brief lié, la révision concordante, les revues indépendantes et les perceptions nécessaires selon production-video.md. Un PNG de couverture avec `visual.state = created` ne ferme pas ce contrôle. Sans fichier ou avec revue/écoute/visionnage requis manquant, conserver `status = incomplete`, même si le fichier a été exporté. Les champs de revue ne doivent pas être remplis par anticipation. Pour une vidéo volontairement muette, le rapport indique que l'écoute vocale est sans objet.

Le validateur vérifie la présence et la cohérence de ces références pour une vidéo annoncée complète, pas leur contenu ni l'accessibilité distante. Les contrôles du fichier et de la livraison restent obligatoires. Les productions statiques historiques gardent leur structure et leurs exigences ; les attributs photo de visual.direction et visual.typography ne s'appliquent qu'au support correspondant.

## Lire et contrôler localement

Utiliser scripts/registre.py validate CHEMIN_JSON pour vérifier la structure, les statuts et les doublons de texte normalisé. Utiliser scripts/registre.py context CHEMIN_JSON pour les extraits bornés et la diversité des piliers ; `--ids` renvoie les entrées exactes demandées. Le script ne lit ni n'écrit à distance et ne détecte pas la similarité de sens : effectuer la comparaison sémantique décrite dans SKILL.md, en relisant les entrées proches intégralement. Ne pas exécuter Python avec -O, qui désactive les assertions de ce validateur.

## Sauvegarder sans écraser l'historique

1. Lire la version actuelle. Pour reprendre un travail interrompu, retrouver l'entrée par id/run_id ou contenu et ne pas la dupliquer.
2. Ajouter l'entrée ou mettre à jour uniquement l'entrée concernée, en conservant versions, préférences, autres entrées et champs inconnus.
3. Vérifier la copie locale avec le script si disponible. Ne pas faire passer un avertissement de texte identique pour un contrôle sémantique réussi.
4. Remplacer la même identité Library ; passer expected_current_version lorsqu'une version concrète est disponible, selon le skill Library. Ne jamais supprimer une garde pour résoudre un conflit.
5. En cas de conflit, relire, fusionner uniquement la modification visée et réessayer. Sérialiser les écritures ; un seul rédacteur écrit, le reviewer reste en lecture seule. Si aucune version n'est exposée, relire juste avant l'écriture et indiquer cette limite de concurrence en interne ; ne pas prétendre à un verrou inexistant.
6. Annoncer l'enregistrement seulement après succès. En cas d'échec, conserver le livrable et signaler que son enregistrement reste à faire ; ne pas garantir l'absence de répétition future. Ne pas créer un second registre pour masquer l'échec.

Le registre est une donnée de travail persistante, pas un fichier à committer dans le skill à chaque post. Une modification des instructions ou des actifs du skill se sauvegarde séparément avec le workflow de création de skills.

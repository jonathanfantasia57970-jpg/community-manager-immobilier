# Registre et mesure

## Persistance

Nom canonique : **CONFIG_GOOGLE_REGISTRY**. À la première production ou analyse utile, utiliser le skill Library et rechercher le titre exact avant création. Si absent, initialiser depuis `assets/registre-template.json` ; ce modèle ne contient aucun historique réel. Ne pas modifier les registres Facebook ou LinkedIn ni conserver l'historique opérationnel dans le dépôt des skills.

Lire la version actuelle, conserver l'identifiant durable, remplacer le même fichier et respecter le contrôle de version s'il existe. En cas de conflit, relire et réconcilier par identifiant stable. Une erreur de lecture n'autorise pas la remise à zéro ni un registre parallèle. Si l'enregistrement échoue, le signaler et ne pas prétendre avoir mémorisé.

Pour écrire, lire les 12 dernières productions, les angles et retours pertinents, puis les textes proches. Pour un bilan, charger les périodes évaluées. Un brouillon compte pour la variété, jamais comme post publié.

## Brief canonique

Conserver le brief dans la collection facultative racine `editorial_briefs[brief_id]` du même registre. Garder `brief_id`, `revision`, sujet/angle/apport/preuve/nuances, destination exacte, `decision_format`, contributions et décision selon le contrat CM. Une intention n'est pas une entrée produite : ne pas ajouter de faux post à `entries`. Lier l'entrée réellement créée et les relais par `brief_id` et `brief_revision` ; la version du média/post reste distincte. Le projet vidéo référence ce brief, sans deuxième autorité éditoriale. Préserver les anciennes entrées et champs inconnus ; aucune migration réelle n'est déclenchée par la mise à jour du modèle.

## Entrée de contenu

Conserver : identifiant stable, canal, type, date de création, question, public, pilier, angle, idées développées, enseignement, localité pertinente, texte exact, nombre de caractères, appel à l'action, sources et dates, référence durable du média et origine réelle/illustrative, statut, portée autorisée, cible, date prévue avec fuseau, id/uuid Metricool, URL de planning, URL publique éventuelle et historique des changements.

États : `draft`, `approved`, `scheduled`, `published`, `failed`, `unknown`, `cancelled`. Seuls un retour d'outil ou un constat explicite justifient un état de diffusion. Un second passage reprend le même identifiant. Une disparition du planning est ambiguë.

Séparer faits observés, commentaires du conseiller, hypothèses et tests proposés. Une note interne n'est pas son approbation. Conserver les refus utiles, pas les détails sensibles des clients. Stocker séparément une synthèse des angles récents pour accélérer la reprise.

## Indicateurs

Priorité : contacts qualifiés, rendez-vous vendeurs et mandats si le suivi les fournit ; ensuite clics d'appel et de site ; puis visibilité Search/Maps, requêtes pertinentes, avis et activité de contenu.

Un clic d'appel n'est ni un appel abouti ni un prospect unique. Sans suivi commercial, écrire « inconnu » et non zéro. Un Sheet n'est pas obligatoire : proposer un suivi simple si utile. Des UTM peuvent aider pour les visites depuis un lien, pas attribuer les appels ou ventes.

## Fenêtres comparables

Privilégier 28 jours complets contre les 28 précédents. Exclure par défaut les sept derniers jours pour tenir compte du retard annoncé de certaines métriques (5 à 6 jours) ; afficher les dates exactes. Pour les requêtes, utiliser des mois complets dont les données sont arrivées. Si l'historique est court, indiquer l'insuffisance, sans fabriquer de comparaison.

Considérer saison, campagnes, changements de fiche, données manquantes et petits volumes. Ne pas sommer des portées comme des visiteurs uniques. Avec un dénominateur nul ou absent, afficher « non calculable ». Une corrélation temporelle n'établit pas que les posts ont amélioré le classement.

Après quatre semaines, vérifier d'abord qualité et régularité. Après huit, proposer une hypothèse prioritaire et un test borné : angle, format, action ou cadence. Éviter de tout changer en même temps. Les données autorisent une recommandation, pas une diffusion ou une modification permanente des fondamentaux.

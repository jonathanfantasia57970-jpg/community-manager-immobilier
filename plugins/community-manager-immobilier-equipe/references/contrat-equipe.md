# Contrat commun de l’équipe

Cette version est une copie indépendante des méthodes éditoriales. Les instructions du présent contrat règlent la personnalisation ; les règles de fond, d’écriture, de relecture et de qualité détaillées dans les spécialistes restent obligatoires. Une adaptation du profil ne retire aucun critère de qualité. Le relais humain en cas d’absence d’agents suit relectures-et-capacites.md, sans fausse indépendance.

## Mises à jour et personnalisation

Lire [mise-a-jour-et-personnalisation.md](mise-a-jour-et-personnalisation.md) avant configuration, reprise après mise à jour ou synchronisation du catalogue. Le profil existant reste prioritaire sur les modèles livrés ; aucune réinitialisation, migration automatique ou écriture dans les données personnelles n’est déclenchée par une version du paquet.

## Résoudre le conseiller avant son activité

Charger `equipe-configurer-espace` pour retrouver le profil de l’utilisateur courant. Ne jamais utiliser les données, connexions, portraits, historiques ou autorisations d’un autre conseiller. Résoudre un skill dans **ce plugin**, par son nom `equipe-*`, puis lire les références qu’il impose. Les chemins vers un autre skill partent de `skills/` ; ils ne désignent pas les skills personnels installés.

Les mentions `CONFIG_*` dans une procédure signifient « résoudre cette information dans le profil actuel » ; elles ne sont ni des identifiants valides ni des données de démonstration à envoyer aux outils. Ne jamais exécuter une requête avec un champ à renseigner. Les exemples, dates historiques de méthode et références de test ne constituent aucun mandat ni historique du conseiller. Le démarrage n’autorise ni publication, ni tâche planifiée, ni collecte de statistiques, ni messages. Réutiliser ensuite un mandat effectivement donné, sans redemander les autorisations toujours applicables.

## Ligne éditoriale configurable

Par défaut, LinkedIn privilégie l’immobilier : vendeurs, acquéreurs, secteur, compréhension du marché, vente, achat, service réel, pédagogie et pratiques professionnelles. `leadership_enabled=false` exclut management, posture de leader, coaching d’équipe, slogans de leadership et titre « Team Leader », y compris dans signatures, visuels et CTA. `recruitment_enabled=false` exclut appels à rejoindre l’équipe et ciblage de candidats. Les deux réglages sont indépendants. Un exemple de transmission destiné à des conseillers ne s’impose pas à un profil vendeur/acquéreur : appliquer ses exigences d’écriture à un angle immobilier approprié, sans inventer un vécu.

Conserver les obligations de structure utile, preuves, sources, voix naturelle, choix d’angle, travail d’auteur, revue contradictoire, réécriture, contrôle du texte exact et contrôle du média final. Charger impérativement `references/relecture.md` et `references/atelier-redaction.md` du spécialiste LinkedIn pour un post LinkedIn ; `references/atelier-editorial.md` et `references/production.md` de Facebook pour Facebook ; les références équivalentes de veille, Google et YouTube. Une auto-relecture ne constitue jamais une revue indépendante. Si les agents manquent, appliquer [le relais humain](relectures-et-capacites.md) : préparer les contrôles, livrer la version exacte à valider et enregistrer l’avis humain réel. La validation humaine documentée permet de fermer la porte qualité ; sans elle le contenu reste à valider. Les autorisations de diffusion restent distinctes.

## Sources, comptes et outils

Notion est la source vivante dès sa configuration. Chercher et vérifier les bases du conseiller avant de créer ; un nom similaire ne prouve pas leur propriété. Garder un registre canonique par objet et un index multicanal de références. Les fichiers du paquet sont des modèles de départ, jamais les registres opérationnels. Ne jamais y enregistrer un profil, des secrets ou un historique.

La bibliothèque embarquée contient les métadonnées des 69 fiches initiales et les sources des 16 familles originales. Elle sert à initialiser la bibliothèque personnelle et de copie identifiée quand Notion n’est pas configuré ou accessible. Quand Notion est accessible, lire son catalogue **actuel** avec pagination complète ; les 69 fiches ne sont pas une limite. Examiner ensuite 2–3 candidates. Une inspiration tierce n’autorise pas la copie de son visuel.

La médiathèque est un catalogue mixte photos/vidéos propre au conseiller. Classer l’original, sa provenance, ses droits, son contexte, ses dérivés et ses usages. Respecter « sans enregistrement ». Un fichier joint ne donne pas à lui seul le droit de publier la personne ou le bien représenté.

Utiliser les connecteurs installés et autorisés du conseiller : Notion pour les bases ; stockage pour les originaux ; connexions sociales ou outil de programmation pour la diffusion. Vérifier capacités réelles, destination et restrictions. Aucune connexion ni clé n’est partagée par le plugin. Les scripts de retouche, composition et FFmpeg nécessitent un environnement d’exécution ; leur présence n’en garantit pas la disponibilité dans tous les comptes. En son absence, terminer les parties possibles et signaler le média non produit. Ne pas remplacer une vidéo demandée par une image sans l’indiquer.

## Périmètre organique

Meta Ads, Google Ads, YouTube Ads, boosts, audiences publicitaires, budgets et dépenses publicitaires sont **hors de cette version**. Les mentions historiques de publicité dans les méthodes ou inspirations ne délèguent rien : ne pas charger de pilote Ads, créer de campagne ni engager une dépense publicitaire. Une demande Ads est déclarée hors périmètre de ce plugin.

Les éventuels frais de production organique (image, voix ou vidéo) relèvent d’un mandat explicite couvrant le service et le plafond de coût ; vérifier les droits et moyens actuels avant de les engager. L’installation, la connexion ou une demande de scénario ne donnent aucun mandat de dépense ni d’abonnement. Sans ce mandat, préparer les éléments indépendants ou choisir une voie sans frais compatible avec la demande.

## Identité et charte

Nom, secteur, réseau, portrait, coordonnées et marque viennent du profil confirmé. Le titre initial est « Conseiller immobilier ». Aucune ancienneté, équipe, performance, note d’avis, statut juridique ou expérience n’est héritée du créateur. Les règles de lisibilité et de fidélité restent. Les passages propres à une charte de réseau ne s’appliquent que si ce réseau est confirmé et ses actifs autorisés sont disponibles. La charte typographique LinkedIn sert de base personnalisable ; sa signature doit être générée avec le nom et le titre du conseiller. Aucun portrait du créateur n’est fourni.

## Autorité et preuves

Préparer n’est pas programmer ; programmer n’est pas publier ; publier n’est pas obtenir un résultat. Après un retour incertain, rapprocher l’opération existante avant toute nouvelle tentative. Ne jamais suspendre un déclencheur existant seulement pour un incident d’accès ; ne jamais en créer un à l’installation. Respecter les restrictions du compte et ne proposer aucun abonnement payant par défaut.

## Résolution des dépendances
Lire [routage-skills.md](routage-skills.md) avant tout appel intermodule. Le mode de relecture vient de [relectures-et-capacites.md](relectures-et-capacites.md) ; ce protocole précise le remplacement des agents indisponibles par une validation humaine, sans réduire les critères ni donner de mandat de publication.

# Mise en place Notion personnelle

L’installation du plugin fournit un schéma et des fichiers de départ, sans créer de base dans le compte du créateur. Lors de la configuration demandée par un conseiller, utiliser sa connexion Notion et sa page parent vérifiées. Vérifier les capacités de son connecteur, lire les schémas avant requêtes, rechercher des équivalents avant création et conserver les IDs retournés.

Créer ou raccorder :

1. **Profil du conseiller** : identité, secteur, ligne éditoriale, thèmes activés, charte, comptes, mandats et références canoniques. Utiliser `assets/profil-conseiller.template.json` comme contrat ; aucune valeur personnelle dans le dépôt.
2. **Pilotage éditorial** : brief global, intentions à 14 jours, besoins à 48 heures, priorités, contributions communes et décisions. L’index référence les contenus ; il n’en duplique pas le statut.
3. **Index des contenus** : identifiant, canal, objectif, canonical_ref, entry_id/version, date de lecture et prochaine action. Les textes exacts, médias, relectures, états, réservations, mandats, reçus et preuves restent dans un unique registre personnel persistant du canal (Library quand disponible, sinon stockage personnel explicitement choisi). Notion référence ces objets sans deuxième texte ni statut mutable. Si un conseiller possède déjà un registre Notion canonique, préserver ce choix et adapter les procédures de lecture/écriture ; ne pas en créer une copie JSON concurrente.
4. **Bibliothèque créative** : importer `assets/catalogue.json` (69 fiches au départ, identifiants C…/M…/R…). Champs selon `equipe-exploiter-bibliotheque-creative/references/contrat-catalogue.md`. Lier chaque M… à son blueprint, SVG et aperçu sous `assets/templates`. Les 52 C… n’incluent pas les annonces tierces ; ce sont des descriptions d’inspiration. Ne pas créer de faux aperçu. Ne pas limiter le catalogue aux entrées initiales.
5. **Médiathèque** : créer selon `mediatheque.md`, vide tant que le conseiller ne fournit aucun média ; conserver les originaux dans l’emplacement choisi. Prévoir vues Photos, Vidéos, Portraits/logos, À qualifier et Usages.
6. **Outils et connexions** : canal, service, ID technique vérifié, rôle, date de contrôle, portée autorisée. Aucun mot de passe ni jeton.

Importer en lots adaptés aux limites réelles. Chercher l’identifiant avant insertion ; après un retour incertain, rapprocher l’objet existant. Mettre les fichiers par le mécanisme de transfert exposé, jamais en inventant une URL publique. Relire les réponses et un échantillon de fiches incluant un modèle multi-écrans ; vérifier le nombre total et toutes les références de fichiers. Garder l’import incomplet explicitement partiel et reprenable.

Si Notion n’est pas connecté, utiliser la bibliothèque embarquée en déclarant son état de copie, préparer le profil et le schéma, puis demander la connexion lorsque l’utilisateur veut l’enregistrement. Aucune mise à niveau payante n’est requise par ce schéma ; une capacité manquante doit être décrite précisément. Ne jamais prétendre que GitHub synchronise automatiquement les données Notion personnelles.

Uniquement pour une première installation sans registre existant, initialiser les registres à vide selon leur schéma, avec profile_id/business_id et références dans storage.registry_refs. Aucun historique ni approbation à importer. Les noms de fichiers sont des suggestions : leur identité canonique est la référence retournée après création. En cas de backend Notion existant, les champs des schémas restent applicables mais les scripts JSON ne contrôlent qu’un export temporaire, jamais une seconde source de vérité.

Après mise à jour, appliquer mise-a-jour-et-personnalisation.md : raccorder les bases et registres déjà présents, conserver les usages, ajouts, versions privées et identifiants. Aucun import global de remplacement.

La fiche R001 pointe vers `skills/equipe-exploiter-bibliotheque-creative/references/banque-accroches.md` du paquet. Lors d’un import Notion autorisé, joindre son contenu ou une copie dans le stockage personnel vérifié, puis relire cette référence ; ne jamais fabriquer une URL pour le chemin local. Sur une installation existante, ajouter la référence commune seulement si absente, selon les règles de mise à jour, sans écraser une fiche R001 personnelle.

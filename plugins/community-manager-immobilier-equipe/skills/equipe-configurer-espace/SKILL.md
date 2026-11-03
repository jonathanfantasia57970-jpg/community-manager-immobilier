---
name: equipe-configurer-espace
description: "Configurer le plugin Community Manager Immobilier pour un conseiller : profil personnel, secteur, LinkedIn sans leadership, connexions, Notion, bibliothèque incluse et médiathèque photo/vidéo."
---
## Routage et relecture du plugin

Pour appeler un autre module ou lire ses références, appliquer `../../references/routage-skills.md`. Pour toute revue de contenu, appliquer `../../references/relectures-et-capacites.md` : utiliser les agents réellement disponibles ou le relais humain documenté, sans inventer de contrôle indépendant.


# Configurer l’espace du conseiller

Lire `../../references/contrat-equipe.md`, `../../references/configuration.md` et `../../references/notion-installation.md`. Une configuration modifie les copies et ressources du conseiller, jamais les skills personnels du créateur.

Avant toute initialisation, lire `../../references/mise-a-jour-et-personnalisation.md`. Une reprise après mise à jour ne relance pas cet onboarding : lire le profil existant, conserver toutes ses valeurs et ne proposer que les ajouts utiles.

1. Rechercher un profil de ce plugin appartenant à l’utilisateur courant. Réutiliser son identité et ses décisions vérifiées ; ne pas importer automatiquement celles d’un autre compte. Si le profil est absent, préparer une copie de `../../assets/profil-conseiller.template.json` dans son espace personnel.
Définir avec le conseiller son ton, ses exemples approuvés, les formulations à éviter et ses préférences par canal dans `editorial.communication`, sans importer celles du créateur.

2. Demander en un petit groupe les seules informations essentielles manquantes : nom et titre public, réseau/marque, secteur, canaux souhaités, emplacement Notion et médias. Le fuseau est celui confirmé du conseiller ; ne pas appliquer une heure de lancement par défaut. Les coordonnées publiques sont facultatives et ne deviennent publiques que sur demande appropriée.
3. LinkedIn démarre avec immobilier prioritaire, leadership et recrutement désactivés. Présenter ces options simplement, sans imposer un ratio de publications. Activer un thème seulement sur choix du conseiller. Un choix de thème ne retire aucune règle d’écriture ou de revue.
4. Vérifier les connexions réelles et identités des comptes. Notion, comptes sociaux et stockage appartiennent au conseiller. Aucune clé ni connexion du créateur n’est incluse. L’absence d’un service ne bloque pas la préparation indépendante. Ne pas proposer un abonnement collectif ou payant comme condition générale.
5. Quand le conseiller demande la mise en place Notion, retrouver les bases existantes, puis créer uniquement les ressources manquantes sous la page qu’il a choisie, selon `notion-installation.md`. Lors de la première installation seulement, importer les 69 fiches sans historique d’usage ; lors d’une mise à jour, effectuer un rapprochement par origine/identifiant sans écraser les adaptations ni l’historique et relier les 16 modèles avec leurs fichiers et aperçus. Vérifier chaque création ou import ; une réponse incertaine exige recherche par clé avant reprise. Tant que les ressources ne sont pas créées, dire « schéma prêt », jamais « Notion installé ».
6. Configurer la médiathèque avec `equipe-gerer-mediatheque`. Accepter les photos/vidéos actuelles ; aucune photo personnelle n’est requise si le canal n’en a pas besoin. Pour un visuel LinkedIn exigeant le visage, utiliser le portrait autorisé du conseiller ou signaler le média en attente, sans lui substituer celui d’une autre personne.
7. Générer hors du plugin une copie de la charte LinkedIn avec le nom, le titre et les couleurs confirmés. Utiliser `scripts/configurer_charte.py` du spécialiste LinkedIn avec le profil, puis passer le chemin renvoyé par `CM_CHARTE` aux scripts de composition et vérification. Le plugin reste immuable ; ne pas partager cette charte personnalisée dans GitHub.
8. Enregistrer les références réellement créées et la portée de chaque mandat dans le profil personnel. Garder publications, messages, programmation et récurrences non autorisés tant qu’aucune demande correspondante n’a été donnée. L’onboarding ne lance aucune campagne.
9. Vérifier par lecture un profil, la bibliothèque, une entrée de médiathèque si disponible et chaque compte retenu. Rendre un bilan exact : configuré, à renseigner, non connecté, non testé. Le premier brouillon de test peut se faire sans diffusion ni tâche planifiée.

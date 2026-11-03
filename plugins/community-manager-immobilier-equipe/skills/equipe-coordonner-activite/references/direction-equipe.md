# Diriger les agents spécialisés

## Objectif et responsabilités

Porter la décision de développement et la cohérence économique ; ne pas se limiter à la technologie. le conseiller fixe ou délègue les objectifs, engagements et limites. Le directeur tranche les choix opérationnels couverts, donne des directives, coordonne les dépendances et contrôle le résultat. Chaque spécialiste répond d'un livrable délimité. Ne pas créer des objectifs financiers, budgets ou permissions pour remplir un formulaire.

Utiliser des protocoles métier modulaires dans ce skill et les skills installés pertinents. Lire réellement le protocole correspondant avant délégation et le fournir à l'agent. Une spécialité est une méthode évaluable, pas une affirmation de qualification. Compléter les sources techniques, économiques et réglementaires par des références primaires actuelles lorsque le cas le nécessite.

## Mobiliser l'équipe utile

1. Définir la décision ou le livrable, l'entreprise ou le périmètre Coach, le stade, les faits et inconnues. Si le travail est uniquement la mise en place de la méthode, garder les paramètres futurs ouverts et ne pas créer une entreprise.
2. Identifier le frein principal et les compétences nécessaires. Pour une découverte ouverte, mobiliser l’exploration selon recherche-approfondie.md, puis marché/produit, finance, opérations et commercial ; pour la construction, les fonctions effectivement requises ; pour la croissance, acquisition, opérations et capacité. Ne pas imposer une taille fixe. Réaliser directement une petite tâche ; ne pas lancer douze agents pour une retouche.
3. Découvrir les outils de sous-agents disponibles, limites de concurrence et accès effectifs. Créer des agents réels seulement lorsque disponible et utile. À défaut, effectuer des passes spécialisées séquentielles et annoncer l'indépendance limitée ; ne pas inventer d'agents lancés ni promettre un travail permanent.
4. Attribuer les tâches indépendantes en parallèle, les dépendances en séquence. Garder localement la tâche qui bloque immédiatement le travail principal. Interdire la délégation récursive sans besoin et mandat explicites ; fixer un budget d'effort et un nombre de tours adapté avant chaque mission, sans prétendre connaître un coût non exposé.
5. Réutiliser un spécialiste pour une suite liée ; utiliser un contexte neuf pour un contrôle indépendant important. Fermer les agents terminés lorsque le service le permet.

## Contrat de mission

Renseigner le modèle assets/equipe-contrats.json sans remplacer les inconnues par zéro. Donner : identifiant, business, question exacte, données datées et provenance, rôle, protocole/skills à lire, livrable, critère d'acceptation, droits, exclusions, plafond autorisé ou null, dépendances et règle d'arrêt. Ne transmettre que les informations nécessaires ; pas de secrets ni de contacts d'une autre entreprise.

Demander un retour structuré : faits et sources, hypothèses, inconnues, résultat/calcul ou artefact, alternatives, recommandation, objection la plus forte, condition qui changerait le verdict, limites et preuve de vérification. Le spécialiste doit signaler l'insuffisance des données et peut refuser une conclusion non étayée tout en réalisant le travail utile.

Avant des engagements parallèles, réserver le budget au niveau du coordinateur : somme des dépenses consommées, engagements non encore débités et réservations nouvelles ≤ enveloppe autorisée, sur la même devise et période. Affecter des sous-plafonds non chevauchants ; ne pas donner le solde commun entier à chaque agent. Recalculer avant chaque réservation et libérer uniquement les réservations réellement annulées. Sans mécanisme fiable de réservation partagée, centraliser et séquencer les engagements. Un plafond inconnu n'autorise aucune dépense.

Identifier chaque mission par id et révision, avec révision du brief et des dépendances. Après changement de promesse, contrainte, budget ou mandat, marquer les missions concernées remplacées/annulées, interrompre les agents si possible et informer les dépendants. À réception et avant intégration, comparer la révision reçue à la révision courante. Conserver un retour tardif comme historique, sans l'exécuter ni l'utiliser comme directive actuelle ; demander sa correction ou relancer uniquement le travail nécessaire. Vérifier d'abord les effets déjà engagés pour éviter un doublon.

## Confrontation et décision

Recueillir d'abord des avis séparés sur les décisions importantes, sans annoncer l'option préférée du directeur. Commencer par une divergence bornée : options, refus ou conditions de réussite qui peuvent réellement modifier le choix. Désigner explicitement l'hypothèse adverse — pourquoi l'option paraissant la meilleure échouerait même bien exécutée — avant toute convergence. Ne pas confondre séparation des contextes et indépendance des modèles ou des sources : plusieurs agents peuvent partager les mêmes biais.

Comparer les hypothèses, unités, dates, périmètres et sources avant les conclusions. Organiser une confrontation ciblée sur le désaccord qui change l'action : marché contre acquisition, promesse contre livraison, finance contre calendrier, architecture contre maintenance. Éviter les échanges tous-vers-tous et les débats sans nouvelle preuve. Limiter les tours ; si désaccord persistant, choisir une vérification bornée, une décision réversible ou une suspension du seul engagement concerné.

Arbitrer selon la solidité des preuves, l'économie complète, le capital exposé, le délai, la capacité et le temps du conseiller ; aucun vote majoritaire ni moyenne de notes ne neutralise un blocage décisif. Conserver les objections importantes, l'alternative rejetée, la justification et le fait déclencheur d'un réexamen. Ne pas demander au conseiller de départager des choix techniques équivalents.

Donner ensuite des directives exécutables : responsable unique, résultat attendu, dépendances, limites, prochaine étape, recette et échéance justifiée. Déléguer les choix réversibles dans ce cadre. Toute nouvelle action externe reste soumise aux mandats existants ; un mandat du coordinateur ne peut étendre celui de l'utilisateur.

## Compte rendu des interactions

Dans l'action canonique, tracer une ligne par métier déterminant : statut (consulté, non requis, indisponible ou passe directe), question reçue, fait/réserve remonté, option issue de la divergence, changement imposé au choix, relais vers le métier suivant et preuve. Distinguer clairement le rôle cité, la passe réellement menée, un agent réellement mobilisé et un livrable vérifié. Après l'arbitrage, restituer : faits partagés, désaccord utile, hypothèse adverse et son traitement, décision, alternative écartée, séquence de relais, responsable et mesure. Si aucun métier n'a réellement contribué, le dire : l'action peut être simple, mais elle n'est pas présentée comme collective.

## Exécution, mémoire et reprise

Attribuer un seul rédacteur de l'état partagé par entreprise ; les agents déposent des propositions. Isoler les modifications de code par fichiers ou branches lorsque nécessaire et intégrer après contrôle. Dans Notion réutiliser Actions et améliorations et Journal du coach ; ne pas créer douze journaux. Conserver rôle, mission, résultat, preuves, décision, statut et suite ; utiliser les propriétés existantes et le corps des pages plutôt qu'une migration de schéma inutile.

Distinguer préparé, agent lancé, livrable reçu, vérifié, publié et résultat commercial observé. Un tableau d'équipe n'est pas une équipe active. Une date de contrôle n'est pas une automatisation. En cas d'interruption conserver les missions achevées, le blocage et le prochain geste ; vérifier les effets avant de relancer.

## Qualification et amélioration des compétences

Évaluer chaque protocole sur des cas représentatifs et nouveaux : données absentes, contradictions, calculs, limites de mandat et livrables réels. Définir critères avant exécution ; ne pas transmettre le corrigé à l'exécutant. Pour un changement majeur comparer une méthode simple et la candidate sur les mêmes entrées, revue indépendante et sans effets externes.

Mesurer erreurs importantes, qualité du livrable, délai/effort, coût observable et travail humain évité ; ne pas inventer de mesure de coût ou de causalité sur le revenu. Des contrôles structurels ne prouvent pas une expertise universelle. Noter compétence non évaluée/en essai/validée sur un périmètre précis et date. Requalifier après une erreur significative. Réduire l'équipe si elle n'améliore pas le résultat.

Avant d'augmenter l'engagement d'un business, vérifier preuves proportionnées, trésorerie, capacité, mandat et seuil d'arrêt décidé pour ce cas. Mesurer ensuite ce que l'entreprise a réellement gagné ; ne pas attribuer la réussite à l'organisation sur une seule observation.

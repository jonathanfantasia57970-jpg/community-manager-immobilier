# Intégration aux métiers et mémoire du projet

Repère : INTEGRATION-VIDEO-2026.11.01.6.

## Répartir les responsabilités

- Le dirigeant ou pilote fixe objectifs, priorités, offre et moyens.
- Le community manager cadre le besoin, le public, les priorités et la séquence ; le spécialiste réseau élabore sujet, angle, idée centrale, preuve et nuances. Le fond est retenu avant l'avis et l'arbitrage de format selon la référence commune du SKILL.md. Le CM confie la production à equipe-creer-monter-videos lorsque l'apport vidéo et sa faisabilité sont établis ; en exécution directe, le spécialiste arbitre dans son périmètre.
- Les méthodes de messages/variantes, structures statiques, apprentissage et présentation sont intégrées dans `equipe-exploiter-bibliotheque-creative` (skill du plugin `skills/equipe-exploiter-bibliotheque-creative`). Le pilote les utilise dans son brief sans déléguer son autorité. La réalisation vidéo reste ici ; aucun appel à Ad Creative n'est nécessaire.
- Le présent skill porte conception audiovisuelle, choix de production, montage, voix, son, contrôle et livrable.
- Le spécialiste de canal apporte avant production les contraintes d’usage et prépare habillage éditorial, publication et mesure dans son mandat.
- Les pilotes Ads gardent objectif, public, offre, angle/mécanisme, preuve, niveau créatif, placements, ciblage, budgets, admission, campagnes et mesure publicitaire. Une vidéo publicitaire produite ici ne crée pas d’autorisation de dépenser en diffusion.
- FFmpeg et les outils médias exécutent les opérations réellement disponibles ; ils ne choisissent pas seuls l’objectif ou l’angle.

Un appel est une délégation de compétence, pas une obligation de sous-agent, de tâche ou de nouvelle conversation. Quand le canal appelant a transmis des exigences actuelles, les utiliser ; ne pas le rappeler récursivement. Un accès au compte n’est pas nécessaire pour préparer une vidéo locale.

## Contrat d’entrée et sortie

Recevoir : lien/identifiant du brief canonique, révision à lire, proposition éditoriale retenue et points intangibles, question/section à traiter, identifiant de projet/contenu et propriétaire, entreprise/profil, audience, objectif, canal/placement, message et preuve, offre/CTA si applicables, médias, droits, contraintes de tournage/coût, validations acquises et livrable attendu ; décision de format, gain audiovisuel attendu, alternative comparée et contrôle de première impression lorsque le brief vient d'une nouvelle intention éditoriale. Reprendre la médiathèque du profil et appliquer mediatheque.md avant de fixer les actifs. Rechercher les informations déjà accessibles avant de questionner. Un détail non bloquant se résout par une hypothèse signalée.

Avant de rendre ou enregistrer une contribution, rapprocher la dernière révision du brief ; intégrer les corrections utilisateur et préserver les changements concurrents. Le réalisateur signale tout changement substantiel nécessaire au propriétaire du brief — spécialiste/CM organique ou pilote de campagne ; il ne simplifie pas le sujet, la preuve ou les nuances pour convenance d'illustration. Une approbation vise la révision et la destination réellement accordées.

Retourner au propriétaire : fichier/version, texte exact, durées/formats observés, sous-titres, sources/actifs, état qualité et limites, références des revues partagées avec couverture/version/destination et cycles réellement consommés, contrôle de première impression réellement accompli, réalisation du gain audiovisuel prévu ou obstacle, variantes réalisées et prochain contrôle. Le statut créatif ne remplace pas la confirmation de publication du fournisseur.

Une vidéo pour plusieurs canaux nécessite des adaptations réelles : ouverture, rythme, lisibilité, durée, fin et contexte. Préserver le noyau factuel et les preuves ; vérifier les exigences actuelles du placement. Ne pas déclarer une déclinaison prête parce qu’un recadrage a été calculé.

## Une source canonique, plusieurs passages

Réutiliser le registre propriétaire et son brief canonique : pour l'organique, appliquer le raccord du canal et la référence CM indiquée dans le SKILL.md ; pour une publicité, appliquer le contrat du pilote de campagne dans son registre existant. La référence CM décrit des principes de relais, pas un schéma à imposer aux campagnes. Ne transférer ni propriété, ni calendrier, ni budget entre organique et Ads. Le modèle de projet vidéo décrit les choix techniques et les fichiers ; il référence le brief et sa révision, sans seconde source mutable pour le sujet, l'angle ou le format. Si le projet est autonome, choisir une seule fiche persistante liée à ses médias. Ne pas créer un deuxième calendrier ou dupliquer des posts. Dans assets/projet-video.json, renseigner editorial_brief.canonical_ref et revision_read ; utiliser mode=referenced_read_only_snapshot lorsque le CM/canal ou le pilote de campagne possède le brief. Le bloc brief éventuel n'est alors qu'un instantané de travail lié à cette révision : aucune modification éditoriale n'y fait foi, et un écart impose de relire la source. Pour un projet réellement autonome, mode=standalone_canonical désigne son unique fiche éditoriale via canonical_record, jusqu'à un transfert explicite de responsabilité. Préserver les anciens projets et ajouter le lien sans réécrire leur historique.

Résoudre l'emplacement réel du brief selon le registre du canal : une intention peut déjà porter un brief avant tout post livré. Pour LinkedIn, la source est `community_management.editorial_briefs[brief_id]` du registre existant, définie par references/registre.md du skill `equipe-creer-posts-linkedin-immobilier` de ce plugin. Référencer cet emplacement stable dans `editorial_brief.canonical_ref`, puis sa révision dans `revision_read` ; ne pas attendre une entrée de production fictive. Le propriétaire lie ensuite l'entrée effectivement produite par `brief_id` et `brief_revision`.

Le modèle assets/projet-video.json donne les champs utiles ; l’adapter au registre existant plutôt que créer systématiquement un nouveau fichier.

Conserver de façon bornée : intention, concept retenu et options écartées, profil et droits, source/périmètre de médiathèque consulté, candidats et médias inspectés, choix motivés et timecodes, script et storyboard, sélection/timecodes, version projet et sorties, outils et coûts connus, approbations avec leur portée, couverture de contrôle, défauts et décisions, nombre de passes, étape suivante et condition de reprise.

États possibles : cadrage, script_prêt, matière_manquante, montage_en_cours, exporté_à_contrôler, à_corriger, contrôle_incomplet, vidéo_prête, transmis_au_canal. Ajouter publication_confirmée seulement sur preuve du canal. Une génération lancée mais non récupérée reste en cours/inconnue, jamais terminée.

À reprise : lire le dernier état, retrouver la version exacte des actifs, rapprocher les opérations incertaines, continuer l’étape déterminante. Réutiliser les parties encore valides. Si texte, voix ou montage change, invalider les timings et contrôles affectés ; préserver le reste avec justification. Ne pas refaire une génération réussie faute d’avoir consulté le projet.

## Portée et sauvegarde

Sauvegarder les livrables et sources dans la destination persistante autorisée ; Library par défaut selon les instructions de l’environnement, ou dépôt déjà propriétaire d’un projet de code. Ne pas héberger sur un nouveau tiers par commodité. Le présent skill n’autorise ni publication, ni message, ni transfert de fichiers à un service non nécessaire.

En cas de blocage, livrer le travail utilisable et préciser manque, preuve ou incertitude, conséquence, reprise et seule intervention humaine indispensable. Une panne de connexion à un réseau ne bloque pas les montages indépendants. Ne pas suspendre une mission ou créer de planification pour compenser.

Les contrôles d’un média demandé et les tests de chargement sont distincts. le conseiller déclenche lui-même les tests de version et de chargement par @, sans chat, sous-agent ou tâche lancés automatiquement à cette fin. Les évaluations métier et non-régressions autorisées en arrière-plan ne prouvent pas ce chargement et ne créent pas de fils de test dans son journal.

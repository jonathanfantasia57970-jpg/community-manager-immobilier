# Raccord LinkedIn à la création vidéo

## Décider puis transmettre

Appliquer le fond de editorial.md avant le choix du support. Lire le contrat et les critères du CM indiqués dans le SKILL.md ; comparer les propositions selon direction-visuelle.md. Une vidéo peut exploiter un rush, des photos pertinentes, une animation calculée ou une génération autorisée. Aucun studio, nouveau tournage, abonnement ou moteur payant n'est présumé disponible. Le gain attendu doit être précis ; une voix qui lit une affiche ne suffit pas.

Le brief canonique reste dans `community_management.editorial_briefs[brief_id]` du registre LinkedIn. Lire registre.md pour la référence stable et les révisions ; ne pas créer un post fictif ni un second brief vidéo. Transmettre au skill du plugin `skills/equipe-creer-monter-videos` : référence canonique et révision, sujet/angle/preuve retenus, nuances intangibles, raison du format, public, destination LinkedIn, textes déjà validés, médias examinés et limites, droits, moyens autorisés, délai, contrôles déjà couverts et cycles consommés.

Le réalisateur applique sa méthode commune et retourne réalisation, preuves ou obstacle. En cas de changement de fond, le spécialiste reprend le point éditorial puis le pilote arbitre dans son mandat. Un problème technique ne donne pas au réalisateur le droit de changer la promesse, d'inventer une preuve ou de supprimer une nuance décisive. En appel direct, le spécialiste assume les passes de cadrage et d'arbitrage sans invoquer une délégation fictive.

## Recevoir le vrai livrable

Rapprocher la dernière révision avant d'intégrer le retour. Recevoir référence du projet, fichier et version exacts, texte parlé et accompagnement exacts, durée et format mesurés, sous-titres, actifs/sources, coûts connus, première impression, contrôles réalisés et manquants. Un retour sur une ancienne révision reste à rapprocher ; ne pas écraser une correction utilisateur.

Vérifier le gain audiovisuel sur le montage et sa promesse par rapport au texte LinkedIn. Examiner l'ouverture réellement montée sur mobile, puis la progression continue ; écouter voix et mix lorsqu'il y a du son. Vérifier aussi la compréhension sans son et les sous-titres utiles. Une planche de captures, une couverture, une transcription ou une mesure de fréquences ne valide pas ces perceptions. Indiquer les contrôles indisponibles et conserver `incomplete`. Une vidéo volontairement muette se juge comme telle ; ne pas inventer un défaut de voix absente.

Appliquer la répartition des revues de relecture.md et la méthode production-et-qualite.md du réalisateur : mêmes preuves réutilisables, responsabilités indépendantes maintenues, contrôles manquants complétés, bornes de cycles respectées. Les critères photo (montage canonique, portrait, signature sur chaque image) s'appliquent seulement à une photo/illustration effectivement choisie, pas comme condition de validation de tout film.

## Enregistrer et livrer

Conserver le fichier final et les sources dans la destination durable autorisée. Dans l'entrée produite, enregistrer `brief_id`, `brief_revision` et `media.kind = video` selon registre.md ; le champ `visual` concerne seulement une éventuelle couverture. Le projet technique référence le même brief, sans en devenir propriétaire.

Livrer texte intégral relu, vidéo finale accessible, lien exact, sous-titres et état réellement prouvé. Vérifier le fichier livré et sa correspondance avec la version revue. Pour contrôler le texte dans une réponse utilisant les blocs de rédaction : `python3 scripts/verifier_livraison.py --response REPONSE_FINALE.md --require-post-block --reviewed-text TEXTE_RELU.txt`. Ce script contrôle le texte et les blocs ; il ne contrôle ni la vidéo ni son lien. Contrôler séparément l'accès au MP4, la durée/décodabilité, la concordance du lien et le reçu de sauvegarde, sans utiliser `--image` sur un MP4 ni fabriquer une preuve de composition photographique.

Un fichier exporté n'est pas forcément prêt ; prêt ne signifie ni approuvé, ni programmé, ni publié. La diffusion éventuelle reste celle du canal et de sa version autorisée. Une impossibilité de diffuser une vidéo n'autorise pas à la remplacer silencieusement par sa miniature.

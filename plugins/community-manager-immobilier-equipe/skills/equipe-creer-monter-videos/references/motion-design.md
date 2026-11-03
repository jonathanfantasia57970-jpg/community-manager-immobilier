# Motion design sans moteur vidéo génératif

Repère : MOTION-VIDEO-2026.11.01.1.

## Choisir ce que le mouvement explique

Faire évoluer une information : construire un parcours, comparer deux usages, révéler une relation, attirer l’attention sur un détail, montrer une variation ou organiser des étapes. Employer texte animé, formes, graphiques, plans simplifiés et illustrations vectorielles. Une vidéo entièrement graphique et un insert de trois secondes relèvent de la même discipline, avec une densité adaptée.

Choisir une direction cohérente avant animation : palette limitée, typographies disponibles, hiérarchie, marges, style des traits et formes, comportement des transitions. Appliquer la charte du profil réel. Comparer les candidats de la bibliothèque plutôt que reproduire toujours le même habillage.

Donner au spectateur un foyer d’attention principal par moment. Révéler une structure progressivement et garder visibles les relations nécessaires. Éviter texte, compteur, musique et décor concurrents. Un graphique doit avoir échelle, unité et données compréhensibles ; aucune donnée inventée pour remplir l’écran.

## Décrire une scène exécutable

Dans le storyboard, renseigner :
- canevas et déclinaisons visées ;
- objets, textes exacts, sources et ordre des couches ;
- position initiale/finale, apparition/disparition, mouvement et repère temporel ;
- fonction du mouvement, lien avec la parole et temps de maintien ;
- zones à protéger : visage, démonstration, sous-titres et interface du canal.

Exprimer les positions dans le cadre ou en coordonnées normalisées pour faciliter l’adaptation. Conserver une seule horloge de montage pour parole, animations, sous-titres et effets. Mesurer la prise réelle avant de verrouiller la scène.

Préférer des accélérations/décélérations lisibles aux déplacements mécaniques continus. Adapter leur amplitude et durée au sens ; ne pas ajouter rebonds, rotations ou zooms par routine. La durée de maintien permet de comprendre le résultat ; l’entrée spectaculaire ne doit pas consommer tout le temps.

## Choisir une voie de rendu réelle

1. **Habillage et animation simples :** charger equipe-monter-videos. Ses opérations observées incluent overlay.py pour texte/image/vidéo, graphics.py pour habillages, insert.py pour carte ou photo animée, caption.py et join.py. Lire l’aide de l’opération utilisée ; ne pas supposer qu’un template accepte une courbe arbitraire. Pour plusieurs opérations, suivre son projet de rendu.
2. **Schéma ou animation 2D personnalisée :** créer une composition vectorielle ou Canvas/HTML/SVG par code avec une timeline explicite, puis rendre les images à des instants déterministes avec les bibliothèques disponibles et assembler avec FFmpeg. Il s’agit d’un artefact graphique local ; respecter les règles du runtime et de tout navigateur réellement utilisé.
3. **Template de composition spécialisé :** utiliser une bibliothèque telle que Remotion seulement si son environnement et sa licence correspondent à l’usage. Ne pas promettre qu’elle est gratuite pour tout contexte ni installer un service cloud par défaut.
4. **3D, morphing photoréaliste, suivi complexe :** vérifier un outil adéquat, les ressources et le temps requis. Une simple animation 2D ne prouve pas cette capacité. Choisir un rendu plus simple compatible ou annoncer la dépendance avant de promettre un effet.

Pour le rendu par code : charger polices et actifs avant capture ; fixer dimensions/cadence/durée ; calculer l’état à t = numéro_image / cadence ; éviter hasard non maîtrisé et dépendance au temps réel. Exporter une séquence ou un format compatible. Préserver l’alpha si le composant doit être incrusté ; ne pas supposer qu’un MP4 H.264 conserve la transparence. Composer et contrôler l’export final.

La présente référence est une méthode de production, pas un moteur embarqué ni un template graphique universel déjà rendu. Vérifier les capacités de chaque session. Une génération d’images peut rester utile pour certains actifs, mais respecter une demande sans génération payante et les instructions de l’outil d’image applicable.

## Production locale et coûts

Choisir un parcours sans achat de crédits vidéo lorsque médias existants, voix fournie et graphisme calculé suffisent. Distinguer coût des logiciels, calcul/rendu, musique, police, image, voix et temps humain. Un téléchargement gratuit n’atteste pas la licence pour une publicité. Ne pas imposer TTS, stock payant, hébergement ou abonnement.

Écrire précisément ce qui sera fabriqué localement et ce qui dépend d’un actif ou service. Une animation sur des photos disponibles ne nécessite pas de générateur vidéo. Une scène photoréaliste nouvelle n’est pas équivalente à une animation de formes.

## Contrôle de mouvement et lisibilité

Contrôler des images clés puis le clip continu : trajectoire, alignement, transitions, tremblements, texte rogné, durée de lecture et exactitude des données. Voir sur une taille d’affichage proche du mobile. Éviter flashs agressifs et mouvements gratuits. Revoir le mix si un effet accompagne un événement.

Conserver la source modifiable, les actifs, les paramètres, la version des dépendances utilisées et les commandes de rendu. Une capture fixe ne valide ni fluidité ni synchronisation. Une qualité visuelle avancée s’évalue sur le fichier obtenu, pas sur la présence de mots comme « premium » dans le brief.

Documentation technique à vérifier au moment d’exécuter : https://ffmpeg.org/ffmpeg-filters.html ; https://ffmpeg.org/about.html. Les noms de scripts cités proviennent du skill FFmpeg personnel relu le 1 novembre 2026.

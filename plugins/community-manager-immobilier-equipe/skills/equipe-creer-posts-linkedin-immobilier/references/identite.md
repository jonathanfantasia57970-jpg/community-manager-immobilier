# Identité et références

- Identité, rôle, réseau et secteur : lire le profil confirmé du conseiller. Le titre par défaut est « Conseiller immobilier » ; aucun statut de leader ni statut juridique n’est présumé.
- Marque et raison sociale : utiliser seulement les informations confirmées du profil ; ne pas inventer statut d’agence ou carte professionnelle.
- Ancrage : secteur réellement couvert et confirmé dans le profil.
- Appliquer la [charte typographique et la signature fixes](#charte-typographique-et-signature-fixes) à chaque visuel ; cette section est leur unique consigne de référence.
- Portrait facultatif selon le concept, son utilité et le choix du conseiller. Utiliser uniquement ses références autorisées.
- Ne pas affirmer un effectif, une ancienneté calculée, une note d’avis ou un nombre de ventes sans confirmation actuelle. Ne pas publier ses objectifs privés.
- Distinguer avis proposé, récit confirmé, cas anonymisé fourni et situation hypothétique. Ne jamais inventer expérience, dialogue, habitude, émotion ou résultat du conseiller. Ne pas importer de détails identifiants de dossiers clients dans une illustration. Ne pas promettre viralité, audience ou résultats commerciaux sans données.
- Si le recrutement est activé, donner envie de connaître l’équipe par des pratiques confirmées, sans démarchage appuyé. Sinon, rester sur l’immobilier et les besoins des clients.

## Positionnement de transmission

Lorsque la transmission ou le leadership est activé, l’accompagnement proposé doit transmettre les moyens d'apprendre et d'agir par soi-même. Ne pas le positionner comme le fournisseur de clients ou d'opportunités dont les conseillers dépendraient. Vérifier l'attente produite par le texte et le visuel, même en l'absence de promesse explicite.

L’entraide, une intervention nécessaire pour le client et une mise en relation ponctuelle restent possibles. Elles ne prouvent pas, seules, un apprentissage ; appliquer le test du cas suivant de la méthode éditoriale pour ce sujet. L’autonomie n’exige pas un retrait systématique du soutien. Cette règle de positionnement ne prouve aucune pratique déjà réalisée par le conseiller.

## Portraits de référence

Résoudre `brand.portrait_media_id` dans la médiathèque personnelle. Aucun portrait n’est inclus. Inspecter et transmettre réellement la référence autorisée à l’outil ; garder provenance, version et autorisations. Ne pas demander de nouveau un portrait déjà disponible et vérifié. Conserver l’original. Une retouche de morphologie ne se présume jamais et n’est reprise que si le conseiller a explicitement choisi cette version comme référence.

Préserver morphologie, âge apparent, cheveux, carnation et proportions. Pour regard et expression, appliquer direction-visuelle.md ; les poses des références ne sont pas imposées. Ajouter un portrait supplémentaire à la médiathèque sans remplacer l’ancien sauf demande. Ne pas prendre un visage trouvé dans les fichiers pour identité confirmée. Un rendu synthétique ne devient pas une source d’identité par défaut.

### Fidélité du portrait avant embellissement

Comparer côte à côte le visage source autorisé et le visage final recadré à taille comparable : forme des yeux et paupières, nez, bouche, ligne des cheveux, mâchoire, asymétries naturelles, texture de peau et âge apparent. « Reconnaissable » ne suffit pas si le rendu devient une version idéalisée ou générique du conseiller. Conserver la morphologie de la référence choisie, sans lisser davantage, rajeunir, symétriser, modifier les traits ni amplifier le sourire.

Privilégier le réemploi d'une photo authentique pertinente ; pour une nouvelle scène, limiter les transformations du visage et transmettre le portrait canonique réel à chaque génération. Ne pas prendre le dernier rendu synthétique pour nouvelle source d'identité. Si la scène exige une pose qui dégrade la ressemblance, adapter la scène ou utiliser le portrait autorisé près de la signature plutôt qu'inventer un visage plus commode. Consigner les écarts effectivement vus ; une intention de prompt « photoréaliste » n'est pas une preuve de fidélité. Un écart matériel non corrigé garde le visuel incomplet.

## Charte typographique et signature fixes

La charte de départ utilise Montserrat : ExtraBold pour l’accroche, Bold pour le nom, Medium pour le titre. Blanc cassé et accent orange, alignement à gauche, marges généreuses et interligne serré. Le conseiller peut choisir une autre charte à la configuration ; ensuite appliquer sa version canonique avec les mêmes exigences de constance et de lisibilité. Ne pas changer silencieusement les couleurs selon une performance supposée.

La signature est typographique : court trait d’accent, nom complet, titre confirmé, en bas à gauche. Générer les lettres depuis la charte personnalisée, jamais depuis un nom générique ou celui d’une autre personne. Le modèle est [charte-linkedin.json](../assets/charte-linkedin.json), la police et sa licence OFL sont dans assets/fonts. Aucun slogan, monogramme ou signature manuscrite ajouté. Lorsque leadership est désactivé, aucune mention « Team Leader » dans la charte, le calque, le visuel ou le texte.

Créer la charte personnelle hors du plugin avec `python3 scripts/configurer_charte.py --profile PROFIL_JSON --output CHARTE_JSON`. Utiliser `CM_CHARTE=CHARTE_JSON` pour chaque commande de composition, signature et vérification. Le chemin et l’empreinte de cette charte sont enregistrés dans la preuve. Les champs non renseignés font échouer le rendu, sans produire une signature de démonstration.

### Produire des lettres réellement constantes

Pour une création synthétique, créer la photographie avec ImageGen **sans titre, signature ni mention imprimée**, en réservant leurs zones. Pour une photo authentique de la photothèque commune, préserver l’original et prévoir un dérivé fidèle compatible avec la mise en page ; ne pas régénérer la scène pour réserver ces zones. Préserver un rendu immersif sans bande blanche plaquée. Privilégier des décors et photographies clairs, lumineux et naturels ; ne plus imposer de fond bleu nuit ni de voile global assombrissant. Adapter le cadrage photographique, le placement de la scène et ses contrastes pour les lettres blanc cassé et orange, sans rendre tout le décor sombre pour les lire. Des zones naturellement ombragées ou une ombre photographique douce et localisée peuvent porter les lettres ; préserver ailleurs la clarté du décor. Un visage éclairé devant une vaste paroi noire ne satisfait pas cette demande. Réserver dans la photographie des zones suffisamment contrastées pour le titre et la signature, sans les transformer en vastes aplats sombres. Composer ensuite les lettres par assemblage mécanique : fournir le calque comme référence à ImageGen ne l'applique pas et ne garantit pas des glyphes identiques. Ne plus régénérer le fichier après composition. Si une correction de la scène est nécessaire, corriger la photographie source puis réappliquer le même calque.

Préparer le titre dans un JSON contenant une à quatre lignes, chacune formée de segments `{ "text": "texte", "accent": true|false }`. Garder libres ses retours à la ligne selon le sens et l'image ; ne pas affaiblir une bonne accroche pour remplir un gabarit. Si elle déborde, redisposer les lignes avant de revoir la formulation. Le générateur de calque `scripts/typographie.py` utilise le fichier Montserrat inclus et convertit les lettres en tracés, sans retoucher la photo.

Appliquer le calque avec `python3 scripts/composer_visuel.py compose --photo CHEMIN_PHOTO --headline-json CHEMIN_JSON --output CHEMIN_FINAL.png`. L’assemblage mécanique sert à assurer cette constance, dans le mandat de création du visuel ; réserver à ImageGen les retouches photographiques. Le script produit le PNG final, les calques SVG/PNG et `CHEMIN_FINAL.composition.json`. Il garde la photo entière, accepte seulement les écarts d'arrondi du ratio et refuse un recadrage silencieux. Le format par défaut est 4:5 ; `--format 1:1` ou `--format 9:16` conserve la largeur, les lettres et les marges, en ancrant la signature au bas. Adapter la scène à l'espace utile ; aucune pose ni composition photographique n'est imposée.

La mention « Illustration IA » est ajoutée par le calque pour une scène synthétique. Réserver `--authentic-photo` à une photographie réellement non générée. Contrôler la provenance, les textes déjà présents dans la photo, le contraste et le placement sur les visages visuellement : le script ne sait pas les juger.

Le script typographique peut reconstruire la signature avec `--signature --output CHEMIN_SIGNATURE` ; les tracés restent ceux de la charte fixe. Vérifier l'assemblage avec `python3 scripts/composer_visuel.py verify --image CHEMIN_FINAL.png --composition CHEMIN_FINAL.composition.json`. Ce contrôle reconstruit le rendu à partir de la photo, du titre et des actifs canoniques et compare les pixels du fichier final. Une déclaration dans le registre ou l'existence du calque seule ne vaut pas application. Canva peut préparer la mise en page par son connecteur ; un export n'est final qu'après un contrôle effectif de la composition. Le parcours local ci-dessus est le chemin vérifiable fourni. S'il est indisponible, signaler le visuel incomplet plutôt que substituer des lettres générées et annoncer la conformité.

Faire varier scène, cadrage, geste et expression tout en conservant ces repères. Si un portrait de signature est retenu, le placer sans déplacer ou masquer les textes. Contrôler à 390 px : accroche comprise, accent pertinent, nom et titre complets lisibles, aucun visage masqué. Ne pas confondre constance graphique et répétition des mises en scène.

## Présence et portrait selon le profil
Le portrait n’est pas obligatoire par défaut. Décider de son utilité pour le concept et l’identification, puis appliquer le choix explicite du conseiller. Ne pas imposer un portrait de signature à chaque création. Si le conseiller exige un portrait pour ce canal, respecter ce réglage sans remplacer son visage ni réduire les contrôles de fidélité. Cette règle remplace toute obligation générale de portrait dans les exemples historiques.

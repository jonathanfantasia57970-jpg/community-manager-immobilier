# Son : production, synchronisation et mixage

Repère : `SON-VIDEO-2026.11.01.2`, transféré du protocole YouTube `SON-VIDEO-2026.11.01.1`. Appliquer à la narration, au dialogue, aux ambiances, à la musique et aux bruitages. Compléter `voix-et-prosodie.md` et le contrôle audiovisuel existant ; ne créer ni approbation ni calendrier supplémentaire.

Sommaire : source sonore ; capacités ; montage ; mixage ; recette ; provenance.

## 1. Identifier ce qui produit réellement le son

Avant une correction, relever séparément le moteur des images, le moteur de la voix, la prise utilisée et les traitements au montage. Retrouver les paramètres du fichier approuvé quand ils existent ; ne pas attribuer son naturel au générateur vidéo d’après le nom du projet. Une voix approuvée, une interprétation approuvée et un mix approuvé sont trois éléments distincts.

| Parcours | Usage pertinent | Contrôle et limite |
| --- | --- | --- |
| Parole enregistrée | Face caméra, voix off ou performance fournie | Préserver intention et phrasé ; corriger bruit et niveau sans effacer la diction. Aucun studio imposé. |
| Voix off générée séparément | Photos, graphisme, plans muets ou narration remplaçable | Tester la voix seule ; fixer ses repères avant le montage. Le moteur vidéo n’impose pas le moteur vocal. |
| Dialogue natif de la vidéo | Interaction, réactions, gestes et lèvres liés à la parole | Contrôler texte, accent, tours de parole et synchronisation dans le fichier réel ; ne pas supposer que tous les modèles produisent du son. |
| Conversion de voix à partir d’une performance | Performance autorisée dont le timbre doit être remplacé | Vérifier que l’outil accepte ce média et préserve effectivement la prosodie ; comparer timing, mots et artefacts. Ne pas promettre une conservation parfaite ni cloner sans autorisation. |

Réutiliser une performance satisfaisante quand le texte, les droits et l’usage conviennent. Ne pas générer une vidéo coûteuse uniquement pour obtenir une voix si une voie audio adaptée suffit. Conserver le parcours sans tournage demandé. Une correction sonore ne justifie pas de refaire les images.

## 2. Traduire la direction vers les capacités disponibles

Conserver, pour le fournisseur et la version effectivement utilisés, une fiche courte : identifiant exact de voix, langue/accent, champ de direction, vitesse, hauteur globale, style/stabilité, lexique, balises, référence audio, formats, restrictions et coût connu. Marquer chaque contrôle `disponible`, `absent` ou `non_vérifié` d’après l’interface ou le schéma actuel.

Ne transmettre que les paramètres exposés. Un service sous-jacent peut offrir plus de commandes que son intégration dans Higgsfield. Ne pas inventer de SSML, de courbe F0, de réglage syllabes/seconde ou de curseur ElevenLabs dans un connecteur qui ne les expose pas. Le champ vitesse d’un moteur n’est pas un débit syllabique garanti ; un réglage de hauteur globale ne dessine pas les intonations de fin de phrase.

Garder texte à prononcer et direction séparés. Employer les balises expressives seulement si le modèle exact les interprète. Réserver l’égalisation au timbre et au masquage, pas à la modulation mélodique. Pour une courbe prosodique inadéquate, diriger une nouvelle prise cohérente ou utiliser une performance de référence si cette capacité est disponible et autorisée.

Commencer avec les outils et la voix déjà approuvés. Ne pas imposer ElevenLabs, Seedance, une API directe ou un abonnement. Un moteur différent est une option motivée par un défaut persistant, pas une garantie de naturel. Lors d’un essai comparatif autorisé, garder texte et voix identiques si l’identifiant est réellement compatible ; sinon signaler que le changement de timbre empêche d’isoler l’effet du moteur. Comparer à volume perçu rapproché. Respecter les passes et le budget existants ; cette référence n’autorise aucune dépense supplémentaire.

## 3. Monter sur la parole réelle

Pour une narration courte, privilégier d’abord une prise continue ou de longues unités de sens afin de conserver les liaisons et l’évolution de l’intention. Reprendre uniquement un passage nécessaire avec ses voisins. Ne pas assembler un mot ou une phrase par fichier par défaut.

Mesurer la prise retenue, établir les repères de mots/groupes de sens, puis régler images et sous-titres sur cet audio. Relire les horodatages automatiques : une transcription peut confondre des homophones et placer une frontière dans un mot. Vérifier noms, nombres, négations, offre et CTA dans l’audio réel. Garder des groupes de sous-titres compréhensibles ; la recette de deux ou trois mots d’Ad Creative est une option graphique, pas une contrainte universelle.

Couper aux frontières naturelles, préserver consonnes, respirations utiles et fins de mots. Employer de courts fondus aux raccords si nécessaire pour éviter les clics, sans superposer deux syllabes. Ne pas supprimer toutes les pauses ni accélérer globalement un texte pour le faire tenir. Une légère retouche temporelle éventuelle doit être écoutée et tracée.

Pour un visage parlant, vérifier les lèvres au début, au milieu, en fin et autour de chaque retouche, puis visionner la séquence continue. Si le son est décalé ou étiré, adapter explicitement le montage ; un décalage moyen nul ne prouve pas la synchronisation de tous les phonèmes. Recontrôler les sous-titres après toute modification temporelle.

## 4. Construire un mix intelligible

Séparer autant que possible parole, ambiance, musique et effets. Décider du rôle de chaque piste :
- conserver la parole utile et les ambiances nécessaires au sens ;
- neutraliser une voix native remplacée pour éviter doublon/écho ;
- retirer le son parasite des plans d’illustration lorsque sans utilité ; ne jamais appliquer « tout muet » au conseiller ou à une démonstration sonore ;
- ajouter musique ou effets seulement s’ils servent la compréhension, l’émotion ou une action visible.

Protéger les mots de l’accroche, du bénéfice et du CTA. Ajuster musique et effets pendant la parole, éventuellement par automation ou ducking ; écouter les consonnes et les noms sensibles. Un pourcentage de volume ne garantit pas le bon équilibre entre des sources de niveaux différents. Vérifier aussi l’absence de pompage, de sifflantes agressives, de saturation ou de réduction de bruit métallique.

Synchroniser chaque effet à l’événement visible et contrôler le premier comme le dernier repère. Ne pas ajouter de notification sans événement correspondant. Adapter les fondus au montage : la sortie musicale d’environ 0,8 seconde proposée par Ad Creative peut être un départ d’essai, jamais une règle qui ampute une parole ou une fin voulue.

Choisir une musique dont l’usage autorisé couvre la destination. Distinguer fichier avec musique intégrée et ajout natif au moment de publier, selon les capacités, droits et contexte organique/publicitaire réellement vérifiés. Une disponibilité dans une application ne prouve pas des droits pour une publicité ou une autre plateforme. Ne pas promettre de gain algorithmique pour un son tendance.

### Niveau et dynamique

Définir la cible du livrable avant traitement et consigner les valeurs mesurées après export. La recette Ad Creative `I=-16 LUFS, TP=-1,5 dBTP, LRA=11 LU` est un point de départ possible, pas une exigence YouTube ni une garantie de qualité. LRA=11 dans un filtre n’est ni une amplitude à atteindre à tout prix, ni une preuve de modulation expressive ; sa lecture est limitée sur un extrait très court. Adapter au programme, à la destination vérifiée et à l’intelligibilité.

Normaliser le mix final avec mesure avant/après ; préférer une approche en deux passes lorsqu’une cible précise est nécessaire. Préserver la dynamique utile de la parole. Contrôler crête vraie après encodage, écrêtage, niveau global, écarts entre prises et passages trop faibles. Ne pas confondre dBFS, dBTP, LUFS et fréquence fondamentale.

Avec FFmpeg, tenir compte de la normalisation automatique de `amix`. Employer `normalize=0` uniquement avec gains et marge maîtrisés, puis vérifier la somme. Un limiteur de crête échantillon, même réglé à 0,95, ne certifie pas le plafond de crête vraie après AAC. Ne pas recopier les bruitages à −9 LUFS ou la musique à 30 % d’un modèle iMessage dans une autre narration.

## 5. Recette et trace unique

Écouter intégralement la voix seule, puis le mix final dans la vidéo continue, sans puis avec le texte. Contrôler l’accent demandé par le profil, l’intention, le naturel, les raccords, la compréhension commerciale et la place du son dans l’image. Comparer les variantes à volume comparable. Vérifier casque, haut-parleur de téléphone et repli mono uniquement lorsque ces écoutes sont réellement disponibles ; tracer celles qui ne le sont pas.

Terminer les contrôles techniques : décodage, flux audio attendu, durée, canaux, format, absence de coupure finale, silence accidentel ou écrêtage. Aucun résultat technique ne remplace l’écoute. Une vidéo peut aussi être volontairement sans son : le documenter selon le brief.

Dans le même registre de contenu, joindre aux champs vocaux : route audio, sources/pistes et droits, repères de synchronisation, traitements, cible et mesures du mix exporté, fichier/version examiné, couverture d’écoute et limites. Employer les statuts vocaux et la décision audiovisuelle existants. Une voix naturelle noyée dans la musique ne passe pas la recette ; une transcription exacte sans écoute reste `contrôle_voix_incomplet`.

## 6. Provenance et portée

Adaptation intégrée le 1 novembre 2026 des références cloud personnelles d’Ad Creative, méthode de conception créative déjà intégrée, sans dépendance externe :
- `references/generative-tools.md` : voies audio native/séparée et choix de moteur ;
- `references/motion-video-ads.md` : prise continue, repères vocaux, sous-titres et normalisation ;
- `references/short-form-video-specs.md` : choix des pistes, fondus et musique intégrée/native ;
- `references/imessage-video-ads.md` : synchronisation événement/effet, équilibre et pièges du mixage.

Adapter ces recettes au public et au contexte de la vidéo ; ne pas reprendre leurs prix, classements de fournisseurs, durées de modèles ou affirmations de portée sans vérification actuelle. Le contrôle expressif détaillé et les métriques proviennent du protocole YouTube et des retours du conseiller ; ne pas les attribuer à Ad Creative. Cette référence est la source commune de son pour equipe-creer-monter-videos et ses appelants : aucun chargement systématique d’Ad Creative ni outil nouveau obligatoire.


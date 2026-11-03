# Contrôle rapide, ciel bleu et secours ImageGen

Appliquer le contrôle léger à toutes les sorties de la passe Pillow. Le remplacement
des ciels pertinents et le secours pour une photo dégradée font partie du processus
classique autorisé, même sans retour utilisateur. Réserver le contrôle détaillé aux
photos signalées et aux résultats ImageGen ; ne pas auditer toutes les images à 100 %.

## Examiner rapidement toutes les sorties

Afficher de petites planches numérotées (quatre à six images au maximum, chaque
vue environ 600 à 900 pixels sur son grand côté, selon l'outil de visualisation),
ou les sorties individuellement à taille d'annonce. Vérifier que toutes ont été
vues, sans compter un fichier absent ou illisible comme contrôlé. Une miniature
trop petite ne suffit pas : afficher une vue plus grande en cas de doute.

Chercher en une lecture : exposition du sujet, zones blanches, rendu naturel,
contraste, couleurs, température, teinte, bruit visible et ciel. Évaluer les
réglages selon `reglages-image.md`, sans imposer une correction à une image déjà
équilibrée ni déduire la couleur réelle d’un matériau de sa seule luminosité. Consulter l'original pour toute anomalie
ou limite de ciel incertaine. Sur une correction forte, examiner une zone sombre
à 100 % pour décider si le bruit ou les bandes compromettent l'usage en annonce.
Le script et ses statistiques ne détectent pas à eux seuls la qualité du ciel,
le bruit gênant, une peinture sombre ou un détail réel du bien.

| Observation | Suite |
| --- | --- |
| Rendu naturel, sujet lisible, ciel agréable ou absent | Accepter après contrôle rapide |
| Dosage de lumière, balance des blancs, contraste ou saturation à corriger | Regrouper les réglages utiles dans au plus un ajustement Pillow depuis l’original, puis recontrôler |
| Ciel gris/terne identifié, lumière compatible | ImageGen pour le ciel uniquement |
| Bruit gênant, aplats/bandes, texture dégradée ou sujet toujours inexploitable malgré une correction raisonnable | Secours ImageGen depuis l'original |
| Dégradation et ciel terne sur la même photo | Un appel ImageGen combiné depuis l'original |
| Vue extérieure indéterminée derrière une fenêtre blanche | Ne pas inventer un ciel ou une vue ; signaler la limite |
| Détail absent, photo irrécupérable ou génération infidèle | Conserver un original de repli identifié, signaler l'échec |
| Document, plan, capture ou illustration | Exclure du lot de photos |

Garder un ciel bleu déjà agréable, un coucher de soleil réussi ou une ambiance
nocturne. Un bleu modéré avec des nuages légers convient mieux à une lumière
couverte qu'un ciel d'été très saturé. Ne pas créer de soleil, d'ombre dure,
de jardin ou d'horizon et ne pas effacer pluie, neige ou surfaces humides.

Le contrôle rapide ne promet pas une inspection exhaustive de chaque pixel.
Consigner les photos réellement vues, leur hash et leur décision. Les limites
numériques de correction déclenchent un examen ciblé, jamais une génération aveugle.

## Résoudre et examiner les cibles

Résoudre chaque numéro par le registre persistant et déterminer la version
montrée à l'utilisateur. Lire la vraie source originale et la version concernée.
Pour une correction de lumière ou de bruit, repartir de l'original ; ne pas
utiliser le résultat Pillow dégradé comme cible. Pour un changement de ciel seul,
la version courante inspectée peut servir de cible si sa luminosité doit rester.

Charger le skill `imagegen` et utiliser l'outil natif avec une cible par appel.
Fournir l'image réelle, jamais une simple description. Ne pas mélanger les
mécanismes de référence et ne pas inventer d'option de masque ou de résolution.
Réutiliser le niveau du lot, sauf nouvelle consigne de l'utilisateur.

La demande de traitement classique ou de reprise permet l’exécution sur les
cibles identifiées ;
ne pas ajouter une approbation par photo. Si le numéro ou la modification est
réellement ambigu, demander uniquement cette précision.

## Prompt pour lumière, couleur ou bruit

Adapter ce canevas au défaut observé et à la demande, en supprimant les opérations
inutiles. Ne pas demander simplement « embellir », « rénover » ou « rendre luxueux ».

```text
Use case: lighting-weather
Asset type: retouche fidèle d'une photographie immobilière existante
Input images: Image 1 = photo originale, seule cible de l'édition
Primary request: corriger l'exposition vers le rendu [normal / un peu plus
lumineux que la normale / beaucoup plus lumineux que la normale]. La normale
désigne une exposition équilibrée. Défaut à corriger : [diagnostic précis].
Ouvrir les ombres et améliorer la lisibilité sans amplifier le bruit ; réduire
discrètement le grain gênant seulement si les textures et défauts restent fidèles.
Conserver le modelé, les couleurs réelles des matériaux, les blancs détaillés et
les noirs. Corriger uniquement la dominante [préciser zone et dominante si observées],
sans blanchir une peinture beige/colorée ni supprimer toute chaleur ambiante.
Ne pas imposer une neutralisation globale si plusieurs éclairages coexistent.
Contraste et saturation naturels, sans aspect HDR ni couleurs forcées.
Composition/framing: conserver exactement cadrage, point de vue, orientation,
proportions, architecture et ouvertures de la source.
Constraints: ne rien ajouter, retirer ni déplacer. Préserver meubles, équipements,
textures, fissures, taches, humidité, usure et état réel. Préserver exactement les
vues extérieures, reflets, végétation, horizon et éléments visibles par les fenêtres.
Ne pas reconstruire de détails absents ou illisibles ; ne pas nettoyer le bien.
Sky: conserver le ciel existant, ou remplacer uniquement les portions identifiées
comme ciel terne lorsque cette correction est retenue, sans modifier la vue réelle.
Avoid: home staging, rénovation, surfaces plastifiées, murs blanchis, netteté
inventée, lumière solaire ou ombres dures ajoutées, HDR, halos, texte ou logo.
```

Une baie vitrée peut fausser la moyenne : évaluer le sujet principal. Une peinture
sombre n'est pas une sous-exposition. Ne pas inventer des détails dans une fenêtre
blanche. Le bruit réduit ne prouve pas la récupération de vrais détails. Supprimer du
prompt toute correction de couleur qui n’est pas justifiée par le diagnostic.

## Prompt pour un ciel à remplacer

Ne remplacer que les portions de ciel réellement identifiables. Conserver une
ambiance nocturne, un coucher de soleil ou la météo si l'utilisateur ne demande
pas de les changer. Ne pas transformer une fenêtre blanche en vue inventée.

```text
Use case: lighting-weather
Asset type: photographie immobilière fidèle destinée à une annonce
Input images: Image 1 = version inspectée choisie pour cette correction de ciel
Primary request: remplacer uniquement les portions de ciel identifiées par un
ciel bleu naturel peu saturé, compatible avec la lumière diffuse et l'heure apparentes.
Conserver la luminosité du bien ; ne pas refaire l'éclaircissement déjà réalisé.
Composition/framing: conserver exactement cadrage, point de vue, proportions,
orientation, architecture, ouvertures, toit et façade.
Constraints: préserver matériaux, textures, défauts, état d'entretien, limites,
éléments fixes ou mobiles, végétation, environnement et vue réelle.
Ne rien ajouter, enlever ni déplacer. Respecter branches, fils, antennes,
montants de fenêtres, rideaux, reflets et les détails à la limite du ciel.
Lighting: rendu naturel, ombres plausibles, blancs non brûlés, aucun aspect HDR,
aucune lumière solaire ou ombre dure inventée.
Avoid: reconstruction, home staging, lissage, peinture neuve, pelouse reverdie,
façade nettoyée, saturation excessive, halo, texte ou logo ajouté.
```

Si le contrôle ou l’utilisateur retient luminosité et ciel ensemble, combiner les corrections
utiles dans un appel depuis l'original, sans étape Pillow supplémentaire imposée.

## Contrôle renforcé des sorties ImageGen

Comparer chaque résultat sélectionné à son original : cadrage, proportions,
objets, détails architecturaux, textures, défauts et vues extérieures inchangés ;
retouche lumineuse naturelle et détourage crédible si ciel modifié. Vérifier
aussi la température, les dominantes, les couleurs des matériaux et l’absence de
noirs bouchés ou de couleurs exagérées après réglage du contraste et de la saturation. Rejeter toute
altération du bien ou détail inventé. Ne pas comparer seulement au candidat Pillow.

Garder la résolution native fournie par ImageGen et signaler une baisse sensible ;
ne pas suréchantillonner pour prétendre retrouver le détail. Respecter le format
retourné et son extension. Ne pas convertir inutilement.

Limiter à trois exécutions de retouche par photo et mission, Pillow initial
compris pour le processus classique. Pour une nouvelle demande ciblée après
livraison, ouvrir une mission distincte avec son propre budget de trois appels. Compter
les appels lancés même échoués ; les lectures et attentes ne sont pas de nouvelles
tentatives. Conserver le compteur à la reprise. Repartir toujours de la même source
choisie, sans régénérer une génération rejetée. Si rien de fidèle ne convient,
garder une version antérieure uniquement si elle est fidèle et exploitable ;
sinon conserver l’original en repli et expliquer l’échec. Ne pas livrer le
candidat Pillow rejeté comme une retouche réussie.

Enregistrer le même numéro avec une nouvelle version, la filiation, la demande,
le moteur, les tentatives, le contrôle et les preuves de transfert. Conserver les
versions précédentes. Séparer motifs ciel et secours, mais compter une photo
une seule fois dans le total livré. Signaler une résolution réduite ou une cible
de luminosité non atteinte.

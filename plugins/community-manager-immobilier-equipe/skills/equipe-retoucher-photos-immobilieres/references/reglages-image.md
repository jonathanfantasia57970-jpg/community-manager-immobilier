# Balance des blancs, contraste et couleurs

Sommaire : objectif ; références neutres ; exécution et reprise ; contrôle et limites.

## Objectif et décision

Rechercher un rendu photographique naturel, lumineux et lisible, adapté à une
annonce immobilière. Évaluer les réglages sur chaque photo lors du contrôle rapide.
Corriger les écarts observés ; un réglage neutre reste une décision valable si
l'image est déjà équilibrée. Ne pas augmenter tous les curseurs par principe.

Le niveau de luminosité choisi reste valable. Ne pas poser une nouvelle série
de questions sur les curseurs : déterminer les réglages utiles dans le périmètre
autorisé. Réutiliser une préférence explicite de rendu chaud ou neutre si fournie,
sans transformer le style du bien ni créer une ambiance luxueuse artificielle.

| Réglage | Décision |
| --- | --- |
| Température | Réduire une dominante jaune/orange ou bleue gênante, en conservant une chaleur ambiante plausible |
| Teinte | Corriger une dominante verte ou magenta réellement observée |
| Contraste | Donner du relief à une image plate, ou calmer un contraste excessif, sans boucher les ombres ni écraser les nuances claires |
| Saturation | Rapprocher les couleurs d'un rendu naturel ; correction légère et seulement si nécessaire |
| Hautes lumières et ombres | Utiliser la courbe sélective existante, préserver les fenêtres et les zones déjà bien exposées |

La température et la teinte forment la balance des blancs : les appliquer une
seule fois. Ne pas annoncer une température absolue en kelvins calculée à partir
d'un JPEG sans référence d'illuminant. Les paramètres du moteur sont des corrections
relatives, pas des mesures de la température de la pièce ou de l'éclairage.

## Éviter les fausses neutralisations

Chercher une référence vraisemblablement neutre et cohérente dans plusieurs zones
quand possible : équipement sanitaire, plafond ou élément dont l'apparence et le
contexte permettent cette interprétation. Ne pas supposer qu'un mur clair est blanc,
qu'un parquet chaud est trop jaune ou qu'une végétation rend la balance trop verte.
Ne pas appliquer une moyenne grise globale (« gray world ») à un intérieur coloré.

Comparer avec l'original et observer ensemble référence, matériaux et éclairage.
Si la dominante est incertaine, conserver une correction neutre ou très modérée
avec sa limite plutôt que blanchir les matériaux. Harmoniser les angles d'une même
pièce sans imposer le même réglage numérique à toutes les photos.

Sous éclairages mélangés (fenêtre froide et ampoules chaudes), une correction globale
peut améliorer un côté et dégrader l'autre. Privilégier un compromis léger. Si la
dominante reste vraiment gênante et nécessite une correction locale, utiliser le
secours ImageGen prévu, depuis l'original, en indiquant les seules zones concernées
et les couleurs/vues à préserver. Si une dominante forte reste gênante au-delà des réglages bornés du moteur,
le secours ImageGen est également possible après ce diagnostic. Rejeter toute
peinture, texture ou ambiance inventée.

## Exécution avec le moteur fourni

Les valeurs neutres sont `temperature=0`, `tint=0`, `contrast=1`, `saturation=1`.

| Paramètre | Plage autorisée | Neutre |
| --- | --- | --- |
| `temperature` | -0,25 à +0,25 | 0 |
| `tint` | -0,20 à +0,20 | 0 |
| `contrast` | 0,85 à 1,15 | 1 |
| `saturation` | 0,85 à 1,15 | 1 |

Une température positive réchauffe, une température négative refroidit. Une teinte
positive tire vers le magenta, une teinte négative vers le vert. Utiliser de petites
corrections, observer le résultat et rester dans les bornes réellement exposées
par `--help` ; ne pas inventer d'option kelvins ou de masque local.

Pour le batch, ajouter aux seules entrées concernées de l'inventaire :

```json
"reglages_image": {
  "temperature": -0.05,
  "tint": 0.02,
  "contrast": 1.04,
  "saturation": 1.02
}
```

Cet exemple illustre les paramètres, pas un préréglage à appliquer au lot. Sans
ce champ, le moteur applique les réglages neutres. Un objet partiel complète
également les clés absentes avec les valeurs neutres : il ne fusionne pas
implicitement les réglages de la version précédente. Un diagnostic déjà établi
permet de les intégrer à la première passe ; sinon le contrôle rapide identifie
les photos à reprendre avec leurs réglages spécifiques.

Toujours repartir des originaux et regrouper les corrections dans le même rendu :
ne pas enchaîner plusieurs JPEG intermédiaires. Le moteur simule les réglages
combinés pour calibrer la luminosité. Les ajustements de couleur viennent après la
correction tonale dans le moteur et ne doivent pas être préappliqués à la source. Conserver le même numéro et créer une version
distincte quand les réglages changent. Lors de la reconstruction d’un inventaire de reprise, réinjecter les quatre
réglages effectivement retenus depuis le registre pour chaque source inchangée.
Pour changer un seul curseur, copier d’abord les quatre réglages conservés puis
modifier ce curseur ; ne pas effacer implicitement les autres en omettant le champ.
Une reprise avec les mêmes réglages normalisés réutilise une sortie intacte ; ne pas modifier manuellement les anciens rapports
pour les faire passer pour un nouveau traitement.

Une correction de couleur seule est aussi possible avec le script unitaire :

```bash
python3 <skill-dir>/scripts/corriger_luminosite.py \
  '/travail/original.JPG' '/travail/resultats/07_v2.jpg' \
  --temperature -0.05 --tint 0.02 --contrast 1.04 --saturation 1.02
```

Les coefficients restent indicatifs ; utiliser ceux que justifie la photo. Les
paramètres absents conservent leur valeur neutre. Ne pas utiliser une correction
lumineuse déjà appliquée comme source de ce nouvel encodage.

Si ImageGen est déjà nécessaire pour ciel et/ou secours, regrouper dans cet appel
les corrections de couleur effectivement diagnostiquées lorsque cela évite une
étape. Pour un ciel seul sur une photo déjà corrigée, demander de préserver son
rendu colorimétrique ; ne pas réappliquer la balance des blancs.

## Contrôle et limites

La correction de couleur doit préserver la luminance autant que possible ; le
moteur limite les couleurs au gamut de sortie plutôt que créer de nouveaux canaux
saturés. Le contraste reste monotone et protège les hautes lumières. Ces protections
mathématiques ne garantissent pas une bonne décision esthétique. Avec une
balance des blancs non neutre, les valeurs RGB des zones claires peuvent changer
volontairement sans hausse de luminance. Ne pas rejeter ce résultat uniquement
parce que `protected_sample_pixels_changed` est non nul : consulter aussi
`protected_sample_linear_luminance_max_delta` et le rendu réel.

Contrôler blancs et gris plausibles, nuances des peintures, bois, sols, végétation,
textures, contraste dans les ombres et cohérence entre les angles d'une même pièce.
Les blancs réellement brûlés ne contiennent pas de nuances récupérables. Un JPEG
réencodé ou une conversion de profil peut changer légèrement les valeurs des pixels.

Ne pas ajouter de netteté artificielle, débruitage agressif, flou de texture,
« clarté » excessive ou filtre HDR par défaut. Ces opérations ne remplacent pas
une exposition et une balance des blancs correctes. Si les réglages dégradent
les couleurs ou les textures, réduire la correction ou appliquer le secours
fidèle selon la référence, dans le budget de tentatives du skill.

Consigner le diagnostic, les réglages lumière/couleur/contraste, la référence
neutre éventuelle, les limites et le hash réellement contrôlé dans le registre
du coordinateur. Les rapports de calcul restent des candidats techniques tant
que ce contrôle n'a pas eu lieu.

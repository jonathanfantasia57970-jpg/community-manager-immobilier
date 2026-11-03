# Éclaircissement sélectif avec Pillow

## Méthode

Utiliser `scripts/traiter_lot_rapide.py`, qui réutilise le moteur
`scripts/corriger_luminosite.py`. Pillow lit, oriente et encode ; NumPy applique
une courbe tonale par bandes en lumière linéaire. Aucune génération, suppression
d'objet, correction spatiale, netteté artificielle ou reconstruction du bien.

Le moteur `pillow-developpement-4` utilise deux courbes monotones, sans opération
spatiale : une remontée des ombres sous l'équivalent gris sRGB 160/255, puis une
correction des tons sombres et moyens ancrée à 220/255. Pour le traitement positif
par défaut (`highlights=0`), les pixels dont la luminance source dépasse ce second
seuil ne reçoivent pas d'éclaircissement. Le raccord tonal est continu, sans masque
spatial flouté ; le contraste près des seuils peut néanmoins être comprimé et doit
être jugé au contrôle rapide. Le gain RGB commun protège les teintes et empêche de
créer un canal à 255 sur un pixel qui n’en contenait pas déjà. Cette conservation
de teinte concerne la courbe lumineuse ; une balance des blancs explicitement
réglée corrige ensuite la dominante selon `reglages-image.md`.

Ce masque repose sur la luminance, pas sur la reconnaissance d'un mur ou d'une
fenêtre. Il n'atteste pas que toute surface sombre manque de lumière. Les couleurs
saturées peuvent limiter le gain ; conserver leur teinte plutôt que forcer la cible.
La protection exacte concerne la courbe avant encodage : une conversion de profil
ou un nouvel encodage JPEG peut modifier légèrement des valeurs. Ne pas promettre
une égalité des octets des zones blanches après JPEG. Un `highlights` non nul ou
une baisse d'exposition explicitement demandée sont des corrections manuelles
séparées, qui peuvent modifier les zones claires.

La calibration `developpement-selectif-4` simule la vraie courbe sur un aperçu de
192 pixels au maximum et recherche en douze étapes bornées la correction utile.
Elle simule aussi le contraste et la couleur lorsqu’ils sont renseignés, sans
appliquer deux fois ces réglages. Elle exclut les zones protégées et les noirs absolus de la population à éclaircir,
puis conserve ce masque source pendant la mesure : une grande fenêtre blanche ne
doit pas masquer une pièce sombre. Les cibles de médiane sont 160, 180 et 198 sur
255 pour les pixels éligibles, sans assombrir une médiane déjà supérieure. Les
repères du premier quartile sont 100, 118 et 135, limités à une cible de
+25/+40/+55 points depuis l'original. Ce sont des repères, pas une norme esthétique.

L'exposition reste bornée à +3 EV et les ombres à 1,5 dans le batch. Ces bornes ne
prouvent ni l'absence de bruit ni la fidélité du contraste. Avec des réglages couleur/contraste neutres, une image entièrement
claire reste inchangée ; le noir absolu ne contient pas de détail à récupérer.
Signaler toute cible non atteinte et tout plafonnement de niveaux. Ne pas forcer
un éclaircissement des blancs pour satisfaire une moyenne globale. Ne produire
que le niveau demandé et n'encoder la pleine définition qu'une fois avant contrôle.

Le contrôle rapide de toutes les sorties et les reprises nécessaires suivent
`retouche-et-controle.md`. Une forte correction ou des limites numériques motivent
un agrandissement ciblé ; elles ne décident pas seules d'une reprise ImageGen.

Vérifier une fois les imports Pillow et NumPy. Le code ne demande aucune clé API.
S'il manque une dépendance ou si un format est refusé, résoudre le problème
technique dans le périmètre autorisé ou le signaler ; ne pas appeler ImageGen.

## Exécuter le batch

```bash
python3 <skill-dir>/scripts/traiter_lot_rapide.py \
  '/travail/inventaire.json' '/travail/resultats' \
  --niveau un_peu_plus_lumineux --workers 3
```

Niveaux : `normal`, `un_peu_plus_lumineux`, `beaucoup_plus_lumineux`.
Entrée : l'objet JSON de `inventorier_photos.py`, enrichi si nécessaire avec un
`source_id` stable dans chaque entrée. Pour une source distante, employer une
identité qualifiée par le service/compte/drive afin d'éviter les collisions.
Sans `source_id`, le script utilise `source_key` de l'inventaire local.

Conserver le même dossier de travail et `suivi-lot-rapide.json` à la reprise.
Le coordinateur écrit le mapping avant le calcul puis le journal à chaque
résultat. Les photos sont traitées dans un pool de trois workers, jusqu'à cinq
si les ressources le permettent. Réduire à un ou deux pour les très grandes
images ou en cas de pression mémoire ; le nombre de CPU ne prouve pas la mémoire
disponible. Ne pas lancer plusieurs batchs écrivant le même journal.

Une source/version, un niveau et les mêmes `reglages_image` normalisés, avec un
résultat intact, peuvent être
réutilisés pour le calcul. Le contrôle visuel et les décisions ciel/secours du
processus classique restent obligatoires si le registre ne les atteste pas.
Conserver `calibration_version` sur chaque version. Après une demande de reprise
et une correction de calibration, ajouter `--recalibrate` : produire une nouvelle
version seulement si la calibration courante diffère, conserver les sorties
antérieures, puis réutiliser la nouvelle version à toute reprise identique.
Sans cette option, une mise à jour du skill ne recalcule pas un lot existant.
Avec une calibration inchangée, `--recalibrate` réutilise également le résultat :
ne pas le présenter comme un bouton d'éclaircissement supplémentaire. Après un
nouveau retour, adapter réellement les réglages ou le niveau selon la demande.
Lire `version_courante` pour choisir le résultat à livrer, plutôt que prendre
systématiquement la dernière entrée de `versions` : revenir à un ancien niveau
réutilise sa sortie intacte sans nouveau calcul ni nouvelle compression.
Les nouvelles sources sont ajoutées à la fin de la numérotation. Un changement
de niveau ou de contenu produit une version distincte depuis l'original.
Ne pas réessayer automatiquement une erreur inchangée : résoudre sa cause avant
une reprise explicite avec `--retry-errors`. Réconcilier d’abord une interruption
avec la destination ; ne pas utiliser cette option pour refaire un succès déjà
livré. Le retour non nul d’un lot partiel ne supprime pas ses succès.

Le batch ne transfère rien sur OneDrive ou Library. Rattacher ses résultats au
registre distant et confirmer chaque transfert séparément. Pour une autre machine,
matérialiser les sorties et adapter seulement les chemins de travail connus ;
les identités et numéros ne dépendent pas de ces chemins. Pour modifier couleur
ou contraste, renseigner `reglages_image` sur les entrées concernées : voir
[reglages-image.md](reglages-image.md). Repartir de l’original, conserver le niveau
et le numéro ; un changement de ces réglages crée une version distincte.

## Conservation et limites

- Conserver la définition native après orientation EXIF. Les aperçus seuls sont réduits.
- Sortie JPEG qualité 95, 4:4:4 ; PNG pour la transparence. Si une sortie sans perte
  est explicitement demandée, utiliser la fonction `estimate_settings` pour calculer
  les réglages puis le script unitaire vers une nouvelle destination PNG, sans
  première sortie JPEG. Conserver le même mapping et le journal avec ce chemin.
  Si les réglages sont nuls, copier une source PNG inchangée ou convertir sans
  perte une autre source compatible ; ne pas présenter cette conversion comme
  une correction de luminosité.
- Si le calcul ne propose pas de correction, conserver les octets et le format
  d'origine ; ne pas compter cette copie comme retouche ou validation esthétique.
- Préserver les profils et l'orientation selon le moteur fourni. Sans profil,
  l'hypothèse sRGB est consignée. Refuser les conversions couleur non fiables.
- Refuser les animations, formats non pris en charge et haute profondeur identifiée
  plutôt que les réduire silencieusement. Ce moteur n'est pas un développeur RAW.
- La passe de calcul ne réalise pas de contrôle visuel. Le coordinateur effectue
  ensuite le contrôle rapide de toutes les sorties et les agrandissements ciblés,
  puis les corrections de ciel ou secours nécessaires avant la livraison finale.
- Les noirs et blancs absolus ne récupèrent pas des détails absents. Le traitement
  peut révéler du bruit ; une dégradation réellement observée déclenche le secours
  ImageGen autorisé depuis l’original, avec contrôle de fidélité.

Le moteur unitaire retourne `candidate_requires_visual_review`. Le batch utilise
`produite_a_controler` ou `copiee_a_controler` et reconnaît les anciens statuts à
la reprise. Ni ces statuts ni les mesures du masque ne constituent une validation
esthétique. Garder `controle_visuel=non_effectue` et `niveau_atteint=null` jusqu'au
contrôle réel dans le registre du coordinateur. Conserver les valeurs de
production dans le journal local du batch ; faire évoluer contrôle, décision,
limites et livraison dans le registre distant, sans remplacer ses statuts locaux.
Seul un transfert confirmé permet `enregistre=true` dans le registre distant.

Pour une correction manuelle Pillow explicitement demandée, le script unitaire
reste disponible pour lumière, couleur et contraste ; repartir de l’original et
garder une nouvelle version. Les paramètres couleur peuvent être employés seuls,
sans éclaircissement supplémentaire, si cela suffit :

```bash
python3 <skill-dir>/scripts/corriger_luminosite.py \
  '/travail/original.JPG' '/travail/resultats/07_v2.jpg' \
  --exposure-ev 0.25 --shadows 0.7
```

Ne pas confondre le temps cumulé du calcul et le temps total jusqu'à la livraison.
Mesurer séparément préparation, calcul et transferts ; annoncer tout délai futur
comme une estimation tant qu'il n'a pas été observé sur ce workflow.

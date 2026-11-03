---
name: equipe-retoucher-photos-immobilieres
description: 'Retoucher des photos immobilières avec un rendu crédible : lumière, couleurs, contraste, verticales, ciel et distractions. Utiliser pour améliorer un dossier photo sans modifier la structure, les volumes, les équipements ou la réalité du bien. Contrôler chaque image finale avant livraison.'
---
## Routage et relecture du plugin

Pour appeler un autre module ou lire ses références, appliquer `../../references/routage-skills.md`. Pour toute revue de contenu, appliquer `../../references/relectures-et-capacites.md` : utiliser les agents réellement disponibles ou le relais humain documenté, sans inventer de contrôle indépendant.


## Profil personnel et version commune

Avant le travail métier, lire `../../references/contrat-equipe.md` et `../../references/mise-a-jour-et-personnalisation.md`. Résoudre le profil courant avec `equipe-configurer-espace` sans le réinitialiser. Le profil, les corrections et préférences du conseiller priment sur les valeurs de départ pour le ton, les thèmes, la charte et les modalités de communication. Les faits, droits, relectures et mandats restent requis. Aucune donnée du créateur ni connexion commune n'est fournie. Les Ads sont hors périmètre.



# Retoucher les photos immobilières

Livrer une série après une passe Pillow rapide, un contrôle visuel léger et les
retouches ImageGen nécessaires. Préserver les zones déjà correctement éclairées.
Lire [luminosite-pillow.md](references/luminosite-pillow.md) et
[reglages-image.md](references/reglages-image.md)
pour le traitement et [execution-et-reprise.md](references/execution-et-reprise.md)
pour les transferts, la reprise ou l'arrière-plan.

## Workflow par défaut

1. Résoudre le dossier et le niveau de luminosité.
2. Inventorier les sources et attribuer des numéros stables.
3. Exécuter une passe Pillow sélective en parallèle : relever les ombres et les
   tons moyens utiles, protéger les zones déjà claires et les hautes lumières.
4. Examiner rapidement **toutes** les sorties à taille lisible, par petites
   planches numérotées si utile ; ouvrir les originaux et détails seulement pour
   les photos suspectes et les zones de ciel à identifier. Évaluer aussi balance
   des blancs, température/teinte, contraste et saturation. Corriger les écarts
   utiles avec Pillow depuis l’original, selon la référence des réglages.
5. Remplacer avec ImageGen les ciels gris/ternes qui s'y prêtent et reprendre
   depuis l'original les images dégradées par Pillow. Vérifier ces résultats.
6. Enregistrer les versions finales dans `Photos retouchées`, livrer le lien et
   les limites éventuelles. Accepter ensuite les retours par numéro.

Ce processus classique remplace le mode « sans contrôle, ImageGen seulement sur
retour utilisateur ». Le contrôle rapide, le ciel bleu pertinent et le secours
ImageGen, ainsi que les ajustements utiles de couleur et de contraste, sont
autorisés par la demande de traiter le dossier : aucune approbation
supplémentaire par photo. Respecter néanmoins une consigne explicite limitant les
moteurs ou interdisant le remplacement de ciel.

Garder un seul passage de calcul pleine définition avant le contrôle, sans audit
approfondi systématique. La calibration sur aperçu ne remplace pas l'examen final.
Les zones déjà blanches ne doivent pas être éclaircies davantage. Ne pas confondre
un masque de luminance avec une compréhension des matériaux : une peinture sombre
n'est pas nécessairement une zone sous-exposée.

Préserver originaux, définition native avec Pillow, cadrage, objets, couleurs et
état réel du bien. La « reconstitution ImageGen » désigne une reprise fidèle depuis
l'original, jamais l'invention d'architecture, de vues ou de détails absents.
Régler la balance des blancs et le contraste si le diagnostic le justifie, sans
neutraliser une couleur réelle ni effacer l’ambiance lumineuse. La température
et la teinte constituent la balance des blancs : ne pas cumuler deux corrections
équivalentes. Ne pas ajouter texte, logo ou cadre.
La numérotation concerne seulement les noms de fichiers.

Une modification du skill ne relance ni ne renomme un dossier déjà traité.
Un « stop » reste valable jusqu'à une demande de reprise. Une question
« tu as fini ? » appelle un bilan bref puis la poursuite du travail autorisé.

## 1. Choisir le niveau et résoudre le dossier

Demander une seule fois le niveau, sauf choix déjà fourni pour ce lot :

- **Normal** : corriger d'abord la sous-exposition pour rendre les pièces lisibles.
- **Un peu plus lumineux** : obtenir une différence visible au-dessus de cette base
  corrigée ; ne pas se contenter d'éclaircir imperceptiblement l'original.
- **Beaucoup plus lumineux** : produire un rendu franchement clair, avec des ombres
  plus ouvertes, en préservant les détails encore présents dans les hautes lumières.

Conserver `normal`, `un_peu_plus_lumineux` ou `beaucoup_plus_lumineux`, avec
`origine_niveau=choix_utilisateur`. Réutiliser ce choix à la reprise. Employer
l'outil de question disponible ; s'il retourne sans réponse, annoncer « Normal »
comme hypothèse et enregistrer `origine_niveau=hypothese_annoncee`. Préparer
l'inventaire pendant l'attente lorsque possible. Transmettre le niveau résolu
à toute tâche autonome ; ne pas y reposer la question.

Réutiliser le service, chemin, lien ou identifiant fourni. Sans service indiqué,
chercher dans Library ; pour un chemin local explicite, utiliser ce chemin.
Charger le skill du connecteur concerné. Ne demander un emplacement qu'en
l'absence de cible identifiable, ou un choix si plusieurs dossiers correspondent.
Vérifier les droits et l'identité du parent une seule fois ; réutiliser le compte,
les outils et la destination durant tout le lot.

Traiter les photos directement dans le dossier ; parcourir les sous-dossiers
uniquement sur demande. Exclure dossiers de résultats, archives de traitement,
liens symboliques et documents explicitement identifiés par leurs métadonnées
ou par l'utilisateur. Ne pas prétendre reconnaître un plan uniquement par son
extension ; écarter les documents repérés lors du contrôle rapide, sans les livrer
comme photographies retouchées.
Lister toutes les pages, signaler les formats illisibles ou incompatibles.
Créer/réutiliser `Photos retouchées` sous le bon parent, sur le même service.

## 2. Numéroter et préparer

Attribuer `01`, `02`, `03`, etc. dans l'ordre naturel des chemins relatifs lors du
premier inventaire. Relier chaque numéro à l'identifiant stable de la source
(distante si disponible), sa version ou son SHA-256, son nom d'origine et ses
résultats. Enregistrer cette correspondance avant le calcul ou les transferts.

Conserver les numéros à toute reprise, même si l'ordre de liste change. Ajouter
les nouvelles sources après le plus grand numéro ; ne pas réutiliser les numéros
des sources absentes. Un changement de contenu de la même source conserve son
numéro et crée une nouvelle version. Sans preuve d'identité stable, préserver
les fichiers et résoudre la correspondance avant une retouche ciblée.

Pour un lot ancien déjà livré sans numéro, ne pas renommer ou recalculer
spontanément. Lors d'une demande portant sur ce lot, établir la correspondance
avec son registre existant ; demander seulement la précision réellement manquante.

Matérialiser les sources selon le workflow du service. Préférer le runtime qui
peut à la fois recevoir les sources, exécuter Pillow/NumPy et transférer les
résultats : éviter les allers-retours entre plusieurs environnements.
Sur les copies de travail, utiliser l'inventaire fourni si nécessaire :

```bash
python3 <skill-dir>/scripts/inventorier_photos.py '/travail/originaux' > '/travail/inventaire.json'
```

Ajouter `--recursive` seulement si autorisé. Rattacher les identités distantes
aux entrées (`source_id`) avant le batch. Vérifier que toutes les sources
inventoriées à distance sont représentées ; ne pas re-télécharger celles déjà
présentes et inchangées. Les champs de contrôle de l’inventaire ne prouvent pas
que les photos ont été examinées ; effectuer le contrôle final prévu ci-dessous.

## 3. Première passe Pillow

Utiliser `scripts/traiter_lot_rapide.py` selon la référence luminosité. Il calibre
la courbe sélective sur le rendu simulé d'un aperçu : tons moyens et ombres utiles,
puis traite la définition native. Ce calcul ne vaut pas appréciation esthétique.
Une tentative automatique par source/version
et niveau avant le contrôle. Par défaut, les réglages couleur/contraste sont
neutres pour un nouveau traitement ; à la reprise, réinjecter ceux retenus depuis
le registre dans l’inventaire plutôt que les omettre. Le contrôle rapide recherche
les améliorations utiles. Si un diagnostic
fiable existe déjà, renseigner `reglages_image` dans l’inventaire et combiner
luminosité, couleur et contraste dans ce premier encodage. Réserver les reprises
aux écarts réellement
observés ; ne pas recalculer automatiquement tout le lot pour une seule photo.

Employer un coordinateur et un pool de calcul, pas cinq agents qui inspectent
les images. Le script utilise trois workers par défaut, réglables de un à cinq
selon CPU et mémoire. Chevaucher lecture, calcul et transfert lorsque leurs
outils le permettent ; suivre la référence pour les contraintes du service.

Livrer `01.jpg`, `02.jpg`, etc. ; garder `.png` si nécessaire, notamment pour
la transparence, et le format exact pour les copies sans recompression. Une
nouvelle version utilise `07_v2.jpg` ou `07_v2.png`, sans changer le numéro 7.
Ne jamais écraser un fichier non identifié. Conserver les anciennes versions.
Les copies ne comptent pas comme retouches.

Le batch produit des candidats : `controle_visuel=non_effectue`,
`niveau_atteint=null`, `enregistre=false`. Conserver ces états
de production dans `suivi-lot-rapide.json`. Le coordinateur fait évoluer les
champs de contrôle et de livraison dans le registre distant `suivi-retouches.json`,
après les étapes réellement réalisées, sans inventer de contrôle ou de transfert.

## 4. Contrôle rapide, ciel et secours

Lire [retouche-et-controle.md](references/retouche-et-controle.md). Voir chaque
photo du lot, y compris les copies et sorties réutilisées non encore contrôlées.
Utiliser des planches internes de quatre à six résultats au maximum, chaque vue
assez grande pour juger pièce, façade et ciel ; agrandir les cas douteux. Ce n'est
ni un simple contrôle statistique ni un examen exhaustif à 100 % de tout le lot.

Repérer rendu trop sombre/clair, contraste aplati, blancs dégradés, bruit visible,
artefacts, dominantes nouvelles et documents à exclure. Sur les corrections fortes
ou suspectes, comparer à l'original et examiner une zone sombre à taille native.
Évaluer la balance des blancs, les dominantes jaune/bleu et vert/magenta, la
profondeur du contraste et la fidélité des couleurs. Suivre
[reglages-image.md](references/reglages-image.md) : pas de gris moyen supposé
ni de refroidissement systématique des intérieurs.
Puis décider : conserver, ajuster Pillow une fois depuis l’original en regroupant
luminosité, couleur et contraste,
ImageGen pour ciel, ImageGen pour dégradation, ou signaler une limite.

Un ciel réellement identifié, gris ou terne, est remplacé par un bleu naturel
compatible avec l'éclairage. Garder un ciel déjà agréable, les couchers de soleil,
ambiances nocturnes et toute vue réelle. Ne pas confondre fenêtre brûlée et ciel.
Si l'image présente aussi du bruit ou une dégradation, demander luminosité et ciel
en un seul appel depuis l’original. Inclure également la correction colorimétrique
justifiée si nécessaire ; ne pas multiplier les passages ou les encodages.
Pour un ciel seul, utiliser le candidat Pillow
accepté afin de conserver son éclaircissement.

Déclencher le secours ImageGen si Pillow révèle trop de bruit, des aplats/bandes,
perd des textures ou laisse le sujet inexploitable à la cible sans correction
propre. Une dominante locale gênante sous éclairages mélangés peut aussi demander
une reprise ImageGen si le réglage global abîmerait les autres zones ; justifier
ce choix et préserver les couleurs réellement observables. Une petite différence esthétique ne suffit pas. Une erreur de dépendance,
de format ou de transfert reste technique ; elle ne déclenche pas ImageGen.

Charger `imagegen`, fournir l'image réelle inspectée et appliquer les contraintes
de fidélité de la référence. Contrôler chaque résultat génératif contre l'original
avant livraison. Maximum trois exécutions de retouche par photo/version source et
mission, Pillow initial compris ; ne pas réinitialiser à la reprise. Si le premier
Pillow est clairement dégradé, passer directement au secours plutôt que multiplier
les essais. Aucune API payante ou autre moteur sans demande.

Consigner le hash/version réellement vu, `controle_visuel=rapide_effectue`, la
`decision_ciel` et son motif, les anomalies, la source de chaque reprise et le
résultat du contrôle ImageGen. Le niveau peut être validé au contrôle ou rester
`niveau_atteint=false` avec sa limite. Distinguer ce contrôle de
`validation_utilisateur=en_attente`. Ne pas livrer un candidat rejeté comme final.
Si aucun résultat fidèle n'est exploitable, conserver l'original en repli identifié
et signaler l'échec ; une retouche jugée dégradée ne devient pas un repli acceptable.

## 5. Enregistrer et livrer

Transférer réellement les photos dans le sous-dossier demandé. Inspecter les
retours de transfert ; confirmer identité, nom, taille et bon parent avec les
métadonnées fournies. Ne pas refaire un GET ou télécharger les octets si la
réponse contient déjà les preuves suffisantes. Marquer `enregistre=true`
uniquement après confirmation. Respecter les contraintes spécifiques Library.

Conserver un registre distant `suivi-retouches.json` avec numéros, identités,
versions/hashes, niveau et origine, réglages lumière/couleur/contraste, motif
des ajustements et référence neutre éventuelle, tentatives, état technique, résultats,
erreurs et preuves de sauvegarde. Le journal local est distinct et ne prouve pas
l'enregistrement distant. Un coordinateur unique écrit les registres ; regrouper
les sauvegardes distantes par petits lots selon la référence.

Ne créer ni ZIP ni rapport détaillé par défaut. Les planches de contrôle sont
des intermédiaires internes, pas des livrables obligatoires. Donner le lien et
un bilan bref : nombre de photos livrées, niveau, ciels remplacés, secours ImageGen,
limites et erreurs éventuelles. Ne compter chaque photo qu'une fois dans le total,
même si un appel ImageGen a corrigé à la fois lumière et ciel.

La livraison finale exige le contrôle rapide et le traitement des décisions ciel
et secours. Si ImageGen est indisponible, livrer seulement les sorties utilisables
avec un bilan explicitement partiel et les numéros restant à traiter. Une ancienne
sortie simplement enregistrée ne prouve pas que ces nouvelles étapes sont terminées.
L'utilisateur peut ensuite demander une modification par numéro.

## 6. Retour sur la luminosité

Si l'utilisateur juge le lot trop sombre, reprendre le lot déjà identifié depuis
les originaux, en conservant le niveau souhaité : une correction insuffisante
n'est pas la preuve qu'il a mal choisi son niveau. Pour des numéros précis,
limiter la reprise à ces sources. Ne pas redemander le dossier ou le niveau connu.

Examiner alors quelques exemples représentatifs (trois au maximum) en comparant
original et version livrée pour comprendre la cause. Ajuster une seule fois, puis
contrôler rapidement toutes les nouvelles sorties et livrer avec les mêmes numéros.
Si la calibration
du script a été corrigée, employer `--recalibrate` pour ne pas réutiliser l'ancien
rendu au même niveau. Enregistrer le retour, la version de calibration, les limites
et les vues réellement examinées. Distinguer le diagnostic sur trois exemples
du contrôle rapide qui couvre toutes les nouvelles sorties.

Pour une reprise de lumière, couleur ou contraste, continuer avec Pillow si la qualité le permet.
En cas de dégradation constatée, appliquer le secours ImageGen du processus classique.
Une modification du skill seule ne relance aucun lot.
Lire la référence luminosité pour une correction manuelle explicitement demandée.

## 7. Retouche ImageGen supplémentaire sur demande

Pour « reprends les photos 3 et 7 avec ImageGen », résoudre les sources et versions
via le registre. Réutiliser le niveau et le motif donnés. Dans une reprise
ImageGen déjà demandée, désigner ensuite des images trop sombres suffit pour
autoriser ces cibles supplémentaires.
Ne pas redemander une approbation photo par photo ni relancer les autres photos.

Charger `imagegen` et [retouche-et-controle.md](references/retouche-et-controle.md).
Inspecter seulement les cibles sélectionnées et leurs originaux ; employer la
vraie image originale pour corriger la lumière, jamais une retouche dégradée.
Pour un ciel seul, utiliser la version courante explicitement choisie et inspectée.
Conserver le bien, ses défauts et les vues extérieures. Vérifier visuellement
chaque résultat ImageGen contre l'original avant livraison.

Pour plusieurs cibles, paralléliser jusqu'à cinq appels indépendants si l'outil
le permet. Des agents sont autorisés pour les retouches ciblées et pour répartir
le contrôle rapide en petits lots ; ne pas les créer pour la passe mécanique Pillow.
Une seule cible par appel et un seul
coordinateur pour le registre. Limiter à trois appels par photo et demande de
reprise ; conserver le compteur à l'interruption. Ne pas lancer une API payante
ou un autre moteur sans demande.

Enregistrer une version distincte avec le même numéro et son vrai format.
Conserver la version précédente, signaler toute limite de résolution ou tout
échec de fidélité. Ne pas publier ni partager le dossier sans demande.

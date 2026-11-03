# Exécution, parallélisme et reprise

## Première passe : minimiser les allers-retours

1. Résoudre une fois le service, le compte, les outils, les identités source et
   destination ; garder ces résultats pendant le lot.
2. Lister les sources en lots et figer leur numérotation avant les tâches parallèles.
   Télécharger jusqu'à cinq fichiers indépendants simultanément si le connecteur
   le permet. Lire entièrement les réponses déportées, pas seulement leur aperçu.
3. Préférer un runtime disposant à la fois de Pillow/NumPy, des sources et du
   moyen de transfert vers le service. Éviter de faire passer les photos par un
   ZIP, Library puis un second téléchargement quand un trajet direct est possible.
   Respecter néanmoins les helpers obligatoires du service et les limites d'accès.
4. Calculer avec un seul batch et un pool de trois workers, jusqu'à cinq selon
   CPU/mémoire. Aucun agent d'inspection photo par photo pour cette passe.
   Tester les écritures avant calcul : le moteur exige des liens physiques pour
   enregistrer sans écraser. Un montage objet (`/mnt/files` dans certains runtimes)
   peut les refuser. Calculer alors sur un disque natif, par exemple `/home/user`,
   puis transférer ; ne pas remplacer le calcul par des écritures non protégées.
   Vérifier aussi si `/tmp` est en mémoire (`tmpfs`) : y copier de gros originaux
   peut épuiser la RAM. Avec environ 1 Go de RAM et des photos de 18 Mpx, commencer
   avec un worker, sur disque natif. Réutiliser les sources déjà récupérées.
   Libérer les images d'aperçu et leur mémoire avant le batch ; le moteur traite
   par bandes de 64 lignes et ferme le décodeur source dès que sa copie est prête.
5. Contrôler rapidement chaque sortie, par petites planches lisibles ; réserver
   les agrandissements et comparaisons aux photos suspectes et ciels à traiter.
   Paralléliser ce tri sur des lots disjoints si utile, avec trois agents au maximum
   et un coordinateur ; chaque fiche cite les numéros et hashes effectivement vus.
   Regrouper les ajustements utiles de lumière, température/teinte, contraste et
   saturation dans une seule reprise depuis l’original. Si ces réglages sont déjà
   identifiés, les intégrer au premier calcul par `reglages_image`.
   Réaliser ensuite les remplacements de ciel et secours ImageGen nécessaires,
   puis contrôler ces résultats contre leurs originaux.
6. Transférer les sorties contrôlées par lots de trois à cinq appels indépendants si
   le service le permet ; chevaucher les autres téléchargements et calculs lorsqu'un
   orchestrateur sait le faire. Le script batch seul ne réalise pas ce pipeline réseau.
   Ne pas attendre la photo la plus lente si des résultats sont déjà disponibles.
7. Inspecter chaque réponse. Réutiliser ses preuves de parent, identité et taille.
   Faire une lecture complémentaire uniquement si ces preuves manquent. Ne pas
   re-télécharger les sorties pour une vérification supplémentaire par défaut.

Les préparations qui partagent un kernel mutable, les écritures du registre et
les opérations dépendantes restent séquentielles. Pour Library, utiliser ses
lots/helpers et son ordre d'écriture imposé ; ne pas paralléliser les écritures
si le service l'interdit. Pour Composio, préférer un appel bulk documenté à des
appels concurrents au même workbench. Ne jamais inventer une capacité de lot.

Un coordinateur unique gère le registre. Écrire atomiquement le journal local
après chaque résultat, puis sauvegarder le registre distant après chaque lot
de cinq confirmations au maximum, ou après environ 60 secondes si l'exécution
continue. Sauvegarder aussi en fin de lot, sur erreur, pause ou interruption
contrôlable. Ne pas écrire une fois par photo sur le réseau par défaut.

Si le journal local n'est pas durable, persister au moins le mapping initial et
les noms de sorties attendus avant transfert. À la reprise d'un lot interrompu,
rapprocher registre et destination avant de réenvoyer : des photos peuvent avoir
été enregistrées après le dernier checkpoint distant. Une présence par nom seule
ne suffit pas ; vérifier identité connue, taille et hash/version si nécessaire.
En cas de doute, préserver le fichier et une version distincte.

En cas de 429 ou saturation, respecter le délai retourné et réduire la concurrence
à trois puis un. Ne pas multiplier agents, comptes ou appels pour contourner un
quota. Attendre tous les travaux lancés via les mécanismes documentés ; aucune
promesse abandonnée en fin de script. Mesurer le temps total et distinguer calcul
et transferts, sans promettre une accélération proportionnelle au nombre de workers.

## Reprise et état

Le registre distant `suivi-retouches.json` conserve service/compte/parents, mode,
niveau et origine, mapping stable numéro/source, version ou hash, nom/identité du
résultat, réglages lumière et `reglages_image`, motif colorimétrique, tentatives, erreurs,
contrôle rapide lié au hash, décision de ciel,
secours et contrôle ImageGen, confirmation de transfert et validation utilisateur. Ne pas y stocker de secrets, URL signées ou chemins éphémères inutiles.
Le journal local du batch reste un état de production, pas une preuve de livraison.

Dans le registre distant du coordinateur uniquement, distinguer `a_traiter`, `en_cours`, `produite_a_controler`, `controle_rapide_ok`,
`ciel_a_traiter`, `secours_imagegen`, `validee_a_enregistrer`, `livree`, `repli` et
`erreur`. Les statuts techniques historiques du batch (`produite_a_revoir`,
`copiee_a_revoir`), comme les nouveaux `produite_a_controler`/`copiee_a_controler`, signifient « à contrôler ». Le script Pillow
ne réalise pas de contrôle visuel. Garder ces statuts de production dans le journal
local `suivi-lot-rapide.json` : ne jamais les remplacer par `controle_rapide_ok`,
`validee_a_enregistrer` ou `livree`, que le batch ne reconnaît pas. Consigner les
contrôles, décisions ciel/secours et livraisons dans `suivi-retouches.json`.
À la reprise, fusionner les seules données de production nécessaires sans écraser
les contrôles/transferts déjà confirmés pour le même hash. Une sortie Pillow
réutilisée reste un intermédiaire si une version ImageGen finale a été retenue ;
ne pas remplacer cette version finale par l’intermédiaire du batch.
Une livraison peut rester `validation_utilisateur=en_attente` après le contrôle
interne ; ne pas confondre ces deux validations.

Lors de la reconstruction de l’inventaire, réinjecter les quatre valeurs
`reglages_image` conservées pour chaque source inchangée. Leur omission signifie
réglage neutre dans le batch, pas « conserver le précédent ». Pour changer un seul
réglage, modifier la copie complète des quatre valeurs.

Ne sauter un résultat que si la source/version, le niveau et les réglages
normalisés `reglages_image` sont inchangés et si
l'artefact attendu existe encore. Réutiliser le calcul, mais effectuer le contrôle
rapide et les décisions ciel/secours manquants avant de le considérer final.
Un contrôle se réutilise uniquement pour le même hash et le même processus
`classique_selectif_couleur_2` ; un changement de moteur sur un lot déjà livré ne relance
rien sans demande. Reprendre un transfert sans refaire le calcul
quand le fichier produit est intact. Un état `en_cours` périmé n'atteste pas qu'un
travail tourne encore. Réutiliser une génération retrouvée avant de la relancer.
Garder les numéros, niveaux et compteurs ; ne jamais reprendre une retouche comme
original. Un nouveau niveau produit une version distincte, pas un écrasement.

Sur « tu as fini ? », donner les nombres livrés, produits à transférer, restants
et bloqués, puis continuer le travail autorisé. Sur « stop », arrêter les nouvelles
affectations et les transferts, interrompre ce qui peut l'être et sauvegarder.
Ne pas relancer le lot pour valider une modification du skill.

## ImageGen après contrôle ou sur demande

Résoudre les numéros signalés au contrôle ou demandés par l’utilisateur et lire
`retouche-et-controle.md`. Paralléliser jusqu'à cinq cibles indépendantes lorsque
possible ; des agents peuvent recevoir chacun une source, sa version, le numéro,
le motif constaté (ciel, dégradation, retour) et le niveau, les contraintes de fidélité et une destination
locale distincte. Ne pas leur faire redécouvrir le service ni écrire le registre.
Le coordinateur transfère les versions retenues et conserve les précédentes.

## Arrière-plan uniquement sur demande

Parallélisme et exécution autonome sont distincts. Ni un skill ni un worker ou
un agent ne garantit une poursuite après la fermeture ou interruption du tour.
Ne créer une tâche autonome ponctuelle que sur demande explicite d'arrière-plan
ou de planification ; ne pas ajouter de récurrence ou surveillance permanente.

Découvrir le planificateur et lire son schéma réel. Vérifier l'accès au skill,
aux sources, à Pillow/NumPy et au service de destination dans la surface cible.
Vérifier ImageGen pour le processus classique (ciels et secours après contrôle).
S'il manque, signaler cette capacité manquante et livrer un bilan partiel lorsque
des photos en ont besoin ; ne pas supprimer silencieusement ces étapes.
Choisir une exécution indépendante uniquement si l'option est réellement exposée ;
ne pas inventer de paramètres `background` ou `standalone`.

Transmettre identités persistantes, périmètre, niveau déjà choisi, mapping,
registre, passe sélective, contrôle rapide, décisions ciel/secours, règles de
fidélité et confirmation
de livraison. Ne pas dépendre des variables du chat ou de fichiers éphémères.
Vérifier la création réelle et si possible le démarrage ; distinguer tâche créée,
lancement demandé, exécution observée et photos livrées. Si indisponible, annoncer
la limite ; ne pas substituer silencieusement une longue exécution dans le chat.

Sur arrêt, suspendre les futurs déclenchements et demander l'arrêt de l'exécution
active avec les outils exposés ; ne pas confondre pause du calendrier et annulation
d'un appel déjà lancé. Une exécution planifiée ne crée pas une seconde tâche.

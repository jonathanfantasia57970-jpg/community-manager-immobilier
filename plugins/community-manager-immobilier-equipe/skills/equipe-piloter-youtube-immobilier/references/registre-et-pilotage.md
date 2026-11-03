# Registre et intégration au pilote

## Propriété et reprise

Le registre YouTube est la référence personnelle dans `storage.registry_refs.youtube`. Lire ses décisions et opérations courantes. Un contenu multicanal existant garde son registre propriétaire ; ne conserver ici qu’un index vers sa référence. Aucun deuxième calendrier ou texte mutable concurrent.

Si une source plus récente remplace cette organisation avec preuve de migration, la suivre et laisser une redirection. Ne pas créer un registre parce qu'un premier accès échoue. Vérifier l'identité avant écriture ; relire versions et changements concurrents. Pour Library, utiliser les mécanismes de version et ne pas écraser un fichier modifié. Pour Notion, faire une mutation ciblée et préserver les autres entrées.

## Entrée minimale par nouveau contenu

- Identifiant stable, business, chaîne, source canonique et version.
- Audience, objectif, preuve/source des faits, format et raison éditoriale.
- Échéance retenue ou simple intention ; titre/description/script complets et médias finaux référencés lorsque produits.
- Droits, état du bien, contexte, offre/date, audience enfants et déclaration IA si applicables.
- Mandat exact, source/date et version couverte ; ne pas remplacer par « compte connecté ».
- Exécutant, réservation, début, opération et état : intention / brief / script_prêt / tournage_requis / montage / vidéo_prête / programmé / traitement / publié / rejeté / issue_inconnue / pause.
- Identifiants et réponse fournisseur, visibilité, URL, heure du contrôle, portée de la preuve.
- Blocage, cause, impact, action suivante, responsable et échéance/condition non garantie.

Ne pas recopier un média comme nouvelle source si une référence durable suffit. Les originaux et dérivés restent dans les emplacements autorisés ; la médiathèque conserve les usages réels. Ne pas modifier son schéma pour ajouter une valeur non prévue sans besoin de configuration retenu.

## Roulement existant

Charger `equipe-coordonner-activite` et ses références `pilotage-tous-reseaux.md`, `orchestration-editoriale.md`, `suivi-execution.md` quand ce skill intervient dans un passage quotidien. Les heures Europe/Paris décrivent les phases du pilote, pas une fréquence de publication :
- 06 h : état, échéances et préparation avant les réveils métier.
- 12 h : reçus, résultats et réparations.
- 16 h : préparation des besoins du lendemain avant 17 h, examen à 48 h, intentions à 14 jours et bilan. Le lundi, cohérence de semaine avec les données déjà accessibles/autorisées.

YouTube est exécuté directement dans ces passages ; ne pas créer de réveil propre. Résoudre les tâches actuelles depuis l'installation du gestionnaire et leur état réel, pas depuis un identifiant historique copié. Ne jamais attribuer un travail à un exécutant supposé actif sans preuve.

Si `scheduled_for` manque, déterminer la phase avec l'heure locale réelle et le dire. Commencer par les obligations échues sans rafale et sans inventer des passages. Respecter les pauses utilisateur. Une absence de besoin de publication ne supprime pas le suivi.

## Reçu et rapport partiel

Inscrire l'exécution, mode, heures réelles, phase, sources/versions, résultats et preuves, état completed/partial/failed. `scheduled_for` et `run_id` uniquement s'ils sont attestés. Identifier le travail dû restant, son responsable et son échéance.

Tout résultat partiel appelle un rapport visible : « Terminé : … / Manque : … / Cause : … / Conséquence : … / Reprise : qui, quoi, quand ou condition / Décision attendue : … ». Ne jamais écrire seulement « couverture partielle » ou « accès à terminer ». Signaler tout manque dès la sortie du passage, même hors bilan de 16 h et même si aucune action humaine n’est requise ; ne pas annoncer une notification envoyée ailleurs sans preuve. En absence d'accès/sauvegarde, expliquer la limite dans la réponse et conserver les éléments récupérables sans faux terminé.

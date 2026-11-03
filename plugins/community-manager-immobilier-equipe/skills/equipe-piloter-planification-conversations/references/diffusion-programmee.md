# Diffusions à l'heure choisie

Sommaire : mandat et responsabilités ; décision horaire ; contrat persistant ; planification ; exécution ; reprise ; clôture et rangement.

## Mandat et responsabilités

Ce protocole concerne les publications organiques déjà retenues, finalisées et autorisées. Il ne crée ni quota, ni mandat de diffusion, ni collecte de statistiques, ni droit sur une publicité. Une campagne Ads conserve son planificateur et son mandat métier propres.

Le développeur fixe le cap. Le community manager ou le spécialiste encore responsable propose l'horaire et la fenêtre de validité dans le calendrier métier. Le pilote quotidien porte la fonction de planification en chargeant ce skill dans son passage ; aucun nouveau pilote récurrent n'est nécessaire si celui existant suffit. Le spécialiste produit et valide la préparation. Une tâche ponctuelle exécute ensuite la seule diffusion convenue. Le pilote et le contrôle de santé rapprochent le résultat. Le passage de préparation du matin n'est pas nécessairement l'heure de publication.

L'installation du protocole n'active pas une migration générale du CM maître. Conserver le mode de transition et les exécutants actuels. Si le maître est encore en observation, le développeur consulte le spécialiste actuel et applique lui-même la fonction de planification autorisée.

La création de tâches de diffusion par un pilote récurrent exige un mandat de configuration explicite conservé dans l'installation et les sources persistantes. Ce mandat peut lever une ancienne interdiction utilisateur générale de tâches enfants pour cette seule fonction ; il ne lève jamais une restriction supérieure du runtime. Ne pas contourner un refus de plateforme par un autre outil. Les workers de diffusion ne créent pas de tâches filles et n'appellent jamais run_now.

## Choisir l'horaire utile

Utiliser d'abord l'horaire imposé ou délégué et la séquence existante. Consulter réellement la compétence réseau avant nouvelle orientation ; réutiliser un avis encore valable. Examiner audience visée, format, contexte, actualité, espacement, disponibilité humaine utile et données déjà accessibles ET autorisées. Sans historique suffisant, qualifier le choix d'hypothèse éditoriale, jamais d'heure optimale mesurée. Aucun appel d'analytics implicite.

Conserver `scheduled_at` avec décalage et fuseau IANA, `valid_until`, motif et preuve/avis. Fixer une fenêtre avant de programmer : par défaut proposé pour un contenu durable, deux heures après l'heure retenue ; la réduire pour une annonce sensible à l'heure, la modifier seulement avec raison et dans le mandat. Une tolérance au retard n'autorise ni diffusion périmée ni report indéfini. Une exécution à heure fixe demande un créneau, sans garantie de début ou fin à la minute. Ne pas déclencher trop tôt pour compenser une latence inconnue.

La revue de semaine peut proposer un essai borné sur les créneaux à partir des résultats déjà autorisés, en distinguant effet du sujet, du format et de l'heure. Ne pas changer tout à la fois ni inventer des performances. Les intentions sur 14 jours ne deviennent pas 14 tâches : programmer seulement un contenu prêt, retenu et autorisé, dans le stock permis au canal.

## Contrat canonique avant toute création

Le registre métier reste seul propriétaire du texte, des médias, de l'accord et du calendrier. Ajouter une extension compatible `distribution` à l'entrée existante, sans modifier les statuts autorisés du registre :

- `operation_id` stable pour entreprise/canal/cible/contenu/version ; `business_id`, `entry_id`, `content_version`, `canonical_ref` et `owner_skill` ;
- cible exacte et connexion vérifiée ; mandat et référence de l'accord ;
- empreinte SHA-256 du texte UTF-8 exact ; références persistantes, versions et empreintes des médias finaux ; droits et contrôles utiles ;
- `scheduled_at`, `timezone`, `valid_until`, motif/avis ; `route` (`provider_native`, `work_one_shot`, `manual`) ;
- `planning_state`, `automation_id` réel ou null, ID fournisseur réel ou null, état de diffusion séparé ;
- réservation coopérative avec exécutant, heure et état ; tentatives/réponses/preuves ; reprise et responsable ;
- contrôleur existant, prochaine vérification, état de nettoyage distinct.

L'inventaire des conversations référence ce contrat, avec sa clé et son ID de tâche ; il ne contient pas une seconde copie éditoriale. La page pilote référence les deux et conserve les décisions de coordination. Conserver les versions attendues du stockage ; relire/fusionner après conflit. Si la sauvegarde préalable échoue, ne pas créer le déclencheur.

## Programmer une fois

1. Relire les décisions récentes, réservations, tentatives et programmations fournisseur ET les tâches actives, en pause et terminées pour la même opération. Une échéance passée ou un bail ancien ne libère pas une opération inconnue. Rechercher son résultat avant reprise. Réserver puis relire l'entrée ; il n'existe pas de verrou atomique garanti.
2. Vérifier le contenu complet, la version approuvée, tous les médias requis accessibles durablement, le compte et les capacités. Réutiliser le contenu prêt ; ne pas le réécrire pour installer la planification. Une URL signée expirante ou un chemin scratch n'est pas une source autonome durable.
3. Préférer la programmation native si l'outil actuel, le compte et les champs requis la permettent réellement. Capturer l'ID fournisseur et l'état exact. Ne pas créer en parallèle une tâche Work qui publierait le même post. Une tâche de contrôle éventuelle est seulement en lecture.
4. Si la programmation native manque mais la publication immédiate est disponible et autorisée, créer **une tâche ponctuelle standalone** via les capacités documentées. Calendrier VEVENT avec DTSTART futur et fuseau, sans RRULE. Utiliser l'outil Automations pour les champs exposés ; recourir au navigateur lorsque nécessaire pour le mode standalone, puis vérifier Avancé → Exécuter dans → Nouveau chat à chaque exécution. Ne pas inventer un champ API de mode ou une API cachée.
5. Le prompt contient uniquement la mission ciblée et les références persistantes du contrat : skill métier, registre/entrée/version/opération, entreprise/cible, référence pilote et contrôle. Demander de relire ce protocole, la fenêtre courante et le mandat avant effet. Ne pas demander au worker de choisir un nouveau sujet, de refaire le calendrier ou de republier après une incertitude.
6. Capturer l'ID réel, relire prompt/calendrier/fuseau/activation/mode et absence de doublon ; enregistrer d'abord le raccord métier puis l'inventaire. Un mode non vérifié ou une sauvegarde échouée rend la configuration partielle. Une tâche Work créée ne signifie pas que le réseau a reçu une programmation : dire « diffusion confiée à une tâche ponctuelle », pas « programmé chez LinkedIn ».
7. Une erreur de création avant acceptation peut être réparée par une voie autorisée. Après timeout ou résultat incertain, rechercher le même objet par clé/prompt/heure et inventaire avant tout nouvel appel ; ne jamais recréer sur le seul titre.

En cas de changement d'heure, mettre à jour la même tâche et le même contrat après intention sauvegardée, puis relire. En cas de changement de version, approbation retirée, annulation ou contenu périmé, marquer d'abord le contrat `revoked` ou `superseded` ; arrêter/remplacer seulement le déclencheur de diffusion concerné dans le mandat explicite de configuration. Vérifier qu'aucune ancienne tâche ne peut encore envoyer ; si elle a déjà démarré ou que son issue est inconnue, rapprocher l'opération avant toute nouvelle programmation. Ne pas créer deux workers actifs. Conserver le suivi par le pilote ; aucune mission récurrente n'est arrêtée par cette opération.

## Exécuter la diffusion ponctuelle

1. Charger réellement le skill du réseau, son protocole de publication, le contrat courant et les décisions utilisateur récentes. Vérifier identité, cible, version, approbation, empreintes, accessibilité des médias et état actuel des tentatives. Une permission technique n'est pas un mandat. Sans source lisible ou contrat exact, aucun effet.
2. Si publié avec preuve : ne rien renvoyer, réparer seulement la trace manquante. Si une programmation fournisseur ou une tentative acceptée/inconnue existe : contrôler cette opération, aucun second envoi. Si un autre exécutant est actif/inconnu : ne pas prendre sa réservation.
3. Respecter l'heure réelle : avant `scheduled_at`, aucun envoi anticipé ni attente pendant des heures ; au-delà de `valid_until`, marquer `expired_not_sent`, conserver le suivi et faire réarbitrer par le pilote. Dans la fenêtre, poursuivre après contrôles. Un retard ne déclenche jamais une rafale.
4. Réserver puis relire l'entrée immédiatement avant mutation. Si version, accord, date ou réservation changent, ne pas envoyer. Sauvegarder une tentative stable `in_flight`, puis appeler une fois l'action de publication immédiate avec texte et média finaux exacts. Aucun texte seul si le média est obligatoire. Respecter toutes les protections du canal.
5. Sauvegarder le retour exact et l'ID fournisseur, puis vérifier l'état utile. `PENDING`, traitement, accepté, programmé et publié restent distincts. Le succès du worker n'est pas une preuve fournisseur. Une lecture 403 signifie contrôle inaccessible par cette route, pas publication échouée ; utiliser les voies de lecture autorisées documentées sans collecter les réactions.
6. Exécuter le contrôle rapproché réalisable prévu par suivi-execution.md. À défaut de preuve terminale, rattacher au prochain pilote ou contrôle existant effectivement actif avec opération/ID exacts, délai visé non garanti ; ne créer aucune tâche fille. Réparer la trace sans rejouer l'effet. Restituer le texte intégral et le média final selon le skill métier, avec état réel et rapport des manques.

## Contrôle, reprise et fin du déclencheur

À chaque passage du pilote, reprendre les demandes `pending_create`, vérifier les déclencheurs à venir et rapprocher les opérations échues. Au contrôle quotidien, rechercher les lancements et reçus manquants depuis la dernière borne attestée. Lire les registres métier même si la tâche ponctuelle est affichée terminée. Ne pas déduire de l'absence au planning l'absence de publication.

Une tâche ponctuelle n'a pas de prochaine occurrence après son unique déclenchement ; sa fin technique est normale, même si le résultat métier est partiel. **Conserver alors l'opération dans la file de reprise du pilote/contrôle**, sans réactiver aveuglément le one-shot ni le transformer en récurrence. Une nouvelle tentative exige résultat précédent rapproché, absence de publication établie, mandat encore applicable et décision nouvelle enregistrée. Aucun incident ne suspend le pilote permanent.

## Rangement sans perte des preuves

Distinguer `trigger_lifecycle` (planifié/terminé), `delivery_state` (non envoyé/inconnu/publié/échec) et `cleanup_state` (non éligible/éligible/manuel/bloqué/supprimé vérifié). Une tâche simplement exécutée, une acceptation fournisseur, un PENDING ou une sauvegarde manquante ne sont pas éligibles au nettoyage automatique.

Éligibilité : preuve terminale du résultat, reçu métier et référence pilote sauvegardés, aucune tentative inconnue ni reprise ouverte, ID exact et mission ponctuelle attestés. Une annulation explicite définitivement réconciliée peut aussi clôturer le contrat. Le pilote ou contrôleur ultérieur effectue le rangement, pas le worker avant d'avoir enregistré son résultat.

Inspecter les outils actuels : si une suppression ou archive réellement exposée, autorisée et réversible est disponible, l'appliquer au seul one-shot éligible puis vérifier ; conserver son ID historique et les preuves dans les registres. Ne pas effacer les registres ni le chat de résultat pour nettoyer la liste. Une suppression irréversible via navigateur exige les confirmations imposées à cet instant ; ne pas promettre une auto-suppression silencieuse ni contourner cette règle. Sans capacité suffisante, conserver `cleanup_state=manual_required` avec cause ; ne pas présenter une désactivation comme suppression. Utiliser si possible le filtre des tâches actives ou replier Terminée pour éviter l'encombrement visuel.

Au 31 octobre 2026, les outils Automations inspectés exposent création, mise à jour et consultation, aucune suppression ; l'interface Planifié montre une section Terminée et un menu Supprimer. Aucun archivage, récupération ou nettoyage automatique n'a été attesté. Recontrôler au moment utile, sans supposer que cette limite est permanente.

# Publication, capacités et reprise

## Porte de diffusion

Résoudre le mandat courant par chaîne, contenu/version, opération, fenêtre et limites. Préparer est distinct de publier/programmer ; un précédent afterwork n'autorise pas tous les prochains posts. Chercher la preuve existante avant de demander ce qui manquerait. L'accord de création du community manager autorise son installation et son cadrage, pas un engagement public ou une dépense implicite.

Vérifier la chaîne par les paramètres de marque et une source fournisseur utilisable. Découvrir les outils actuels, lire leurs schémas et les champs requis. Au 31 octobre 2026, Metricool expose une action de post avec `blogId`, `date`, `info`, `mediaFiles` : ne pas inventer la structure des options YouTube dans `info`. Obtenir un exemple documenté compatible ou un objet existant lisible et ses limites. Confirmer titre, audience enfants, visibilité, type de vidéo, date/fuseau et déclaration IA si nécessaire. Une propriété absente ne doit pas être supposée supportée.

Si le connecteur ne couvre pas un champ requis, garder le livrable prêt, examiner une autre voie documentée autorisée ; recourir à l'interface uniquement selon les règles d'accès applicables. Ne pas demander une reconnexion quand le problème est une capacité non exposée. Décrire le vrai manque sans bloquer les autres préparations ou réseaux.

Contrôler le fichier final et l'accès au média avant envoi. Ne pas publier un texte nu pour contourner l'échec du transfert vidéo. Respecter les droits, le budget et les services autorisés. La fonctionnalité de playlist ou de miniature peut être disponible dans l'interface et absente de l'outil : ne pas confondre les deux.

## Opération unique

1. Lire l'entrée canonique et les réservations actives ; rapprocher tout résultat incertain avant de reprendre.
2. Inscrire `execution_id`, opération, chaîne, contenu/version, exécutant et heure de réservation. Relire l'entrée immédiatement avant mutation ; en cas de concurrence, se retirer de l'opération et poursuivre ailleurs. Aucun verrou atomique revendiqué.
3. Effectuer l'opération une fois. Conserver identifiants fournisseur et réponse exacte. Après un timeout, noter `issue_inconnue` et rapprocher cette même opération ; ne pas envoyer une nouvelle création à l'aveugle.
4. Diagnostiquer média/transfert/format/permission/outil/état. Corriger seulement ce qui est autorisé et conserver les versions. Ne pas dépasser le mandat pour réparer.
5. Contrôler l'état terminal lorsque réalisable : réponse fournisseur, URL et accessibilité/visibilité. `PENDING`, programmé ou traitement ne signifient pas publié ; privé/non répertorié ne signifie pas public. L'absence du planning ne prouve ni succès ni échec.

## Contrôle rapproché et continuité

Après une opération non terminale, tenter un contrôle rapproché réaliste avec le même identifiant (par exemple dans les dix minutes si l'exécution le permet, avec des attentes courtes). Ne pas immobiliser les autres canaux. Si l'état reste inconnu ou le créneau ne permet pas de rester, rattacher explicitement la reprise au prochain passage existant du pilote ou au contrôle commun de 18 h : opération, source, responsable, heure visée et délai non garanti. Ne pas créer de tâche enfant, appeler run_now ni désactiver une mission.

Sauvegarder le résultat exact dans le registre propriétaire du contenu, puis seulement le reçu de coordination. `completed` exige que le travail demandé et sa sauvegarde soient réellement terminés ; une programmation réussie peut compléter une demande de programmation tout en gardant l'état vidéo `scheduled`, sans prétendre à la publication.

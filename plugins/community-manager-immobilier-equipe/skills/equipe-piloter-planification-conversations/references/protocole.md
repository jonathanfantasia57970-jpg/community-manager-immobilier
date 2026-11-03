# Protocole opérationnel

## Migration d'une tâche dont le mode est figé

1. Capturer ID, titre, prompt complet, calendrier, fuseau, activation, modèle/effort s'ils sont disponibles, sources et derniers effets incertains. Conserver une intention de remplacement dans l'inventaire.
2. Résoudre le contexte utile hors du chat, préserver les autorisations métier et les opérations déjà engagées.
3. Créer depuis Planifié → Nouvelle tâche. Cocher explicitement le nouveau chat. Choisir le bon modèle/capacités. Si le calendrier exact est saisissable, l'enregistrer directement. Sinon préparer un objet de migration à échéance future avec un prompt explicitement sans effet métier ; puis enregistrer simultanément prompt métier et calendrier exact via les champs officiellement exposés. Ne jamais créer une mission métier récurrente active avec une cadence provisoire incorrecte.
4. Rapprocher l'objet créé par le retour ou le delta d'inventaire (titre/prompt/heure), jamais par un titre seul s'il existe des homonymes.
5. Avant le prochain créneau commun, désactiver l'ancienne tâche dans le cadre du remplacement autorisé. Si une exécution est en cours, ne pas l'interrompre aveuglément : réconcilier les effets et le relais. Ne pas laisser deux exécutants actifs sur la même opération.
6. Renommer l'ancienne « Remplacée — [titre] » et enregistrer replaced_by. Conserver l'historique, ne pas supprimer définitivement sans demande.
7. Vérifier la nouvelle tâche : Nouveau chat à chaque exécution, active, règle exacte, fuseau, pas de fin involontaire. Ne pas déclarer migré avant ces preuves.
8. Actualiser l'ID courant et les références opérationnelles actives (prompts de coordination, installation des skills, page pilote). Conserver les anciens ID dans l'historique/aliases. Ne pas réécrire les reçus historiques comme si la nouvelle tâche les avait exécutés.
9. Enregistrer la preuve et la prochaine échéance. Si une étape échoue, garder un état de migration partiel et la reprise précise ; ne pas créer une troisième tâche. Avant désactivation de l'ancienne, laisser l'ancienne autorisée active et la remplaçante sans effet métier. Après désactivation de l'ancienne, si la remplaçante est défectueuse, n'avoir aucun exécutant incontrôlé : remettre l'ancienne dans son état autorisé antérieur seulement si cela ne contourne ni arrêt utilisateur ni restriction de plateforme et ne réintroduit aucun doublon, sinon laisser la mission en migration partielle et signaler l'interruption. Une ancienne tâche déjà suspendue ne doit pas être réactivée comme prétendu rollback.

## Inventaire persistant

Pour chaque mission, conserver au minimum :
- logical_key, business_id ou périmètre, title, automation_id courant et aliases ;
- skill et sources stables de contexte ;
- expected_mode (standalone/contextual), mode_reason ;
- expected_enabled et autorisation source ;
- schedule/RRULE, timezone, condition de fin et tolérance de retard ;
- observed_mode, observed_enabled, observed_schedule, observed_at, preuve UI/outil ;
- dernier run attesté et résultat, sans assimiler scheduled_for et heure réelle ;
- lifecycle (recurring, one_shot, completed, superseded) ;
- pause : raison et provenance (utilisateur, assistant, plateforme, inconnue), condition de reprise ; blocage des effets métier enregistré séparément ;
- changement en cours et historique d'événements ;
- contrôleurs réellement configurés et dernière couverture complète.

Conserver un journal borné ou archivé avec références durables, sans recopier les conversations. Une collision de version impose relecture/fusion des seules lignes concernées. Ne pas écraser l'inventaire à partir d'une liste partielle.

Avant une correction d'activation, conserver l'intention dans le journal de l'inventaire de planification accessible, avec mandat, ID, provenance de la pause et état avant/après ; relire puis vérifier le résultat de la mutation. Ce journal est distinct du registre métier Sheets éventuellement inaccessible. Si le journal préalable obligatoire est lui-même inaccessible, signaler que la correction n'est pas effectuée et garder sa reprise ouverte ; ne pas désactiver d'autres tâches ni inventer une sauvegarde. L'accès métier reste nécessaire avant les effets, pas avant la reprise du réveil.

## Cas particuliers

- Mission en pause demandée par l'utilisateur : mode standalone possible, activation inchangée sauf nouveau mandat.
- Mission récurrente suspendue après réussite : anomalie ; rétablir si le mandat le permet, distinguer cette reprise d'une exécution métier.
- Source inaccessible : conserver attendu actif et le réveil programmé ; empêcher les effets dépendants, exposer le blocage et réexaminer au prochain passage. Ne pas transformer le blocage en pause de campagne ni en suppression du déclencheur.
- Ancienne tâche remplacée : ne jamais alerter sur sa pause attendue ni la réactiver.
- Rappel ponctuel : terminer à l'échéance prévue ; ne pas transformer en mission récurrente ni l'activer après expiration.
- Formation : sourcer le protocole et sa mémoire hors du fil ; pas d'envoi/publication implicite.
- Absence de prochaine date dans l'API : inconnue ; vérifier la règle et l'interface, ne pas conclure que la tâche est suspendue.
- UI et API en désaccord d'horaire : relire fuseau et règle enregistrée, ne pas convertir arbitrairement ni prétendre le désaccord résolu.
- Tolérance absente : signaler l'échéance passée et la preuve manquante sans inventer un seuil d'incident ; proposer une tolérance documentée pour la prochaine configuration.
- Pause créée par l'assistant pour source inaccessible : selon le mandat enregistré, rétablir le réveil avec les effets dépendants toujours bloqués. Une lecture actuelle réussie des contrôles, oppositions/quotas exploitables et réconciliation des tentatives incertaines sont nécessaires avant l'envoi, pas avant le simple réveil de contrôle. Respecter toute suspension utilisateur ou imposée par la plateforme.


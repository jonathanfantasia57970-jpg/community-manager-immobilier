# Tenir la liste attendue indépendamment de l'état observé

Le skill de planification est responsable de l'inventaire canonique indiqué dans installation.md. Cette liste représente les missions confiées et la volonté vérifiée de l'utilisateur ; elle ne reflète pas simplement les boutons actuellement actifs.

## Champs et autorité

Conserver les champs existants et compléter au besoin : mission_key, ID courant, alias, titre, skill/sources, expected_enabled, expected_schedule, expected_timezone, expected_mode, condition de fin, expected_revision, expectation_authority (instruction ou terme autorisé, date connue, référence vérifiée), observation séparée (exists, enabled, schedule, observed_at, preuve), lifecycle et historique des transitions.

Pour un arrêt, conserver en plus stop_authorization : nature (demande utilisateur, fin prévue, remplacement), objet et périmètre exacts, référence/preuve, date connue et condition de reprise. Ne jamais inventer une citation, un ID de conversation, un acteur ou une heure de décision. Une phrase produite par un assistant, un statut inactif ou une erreur fournisseur ne prouve pas une volonté d'arrêt de l'utilisateur.

## Mise à jour à chaque opération

| Événement | Mise à jour de l'attendu |
| --- | --- |
| Création autorisée | Enregistrer la mission et l'attente avant l'effet ; après succès, raccorder l'ID réel et vérifier mode/activation/calendrier. Un échec de création reste pending_create, sans ID inventé. |
| Changement demandé de calendrier, périmètre ou mode | Mettre à jour seulement les champs autorisés, leur preuve et la révision ; conserver la dernière observation séparément. |
| Arrêt/pause explicitement demandé | Mettre expected_enabled=false pour le seul objet demandé, conserver la mission et stop_authorization. La pause d'une campagne ne désactive pas implicitement un pilote partagé. |
| Reprise demandée | Mettre expected_enabled=true, conserver l'ancien arrêt dans l'historique et vérifier l'activation réelle. |
| Fin bornée prévue | Clôturer la mission seulement selon sa condition de fin vérifiée ; préserver reçu et mandat initial. Un run récurrent completed n'est pas une fin de mission. |
| Remplacement autorisé | Garder la mission logique unique, ancien ID historique inactif et nouveau ID courant ; ne pas diminuer le nombre de missions attendues. |
| Désactivation par assistant/plateforme ou origine inconnue | Garder l'attendu existant, enregistrer l'état observé et ouvrir l'incident ; aucune baisse automatique de expected_enabled. |
| Tâche absente ou découverte hors inventaire | Signaler disparition ou mission non rapprochée ; rechercher le mandat existant. Ne supprimer aucune attente et ne déduire aucune autorisation de la seule présence d'une tâche. |

Lire la version actuelle, enregistrer l'intention, effectuer seulement la mutation autorisée, vérifier le résultat puis fusionner dans le même inventaire avec garde de version. Conserver les modifications concurrentes des autres missions. Une création/modification n'est pas entièrement terminée tant que l'inventaire n'est pas sauvegardé avec l'ID courant, la décision et l'observation vérifiée.

Si la sauvegarde après mutation échoue, annoncer l'état partiel, garder ID/avant/après et intention pour réconciliation ; ne pas recréer la tâche ni annuler l'attendu pour masquer le problème. Si l'inventaire est indisponible au contrôle, déclarer couverture partielle et anomalie de supervision ; ne pas le reconstruire uniquement depuis les tâches actives.

## Désactivation et compte rendu

Comparer expected_enabled à l'observation. Pour une mission attendue active devenue inactive ou absente, rechercher une décision d'arrêt applicable. Si elle est vérifiée, mettre l'attendu à jour avec sa preuve ; sinon ouvrir/actualiser un incident stable par mission, incluant dernière preuve active et moment de détection.

Classer l'origine seulement sur preuve : user_requested, assistant, platform ou unknown. La mention « automatique » est réservée à une preuve attribuable ; un is_enabled=false ne suffit pas. Une pause dont l'origine est inconnue est signalée comme inattendue et inexpliquée, sans réactivation aveugle. Les corrections de pause assistant restent celles du mandat de continuité ; ne jamais contourner une suspension de plateforme.

Le bilan quotidien comprend les incidents nouveaux, persistants et résolus depuis la dernière borne. Même une correction automatique vérifiée laisse une ligne : ce qui s'est arrêté, ce qui a été rétabli, preuve et prochaine échéance. Dédupliquer les notifications, jamais effacer l'événement. Ne clore qu'après réactivation prouvée, arrêt utilisateur retrouvé ou fin/remplacement autorisé établi.

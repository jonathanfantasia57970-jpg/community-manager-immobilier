---
name: equipe-piloter-planification-conversations
description: Créer, modifier, migrer et contrôler les tâches planifiées qui lancent des conversations ChatGPT Work. Utiliser pour choisir standalone ou même chat, programmer via le navigateur, vérifier activation et horaires, diagnostiquer une pause ou un lancement manquant, maintenir l'inventaire des tâches attendues et signaler les suspensions. Ne gère pas les tâches métier Notion ni les campagnes elles-mêmes.
---
## Routage et relecture du plugin

Pour appeler un autre module ou lire ses références, appliquer `../../references/routage-skills.md`. Pour toute revue de contenu, appliquer `../../references/relectures-et-capacites.md` : utiliser les agents réellement disponibles ou le relais humain documenté, sans inventer de contrôle indépendant.


## Profil personnel et version commune

Avant le travail métier, lire `../../references/contrat-equipe.md` et `../../references/mise-a-jour-et-personnalisation.md`. Résoudre le profil courant avec `equipe-configurer-espace` sans le réinitialiser. Le profil, les corrections et préférences du conseiller priment sur les valeurs de départ pour le ton, les thèmes, la charte et les modalités de communication. Les faits, droits, relectures et mandats restent requis. Aucune donnée du créateur ni connexion commune n'est fournie. Les Ads sont hors périmètre.


# Piloter la planification des conversations

## Contrat

Gérer le déclenchement, pas réaliser le métier à la place de l'exécutant. Séparer configuration attendue, configuration observée, lancement réel, résultat métier et notification. Ne jamais déclarer une tâche opérationnelle sur le seul texte de son prompt ou le succès d'un appel.

Lire [installation.md](references/installation.md) pour résoudre l'inventaire persistant de l'utilisateur. Lire [protocole.md](references/protocole.md) pour création, migration et contrôle. Utiliser skill-creator pour toute modification de ce skill ; equipe-rendre-compte-actions pour les modifications planifiées.

Pour le contrôle quotidien, appliquer [verification-quotidienne.md](references/verification-quotidienne.md) : comparer les échéances attendues aux lancements et résultats attestés, puis rendre le bilan prévu, même si aucun incident nouveau n'apparaît.

## Choisir le mode

- Choisir **standalone / nouveau chat à chaque exécution** pour toute mission récurrente dont le contexte peut être rechargé depuis un skill et des sources persistantes : synchronisation, gestion courante, réseaux, formation, prospection, supervision, rapports.
- Choisir **même chat** seulement pour un suivi borné qui dépend réellement de la discussion courante (opération temporaire, clarification ou rappel contextuel). Documenter raison, terme et condition d'arrêt. Un rappel ponctuel ne nécessite pas automatiquement une migration.
- Une mission récurrente sans source persistante doit être raccordée à une source avant migration. Ne pas remplacer une mémoire manquante par l'accumulation infinie d'un fil.
- « autonome », « standalone », conversation_id non nul, titre, dernière conversation et regroupement visuel ne prouvent jamais le mode. Vérifier dans le navigateur : **Avancé → Exécuter dans → Nouveau chat à chaque exécution** après sauvegarde.
- Un nouveau chat évite l'accumulation dans le même historique ; il ne supprime ni quotas globaux, ni limites d'outils ou d'abonnement.

## Mandat et inventaire attendu

À la première configuration, enregistrer chaque mission autorisée dans un seul inventaire : clé métier stable, ID du planificateur, titre, skill, sources, fuseau, récurrence, mode attendu, activation attendue, condition de fin, dépendances et notification. Enregistrer séparément les observations horodatées et les preuves.

L'inventaire attendu ne doit jamais être déduit seulement des tâches actuellement actives : sinon une tâche disparue ou suspendue disparaît aussi du contrôle. Une pause observée ne modifie pas automatiquement l'état attendu.

**Mettre à jour la liste attendue après chaque création, modification, remplacement, fin prévue ou arrêt explicitement autorisé**, selon [tenue-inventaire.md](references/tenue-inventaire.md). Conserver la preuve de la volonté de l'utilisateur séparément de l'état observé. Une désactivation automatique ou de provenance inconnue ne change jamais `expected_enabled=true` en faux : elle ouvre un écart visible dans le compte rendu quotidien, même si elle a été corrigée avant ce compte rendu. Ne jamais attribuer une pause à l'utilisateur ou à la plateforme sans preuve.

Avant mutation, conserver l'état initial et l'intention. Après réponse incertaine, rapprocher le même objet avant de recréer. Préserver les versions et changements concurrents. Les anciens ID deviennent des alias historiques lors d'une migration, pas des missions supplémentaires attendues.

## Créer ou modifier

1. Lire les tâches actives, en pause et terminées, le mandat courant et les dépendances. Ne pas réactiver les tests terminés, rappels expirés ou anciennes tâches remplacées.
2. Résoudre l'objectif et la fréquence depuis la demande ou la configuration vérifiée. Utiliser le fuseau utilisateur IANA, celui confirmé dans le profil ; conserver les heures locales lors des changements été/hiver.
3. Utiliser **le navigateur pour créer les tâches standalone, régler le mode et le vérifier**. Les outils Automations peuvent compléter l'inventaire, les horaires, les titres, les prompts ou l'activation lorsqu'ils exposent ces champs. Ne jamais appeler une API cachée par le navigateur.
4. Le commutateur de création « Démarrer chaque exécution dans un nouveau chat » peut être désactivé par défaut : le cocher explicitement. Ne pas supposer sa valeur.
5. Si le mode d'une tâche existante est affiché sans contrôle éditable, appliquer la migration de protocole.md. Ne pas prétendre l'avoir modifié en ajoutant une phrase au prompt.
6. Garder le prompt court : action, skill, identifiant du dossier ou de la campagne, référence de configuration, résultat attendu. Mettre les règles durables dans le skill et les données variables dans le registre. Une exception de test datée n'a pas sa place dans le déclencheur récurrent.
7. Avant d'alléger un ancien prompt, vérifier que chaque exigence utile existe réellement dans le skill ou sa source. Une migration de mode n'autorise pas à perdre des mandats ou garde-fous.
8. Contrôler après sauvegarde : mode, activation, cadence complète, fuseau, fin de récurrence, modèle/capacités nécessaires et absence de doublon. Vérifier tous les créneaux d'une règle multi-horaire. Un horaire affiché par défaut ne remplace pas une règle enregistrée.
9. Ne pas utiliser « Lancer maintenant » pour tester un réglage si cela envoie des emails, publie, dépense ou synchronise des données sans mandat d'exécution immédiate.
10. Sauvegarder l'inventaire attendu et l'observation vérifiée sur la même identité persistante, avec autorité et historique. Une mutation réussie dont l'inventaire n'est pas enregistré reste une configuration partielle à signaler et réparer ; ne pas annoncer la planification entièrement terminée.

## Pauses et continuité

**Une impossibilité d'exécuter ne doit jamais conduire l'assistant à suspendre une campagne ou son déclencheur.** Cela couvre refus d'accès, 403/429, connexion expirée, quota, outil absent, source illisible, sauvegarde échouée, permission manquante, résultat incertain et blocage durable. Bloquer uniquement les effets dépendants, signaler la cause et conserver la programmation ainsi que l'activation attendue. Un passage réussi, sans travail ou au quota termine seulement ce passage.

Ne jamais diminuer le nombre des tâches attendues pour faire disparaître une anomalie. Ne pas désactiver une tâche pour rendre un tableau vert.

Une désactivation décidée par l'assistant est réservée à une demande explicite de l'utilisateur, une fin bornée prévue ou un remplacement autorisé sans doublon. Un incident technique ou métier, même nommé « sécurité », n'est pas une autorisation de désactiver le réveil. Respecter une suspension imposée par la plateforme ou une instruction supérieure, sans contournement ni boucle de réactivation. Consigner toute pause observée : motif, auteur connu ou inconnu, preuve, date, périmètre et condition de reprise ; la signaler à l'utilisateur.

Séparer strictement activation du déclencheur et autorisation d'un effet. Le réveil reste actif pour diagnostiquer et vérifier de nouveau ; aucun email sans oppositions, quota et doublons vérifiés, aucune publication ou dépense sans conditions réunies. Respecter restrictions fournisseur, délais de reprise et contrôles de sécurité. Retrouver l'accès n'autorise ni rattrapage en rafale ni répétition d'une tentative incertaine. Une pause expressément demandée par l'utilisateur reste respectée jusqu'à nouveau mandat.

## Contrôler les tâches attendues

Pour chaque tâche de l'inventaire non terminée/remplacée :
- existence par ID ou alias rapproché ;
- mode réellement vérifié, ou dernière preuve datée si le navigateur est indisponible ;
- activation et suspension inattendue ;
- cadence, fuseau, échéance, fin et prochain lancement quand exposé ;
- dernière exécution attendue vs attestée, éventuelle erreur ou interruption ;
- présence du résultat ou du reçu métier lorsque nécessaire, sans exécuter le métier ;
- dépendances vers des ID remplacés et doubles exécutants.

Un retard au-delà de la tolérance enregistrée produit « lancement attendu non attesté », pas un échec métier inventé. Une heure passée, un statut completed ou le silence ne prouvent pas une publication, un envoi ou une synchronisation.

Si le navigateur est indisponible, le connecteur peut contrôler l'existence et l'activation ; conserver **mode non revérifié**, sans prétendre avoir vérifié standalone. Reprendre les parties indépendantes.

## Réagir et notifier

Signaler toute nouvelle pause inattendue, disparition, dérive de mode, changement d'horaire ou échec récurrent : tâche, constat horodaté, attendu, effet concret, cause prouvée ou inconnue, correction effectuée ou décision requise. Signaler aussi le retour à la normale. Dédupliquer les alertes inchangées tout en conservant un reçu de contrôle. Un défaut nouveau d'accès à l'inventaire ou d'enregistrement du contrôle doit être visible.

Réactiver une tâche attendue active seulement dans le mandat enregistré, après avoir établi que sa désactivation vient d'un assistant à cause d'un empêchement ou d'une fin de passage, sans doublon ni décision utilisateur contraire. La reprise du réveil ne lève aucun contrôle métier et n'exige pas de prétendre la source réparée. Une cause inconnue, une pause utilisateur, un objet remplacé/terminé ou une suspension de plateforme impose une alerte, jamais une réactivation aveugle. Ne jamais faire de boucle pause/reprise.

Conserver le contrôle existant lorsqu'il suffit ; ne pas multiplier les réveils. Raccorder le contrôle de planification à au moins un réveil actif effectivement vérifié et, si possible, vérifier ce réveil depuis une autre tâche existante. Une inscription dans un registre n'est pas une surveillance programmée.

**Limite à dire :** un skill ne verrouille pas les boutons de ChatGPT et ne peut pas empêcher une suspension technique. Si tous les contrôleurs s'arrêtent ou que la plateforme est indisponible, aucune alerte interne immédiate n'est garantie. Ne pas annoncer une surveillance continue ou un délai garanti sans mécanisme indépendant attesté.

## Restitution

Donner les changements confirmés, la liste des tâches actuelles avec mode/activation/cadence, les anciennes remplacées, les pauses justifiées restantes et le rythme réel du contrôle. Présenter une preuve visuelle utile des réglages modifiés selon les règles du navigateur. Conserver la trace persistante et distinguer « configuration vérifiée » de « premières exécutions futures vérifiées ».

## Diffusion ponctuelle à l'horaire éditorial

Pour transformer un contenu organique prêt et autorisé en envoi à l'heure choisie, lire et appliquer [diffusion-programmee.md](references/diffusion-programmee.md) : programmation native prioritaire, sinon tâche Work ponctuelle standalone, contrat métier versionné, opération unique, contrôle et rangement. Le pilote existant porte la planification ; les workers diffusent sans créer de tâche fille. Ne pas confondre fin du déclencheur, publication vérifiée et suppression de la tâche. L'autorisation de configuration ne lève aucune restriction supérieure du runtime.
## Primauté du skill sur le réveil
Le rappel planifié est un déclencheur remplaçable, jamais le lieu de vérité du métier. Son prompt ne contient que l’action, le ou les skills à charger, l’identifiant du dossier et la référence de configuration. Mettre dans le skill les règles durables : objectif, séquence, conditions d’arrêt, contrôles, reprises, quotas, sources, routes, qualité, exceptions et compte rendu. Mettre dans le registre les données variables et l’état. Avant de raccourcir un rappel, transférer chaque règle utile dans le skill ou sa source persistante, puis vérifier qu’elle est effectivement enregistrée. Une suppression, recréation ou migration de tâche ne doit faire perdre aucune règle métier.

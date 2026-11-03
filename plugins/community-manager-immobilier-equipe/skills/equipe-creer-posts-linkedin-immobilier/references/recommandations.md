# Relier les conseils, les actions et les résultats

Faire du conseil un travail suivi : observation ou difficulté → recommandation précise → décision → application vérifiée → diffusion vérifiée si nécessaire → retour et prochaine décision. Utiliser les deux mémoires existantes ; ne pas créer un tableau ou un fichier parallèle. Ne pas traiter une intention, une rédaction ou une auto-évaluation comme un résultat du public.

## Formuler des recommandations applicables

Proposer une à trois priorités utiles au maximum, sans remplir un quota. Pour chaque piste, préciser brièvement : sur quoi elle repose, ce qu'il faut changer, sur quels contenus ou quelle période, l'objectif et la manière d'en apprécier l'effet. Une piste sans retours publics est un conseil éditorial ou une hypothèse, jamais une conclusion de performance.

Adapter les pistes à la présence du conseiller : approfondir un sujet qui suscite des questions, varier des angles trop proches, clarifier une accroche, rendre une question finale plus accessible, essayer un format adapté à la matière, mieux relier le visuel au propos, préparer une suite ou des réponses. Proposer aussi, si pertinent, un ajustement de calendrier, une amélioration de présentation du profil ou de ses contenus mis en avant. Les outils et permissions disponibles déterminent ce qui peut être exécuté ; ne pas promettre une modification de profil ou une publication sans capacité réelle.

Les corrections ordinaires déjà exigées par le brief (clarté, exactitude, qualité visuelle, variété) restent autonomes ; ne pas créer une demande de validation pour chaque amélioration. Une expérimentation issue du coaching, un changement de cadence ou de positionnement requiert le choix correspondant, réutilisable dans toute sa portée. Une demande de mieux suivre les recommandations n'accepte pas toutes les futures propositions et n'active ni diffusion ni surveillance.

## Passer de l'accord à l'action

Conserver la recommandation et sa décision dans `experiments` selon apprentissage.md. Dès son acceptation, créer ou reprendre une action dans `community_management.open_actions` avec le même `recommendation_id` ; ne pas attendre une seconde consigne pour préparer la mise en œuvre autorisée.

Une action conserve : `id`, `recommendation_id`, `owner` (skill, le conseiller ou tiers identifié), `scope`, `target_entry_ids` et/ou `calendar_ids` quand connus, `due_at` (date ou condition explicite), `next_step`, `implementation_stage`, `evidence_refs` et un éventuel `blocker`. Une cible encore inconnue reste explicitement inconnue ; la lier au contenu réel dès qu'il existe. La portée et le critère de réussite priment sur une date arbitraire. Une échéance de bilan doit dépendre de la diffusion réelle quand elle mesure la réception du post.

Utiliser ces étapes opérationnelles sans changer les statuts de décision de `experiments` :

| Étape | Preuve ou condition |
| --- | --- |
| `planned` | Accord applicable, action concrète, responsable et cible/échéance définis. |
| `in_progress` | Travail engagé, prochaine étape connue ; une intention seule ne suffit pas. |
| `applied_to_draft` | Version préparée réellement inspectée et changement identifiable ; la diffusion reste inconnue. |
| `published` | Version diffusée ou autre changement externe réellement confirmé, avec sa preuve. |
| `awaiting_observation` | Application externe vérifiée, délai de recul ou données encore manquants. |
| `evaluated` | Bilan réalisé sur une couverture explicitée ; sa conclusion peut être « non évaluable ». |
| `blocked` | Dépendance ou décision manquante explicitée, avec condition de reprise. |
| `cancelled` | Abandon explicite ou expiration de la portée, avec sa cause ; aucune conclusion de performance. |

Les étapes ne sont pas toutes obligatoires : une action de calendrier interne peut se terminer par une vérification d'exécution, sans prétendre avoir été publiée. Pour une série, suivre la preuve par post et résumer l'avancement ; « appliqué sur un brouillon sur trois » ne signifie pas « série publiée ». Un avis général favorable du conseiller ne prouve pas qu'il a effectué une action externe.

## Exécuter au fil des passages

Relire les actions acceptées avant de formuler de nouveaux conseils. Prendre les quelques actions dues ou applicables au contenu prévu et effectuer celles qui relèvent du skill : préparer ou corriger le texte et le visuel, placer les essais dans le calendrier, produire une réponse prête à envoyer, préparer une proposition de titre de profil. Réutiliser un contenu existant pertinent plutôt que multiplier les brouillons. Respecter versions, éléments déjà appréciés et portée des autorisations ; ne pas modifier un ancien post diffusé sans demande correspondante.

Lier la mise en œuvre au contenu réel dans `entry.recommendation_applications` : `recommendation_id`, `action_id`, `version`, `applied_at`, `change_summary`, `evidence` (court passage ou référence du visuel/livrable inspecté), puis référence à la preuve de diffusion et à l'observation lorsqu'elles existent. Conserver l'historique utile des versions ; ne pas prétendre qu'une réécriture contient toujours le changement sans la vérifier. Un changement réellement appliqué au texte suit le protocole normal de version ; une simple mise à jour de suivi ne change pas sa version.

Pour une action du conseiller, fournir le livrable précis et l'étape restante : par exemple le post final et son créneau, ou le titre de profil prêt à copier. Laisser l'action en attente jusqu'à preuve accessible dans un relevé autorisé ou confirmation explicite. Regrouper les points en attente dans le bilan hebdomadaire ; ne pas répéter tous les jours la même relance et ne pas supposer une publication parce que la date prévue est passée. Si les brouillons s'accumulent, proposer un ajustement de cadence, sans arrêter silencieusement la production convenue.

Si l'accord porte sur « les trois prochains posts », compter seulement les contenus de la portée convenue et préserver le suivi après changement de date ; si l'accord vise une période précise expirée, ne pas l'étendre automatiquement. Ne pas dépasser trois pistes suivies dans la mémoire courte pour empiler des recommandations nouvelles ; traiter d'abord celles déjà ouvertes.

## Évaluer ce qui a réellement eu lieu

Vérifier d'abord si le changement a été appliqué, ensuite s'il a été diffusé, puis ce qui a été observé. Sans publication confirmée, évaluer la mise en œuvre éditoriale uniquement. Sans collecte autorisée et accessible, ne pas lancer un relevé pour clôturer le suivi ; indiquer « résultats inconnus » et la condition nécessaire. Une surveillance activée alimente ce suivi à ses échéances, sans collectes redondantes.

Comparer des posts d'âge, format et contexte proches lorsque c'est possible. Employer les observations datées et leurs limites : propos des lecteurs, participants distincts, réactions et métriques privées réellement disponibles. Les réponses du conseiller ne comptent pas comme autant de nouveaux lecteurs. Sans portée, ne pas inventer un taux d'engagement ni une visibilité. Une amélioration observée suggère une piste ; elle ne prouve pas à elle seule que le changement en est la cause.

Conclure par maintenir, ajuster, arrêter l'essai, ou conserver le résultat non évaluable avec sa cause. Une conclusion ne devient pas une règle permanente sans décision correspondante. Garder une action ouverte tant qu'il reste une étape promise ; si elle doit être clôturée faute de données ou par expiration, conserver ce motif, la couverture et les preuves disponibles. Ne pas effacer une recommandation non résolue pour faire de la place.

## Sauvegarder et rendre l'avancement visible

Sauvegarder d'abord les actions, liaisons au calendrier et preuves dans le registre canonique avec sa garde de version, puis actualiser la décision et la synthèse courte de `experiments` dans la mémoire de coaching. Réconcilier par `recommendation_id` après interruption, sans dupliquer une action ni attribuer à une autre version une preuve existante. Pour une nouvelle observation du public, utiliser le protocole d'intégration distinct de apprentissage.md. Ne pas écrire le registre et la mémoire en parallèle.

Dans le point quotidien, montrer seulement une avancée utile ou un blocage nouveau. Dans le bilan hebdomadaire, restituer pour chaque priorité suivie : recommandation → application concrète et contenus concernés → diffusion connue ou inconnue → résultat observable → prochaine étape et responsable. Conserver les liens utiles, sans imposer un long rapport. Les termes « proposé », « préparé », « publié » et « évalué » doivent correspondre à des faits distincts.

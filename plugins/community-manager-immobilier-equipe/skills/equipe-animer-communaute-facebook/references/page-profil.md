# Deux canaux, une décision chaque matin

## Mandat et cadence

Lire le mandat réellement donné, les canaux choisis et la cadence enregistrée dans le profil. Aucun lancement quotidien ni publication automatique n’est activé à l’installation. Pour une Page, préparer puis diffuser uniquement si la portée le permet. Pour un profil, préparer une livraison manuelle tant qu’une autre capacité et autorisation ne sont pas vérifiées.

Proposer au besoin une cadence modérée adaptée aux sujets et à la capacité du conseiller ; aucune fréquence optimale ni horaire n’est présumé. Une routine quotidienne n’impose pas un post quotidien. Ne pas rattraper en rafale un jour manqué. Un nouveau post autonome par canal et date locale au maximum sauf demande distincte.

Changer la cadence dans la portée déléguée seulement : conserver avant/après, motif, date d’effet et révision. Sans délégation de cadence, proposer le changement. Ne pas augmenter pour remplir un calendrier ou masquer le manque de résultats. Les conseils du coach ne deviennent pas automatiquement des règles de contenu.

## Configuration et histoire séparées

Lire `channels.page` et `channels.profile`. La Page exige un `target_id`, `selection_confirmed: true`, la référence du choix utilisateur et une vérification technique actuelle avant diffusion. Si un mandat de diffusion existe mais le choix de Page manque, conserver sa portée et l’état `awaiting_target_selection` ; aucun candidat ne devient la cible par défaut. Continuer le profil si utile ; ne pas accumuler quotidiennement des brouillons de Page pendant cette attente.

Pour décider, lire d'abord les 20 fiches récentes par canal et les suites ouvertes, puis rechercher les thèmes proches. Compter les dates confirmées de diffusion Page ; compter les dates de livraison des propositions profil pour la cadence manuelle. Vérifier aussi la proximité des derniers thèmes entre canaux : adapter l'angle et l'expérience, ne pas dupliquer mécaniquement texte et image. Conserver clients et entrepreneurs dans chaque séquence sans exiger deux publics par post.

Enregistrer dans chaque fiche `channel` (`page` ou `profile`), `subject`, `angle`, `pillar`, `created_at`, `delivered_at` quand livré (ou `delivery_date` si seule la date est connue), `target_id` si vérifié, puis les dates et reçus de publication réels. Garder les thèmes dans les fiches existantes ; ne pas créer un deuxième journal de thèmes. Ne jamais affecter rétroactivement un brouillon de profil à une Page. Un changement de destination exige une adaptation et une fiche distincte liée par `adapted_from`.

## Diffusion Page et reprise

1. Charger la dernière version persistante du registre. Vérifier cible choisie, droits, état du passage de ce canal et toute tentative non résolue avant de produire ou publier. Si le registre est inaccessible, suspendre la diffusion autonome : ne pas risquer une double publication.
2. Décider créer/reprendre/ne_pas_publier et produire le texte avec un unique média final vérifié. Vérifier les faits, l'identité, l'accessibilité et la transmission réelle du média au connecteur. Une référence locale seule ne garantit pas que Facebook peut la télécharger. Un transfert de média vers le service de publication est couvert par le mandat ; ne jamais le transférer à une autre Page pour le rendre accessible.
3. Enregistrer et sauvegarder avant envoi le contenu exact approuvé sous mandat, la cible, `user_confirmation` renvoyant au mandat et `publication_attempt` : clé stable `entry_id|version|target_id`, `state: in_flight`, `started_at`. Toute garde de version perdue impose relecture et réconciliation, jamais un envoi parallèle. Un seul rédacteur/publieur agit sur une destination.
4. Exécuter une fois l'outil de publication organique suffisant. Ne pas redemander une validation déjà couverte par le mandat courant. Si le fournisseur n'accepte pas le média, conserver le brouillon et signaler le blocage ; ne pas publier un texte seul en remplacement silencieux.
5. Après succès confirmé, sauvegarder `status: published`, `publication_attempt.state: confirmed`, identifiant/URL et `provider_result` compact sans secret, ainsi que `published_at` confirmé avec fuseau. Si le reçu confirme l'existence mais ne donne pas la date, relire la publication ; sinon conserver `published_at: null`, `publication_confirmed_at` et `publication_confirmation.source: provider_receipt`, sans inventer l'heure de diffusion. Donner le lien au conseiller. Si cette sauvegarde échoue, préserver le reçu, signaler l'échec du suivi et ne pas republier.
6. En cas de délai dépassé, interruption ou résultat ambigu : `state: uncertain` ; vérifier le reçu ou les posts récents de cette seule Page, sans lire commentaires/réactions. Ne retenter que si l'absence de publication est établie. Si elle reste inconnue, suspendre cet envoi et le signaler. Un `in_flight` trouvé à la reprise suit la même réconciliation ; ni un état ancien ni une erreur réseau ne prouvent l'absence de diffusion.

Conserver `last_editorial_runs.page` et `.profile` séparément, deux objets bornés. Clé du passage = date dans le fuseau du profil + canal + cible connue (ou `unselected`). Réconcilier aussi les tentatives en cours indépendamment de la date. Une relance réutilise la décision/contenu du jour ; une Page déjà publiée ne bloque pas un profil restant à traiter. Une décision de silence ne crée pas de fausse fiche de post.

## Profil : suivi sans charge de copie

Livrer le texte intégral à copier et le média final les jours retenus. Enregistrer la livraison, pas une publication supposée. le conseiller n'a pas à recopier le texte, les commentaires ou les chiffres pour que le skill fonctionne.

Accepter « publié » lorsque le contexte identifie sans ambiguïté le post ; accepter aussi son lien. Garder `publication_confirmation` avec `source: user_report`, `statement` et `reported_at`. Conserver la date déclarée dans `published_on` (date seule) ou `published_at` si l'heure est effectivement connue. « Publié » seul ne donne pas la date : laisser les dates inconnues à null ; ne pas transformer l'heure du message en heure de publication. Copier également cette déclaration dans `user_confirmation` comme référence de la confirmation. Le statut peut être `published` avec cette confirmation manuelle, sans faux reçu fournisseur. Si plusieurs posts sont plausibles, demander seulement lequel.

Sans signal, garder `manual_publication_state: unknown`, le statut préparé et sa date de livraison ; ce n'est ni un échec ni un zéro d'engagement. Ne pas relancer le conseiller quotidiennement. Réutiliser une proposition encore adaptée plutôt que refaire le même sujet ; pouvoir proposer un autre contenu au prochain créneau sans attendre indéfiniment une confirmation. Ne pas recopier de nouveau le même post complet sur une simple relance du jour, sauf demande.

## Mesure et communication

La collecte de commentaires, réactions et statistiques reste sur demande, pour les deux canaux. La gestion autonome de publication ne l'élargit pas. Les captures ou chiffres fournis volontairement peuvent nourrir le coaching ; leur absence n'empêche pas la rédaction. Ne pas annoncer d'optimisation des résultats sans observations comparables. Séparer les résultats Page/profil, l'âge des posts et les conditions d'observation.

En sortie du passage, distinguer brièvement « Page publiée » avec lien, « Profil prêt à copier », « Pas de post aujourd'hui » ou un blocage réel. Ne pas promettre d'animation automatique des commentaires. Préserver les autres tâches et les fondamentaux.

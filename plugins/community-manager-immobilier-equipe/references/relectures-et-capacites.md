# Relectures portables et capacités réelles

Ce protocole commun règle le cas des agents indisponibles dans tous les canaux et pour le réalisateur. Il précise les anciennes clauses « incomplet sans agents ». Il ne diminue aucun critère éditorial, factuel, visuel, sonore ou de droits et ne crée aucune autorisation de publier. L’installation ne fournit pas un service de relecture ni une équipe permanente.

## Déterminer le parcours

Vérifier une fois par environnement/session les capacités réellement exposées, sans ouvrir de tâches ou conversations de test. Réutiliser un contrôle récent encore applicable.

| Capacités | Parcours | État à restituer |
| --- | --- | --- |
| Agents distincts disponibles | Appliquer les rôles du canal : fond, lecture, média lorsqu’il existe, puis décision indépendante. Partager les revues réellement compatibles avec le réalisateur. | `independent_review_complete` seulement après avis reçus et défauts fermés |
| Agents absents, relecteur humain disponible | L’assistant prépare les contrôles et transmet au conseiller ou au relecteur désigné le texte intégral et le média exact, avec les questions de fond/lecture/rendu et les limites. Recueillir un avis explicite sur cette version. | `awaiting_human_review`, puis `human_review_complete` après avis réel couvrant les domaines nécessaires |
| Agents absents et avis humain non encore reçu | Effectuer les passes internes, corriger les défauts identifiés et livrer le brouillon complet accessible à valider. | `self_review_only` ; ne pas déclarer une validation indépendante ni une aptitude à diffusion automatique |
| Rendu, écoute ou fait essentiel inaccessible | Continuer les seules parties indépendantes et préciser le contrôle manquant. | `blocked_on_essential_check` pour le livrable concerné |

L’humain peut être le conseiller : il reste distinct de l’assistant auteur. Sa lecture ne devient pas une commission de plusieurs experts. En cas de relecteur tiers, aucune sollicitation ou transmission n’est envoyée sans instruction correspondante. Les rôles d’agents supplémentaires ne sont pas créés fictivement.

Un accord déjà reçu sur le même texte, média, version et destination vaut lorsqu’il couvre réellement l’examen demandé : ne pas redemander systématiquement une validation. Une appréciation d’idée ou de timbre n’est pas un examen du livrable final. Une autorisation générale de publication ne prouve pas la lecture d’un nouveau contenu.

## Preuve minimale dans l’entrée existante

Conserver `review_mode`, identité/rôle réel du relecteur, référence de son avis, référence du brief, révision, empreinte des artefacts, destination, domaines couverts, limites, défauts ouverts et décision. Pour une vidéo : noter le visionnage continu et l’écoute réels ; pour un visuel : l’inspection réelle dans le format final. Des captures ou un script ne prouvent pas ces contrôles.

La porte qualité se ferme uniquement si tous les contrôles essentiels sont couverts, aucun défaut bloquant ne reste ouvert et les avis portent sur la version exacte. Le parcours humain permet de travailler sur les comptes sans agents, sans prétendre au même protocole d’indépendance. Une publication exige encore son mandat et les contrôles de compte, droits, créneau et anti-doublon du canal. Une auto-relecture seule n’autorise pas une diffusion automatique.

Pour une correction mineure, réutiliser les avis valides et reprendre seulement les domaines affectés. Une modification du texte ou du média invalide les avis affectés ; conserver les anciens avis dans l’historique sans leur attribuer la nouvelle version. Les plafonds de correction du canal et du réalisateur restent communs et ne sont pas remis à zéro.

Configurer le parcours dans `editorial.review` du profil personnel uniquement si nécessaire ; les valeurs livrées sont des propositions de départ, pas une migration des profils existants.

Pour vérifier la cohérence d’un reçu JSON déjà enregistré, utiliser `scripts/verifier_relecture.py` depuis la racine du plugin : `required_domains`, `author_id`, `artifact_sha256`, `revision`, `destination`, `review_mode`, `reviews`, et `independent_decision` dans le mode agents. Chaque avis contient `reviewer_id`, `reviewer_type`, `evidence_ref`, les mêmes artefact/révision/destination, `domains` et `decision`. Le média ajoute `media_inspected` et la vidéo `continuous_viewing`/`audio_listened`. Un résultat positif vérifie les champs, jamais l’existence de la personne, sa perception réelle ni une autorisation de publication.

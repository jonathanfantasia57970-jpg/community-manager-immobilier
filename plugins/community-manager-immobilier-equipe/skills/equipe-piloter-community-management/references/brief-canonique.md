# Brief éditorial canonique et relais métier

Repère : BRIEF-CM-2026.11.01.2.

## Une seule source de vérité

Conserver le brief dans le registre propriétaire du canal dès le cadrage autorisé, à l'emplacement défini par ce canal. Rechercher d'abord brief, intention, entrée produite, révisions et réservations. Un brief en travail n'est pas un post livré : ne pas créer une entrée de production fictive pour pouvoir déléguer. L'identifiant et l'emplacement du brief restent stables quand une entrée produite est ensuite créée et liée. La coordination multicanale et le projet vidéo conservent cette référence, pas une copie modifiable.

Pour LinkedIn, appliquer le raccord exact de `references/registre.md` du skill `equipe-creer-posts-linkedin-immobilier` de ce plugin : `community_management.editorial_briefs[brief_id]` dans le registre existant, références `brief_id` depuis calendrier, consultation et entrée produite. La révision du brief et la version du post sont distinctes. Pour un autre canal, résoudre son emplacement réellement admis avant l'écriture ; ne pas lui imposer le schéma LinkedIn ni créer une base concurrente.

Utiliser [le modèle de champs](../assets/brief-editorial.json) comme contrat logique. L'intégrer aux champs/blocs ou à la pièce jointe unique déjà admis par le registre. Ne pas ajouter automatiquement des propriétés à une base. Si une structure ne peut pas être écrite, préparer le bloc exact et annoncer la sauvegarde manquante ; une copie locale seule ne devient pas canonique. Si le même concept sert plusieurs canaux, conserver une source commune pour les faits et des briefs/adaptations liés propres à chaque canal ; ne pas écraser leurs angles et validations.

Le brief appartient au contenu, pas à la conversation ni au sous-agent. Les fichiers de montage et livrables peuvent être ailleurs dans leur emplacement durable autorisé ; le brief référence leur version exacte. Le projet technique vidéo reste lié au brief, sans seconde autorité sur sujet, angle ou format.

## Qui écrit quoi, dans quel ordre

| Étape | Contributeur | Informations à rendre |
| --- | --- | --- |
| Besoin cadré | CM ou pilote du canal dans sa délégation | Public/situation, objectif, apport recherché, contexte, priorité, échéance réelle, contraintes et mandat ; instructions explicites du conseiller |
| Proposition éditoriale | Spécialiste réseau effectivement chargé | Sujet, angle, idée centrale, utilité distincte, preuve et sources, nuances, suite utile, points à préserver, réserves ; médias/concepts examinés |
| Fond retenu | CM après avis du spécialiste, ou spécialiste en exécution directe | Proposition retenue et motif, réserves résolues ou obstacle précis, version de référence |
| Format retenu | Spécialiste recommande ; CM arbitre si actif | Supports comparés, gain audiovisuel ou motif du statique, faisabilité, matière, coût/délai, choix, raison et besoin d'avis technique |
| Production | Exécutant du canal, graphisme ou réalisateur | Livrables et versions, conformité au fond retenu, écarts/obstacles, contrôles effectués et manquants |
| Revue et état prêt | Relecteurs requis, arbitre puis propriétaire du canal | Avis réellement obtenus, défauts corrigés, inspection de l'accroche et du rendu, état exact ; approbation éventuelle liée à la version/destination |

L'ordre correspond à des décisions, pas à six réunions. Les passes peuvent s'enchaîner dans la même session. Un brief proportionné peut tenir dans quelques paragraphes ; les champs sans objet restent sans objet avec raison plutôt qu'inventés. Respecter le mandat d'écriture ; un contributeur en lecture seule remet sa proposition à l'unique exécutant chargé de l'enregistrer.

## Contrat d'un relais

Avant une délégation ou passe métier, transmettre : lien/identifiant canonique, révision à lire, question ou section à compléter, contraintes et points intangibles, résultat attendu, limite d'action et échéance connue. Le destinataire lit le brief et les sources utiles, puis rend sa contribution, ses preuves/limites et l'effet sur la décision. Une simple mention « demander au réseau » ne vaut pas avis reçu.

Une contribution reçue modifie la même entrée après rapprochement de la version actuelle. Un seul exécutant réalise chaque mutation. Vérifier les réservations et relire avant écriture ; une réservation documentaire n'est pas un verrou atomique. En cas de changement concurrent, réconcilier les sections pertinentes sans écraser un avis, une correction utilisateur ou une validation nouvelle.

Dans `relais`, garder seulement les échanges qui changent une décision : rôle/source réelle, révision lue, question, contribution/réserve, décision, responsable et état. Ne pas créer un journal bavard de chaque lecture ; ne pas préremplir un échange ou une revue comme s'ils avaient eu lieu.

## Version et changements

Augmenter `revision` lors d'un changement substantiel du sujet, de l'angle, des faits/preuves, du format, de la destination ou du livrable soumis. Noter origine, raison, champs concernés et validations affectées. Conserver les décisions précédentes dans l'historique du registre, sans dupliquer un contenu actif. Une correction cosmétique se trace selon le système de versions existant, sans refaire toute la stratégie.

- **Sujet, angle, message central, preuve ou nuance** : retour au spécialiste, puis arbitrage du fond et recontrôle du format ; ne pas laisser le réalisateur réécrire pour faciliter son montage.
- **Format** : motiver le changement avec le spécialiste/CM ; préserver le fond, vérifier faisabilité, contraintes du canal et contrôles propres au nouveau média.
- **Texte, voix ou montage** : invalider les timings, sous-titres et contrôles réellement affectés ; garder les autres contrôles avec leur portée.
- **Approbation/publication** : ne pas transférer une approbation ancienne à une nouvelle version ou destination par défaut. Rapprocher le mandat applicable ; ne pas toucher à une programmation existante sans décision autorisée.

## États et recette minimale

Reprendre les états existants du registre. Le modèle propose, à adapter sans migration automatique : `besoin_cadre`, `proposition_editoriale`, `fond_retenu`, `format_retenu`, `en_production`, `a_corriger`, `controle_incomplet`, `pret`, `reporte`. Ne pas inventer que ces états sont implémentés dans l'outil.

Avant production : sujet/angle/apport/preuve établis, nuances explicites, format motivé après le fond, matière/droits et faisabilité vérifiés, exécutant et prochaine étape connus. Une donnée indispensable inconnue laisse l'étape concernée ouverte ; poursuivre les parties indépendantes utiles.

Avant état prêt : texte intégral et médias réels accessibles dans leur version contrôlée, revues requises accomplies, accroche/rendu examinés, réserves critiques closes. `pret` ne signifie ni approuvé pour toute destination, ni programmé, ni publié. Le statut de diffusion et ses reçus restent dans le registre métier existant ; le brief les référence sans les concurrencer.

À chaque reprise, lire la dernière révision canonique, vérifier ce qui a changé et continuer l'étape ouverte. Ne pas demander au conseiller de recopier le contexte. Si le brief est inaccessible, exposer le défaut et éviter toute décision contradictoire ou publication ; une panne ne supprime pas les travaux indépendants autorisés.

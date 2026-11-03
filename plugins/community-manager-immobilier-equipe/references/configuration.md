# Correspondances de configuration

Le profil créé à partir de `assets/profil-conseiller.template.json` est enregistré dans l’espace personnel choisi par le conseiller, hors du dépôt et du plugin. `CONFIG_BUSINESS_ID` désigne `business_id`. Les identifiants de comptes viennent de `channels`. Les sources Notion viennent de `notion` : bibliothèque → creative_data_source/creative_view ; médiathèque → media_data_source/media_view ; entreprise/profil → profile_page ; pilotage → coordination_page ; contenus → content_data_source. Les registres existants sont dans `storage.registry_refs` ; les originaux dans `storage.originals_folder` ; les tâches attendues dans `storage.schedule_inventory`. Une valeur nulle ou non rapprochée bloque uniquement l’effet qui en dépend.

Ne pas écrire un profil réel dans le dépôt GitHub, même privé. Ne stocker aucun jeton dans le profil : connecter le service par son mécanisme sécurisé. Chaque conseiller utilise ses propres connexions.

# Metricool : capacités et actions

## Destination principale à vérifier

Résoudre marque du connecteur, fiche Google Business exacte et identifiants depuis `channels.google_business`. Vérifier par lecture les réglages actuels et la correspondance. Aucun compte ni fiche par défaut. Ne pas utiliser un ancien compte après changement de destination. Utiliser le fuseau réel du service et le fuseau du conseiller, avec décalage à la date prévue. Un libellé Instagram ne prouve pas la destination Google ; plusieurs candidats imposent une résolution de cible, pas le premier résultat.

## Capacités observées, à redécouvrir

Les noms ci-dessous décrivent les méthodes ; ne pas inventer de slug ou de schéma.

| Fonction | Capacité / limite |
|---|---|
| Connexions | `getBrandSettings`. |
| Métriques | `getAnalyticsAvailableMetrics`, réseau `googleBusinessProfile`, puis `getAnalyticsDataByMetrics` avec les identifiants renvoyés. |
| Programmer | `createScheduledPost`, réseau `gmb`, type explicite `gmbData`. |
| Lire le planning | `getScheduledPosts` retourne seulement les posts encore programmés. |
| Modifier | `updateScheduledPost` exige l'objet complet relu, en modifiant uniquement les champs demandés. L'id change, l'uuid reste stable. |
| Avis | Des champs de lecture sont annoncés dans les métriques, mais les docs MCP indiquent des limites : vérifier le résultat avant de promettre texte et état. Aucun outil de réponse publique exposé. |
| Paramètres de fiche | Aucune action exposée pour adresse, horaires, catégories, description et services. |
| Suppression / contenu déjà publié | Ne pas promettre une action non exposée. |

Les métriques disponibles ne prouvent pas qu'elles sont effectivement alimentées. Ne pas utiliser les champs Deprecated. Les groupes `reels` et `keyworks` peuvent apparaître avec un sens propre à Google : suivre les identifiants renvoyés.

Au 25/10/2026, documentation web et MCP divergent pour la vidéo : le web décrit des posts avec vidéo, le MCP la route vers le type galerie `photo`, sans texte. Pour exécuter, suivre le contrat actuel de l'outil et expliquer toute limitation qui change le livrable. Ne pas transformer silencieusement un mini-article vidéo en galerie muette. Privilégier texte + image pour les mini-articles.

Pour une stratégie initiale ou un bilan demandé, lire seulement la période nécessaire. Ne pas lancer une collecte exhaustive d'avis pour rédiger un post. En cas d'accès insuffisant, avancer avec une stratégie qualitative et des inconnues explicites.

## Programmation autorisée

1. Résoudre compte, fiche, contenu final, média accessible et date future. Une demande de programmer une série autorise cette série ; une demande de stratégie ne l'autorise pas.
2. Résoudre le type selon l'intention explicite : mini-article = `publication` avec texte ; galerie = `photo`, sans texte. Si le choix reste ambigu et que l'outil l'exige, poser cette seule question. Ne pas redemander un choix déjà donné.
3. Lire planning et registre pour éviter les doublons de date, cible, texte et média. Ne pas altérer un autre réseau d'un objet multicanal sans autorisation correspondante.
4. Lire le schéma complet. Si la structure JSON du champ `info` manque, obtenir un modèle complet ou une documentation officielle ; ne pas deviner et ne pas faire de test public.
5. Compter les 1 500 caractères. Vérifier l'accès effectif du service au média : chemin local, image affichée et URL privée ne sont pas automatiquement téléversables. Utiliser le transfert prévu ; sinon signaler le blocage sans publier une version amputée.
6. Écrire une seule fois, contrôler le retour et si utile relire le planning. Consigner id, uuid, date, fuseau et `plannerUrl` ; présenter le lien renvoyé. Un succès de programmation signifie `scheduled`, pas `published`.
7. Après timeout ou réponse incertaine, lire avant de réessayer. Sans preuve suffisante, garder `unknown`. Une disparition du planning ne prouve pas la publication.

Pour « maintenant », utiliser une action immédiate seulement si exposée ; sinon indiquer l'heure imminente de programmation conforme à la demande. Ne pas annoncer une diffusion effective avant preuve. Le mode d'approbation qui envoie des emails aux collaborateurs n'est pas un mode préparatoire par défaut : l'utiliser seulement si demandé.

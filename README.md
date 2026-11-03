# Community Manager Immobilier — Équipe

Plugin v0.2.1 : 16 skills, catalogue créatif et ressources. Chaque conseiller configure son profil et ses connexions. Publicité payante exclue.

## Installation sur un PC Windows avec un compte personnel

Prérequis : application ChatGPT de bureau à jour et Codex CLI installé, accessible depuis PowerShell et connecté au compte du conseiller. Préparer Codex selon la [documentation officielle](https://learn.chatgpt.com/docs/codex/cli). Lancer `codex --version` pour vérifier sa présence. Si PowerShell ne reconnaît pas `codex`, terminer cette installation avant les commandes suivantes.

Le dépôt doit être publié avant d'utiliser la méthode GitHub. Un lien de dépôt ou un ZIP joint à une conversation ne remplace pas l'enregistrement du catalogue.

Dans PowerShell :

```powershell
codex plugin marketplace add jonathanfantasia57970-jpg/community-manager-immobilier --ref main
codex plugin list --available --json
codex plugin add community-manager-immobilier-equipe@cm-immobilier-equipe
codex plugin list --json
```

Vérifier que le plugin apparaît dans la liste des éléments installés. Ouvrir ensuite l'application ChatGPT de bureau, consulter Plugins et le catalogue « Community Manager Immobilier — Équipe », puis ouvrir une nouvelle conversation. S'il n'apparaît pas, fermer puis rouvrir l'application. La disponibilité locale ne prouve pas une installation sur le web, le mobile ou un autre PC.

Première demande : « Configure mon community manager immobilier avec mes informations et mes comptes. Conserve tout profil et historique existants. » Connecter personnellement les services nécessaires lorsque demandé.

## Variante locale sans dépôt publié

Décompresser cette distribution dans un dossier permanent. Dans PowerShell, se placer dans le dossier qui contient `.agents` et `plugins`, puis exécuter :

```powershell
codex plugin marketplace add .
codex plugin add community-manager-immobilier-equipe@cm-immobilier-equipe
codex plugin list --json
```

Cette variante nécessite aussi Codex CLI. Ne pas déplacer ce dossier ensuite. Ne pas utiliser le ZIP original du plugin seul : cette distribution ajoute le catalogue qui lui manquait.

## Mise à jour et données personnelles

```powershell
codex plugin marketplace upgrade cm-immobilier-equipe
codex plugin list --available --json
```

Cette commande actualise le catalogue GitHub. Vérifier ensuite la version installée dans Plugins et appliquer la mise à jour proposée par le client. Elle ne prouve pas, à elle seule, que le plugin installé a changé de version.

Ce dépôt contient uniquement la version commune. Ne jamais y enregistrer les profils remplis, mots de passe, clés, contacts, médias personnels ou historiques. Conserver les données personnelles dans les emplacements externes configurés par le conseiller. Un contenu enregistré manuellement dans le dossier du plugin ne bénéficie pas de cette séparation. Les connexions restent propres à chaque compte.

## Vérifications avant diffusion générale

Structure du catalogue et conservation des 393 fichiers du plugin contrôlées. Installation réelle sur le PC d'un conseiller, disponibilité des outils et conservation des données lors d'une mise à jour : à valider. L'installation n'active aucune publication ni tâche planifiée.

Si une commande échoue, conserver son message exact. `codex plugin marketplace list` vérifie les sources ; `codex plugin list --available --json` vérifie la découverte du plugin. Une erreur « commande inconnue » nécessite de vérifier la version de Codex, sans supprimer les données ni les autres plugins.

## Sources officielles

- [Packaging et catalogues personnels](https://developers.openai.com/plugins/build/plugins)
- [Commandes d'installation et de contrôle](https://learn.chatgpt.com/docs/developer-commands)

Le plugin local peut nécessiter un environnement Python, FFmpeg et les connexions des services utilisés. Ces logiciels et connexions ne sont pas installés par ce dépôt.

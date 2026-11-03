# Résoudre les skills de ce plugin

La table exhaustive `skills-map.json` associe chaque nom exact à son SKILL.md dans le paquet. Ces chemins sont relatifs à la racine du plugin : ils ne sont jamais des identifiants de package à transmettre tels quels à `skills.read`. Ne pas demander le package `skills/equipe-…`.

1. Retrouver le nom exact dans le catalogue des skills disponibles pour cette installation et ce plugin. Réutiliser le package/main_resource fourni par l’hôte, sans inventer de version, d’identifiant cloud ou de chemin de cache. Lire son SKILL.md et résoudre ses références avec ce même package.
2. Si les fichiers du plugin sont disponibles localement, partir de sa racine effectivement observée, lire la table puis le fichier. Le script `scripts/resoudre_skill.py NOM [--reference references/FICHIER]` fournit le chemin vérifié. Ne pas utiliser un ancien chemin de scratch ou un dossier personnel du créateur.
3. Un chemin `references/x.md` appartient au répertoire du skill désigné ; un chemin donné comme `skills/equipe-x/references/y.md` part de la racine du plugin. Les références communes sont dans `references/` à la racine. Ne pas chercher toutes les références dans le module courant.
4. Si l’hôte ne rend pas un skill visible, vérifier la version/installabilité du plugin. Garder les travaux indépendants ; décrire le seul module inaccessible. Ne pas lui substituer silencieusement un skill personnel de même nom et ne pas installer une copie concurrente pour masquer le manque.

Les appels entre CM, spécialistes et réalisateur transmettent le même identifiant de brief et sa révision ; ils ne lancent pas une nouvelle conversation ni un nouveau calendrier. Les retours portent le fichier/version exacts et les contrôles réellement réalisés.

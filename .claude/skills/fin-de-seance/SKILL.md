---
name: fin-de-seance
description: Clôture une séance de travail - met à jour branches/<branche>.md avec l'avancement et la prochaine étape, fait un commit, puis pousse sur la branche courante (jamais sur main).
disable-model-invocation: true
---

# Fin de séance

Quand l'utilisateur lance /fin-de-seance, suis ces étapes dans l'ordre.
Explique chaque étape en français simple : l'utilisateur débute peut-être sous Linux et Git.

## 1. Faire le point

- Lance `git branch --show-current` pour connaître la branche actuelle (appelée `<branche>` ci-dessous).
- Si la branche est `main` : **arrête-toi**. On ne travaille jamais sur `main`. Demande à l'utilisateur sur quelle branche il voulait travailler.
- Lance `git status` et `git diff --stat` pour voir ce qui a changé.
- S'il n'y a aucun changement, dis-le et passe quand même à l'étape 2.

## 2. Mettre à jour `branches/<branche>.md`

- Ouvre `branches/<branche>.md` (crée-le s'il n'existe pas, avec un titre `# Branche <branche>`).
- **Ne modifie pas `CLAUDE.md`** : il est commun à toute l'équipe et ne change que par Pull Request.
- Remplace la section `## Où on en est` (ou crée-la à la fin du fichier) par :

  ## Où on en est
  _Dernière mise à jour : <date du jour>_

  **Fait pendant cette séance :**
  - <résumé en 2 à 5 puces de ce qu'on a fait>

  **Prochaine étape :**
  - <la prochaine chose concrète à faire>

- Ne garde qu'UNE seule section « Où on en est » : remplace l'ancienne, n'en ajoute pas une nouvelle à chaque fois.
- Ne touche pas aux autres sections du fichier.
- Montre le texte à l'utilisateur et demande-lui s'il veut corriger la prochaine étape.

## 3. Commit

- Ajoute les fichiers modifiés avec `git add` (y compris `branches/<branche>.md`).
- N'ajoute jamais de fichiers de secrets (.env, clés, mots de passe) ni de gros fichiers générés (`build/`, `install/`, `log/` de ROS 2). Si tu en vois, signale-les.
- Écris un message de commit court et clair, en français, qui résume la séance.
- Lance `git commit`.

## 4. Push

- Lance `git push origin <branche>` (ajoute `-u` si la branche n'existe pas encore sur GitHub).
- Ne pousse **jamais** sur `main`.
- Si le push échoue, n'essaie pas de forcer (`--force` interdit). Explique l'erreur simplement et propose une solution.

## 5. Résumé final

Termine par 3 lignes maximum : le commit créé, le push réussi ou non, et la prochaine étape.

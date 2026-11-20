---
name: fin-de-seance
description: Clôture une séance de travail - met à jour la section « Où on en est » du CLAUDE.md de la branche, fait un commit, puis pousse sur la branche courante (sur main uniquement avec l'accord explicite de l'utilisateur).
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

## 2. Mettre à jour le `CLAUDE.md` de la branche

- Chaque branche de lot a son propre `CLAUDE.md` (il n'y en a pas sur `main`). S'il n'existe pas, demande à l'utilisateur avant d'en créer un.
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

- Ajoute les fichiers modifiés avec `git add` (y compris `CLAUDE.md`).
- N'ajoute jamais de fichiers de secrets (.env, clés, mots de passe) ni de gros fichiers générés (`build/`, `install/`, `log/` de ROS 2). Si tu en vois, signale-les.
- Écris un message de commit court et clair, en français, qui résume la séance.
- Lance `git commit`.

## 4. Push

- Lance `git push origin <branche>` (ajoute `-u` si la branche n'existe pas encore sur GitHub).
- Si le push échoue, n'essaie pas de forcer (`--force` interdit). Explique l'erreur simplement et propose une solution.

### Pousser sur `main` (seulement avec autorisation)

- On travaille sur les branches de lot. `main` ne sert **qu'aux skills** (`.claude/skills/`) : aucun autre fichier n'y va.
- Par défaut, on ne pousse **jamais** sur `main`.
- Si la séance a modifié un skill (`.claude/skills/`), propose de l'envoyer aussi sur `main`. Explique ce qui partirait sur `main` et pourquoi.
- **Pose la question et attends un « oui » explicite** de l'utilisateur pour ce push-là. Un accord donné une fois ne vaut pas pour les séances suivantes.
- Si l'utilisateur accepte :
  1. `git fetch origin`, puis `git switch main` et `git pull origin main` pour partir de la version à jour.
  2. `git checkout <branche> -- .claude/skills/` pour ne copier **que** les skills. N'envoie jamais sur `main` le `CLAUDE.md` d'une branche de lot, ni des fichiers propres au lot (`maps/`, `config/`…).
  3. `git commit`, puis `git push origin main`.
  4. `git switch <branche>` pour revenir sur la branche de travail.
- Si l'utilisateur refuse, ou si le push sur `main` est rejeté (branche protégée, conflit), propose plutôt une Pull Request de `<branche>` vers `main`.
- Jamais de `--force` sur `main`.

## 5. Résumé final

Termine par 3 lignes maximum : le commit créé, le push réussi ou non (et sur `main` si l'utilisateur l'a autorisé), et la prochaine étape.

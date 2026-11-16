# CLAUDE.md

Instructions pour Claude Code sur ce projet.

## Contexte

- L'utilisateur débute avec Git : rester pédagogique.
- Dépôt partagé : `akiiko-prog/ESMEBOT` (remote `origin`).
- Branche de travail : `reperer`.

## Règles Git

- Toujours travailler sur la branche `reperer`.
- **Ne jamais pousser sur `main`.**
- **Ne jamais** utiliser `git push --force`, `git reset --hard` ni supprimer une branche (locale ou distante) sans demander l'accord explicite de l'utilisateur au préalable.
- Expliquer chaque commande Git en une phrase avant ou en même temps que son exécution.

## Raspberry Pi

- Le Pi est joignable via : `ssh ruben@robotpi.local`
- Test de connexion : `ssh ruben@robotpi.local "echo ok"` (doit afficher `ok`).

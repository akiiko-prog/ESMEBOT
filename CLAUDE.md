# CLAUDE.md — Robot ESME, partie « Se déplacer »

Instructions pour Claude Code sur cette branche.

## Contexte
- Robot autonome qui guide les familles aux portes ouvertes de l'ESME (bouton → destination). Équipe de 7.
- Cette branche couvre le **déplacement** : roues motorisées, ESP32 et contrôleurs moteurs. _(À préciser par l'équipe.)_
- Plusieurs membres débutent avec Git, Linux et ROS : **rester pédagogique**, une étape à la fois, en français simple.
- Dépôt partagé : `akiiko-prog/ESMEBOT` (remote `origin`).
- Branche de travail : `Deplacer`.

## Règles Git
- Toujours travailler sur la branche `Deplacer`, **jamais directement sur `main`**.
- Ne jamais pousser sur `main` : passer par une Pull Request sur GitHub.
- Ne jamais utiliser `git push --force`, `git reset --hard` ni supprimer une branche (locale ou distante) sans l'accord explicite de l'utilisateur.
- Expliquer chaque commande Git en une phrase avant ou pendant son exécution.
- Ne pas modifier le code d'un autre lot (perception, etc.) sans demande explicite.
- Ne jamais committer de secrets (.env, clés, mots de passe) ni de dossiers générés par ROS 2 (`build/`, `install/`, `log/`).
- Les skills Claude sont sur `main` (`.claude/skills/`). Pour les avoir ici : `git fetch origin` puis `git merge origin/main`.
- En fin de séance : lancer `/fin-de-seance` (met à jour « Où on en est » ci-dessous, commit, push).

## Architecture du robot
- **PC de développement** : Ubuntu 24.04 (WSL). Le code s'écrit et se versionne ici.
- **Raspberry Pi 5 (4 Go)** = cerveau embarqué : Ubuntu Server 24.04 arm64, **ROS 2 Jazzy (ros-base)**, capteurs LiDAR + IMU, SLAM, plus tard Nav2.
- **ESP32 + contrôleurs moteurs** = pilotage des roues motorisées. Liaison ESP32 ↔ Pi : à préciser.
- **Interface avec la perception** : le Pi publie des ordres de vitesse sur **`/cmd_vel`** (`geometry_msgs/Twist`), la partie ESP32/moteurs les exécute.

## Raspberry Pi
- Joignable via `ssh <utilisateur>@robotpi.local` (sinon IP en `172.20.10.x`, partage de connexion iPhone).
- Test de connexion : `ssh <utilisateur>@robotpi.local "echo ok"` (doit afficher `ok`).
- Commandes ROS via SSH, par exemple :
  `ssh <utilisateur>@robotpi.local "source /opt/ros/jazzy/setup.bash && ros2 topic list"`
- Envoi d'un fichier **par SSH uniquement** (pas de dépôt Git ni de scp sur le Pi) :
  `ssh <utilisateur>@robotpi.local "cat > ~/<chemin>" < <fichier_local>`, puis `colcon build` si c'est un paquet ROS.
- WSL **ne voit pas** les topics ROS du Pi : toujours passer par SSH. Visualisation = Foxglove (`ws://<IP_Pi>:8765`).

## Règles de travail sur le Pi
- **Ne jamais lancer de commande `sudo` via SSH** : l'utilisateur la tape lui-même. Proposer la commande, ne pas l'exécuter.
- Installation de paquets : en cas de « held broken packages » → `sudo aptitude install <paquet>`, accepter la solution **« Downgrade »**, refuser toute solution qui n'installe pas le paquet ou supprime `ros-jazzy-ros-base`.
- **Jamais** de gros copier-coller de fichiers dans un terminal SSH (caractères parasites `[200~`).

## Topics ROS disponibles
| Topic | Contenu | Repère | Fréquence | Fourni par |
|---|---|---|---|---|
| `/scan` | LiDAR LD19 | `base_laser` | 10 Hz | `reperer` (`ldlidar.service`) |
| `/imu` | IMU MPU-6050 (gyro + accéléro) | `imu_link` | 50 Hz | `reperer` (`imu.service`) |
| `/cmd_vel` | ordres de vitesse | — | — | consommé par cette partie (moteurs) |

## Décisions d'équipe
- **Pas d'encodeurs de roues.** Le mouvement est estimé par l'IMU (gyro) + le scan matching du LiDAR.
- Nav2 : plus tard (robot roulant + carte de l'école nécessaires).

## Matériel et code du lot
_À compléter par l'équipe : modèle des moteurs et contrôleurs, carte ESP32, câblage, liaison avec le Pi (USB série, micro-ROS…)._

## Où on en est
_À compléter par l'équipe._

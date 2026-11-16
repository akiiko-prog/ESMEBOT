# CLAUDE.md — Robot ESME (commun à toute l'équipe)

Instructions pour Claude Code, partagées par les 7 membres de l'équipe.
Ce fichier vit sur `main`.

## Au début de chaque séance
1. Lance `git branch --show-current` pour connaître la branche de travail.
2. Lance `git log --oneline -5` pour voir où en était la dernière séance.

## Le projet
- Robot autonome qui guide les familles aux portes ouvertes de l'ESME (bouton → destination).
- Dépôt partagé : `akiiko-prog/ESMEBOT` (remote `origin`).
- Plusieurs membres débutent avec Git, Linux et ROS : **rester pédagogique**, une étape à la fois, en français simple.

## Organisation des branches
Chaque lot a sa branche ; `main` ne reçoit que du travail validé, via Pull Request.

| Branche | Lot |
|---|---|
| `reperer` | Perception : LiDAR + IMU, fusion, SLAM |
| `Deplacer` | à compléter par l'équipe |
| `autonome` | à compléter par l'équipe |
| `presenter` | à compléter par l'équipe |

## Règles Git
- Travailler sur la branche de son lot, **jamais directement sur `main`**.
- Ne jamais pousser sur `main` : passer par une Pull Request sur GitHub.
- Ne jamais utiliser `git push --force`, `git reset --hard` ni supprimer une branche (locale ou distante) sans l'accord explicite de l'utilisateur.
- Expliquer chaque commande Git en une phrase avant ou pendant son exécution.
- Ne pas modifier le code d'un autre lot sans demande explicite.
- Ne jamais committer de secrets (.env, clés, mots de passe) ni de dossiers générés par ROS 2 (`build/`, `install/`, `log/`).
- En fin de séance : lancer `/fin-de-seance` (résumé de la séance, commit, push).

## Architecture du robot
- **PC de développement** : Ubuntu 24.04 (WSL). Le code s'écrit et se versionne ici.
- **Raspberry Pi 5 (4 Go)** = cerveau embarqué : Ubuntu Server 24.04 arm64, **ROS 2 Jazzy (ros-base)**, capteurs LiDAR + IMU, SLAM, plus tard Nav2.
- **ESP32 + contrôleurs moteurs** = pilotage des roues motorisées. Liaison ESP32 ↔ Pi : à préciser.
- **Interface entre les lots** : le Pi publie des ordres de vitesse sur **`/cmd_vel`**, la partie ESP32/moteurs les exécute.

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
- Avant un test manuel d'un capteur, arrêter son service (`sudo systemctl stop imu` / `ldlidar`), sinon conflit d'accès.
- Installation de paquets : en cas de « held broken packages » → `sudo aptitude install <paquet>`, accepter la solution **« Downgrade »**, refuser toute solution qui n'installe pas le paquet ou supprime `ros-jazzy-ros-base`.
- **Jamais** de gros copier-coller de fichiers dans un terminal SSH (caractères parasites `[200~`).

## Topics ROS disponibles
| Topic | Contenu | Repère | Fréquence | Fourni par |
|---|---|---|---|---|
| `/scan` | LiDAR LD19 | `base_laser` | 10 Hz | `reperer` (`ldlidar.service`) |
| `/imu` | IMU MPU-6050 (gyro + accéléro) | `imu_link` | 50 Hz | `reperer` (`imu.service`) |
| `/cmd_vel` | ordres de vitesse | — | — | consommé par la partie moteurs |

## Décisions d'équipe
- **Pas d'encodeurs de roues.** Le mouvement est estimé par l'IMU (gyro) + le scan matching du LiDAR. Limite : risque de dérive dans les longs couloirs uniformes.
- Nav2 : plus tard (robot roulant + carte de l'école nécessaires).

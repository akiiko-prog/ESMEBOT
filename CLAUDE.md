# CLAUDE.md — Robot ESME, partie « Se repérer » (perception)

Instructions pour Claude Code sur ce projet.

## Contexte
- Robot autonome qui guide les familles aux portes ouvertes de l'ESME (bouton → destination). Équipe de 7.
- Cette branche couvre la **perception** : LiDAR + IMU, et leur fusion pour le SLAM.
- L'utilisateur débute avec Git, Linux et ROS : **rester pédagogique**, une étape à la fois.
- Dépôt partagé : `akiiko-prog/ESMEBOT` (remote `origin`).
- Branche de travail : `reperer`.

## Règles Git
- Toujours travailler sur la branche `reperer`.
- Ne jamais pousser sur `main`.
- Ne jamais utiliser `git push --force`, `git reset --hard` ni supprimer une branche (locale ou distante) sans demander l'accord explicite de l'utilisateur au préalable.
- Expliquer chaque commande Git en une phrase avant ou en même temps que son exécution.
- Sur cette branche, seul le dossier `maps/` est propre au lot (cartes SLAM). Les skills viennent de `main` (`.claude/skills/`).
- Ne jamais committer de secrets (.env, clés) ni `build/`, `install/`, `log/` de ROS 2.
- En fin de séance : lancer `/fin-de-seance` (met à jour « Où on en est » ci-dessous, commit, push).

## Architecture du robot
- Claude Code tourne sur le **PC** (Ubuntu 24.04 dans WSL), dans ce dépôt cloné.
- Le robot = une **structure à roues motorisées** (montée par un autre membre de l'équipe, hors de cette branche) + :
  - **Raspberry Pi 5 (4 Go)** = cerveau embarqué : Ubuntu Server 24.04 arm64, **ROS 2 Jazzy (ros-base)**, capteurs LiDAR + IMU, SLAM, plus tard Nav2.
  - **ESP32 + contrôleurs moteurs** = pilotage des roues (lot d'un coéquipier, pas encore branché). Liaison ESP32 ↔ Pi : à préciser par l'équipe.
- Interface prévue entre les deux : le Pi publie des ordres de vitesse sur **`/cmd_vel`**, la partie ESP32/moteurs les exécute.
- **Ne pas modifier le code moteurs/ESP32** depuis cette branche, sauf demande explicite.

## Raspberry Pi
- Le Pi est joignable via : `ssh ruben@robotpi.local` (sinon IP en `172.20.10.x`, partage de connexion iPhone).
- Test de connexion : `ssh ruben@robotpi.local "echo ok"` (doit afficher `ok`).
- **Rien n'est installé côté Claude sur le Pi.** Toute commande ROS s'y exécute via SSH, par exemple :
  `ssh ruben@robotpi.local "source /opt/ros/jazzy/setup.bash && ros2 topic hz /imu"`
- Le code s'écrit **ici, en local** (versionné dans ce dépôt). **Pas de dépôt Git sur le Pi, pas de scp.** Envoi d'un fichier **par SSH uniquement** : `ssh ruben@robotpi.local "cat > ~/<chemin>" < <fichier_local>`, puis `colcon build` sur le Pi si c'est un paquet ROS.
- WSL **ne voit pas** les topics ROS du Pi (isolement réseau) : toujours passer par SSH. Visualisation = Foxglove (`ws://<IP_Pi>:8765`).

## Règles de travail sur le Pi
- **Ne jamais lancer de commande `sudo` via SSH** : l'utilisateur la tape lui-même. Proposer la commande, ne pas l'exécuter.
- Avant tout test manuel d'un capteur, arrêter son service (`sudo systemctl stop imu` / `ldlidar`) — sinon conflit d'accès au capteur.
- Installation de paquets sur le Pi : conflits fréquents (« held broken packages ») → `sudo aptitude install <paquet>`, accepter la solution **« Downgrade »**, refuser toute solution qui n'installe pas le paquet ou supprime `ros-jazzy-ros-base`.
- **Jamais** de gros copier-coller de fichiers dans un terminal SSH (caractères parasites `[200~`) : envoyer le fichier par `ssh ... "cat > ..." < fichier`.

## Capteurs (en place et fonctionnels)
| Capteur | Topic | Repère | Fréquence | Service au boot |
|---|---|---|---|---|
| LiDAR LDROBOT STL-19P (profil LD19), USB via CP2102, `/dev/ttyUSB0`, 230400 bauds | `/scan` | `base_laser` | 10 Hz | `ldlidar.service` |
| IMU GY-521 (MPU-6050, 6 axes, sans magnéto), I2C adresse `0x68` | `/imu` | `imu_link` | 50 Hz | `imu.service` |

- Driver LiDAR : `~/ldlidar_ros2_ws` (paquet `ldlidar_stl_ros2`, launch `ld19.launch.py`). Deux correctifs pour Jazzy : `#include <pthread.h>` en tête de `ldlidar_driver/src/logger/log_module.cpp`, et `target_link_libraries(ldlidar_stl_ros2_node pthread)` **après** (pas dans) `ament_target_dependencies(...)`.
- Nœud IMU : `~/imu_ws` (paquet Python `imu_publisher`, exécutable `imu_node`). Calibre le biais du gyro pendant 2 s au démarrage → **capteur immobile au boot**. Gyro en rad/s, accéléro en m/s², `orientation_covariance[0] = -1`.
- IMU montée à plat, axe Z vers le haut (`linear_acceleration.z ≈ +9,8`).

## SLAM
- `slam_toolbox` + `nav2_map_server` installés sur le Pi. Config : `~/mapper_params_online_async.yaml` (`base_frame: base_laser`, `odom_frame: odom`, `scan_topic: /scan`).
- Démo actuelle **sans odométrie** : faux repère `static_transform_publisher 0 0 0 0 0 0 odom base_laser` → fragile.
- Sauvegarde de carte : `ros2 run nav2_map_server map_saver_cli -f ~/<nom>` (pendant que slam_toolbox tourne). Les cartes du dépôt vont dans `maps/`.

## Décisions d'équipe
- **Pas d'encodeurs de roues** (les roues sont motorisées, mais sans mesure de leur rotation). Source de mouvement = **IMU (gyro) + scan matching du LiDAR**.
  Limite connue : l'IMU ne mesure pas la distance → risque de dérive dans les longs couloirs uniformes.
- Nav2 : plus tard (robot roulant + carte de l'école nécessaires).

## Où on en est
_Dernière mise à jour : 2026-11-16_

**Fait :**
- LiDAR et IMU publiés au boot sur le Pi (`/scan`, `/imu`).
- Première carte SLAM avec slam_toolbox (sans odométrie).
- Connexion SSH par clé au Pi.

**Prochaine étape :**
- **Fusion IMU + scan avec `robot_localization`** : produire un repère `odom` à partir de `/imu` (et du scan matching) pour remplacer le faux `odom` du SLAM.
- À définir avec l'équipe châssis : position du LiDAR et de l'IMU sur le robot (`base_link → base_laser`, `base_link → imu_link`).
- Gyro z à ≈ −0,024 rad/s à l'arrêt : recalibrer (`sudo systemctl restart imu`, robot immobile).

# Branche reperer — « Se repérer » (perception)

Notes propres au lot perception : LiDAR + IMU, leur fusion et le SLAM.
Les règles communes (Git, Pi, architecture) sont dans le `CLAUDE.md` à la racine.

## Spécifique à cette branche
- Travailler sur la branche `reperer` ; utilisateur SSH du Pi : `ruben@robotpi.local`.
- Ne pas modifier le code moteurs/ESP32 depuis cette branche, sauf demande explicite.

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

## Où on en est
_Dernière mise à jour : 2026-11-16_

**Fait :**
- LiDAR et IMU publiés au boot sur le Pi (`/scan`, `/imu`).
- Première carte SLAM avec slam_toolbox (sans odométrie).
- CLAUDE.md commun et skill `/fin-de-seance` proposés sur `main` (PR #2).

**Prochaine étape :**
- **Fusion IMU + scan avec `robot_localization`** : produire un repère `odom` à partir de `/imu` (et du scan matching) pour remplacer le faux `odom` du SLAM.
- À définir avec l'équipe châssis : position du LiDAR et de l'IMU sur le robot (`base_link → base_laser`, `base_link → imu_link`).

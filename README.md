# ESMEBOT


Robot Autonome "Mascot de l'école"'

## Branche `reperer` : se repérer

Cette branche contient la partie perception du robot : le LiDAR, qui produit le `/scan` dont ont besoin le SLAM et la navigation.

| Dossier | Contenu |
|---|---|
| [`esmebot_lidar/`](esmebot_lidar/) | paquet ROS 2 Jazzy : lancement du LiDAR D500 (LD19), TF `base_link → laser`, outil de vérification `scan_check` |

Démarrage rapide : voir [`esmebot_lidar/README.md`](esmebot_lidar/README.md).

📋 **Toutes les commandes utiles** (LiDAR, RViz, faire la carte, Nav2, Pi ↔ PC, débogage) : [`COMMANDES.md`](COMMANDES.md).

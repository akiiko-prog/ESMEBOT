# Aide-mémoire des commandes ESMEBOT

Ce fichier regroupe toutes les commandes utiles pour ESMEBOT : lancer le LiDAR, ouvrir RViz, faire la carte de l'école, naviguer, déboguer.

> **Convention** : chaque bloc `Terminal 1`, `Terminal 2`… correspond à un terminal différent, à ouvrir en parallèle.
> Ces commandes sont prévues pour ROS 2 **Jazzy** et le workspace `~/esmebot_ws`.

---

## 0. À faire dans CHAQUE nouveau terminal

```bash
source /opt/ros/jazzy/setup.bash
source ~/esmebot_ws/install/setup.bash
```

Pour ne plus avoir à le taper (une seule fois) :

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "source ~/esmebot_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## 1. Installer / compiler

```bash
# Paquets ROS utilisés par le projet (une seule fois)
sudo apt update
sudo apt install ros-jazzy-slam-toolbox ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
                 ros-jazzy-teleop-twist-keyboard ros-jazzy-rqt-tf-tree ros-jazzy-rviz2

# Récupérer les dépendances déclarées dans les package.xml
cd ~/esmebot_ws
rosdep install --from-paths src --ignore-src -y

# Compiler tout le workspace
colcon build --symlink-install

# Compiler un seul paquet (plus rapide)
colcon build --symlink-install --packages-select esmebot_lidar

# Tout recompiler de zéro (en cas d'erreur bizarre)
rm -rf build install log && colcon build --symlink-install
```

> Après chaque `colcon build`, refaire `source ~/esmebot_ws/install/setup.bash`.

Mettre à jour le code depuis GitHub :

```bash
cd ~/esmebot_ws/src/ESMEBOT
git pull
```

---

## 2. LiDAR

### Brancher (sous WSL uniquement)

Dans **PowerShell en administrateur** (Windows) :

```powershell
usbipd list                         # repérer le BUSID du "CP210x"
usbipd bind --busid 1-3             # une seule fois (remplacer 1-3)
usbipd attach --wsl --busid 1-3     # à refaire à chaque branchement
```

### Vérifier que le LiDAR est vu

```bash
lsusb | grep -i cp210               # "Silicon Labs CP210x"
ls -l /dev/ttyUSB* /dev/ldlidar     # le port série
sudo chmod 666 /dev/ttyUSB0         # si "Permission denied" (sans règle udev)
```

### Lancer

```bash
ros2 launch esmebot_lidar lidar.launch.py                    # LiDAR + TF
ros2 launch esmebot_lidar lidar.launch.py rviz:=true         # + RViz
ros2 launch esmebot_lidar lidar.launch.py port:=/dev/ttyUSB0 # autre port
ros2 launch esmebot_lidar lidar.launch.py z:=0.35 yaw:=3.14  # position du LiDAR sur le robot
```

### Vérifier le `/scan`

```bash
ros2 run esmebot_lidar scan_check   # résumé toutes les 2 s (Hz, % valides, distances)
ros2 topic hz /scan                 # doit afficher ~10 Hz
ros2 topic echo /scan --once        # un message complet
ros2 topic info /scan -v            # qui publie, qui écoute, QoS
```

---

## 3. RViz (visualisation)

```bash
rviz2                                                    # RViz vide
rviz2 -d $(ros2 pkg prefix esmebot_lidar)/share/esmebot_lidar/rviz/lidar.rviz   # config LiDAR
ros2 launch nav2_bringup rviz_launch.py                  # config Nav2 (carte + navigation)
```

Réglages à connaître dans RViz :
- **Fixed Frame** (en haut à gauche) : mettre `base_link` pour voir le LiDAR seul, et `map` pendant le SLAM ou la navigation.
- **Add → By topic** : ajoute `/scan`, `/map`, etc.
- Si `/scan` ne s'affiche pas : dans l'affichage LaserScan, passer *Reliability Policy* à **Best Effort**.
- Pour sauvegarder la config : *File → Save Config As*.

---

## 4. Faire la carte de l'école (SLAM)

Le SLAM a besoin de **deux choses** : le `/scan`, et l'odométrie (la TF `odom → base_link`), qui dit de combien le robot a bougé.

- **Avec le vrai robot** : l'odométrie vient des moteurs (encodeurs), c'est l'équipe « Deplacer » qui la fournit.
- **Pour tester avec le LiDAR seul, sans moteurs** : `rf2o_laser_odometry` calcule une odométrie à partir du scan (voir 4.b).

### 4.a Cartographie

```bash
# Terminal 1 : LiDAR
ros2 launch esmebot_lidar lidar.launch.py

# Terminal 2 : odométrie (moteurs du robot, OU rf2o, voir 4.b)

# Terminal 3 : SLAM
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=$(ros2 pkg prefix esmebot_lidar)/share/esmebot_lidar/config/slam_mapping.yaml

# Terminal 4 : visualiser (Fixed Frame = map, ajouter /map et /scan)
rviz2

# Terminal 5 : déplacer le robot au clavier (i = avancer, , = reculer, j/l = tourner, k = stop)
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Conseils pour une bonne carte : rouler **lentement**, tourner doucement, et repasser par le point de départ à la fin. Ce retour permet au SLAM de « fermer la boucle » et de corriger la dérive.

### 4.b Odométrie à partir du LiDAR (test sans moteurs)

À installer une seule fois (le paquet n'existe pas en `apt`) :

```bash
cd ~/esmebot_ws/src
git clone -b ros2 https://github.com/MAPIRlab/rf2o_laser_odometry.git
cd ~/esmebot_ws && colcon build --symlink-install --packages-select rf2o_laser_odometry
```

Lancer (à la place de l'odométrie moteurs) :

```bash
ros2 run rf2o_laser_odometry rf2o_laser_odometry_node --ros-args \
  -p laser_scan_topic:=/scan -p odom_topic:=/odom_rf2o -p publish_tf:=true \
  -p base_frame_id:=base_link -p odom_frame_id:=odom -p init_pose_from_topic:="''" -p freq:=10.0
```

Il suffit alors de **porter le LiDAR à la main** (ou de le poser sur un chariot) et de marcher doucement dans les couloirs.

### 4.c Sauvegarder la carte

```bash
mkdir -p ~/maps

# Carte image (ecole.pgm + ecole.yaml), utilisée par Nav2
ros2 run nav2_map_server map_saver_cli -f ~/maps/ecole

# Graphe SLAM complet (pour reprendre/compléter la carte plus tard avec slam_toolbox)
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph \
  "{filename: '$HOME/maps/ecole'}"
```

> Dans RViz, le panneau *Panels → Add New Panel → SlamToolboxPlugin* propose aussi les boutons « Save Map » et « Serialize Map ».

---

## 5. Naviguer avec la carte (Nav2)

```bash
# Terminal 1 : LiDAR
ros2 launch esmebot_lidar lidar.launch.py

# Terminal 2 : odométrie (moteurs)

# Terminal 3 : Nav2 complet (localisation AMCL + navigation) sur la carte sauvegardée
ros2 launch nav2_bringup bringup_launch.py map:=$HOME/maps/ecole.yaml use_sim_time:=false

# Terminal 4 : RViz préréglé pour Nav2
ros2 launch nav2_bringup rviz_launch.py
```

Ensuite, dans RViz :
1. Clique sur **2D Pose Estimate**, puis indique sur la carte où se trouve le robot et dans quelle direction il regarde.
2. Clique sur **Nav2 Goal**, puis indique la destination. Le robot y va.

> ⚠️ Les paramètres Nav2 par défaut supposent un robot TurtleBot (`base_footprint`, taille, vitesses).
> L'équipe navigation devra fournir son propre fichier `params_file:=...` adapté à ESMEBOT.

Voir la carte seule, sans naviguer :

```bash
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=$HOME/maps/ecole.yaml
ros2 run nav2_util lifecycle_bringup map_server
```

---

## 6. Simulation (sans robot)

```bash
# Robot TurtleBot3 simulé avec Nav2 + RViz, pour s'entraîner
sudo apt install ros-jazzy-nav2-minimal-tb3-sim
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False
```

---

## 7. Enregistrer et rejouer des données (rosbag)

C'est très pratique : on enregistre une seule fois une balade dans l'école, puis on peut retester le SLAM chez soi autant de fois qu'on veut.

```bash
ros2 bag record -o balade_ecole /scan /tf /tf_static /odom    # Ctrl+C pour arrêter
ros2 bag info balade_ecole
ros2 bag play balade_ecole --clock                              # rejouer
```

> Pour lancer le SLAM sur un bag rejoué, ajoute `use_sim_time:=true`.

---

## 8. PC ↔ Raspberry Pi (deux machines)

Les deux machines doivent être sur le **même réseau WiFi** et avoir le **même `ROS_DOMAIN_ID`** :

```bash
echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc     # sur le PC ET sur le Pi (même nombre)
source ~/.bashrc
```

```bash
# Sur le Pi : lancer le LiDAR
ros2 launch esmebot_lidar lidar.launch.py

# Sur le PC : vérifier qu'on reçoit bien le scan
ros2 topic list
ros2 topic hz /scan
```

Se connecter au Pi depuis le PC :

```bash
ssh <utilisateur>@<adresse-ip-du-pi>
hostname -I                         # (sur le Pi) affiche son adresse IP
```

> **WSL** : par défaut, WSL ne « voit » pas les autres machines du réseau pour ROS.
> Crée le fichier `C:\Users\<toi>\.wslconfig` avec ce contenu :
> ```
> [wsl2]
> networkingMode=mirrored
> ```
> puis lance `wsl --shutdown` dans PowerShell et rouvre Ubuntu.

---

## 9. Déboguer

```bash
ros2 node list                      # nœuds qui tournent
ros2 topic list                     # topics existants
ros2 topic hz <topic>               # fréquence d'un topic
ros2 topic echo <topic>             # contenu d'un topic
ros2 node info /ldlidar             # ce que publie/écoute un nœud
ros2 param list /ldlidar            # paramètres d'un nœud
ros2 param get /ldlidar port_name

rqt_graph                           # schéma des nœuds et topics
ros2 run rqt_tf_tree rqt_tf_tree    # arbre des repères (map → odom → base_link → laser)
ros2 run tf2_tools view_frames      # même chose, exporté en PDF
ros2 run tf2_ros tf2_echo map base_link   # position du robot sur la carte

ros2 doctor                         # diagnostic général de l'installation ROS
```

Arbre de repères attendu quand tout tourne :

```
map ──(SLAM / AMCL)──▶ odom ──(odométrie)──▶ base_link ──(esmebot_lidar)──▶ laser
```

---

## 10. Arrêter

- **Ctrl + C** dans chaque terminal.
- Si un nœud reste bloqué : `pkill -f ldlidar` (ou le nom du nœud).
- Sous WSL, pour libérer l'USB : `usbipd detach --busid 1-3` dans PowerShell.

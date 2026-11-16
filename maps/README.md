# Cartes du robot ESME

Cartes produites par `slam_toolbox` sur le Raspberry Pi, puis copiées ici.

Chaque carte = 2 fichiers (lus plus tard par Nav2) :
- `<nom>.pgm` : image de la carte (noir = mur, blanc = libre, gris = inconnu)
- `<nom>.yaml` : résolution, origine, nom de l'image

Optionnel (pour reprendre une cartographie) : `<nom>.posegraph` + `<nom>.data` (sérialisation slam_toolbox).

## Procédure
```bash
# 1. Sur le Pi, pendant que slam_toolbox tourne
ssh ruben@robotpi.local "mkdir -p ~/maps && source /opt/ros/jazzy/setup.bash && ros2 run nav2_map_server map_saver_cli -f ~/maps/<nom>"
# 2. Copie Pi -> PC
scp ruben@robotpi.local:~/maps/<nom>.* ~/ESMEBOT/maps/
# 3. Git (branche reperer)
git add maps/ && git commit -m "Carte <nom>" && git push origin reperer
```

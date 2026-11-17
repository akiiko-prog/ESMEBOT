# Cartographie : fusion (IMU + rf2o) + slam_toolbox + Foxglove
#
# Arbre des reperes :
#   map --(slam_toolbox)--> odom --(EKF)--> base_link --(statiques)--> base_laser / imu_link
#
# Plus besoin du faux "static_transform_publisher odom base_laser".
#
# Sur le Pi :
#   source /opt/ros/jazzy/setup.bash && source ~/rf2o_ws/install/setup.bash
#   ros2 launch ~/fusion/slam.launch.py
# Visualisation : Foxglove -> ws://<IP_Pi>:8765
# Sauvegarde (dans un 2e terminal, pendant que ca tourne) :
#   ros2 run nav2_map_server map_saver_cli -f ~/<nom>

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

HERE = os.path.dirname(os.path.abspath(__file__))


def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(HERE, 'fusion.launch.py')),
        ),
        # Launch officiel : il active le noeud slam_toolbox (noeud a cycle de vie en Jazzy)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')),
            launch_arguments={
                'slam_params_file': os.path.join(HERE, 'mapper_params_online_async.yaml'),
                'use_sim_time': 'false',
            }.items(),
        ),
        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            parameters=[{'port': 8765}],
        ),
    ])

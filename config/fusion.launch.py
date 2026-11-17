# Fusion IMU + odometrie laser -> repere odom -> base_link
#
# Lance :
#   1. base_link -> imu_link (repere statique, PROVISOIRE : IMU au centre, a plat)
#   2. rf2o_laser_odometry : /scan -> /odom_rf2o (sans publier de TF)
#   3. ekf_node (robot_localization) : /odom_rf2o + /imu -> TF odom -> base_link
#
# Le repere base_link -> base_laser est deja publie par ldlidar.service.
#
# Sur le Pi :
#   source /opt/ros/jazzy/setup.bash && source ~/rf2o_ws/install/setup.bash
#   ros2 launch ~/fusion/fusion.launch.py

import os

from launch import LaunchDescription
from launch_ros.actions import Node

EKF_PARAMS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ekf.yaml')


def generate_launch_description():
    return LaunchDescription([
        # A remplacer par la vraie position de l'IMU (equipe chassis)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_imu_link',
            arguments=['--x', '0', '--y', '0', '--z', '0',
                       '--yaw', '0', '--pitch', '0', '--roll', '0',
                       '--frame-id', 'base_link', '--child-frame-id', 'imu_link'],
        ),
        Node(
            package='rf2o_laser_odometry',
            executable='rf2o_laser_odometry_node',
            name='rf2o_laser_odometry',
            output='screen',
            parameters=[{
                'laser_scan_topic': '/scan',
                'odom_topic': '/odom_rf2o',
                'publish_tf': False,          # c'est l'EKF qui publie la TF
                'base_frame_id': 'base_link',
                'odom_frame_id': 'odom',
                'init_pose_from_topic': '',
                'freq': 10.0,                 # = frequence du LiDAR
            }],
            arguments=['--ros-args', '--log-level', 'warn'],  # coupe le log a chaque scan
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[EKF_PARAMS],
        ),
    ])

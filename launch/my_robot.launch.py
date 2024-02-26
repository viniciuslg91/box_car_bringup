#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import Node

def generate_launch_description():
    
    pkg_box_car_gazebo = get_package_share_directory('box_car_gazebo')
    pkg_box_car_description = get_package_share_directory('box_car_description')
    
    # Start world
    start_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_box_car_gazebo, 'launch', 'start_world_launch.py'),
        )
    ) 
    
    spawn_robot_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_box_car_description, 'launch', 'spawn_robot_launch_v4.launch.py'),
        )
    )
    
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )
    
    robot_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=["joint_trajectory_controller", "-c", "/controller_manager"],
    )
    
    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[robot_controller_spawner],
            )
        ),
        start_world,
        spawn_robot_world,
        joint_state_broadcaster_spawner
    ])
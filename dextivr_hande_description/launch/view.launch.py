#!/usr/bin/env python3
#
# Copyright (c) 2025, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
#
# All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "com_port", description="The communication port for the hardware interface.", default_value="/dev/ttyUSB0"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "finger_xacro", description="The xacro for the desired gripper finger.", default_value="fngr_v6"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_fake_hardware", description="Run with ros2 control fake hardware interface", default_value="false"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "tf_prefix",
            default_value="''",
            description="tf_prefix of the joint names, useful for \
                multi-robot setup. If changed than also joint names in the controllers' configuration \
                have to be updated.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "name",
            default_value="dextivr_hande",
            description="Name of the robot. Gets used by ros2 control",
        )
    )

    # Initialize arguments
    com_port = LaunchConfiguration("com_port")
    finger_xacro = LaunchConfiguration("finger_xacro")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    tf_prefix = LaunchConfiguration("tf_prefix")
    name = LaunchConfiguration("name")

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare("dextivr_hande_description"), "urdf", "dextivr_hande.urdf.xacro"]),
            " ",
            "com_port:=",
            com_port,
            " ",
            "finger_xacro:=",
            finger_xacro,
            " ",
            "use_fake_hardware:=",
            use_fake_hardware,
            " ",
            "tf_prefix:=",
            tf_prefix,
            " ",
            "name:=",
            name,
        ]
    )

    robot_description = {"robot_description": robot_description_content}

    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("dextivr_hande_description"), "rviz", "visualization.rviz"]
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    nodes_to_start = [
        joint_state_publisher_node,
        robot_state_publisher_node,
        rviz_node,
    ]

    return LaunchDescription(declared_arguments + nodes_to_start)

# Copyright (c) 2022 PickNik, Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the {copyright_holder} nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import launch
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch.actions import DeclareLaunchArgument
import launch_ros
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():
    gripper = '_hande'

    finger_type_string = 'nasa'
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "com_port",
            description="The communication port to connect to the gripper.",
            choices=['/dev/ttyUSB0', '/dev/ttyACM0'],
            default_value='/dev/ttyACM0'
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "finger_type",
            description="The type of fingers to use.",
            choices=['standard', 'nasa'],
            default_value='standard'
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_fake_hardware",
            description="Run with ros2 control fake hardware interface",
            default_value="false"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "prefix",
            default_value="''",
            description="Prefix of the joint names, useful for \
                multi-robot setup. If changed than also joint names in the controllers' configuration \
                have to be updated.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "name",
            default_value='robotiq_gripper_hande',
            description="Name of the robot. Gets used by ros2 control",
        )
    )
    if finger_type_string == 'nasa':
        declared_arguments.append(
            DeclareLaunchArgument(
                "finger_file", default_value="package://robotiq_hande_description/meshes/hande_fngr_nail_v2.stl",
                description="The path to the finger file.",
            )
        )
        declared_arguments.append(
            DeclareLaunchArgument(
                "scale", default_value="1.0",
                description="The scale of the finger meshes.",
            )
        )
        declared_arguments.append(
            DeclareLaunchArgument(
                "mount_x", default_value="0.0",
                description="The translation to the origin of the finger mesh.",
            )
        )
        declared_arguments.append(
            DeclareLaunchArgument(
                "mount_y", default_value="0.0032",
                description="The translation to the origin of the finger mesh.",
            )
        )
    else:
        declared_arguments.append(
            DeclareLaunchArgument(
                "finger_file", default_value="package://robotiq_hande_description/meshes/finger_1.stl",
                description="The path to the finger file.",
            )
        )
        declared_arguments.append(
            DeclareLaunchArgument(
                "scale", default_value="0.001",
                description="The scale of the finger meshes.",
            )
        )
        declared_arguments.append(
            DeclareLaunchArgument(
                "mount_x", default_value="0.025",
                description="The translation to the origin of the finger mesh.",
            )
        )
        declared_arguments.append(
            DeclareLaunchArgument(
                "mount_y", default_value="0.0",
                description="The translation to the origin of the finger mesh.",
            )
        )
    # Parameters that probably won't change
    declared_arguments.append(
        DeclareLaunchArgument(
            "mount_z", default_value="0.099",
            description="The translation to the origin of the finger mesh.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "mount_pitch", default_value="0.0",
            description="The rotation to the origin of the finger mesh.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "mount_yaw", default_value="0.0",
            description="The rotation to the origin of the finger mesh.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "mount_roll", default_value="0.0",
            description="The rotation to the origin of the finger mesh.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "marker_opacity", default_value="0.25",
            description="The opacity of the grasp and push frame markers.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "grasp_distance", default_value="0.148",
            description="The distance from the gripper base frame to the grasp frame.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "finger_length", default_value="0.0605",
            description="The length of the fingers for placing the push frames.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "push_marker_size", default_value="0.01",
            description="The size of the push markers.",
        )
    )

    description_pkg_share = launch_ros.substitutions.FindPackageShare(
        package="robotiq" + gripper + "_description"
    ).find("robotiq" + gripper + "_description")
    default_model_path = os.path.join(
        description_pkg_share, "urdf", "robotiq_gripper" + gripper + ".urdf.xacro"
    )
    default_rviz_config_path = os.path.join(
        description_pkg_share, "rviz", "visualization.rviz"
    )

    pkg_share = launch_ros.substitutions.FindPackageShare(
        package="robotiq_driver"
    ).find("robotiq_driver")

    declared_arguments.append(
        launch.actions.DeclareLaunchArgument(
            name="model",
            default_value=default_model_path,
            description="Absolute path to gripper URDF file",
        )
    )
    declared_arguments.append(
        launch.actions.DeclareLaunchArgument(
            name="rvizconfig",
            default_value=default_rviz_config_path,
            description="Absolute path to rviz config file",
        )
    )

    # Initialize arguments
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    com_port = LaunchConfiguration("com_port")
    prefix = LaunchConfiguration("prefix")
    name = LaunchConfiguration("name")
    # Variables for the finger link and mounting location
    finger_type = LaunchConfiguration("finger_type")
    finger_file = LaunchConfiguration("finger_file")
    scale = LaunchConfiguration("scale")
    mount_x = LaunchConfiguration("mount_x")
    mount_y = LaunchConfiguration("mount_y")
    mount_z = LaunchConfiguration("mount_z")
    mount_roll = LaunchConfiguration("mount_roll")
    mount_pitch = LaunchConfiguration("mount_pitch")
    mount_yaw = LaunchConfiguration("mount_yaw")  
    # Push and marker frame variables
    marker_opacity = LaunchConfiguration("marker_opacity")
    grasp_distance = LaunchConfiguration("grasp_distance")
    finger_length = LaunchConfiguration("finger_length")
    push_marker_size = LaunchConfiguration("push_marker_size")

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare("robotiq_hande_description"), "urdf", "robotiq_gripper_hande.urdf.xacro"]),
            " ", "com_port:=", com_port,
            " ", "finger_type:=", finger_type,
            " ", "use_fake_hardware:=", use_fake_hardware,
            " ", "prefix:=", prefix,
            " ", "name:=", name,
            " ", "finger_file:=", finger_file,
            " ", "scale:=", scale,
            " ", "mount_x:=", mount_x,
            " ", "mount_y:=", mount_y,
            " ", "mount_z:=", mount_z,
            " ", "mount_roll:=", mount_roll,
            " ", "mount_pitch:=", mount_pitch,
            " ", "mount_yaw:=", mount_yaw,
            " ", "marker_opacity:=", marker_opacity,
            " ", "grasp_distance:=", grasp_distance,
            " ", "finger_length:=", finger_length,
            " ", "push_marker_size:=", push_marker_size
        ]
    )
    robot_description_param = {
        "robot_description": launch_ros.parameter_descriptions.ParameterValue(
            robot_description_content, value_type=str
        )
    }

    controllers_file = "robotiq" + gripper + "_controllers.yaml"
    initial_joint_controllers = PathJoinSubstitution(
        [pkg_share, "config", controllers_file]
    )

    control_node = launch_ros.actions.Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            robot_description_param,
            initial_joint_controllers,
        ],
    )

    robot_state_publisher_node = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description_param],
    )

    joint_state_broadcaster_spawner = launch_ros.actions.Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    robotiq_activation_controller_spawner = launch_ros.actions.Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robotiq_activation_controller", "-c", "/controller_manager"],
    )
    
    robotiq_gripper_controller_spawner = launch_ros.actions.Node(
        package="controller_manager",
        executable="spawner",
        arguments=["robotiq_gripper_hande_controller", "-c", "/controller_manager"],
    ) 
    
    rviz_node = launch_ros.actions.Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", LaunchConfiguration("rvizconfig")],
    )

    nodes = [
        control_node,
        robot_state_publisher_node,
        joint_state_broadcaster_spawner,
        robotiq_gripper_controller_spawner,
        robotiq_activation_controller_spawner,
        rviz_node,
    ]

    return launch.LaunchDescription(declared_arguments + nodes)

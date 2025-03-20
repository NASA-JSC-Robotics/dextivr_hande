import launch
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
import launch_ros
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "com_port", description="The communication port for the hardware interface.", default_value="/dev/ttyUSB0"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "finger_xacro", description="The xacro for the desired gripper finger.", default_value="fngr_nail_v2"
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
            description="Prefix of the joint names, useful for \
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

    description_pkg_share = launch_ros.substitutions.FindPackageShare(package="dextivr_hande_description").find(
        "dextivr_hande_description"
    )
    default_model_path = os.path.join(description_pkg_share, "urdf", "dextivr_hande.urdf.xacro")
    default_rviz_config_path = os.path.join(description_pkg_share, "rviz", "visualization.rviz")

    pkg_share = launch_ros.substitutions.FindPackageShare(package="robotiq_hande_description").find(
        "robotiq_hande_description"
    )

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

    declared_arguments.append(
        launch.actions.DeclareLaunchArgument(
            name="launch_rviz",
            default_value="True",
            description="launch rviz2",
        )
    )

    # Initialize arguments
    com_port = LaunchConfiguration("com_port")
    finger_xacro = LaunchConfiguration("finger_xacro")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    tf_prefix = LaunchConfiguration("tf_prefix")
    name = LaunchConfiguration("name")
    launch_rviz = LaunchConfiguration("launch_rviz")

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
    robot_description_param = {
        "robot_description": launch_ros.parameter_descriptions.ParameterValue(robot_description_content, value_type=str)
    }

    controllers_file = "robotiq_hande_controllers.yaml"
    initial_joint_controllers = PathJoinSubstitution([pkg_share, "config", controllers_file])

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
        condition=IfCondition(launch_rviz),
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

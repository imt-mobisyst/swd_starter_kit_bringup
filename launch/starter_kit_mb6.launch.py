from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Declare launch arguments
    launch_args = [
        DeclareLaunchArgument("master_ip", default_value="10.0.0.1"),
        DeclareLaunchArgument("lidar_sensor", default_value="idec_se2l"),
        DeclareLaunchArgument("lidar_sensor_ip", default_value="10.0.0.5"),
        DeclareLaunchArgument("scan_prefix", default_value="laser_1"),
        DeclareLaunchArgument("scan_topic", default_value=["/", LaunchConfiguration("scan_prefix"), "/scan"]),
        DeclareLaunchArgument("scan_frame_id", default_value=LaunchConfiguration("scan_prefix")),
        DeclareLaunchArgument("odom_frame_id", default_value="odom"),
        DeclareLaunchArgument("base_frame_id", default_value="base_link"),
        DeclareLaunchArgument("global_frame_id", default_value="map"),
        DeclareLaunchArgument("baseline_m", default_value="0.485"),
        DeclareLaunchArgument("joy_config", default_value="xbox"),
        DeclareLaunchArgument("enable_cmd_vel_mux", default_value="true"),
        DeclareLaunchArgument("enable_laser_filter", default_value="true"),
        DeclareLaunchArgument("enable_joystick", default_value="true"),
        DeclareLaunchArgument("enable_websocket", default_value="true"),
        DeclareLaunchArgument("nav_mode", default_value="mapping"),
        DeclareLaunchArgument("nav_algo", default_value="hector"),
        DeclareLaunchArgument("nav_localization_static_map", default_value=os.path.join(os.getenv("ROS_PACKAGE_PATH", ""), "swd_starter_kit_bringup/assets/map_box2_v2.yaml")),
    ]

    # Include differential drive controller
    diff_drive_controller_dir = get_package_share_directory('swd_ros2_controllers')
    diff_drive_controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(diff_drive_controller_dir + "/launch/swd_diff_drive_controller.launch.py"),
        launch_arguments={
            "baseline_m": LaunchConfiguration("baseline_m"),
            "base_frame": LaunchConfiguration("base_frame_id"),
            "odom_frame": LaunchConfiguration("odom_frame_id"),
        }.items()
    )
    launch_args.append( diff_drive_controller )

    # Include LiDAR launch file
    bringup_launch_dir = get_package_share_directory('swd_starter_kit_bringup')
    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(bringup_launch_dir + "/launch/lidar_idec_se2l.launch.py"),
        # PythonLaunchDescriptionSource(bringup_launch_dir + "/launch/lidar_" + LaunchConfiguration("lidar_sensor") + ".launch.py"),
        launch_arguments={
            "sensor_ip": LaunchConfiguration("lidar_sensor_ip")
        }.items()
    )
    launch_args.append( lidar_launch )

    # Multiplexer Node:
    launch_args.append( Node(
        package= "basic_node",
        executable= "multiplexer"
    ))

    # Joystick teleoperation include launch
    launch_args.append( Node(
            package='joy',
            executable='joy_node'
    ))
    launch_args.append( Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            parameters=[
                {"axis_linear.x": 1},
                {"scale_linear.x": 0.6},
                {"axis_angular.yaw": 3},
                {"scale_angular.yaw": 3.0}
            ],
            remappings=[
                ("cmd_vel", "multi/cmd_teleop")
            ]
    ))

    # Robot description include launch
    robot_description_launch_dir = get_package_share_directory('swd_starter_kit_description')
    robot_description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource( robot_description_launch_dir + "/launch/robot_description.launch.py")
    )
    launch_args.append(robot_description_launch)

    return LaunchDescription(launch_args)

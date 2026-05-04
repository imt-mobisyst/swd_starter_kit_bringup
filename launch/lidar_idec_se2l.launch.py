from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare launch arguments
    sensor_ip = DeclareLaunchArgument("sensor_ip", default_value="10.0.0.5")

    # LiDAR node
    urg_node = Node(
        package="urg_node",
        executable="urg_node_driver",
        name="urg_node_driver",
        parameters=[
            {"ip_address": LaunchConfiguration("sensor_ip")},
            {"angle_min": -2.1},
            {"angle_max": 2.1}
        ]
    )

    # Static transform publisher
    # static_transform_publisher = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     name="laser_broadcaster",
    #     arguments=["0.04", "0", "0", "0", "0", "0", "base_link", "laser"]
    # )

    return LaunchDescription([
        urg_node,
        # static_transform_publisher
    ])


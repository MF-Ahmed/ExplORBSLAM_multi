from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'num_robots',
            default_value='0',
            description='Number of robots'
        ),
          DeclareLaunchArgument(
            'num_drones',
            default_value='0',
            description='Number of drones'
        ),
        Node(
            package='map_merge',
            executable='map_merge',
            output='screen',
            parameters=[{'use_sim_time': True}, {'num_robots': LaunchConfiguration('num_robots')}, {'num_drones': LaunchConfiguration('num_drones')}]
        )
    ])

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
        Node(
            package='merge_map',
            executable='merge_map',
            output='screen',
            parameters=[{'use_sim_time': True}, {'num_robots': LaunchConfiguration('num_robots')}]
        )
    ])

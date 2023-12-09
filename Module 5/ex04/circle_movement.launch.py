import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Получить путь к пакету
    pkg_chair_circle_move = get_package_share_directory('chair_circle_move')
    pkg_robot_bringup = get_package_share_directory('robot_bringup')

    # Запустить узел chair_circle_move
    chair_circle_move = Node(
        package='chair_circle_move',
        executable='chair_circle_move',
        output='screen',
    )

    # Включить launch-файл из пакета robot_bringup
    robot_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robot_bringup, 'launch', 'diff_drive.launch.py')),
    )

    return LaunchDescription([
        robot_bringup,
        chair_circle_move,
    ])

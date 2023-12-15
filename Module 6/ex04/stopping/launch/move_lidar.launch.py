import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Получить путь к пакету
    pkg_stopping = get_package_share_directory('stopping')
    pkg_robot_bringup = get_package_share_directory('robot_bringup')

    # Запустить узел stopping
    stopping = Node(
        package='stopping',
        executable='stopping',
        output='screen',
    )

    # Включить launch-файл из пакета robot_bringup
    robot_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robot_bringup, 'launch', 'diff_drive.launch.py')),
    )

    return LaunchDescription([
        robot_bringup,
        stopping,
    ])

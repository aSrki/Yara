import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
def generate_launch_description():
    
    urdf_file_name = 'yara.urdf'
    urdf = os.path.join(
        get_package_share_directory('yara_description'),
        urdf_file_name)
    print(urdf)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    
    #LAUNCH PARAMS
    config_use_sim_time = LaunchConfiguration('use_sim_time')
    config_use_joystick = LaunchConfiguration('joystick')

    declare_joystick_arg = DeclareLaunchArgument(
            'joystick',
            default_value='true',
            description="Argument for customising param.")

    declare_use_sim_time = DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='YARA Launch')

    #NODES
    rsp_node = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': config_use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf])
    
    yara_driver_node = Node(
            package='yara_driver',
            executable='yara_driver',
            name='state_publisher',
            parameters=[{"joystick": config_use_joystick}],        
            output='screen')
    
    #LAUNCH FILES
    yara_moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('yara_moveit'), '/launch/demo.launch.py']),
        launch_arguments={}.items()
    )

    return LaunchDescription([
        declare_joystick_arg,   
        declare_use_sim_time,
        yara_driver_node,
        yara_moveit_launch,
    ])
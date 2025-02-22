import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import serial
import pygame 
import struct
import time
import array
import serial.tools.list_ports
from control_msgs.action import FollowJointTrajectory
from control_msgs.action import JointTrajectory

from rclpy.action import ActionServer

class RobotStatePublisher(Node):

    def __init__(self):
        super().__init__('yara_state_publisher')
        self.timer = self.create_timer(0.07, self.timer_callback)

        self.joint_state_publisher = self.create_publisher(JointState, 'joint_states', 10)

        self.joint_state = JointState()

        self.joint_state.name = ['yara_joint_1', 'yara_joint_2', 'yara_joint_3', 'yara_joint_4', 'yara_joint_5']

        self.action_server = ActionServer(
            self,
            FollowJointTrajectory,
            'yara_arm_controller/follow_joint_trajectory',
            self.execute_callback
        )

        # self.trajectory_subscriber = self.create_subscription(
        #     JointTrajectory,
        #     '/yara_arm_controller/joint_trajectory',
        #     self.received_angles_callabck,
        #     10)

        ports = serial.tools.list_ports.comports()
        self.ser = None
        self.msg = bytearray()
        self.joint = 0
        self.msg_done = False

        self.declare_parameter(name="joystick")

        self.use_joystick = self.get_parameter('joystick').get_parameter_value().bool_value

        if(self.use_joystick):
            pygame.joystick.init()
            pygame.init()
            self._joystick = pygame.joystick.Joystick(0)
            self._joystick.init()
            self.arm_control_timer = self.create_timer(0.005, self.control_timer_callback)

        for port, desc, _ in sorted(ports):
                if "STM" in desc:
                    try:
                        self.ser = serial.Serial(str(port), 115200)
                        print(f'Successfully opened port: {desc}')
                    except Exception as e:
                        print(f'error trying to open port: {e}')
                    time.sleep(0.1)
        
        self.init_robot_arm()

    def received_angles_callabck(self, msg):
        self.get_logger().info('Executing trajectory...')
        self.get_logger().info(f'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        self.get_logger().info(f'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        self.get_logger().info(f'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        self.get_logger().info(f'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        self.get_logger().info(f'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        self.get_logger().info(f'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        self.get_logger().info(f'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        self.get_logger().info(f'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        
    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing trajectory...')
        self.get_logger().info(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.get_logger().info(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.get_logger().info(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.get_logger().info(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.get_logger().info(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.get_logger().info(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.get_logger().info(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        self.get_logger().info(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAA')

        feedback_msg = FollowJointTrajectory.Feedback()
        

        success = True
        trajectory = goal_handle.request.trajectory
        self.get_logger().info(f'Following point: {trajectory.points[-1].postions}')
        for point in trajectory.points:
            self.get_logger().info(f'Following point: {point.positions}')
            feedback_msg.status = f'Following point: {point.positions}'
            goal_handle.publish_feedback(feedback_msg)
            
            rclpy.spin_once(self, timeout_sec=1)
        
        result = FollowJointTrajectory.Result()
        if success:
            result.success = True
            self.get_logger().info('Trajectory followed successfully.')
        else:
            result.success = False
            self.get_logger().warn('Failed to follow trajectory.')

        goal_handle.succeed()
        return result

    def init_robot_arm(self):
        msg1 = bytearray(struct.pack("<f", 1))
        self.msg.append(0xAC)
        self.msg.append(0xAC)

        for b in msg1:
            self.msg.append(b)
        self.msg_done = True

        if (self.msg_done):
            self.ser.write(self.msg)
            print('Init done')
            self.msg = bytearray()
            self.msg_done = False

    def control_timer_callback(self):
            axis1 = self._joystick.get_axis(0)
            axis2 = self._joystick.get_axis(1)
            axis3 = self._joystick.get_axis(4)
            axis4 = self._joystick.get_axis(3)
            axis5_cw = self._joystick.get_axis(2)
            axis5_ccw = self._joystick.get_axis(5)
            pygame.event.pump()

            if axis1 != 0:
                self.joint = 0xA1
                if(axis1 > 0.8):
                    msg1 = bytearray(struct.pack("<f", 1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                elif(axis1 < -0.8):
                    msg1 = bytearray(struct.pack("<f", -1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                if (self.msg_done):
                    self.ser.write(self.msg)
                    self.msg = bytearray()
                    self.msg_done = False

            if axis2 != 0:
                self.joint = 0xA2
                if(axis2 > 0.5):
                    msg1 = bytearray(struct.pack("<f", 1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                elif(axis2 < -0.5):
                    msg1 = bytearray(struct.pack("<f", -1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                if (self.msg_done):
                    self.ser.write(self.msg)
                    self.msg = bytearray()
                    self.msg_done = False

            if axis3 != 0:
                self.joint = 0xA3
                if(axis3 > 0.1):
                    msg1 = bytearray(struct.pack("<f", 1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                elif(axis3 < -0.1):
                    msg1 = bytearray(struct.pack("<f", -1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                if (self.msg_done):
                    self.ser.write(self.msg)
                    self.msg = bytearray()
                    self.msg_done = False

            if axis4 != 0:
                self.joint = 0xA4
                if(axis4 > 0.8):
                    msg1 = bytearray(struct.pack("<f", 1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                elif(axis4 < -0.8):
                    msg1 = bytearray(struct.pack("<f", -1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                if (self.msg_done):
                    self.ser.write(self.msg)
                    self.msg = bytearray()
                    self.msg_done = False

            if axis5_cw > 0 or axis5_ccw > 0:
                self.joint = 0xA5
                if(axis5_cw > 0):
                    msg1 = bytearray(struct.pack("<f", 1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                elif(axis5_ccw > 0):
                    msg1 = bytearray(struct.pack("<f", -1))
                    self.msg.append(0xAA)
                    self.msg.append(self.joint)
                    for b in msg1:
                        self.msg.append(b)
                    self.msg_done = True
                if (self.msg_done):
                    self.ser.write(self.msg)
                    self.msg = bytearray()
                    self.msg_done = False

    def timer_callback(self):
        msg1 = bytearray(struct.pack("<f", 1))
        self.msg.append(0xAD)
        self.msg.append(0xAD)

        for b in msg1:
            self.msg.append(b)
        self.msg_done = True

        if (self.msg_done):
            self.ser.write(self.msg)
            ret_msg = self.ser.read(20)
            arr = array.array('f', ret_msg)
            arr.tolist()
            arr.tolist()
            self.msg = bytearray()
            self.msg_done = False
        
        now = self.get_clock().now()

        self.joint_state.header.stamp = now.to_msg()

        self.joint_state.position=(math.radians(arr[0]), math.radians(arr[1]), math.radians(arr[2]), math.radians(arr[3]), math.radians(arr[4]))

        # self.robot_trans.header.stamp = now.to_msg()

        self.joint_state_publisher.publish(self.joint_state)
        # self.robot_state_publisher.sendTransform(self.robot_trans)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = RobotStatePublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

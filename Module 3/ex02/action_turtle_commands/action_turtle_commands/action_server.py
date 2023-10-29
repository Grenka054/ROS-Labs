import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from turtle_action.action import MessageTurtleCommands
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import numpy as np

class TurtleActionServer(Node):

    def __init__(self):
        super().__init__('turtle_action_server')
        self._action_server = ActionServer(
            self,
            MessageTurtleCommands,
            'MessageTurtleCommands',
            self.execute_callback)
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.odom = 0

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = MessageTurtleCommands.Feedback()
        
        command = goal_handle.request.command
        s = goal_handle.request.s
        angle = goal_handle.request.angle

        tw = Twist()	
        
        if command == 'forward':
            for i in range(s):
                tw.linear.x += 1
                self.publisher.publish(tw)
                self.odom += 1
                feedback_msg.odom = self.odom
                goal_handle.publish_feedback(feedback_msg)
                time.sleep(1)
        elif command == 'turn_left':
            tw.angular.z = angle * np.pi / 180
            self.publisher.publish(tw)
            time.sleep(1)
        elif command == 'turn_right':
            tw.angular.z = -1 * angle * np.pi / 180
            self.publisher.publish(tw)
            time.sleep(1)
        else:
            self.get_logger().error('Invalid command received: {}'.format(command))
            raise ValueError('Invalid command')
        
        self.get_logger().info('Goal reached')

        result = MessageTurtleCommands.Result()
        result.result = True
        goal_handle.succeed()
        return result


def main(args=None):
    rclpy.init(args=args)

    turtle_action_server = TurtleActionServer()

    rclpy.spin(turtle_action_server)
    turtle_action_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

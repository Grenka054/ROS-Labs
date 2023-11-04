import math
import rclpy
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from turtle_action.action import MessageTurtleCommands

def distance(pose1: Pose, pose2: Pose):
    return math.sqrt((pose1.x - pose2.x)**2 + 
                    (pose1.y - pose2.y)**2)

class CommandActionServer(Node):

    def __init__(self):
        super().__init__('turtle_action_server')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self._action_server = ActionServer(
            self,
            MessageTurtleCommands,
            'MessageTurtleCommands',
            self.execute_callback)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.pose = Pose()
        self.last_pose = Pose()

    def pose_callback(self, msg):
        self.pose = msg

    def is_turtle_moving(self):
        return self.pose.linear_velocity or self.pose.angular_velocity

    def publish_feedback(self):
        feedback_msg = MessageTurtleCommands.Feedback()
        feedback_msg.odom = distance(self.last_pose, self.pose)
        self.goal_handle.publish_feedback(feedback_msg)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        command = goal_handle.request.command
        twist = Twist()

        if command == 'forward':
            twist.linear.x = float(goal_handle.request.s)
        elif command == 'turn_left':
            twist.angular.z = goal_handle.request.angle * math.pi / 180
        elif command == 'turn_right':
            twist.angular.z = -goal_handle.request.angle * math.pi / 180
        else:
            self.get_logger().error('Invalid command received: {}'.format(command))
            raise ValueError('Invalid command')

        self.publisher.publish(twist)

        # Ждем начала движения
        while not self.is_turtle_moving():
            pass
        
        self.last_pose = self.pose
        self.goal_handle = goal_handle
        feedback_timer = self.create_timer(0.5, self.publish_feedback)

        # Пока черепаха движется выводим фидбек
        while self.is_turtle_moving():
            pass
        
        feedback_timer.cancel()
        goal_handle.succeed()
        result = MessageTurtleCommands.Result()
        result.result = True
        return result


def main(args=None):
    rclpy.init(args=args)
    action_turtle_server = CommandActionServer()

    # Второй поток нужен для обработки положения черепахи
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(action_turtle_server)
    executor.spin()

if __name__ == '__main__':
    main()

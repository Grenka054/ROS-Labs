import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from turtle_action.action import MessageTurtleCommands
import time

class TurtleActionClient(Node):

    def __init__(self):
        super().__init__('turtle_action_client')
        self.action_client = ActionClient(self, MessageTurtleCommands, 'MessageTurtleCommands')

    def send_goal(self, goal):
        goal_msg = MessageTurtleCommands.Goal()
        goal_msg.command = goal[0]
        if goal_msg.command == 'forward':
            goal_msg.s = goal[1]
            goal_msg.angle = 0
        else:
            goal_msg.s = 0
            goal_msg.angle = goal[1]

        self.action_client.wait_for_server()
        return self.action_client.send_goal_async(goal_msg, self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Distance: {0}'.format(feedback.odom))


def main(args=None):
    rclpy.init(args=args)

    turtle_action_client = TurtleActionClient()

    commands = [['forward', 2],['turn_right', 90],['forward', 1]]
    for command in commands:
        future = turtle_action_client.send_goal(command)
        rclpy.spin_until_future_complete(turtle_action_client, future)

    rclpy.spin(turtle_action_client)

    turtle_action_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

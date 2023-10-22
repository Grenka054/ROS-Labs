import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from turtle_action.action import MessageTurtleCommands


class TurtleActionClient(Node):

    def __init__(self):
        super().__init__('turtle_action_client')
        self._action_client = ActionClient(self, MessageTurtleCommands, 'MessageTurtleCommands')

    def send_goal(self, goal):
        goal_msg = MessageTurtleCommands.Goal()
        goal_msg.command = goal[0]
        goal_msg.s = goal[1]
        goal_msg.angle = goal[2]

        self._action_client.wait_for_server()

        return self._action_client.send_goal_async(goal_msg, self.feedback_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.result))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Distance: {0}'.format(feedback.odom))


def main(args=None):
    rclpy.init(args=args)

    turtle_action_client = TurtleActionClient()

    commands = [['forward', 2, 0],['turn_right', 0, 90],['forward', 1, 0]]
    for i in range(len(commands)):
        future = turtle_action_client.send_goal(commands[i])
        rclpy.spin_until_future_complete(turtle_action_client, future)

    turtle_action_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

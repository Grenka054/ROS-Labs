import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from turtle_action.action import MessageTurtleCommands


class CommandActionClient(Node):

    def __init__(self):
        super().__init__('turtle_action_server')
        self._action_client = ActionClient(self, MessageTurtleCommands, 'MessageTurtleCommands')
        self.commands = iter([])

    def send_goal(self, goal):
        goal_msg = MessageTurtleCommands.Goal()
        goal_msg.command, value = goal
        if goal_msg.command == 'forward':
            goal_msg.s = value
            goal_msg.angle = 0
        else:
            goal_msg.s = 0
            goal_msg.angle = value

        self._action_client.wait_for_server()
        
        self._send_goal_future = self._action_client.send_goal_async(goal_msg,
                                self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)   

    def goal_response_callback(self, future):
        # Принял ли сервер команду
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        # Запуск следующей команды
        try:
            next_goal = next(self.commands)
        except StopIteration:
            rclpy.shutdown()
        else:
            self.send_goal(next_goal)

        # Обработка результата
        result = future.result().result
        if result.result:
            self.get_logger().info('Goal achieved')

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Distance: {feedback.odom:.2f}')


def main(args=None):
    rclpy.init(args=args)
    action_client = CommandActionClient()
    
    # Итератор по коммандам
    action_client.commands = iter([['forward', 2], ['turn_right', 90], ['forward', 2]])
    action_client.send_goal(next(action_client.commands))
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()

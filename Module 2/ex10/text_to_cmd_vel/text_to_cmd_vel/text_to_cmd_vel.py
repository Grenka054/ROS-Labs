import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from numpy import pi
class TextToCmdVel(Node):

    def __init__(self):
        super().__init__('text_to_cmd_vel')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(String, 'cmd_text', self.listener_callback, 10)

    def listener_callback(self, msg):
        message = Twist()
        if msg.data == "turn_right":
            message.angular.z = -pi/2
        elif msg.data == "turn_left":
            message.angular.z = pi/2
        elif msg.data == "move_forward":
            message.linear.x = 1.0
        elif msg.data == "move_backward":
            message.linear.x = -1.0
        self.publisher_.publish(message)

def main(args=None):
    rclpy.init(args=args)
    
    text_to_cmd_vel = TextToCmdVel()
    
    rclpy.spin(text_to_cmd_vel)
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    text_to_cmd_vel.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


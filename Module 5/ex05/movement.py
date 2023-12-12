import rclpy, sys
from rclpy.node import Node
from geometry_msgs.msg import Twist
from math import pi
import signal
import time

class StarPublisher(Node):

    def __init__(self):
        super().__init__('publisher')
        self.publisher = self.create_publisher(Twist, '/robot/cmd_vel', 10)
        timer_period = 0.1  # уменьшим период таймера для более плавного движения
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.start_time = time.time()

    def timer_callback(self):
        twist = Twist()
        current_time = time.time()
        # меняем скорость вращения и линейную скорость в зависимости от времени, чтобы создать движение "звезды"
        if int((current_time - self.start_time) / 5) % 2 == 0:
            twist.linear.x = 1.0
        else:
            twist.angular.z = pi / 2
        self.publisher.publish(twist)

def signal_handler(sig, frame):
    rclpy.shutdown()

signal.signal(signal.SIGINT, signal_handler)        
        
def main(args=None):
    rclpy.init(args=args)
    star = StarPublisher()
    rclpy.spin(star)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

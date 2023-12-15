import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import numpy as np


class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.publisher = self.create_publisher(Twist, '/robot/cmd_vel', 10)
        self.sub = self.create_subscription(Image, '/depth/image', self.image_callback, 1)
        self.timer = self.create_timer(0.2, self.go_forward)
        self.msg = np.array([[]])

    def image_callback(self, data):
        bridge = CvBridge()
        img = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        self.msg = img

    def go_forward(self):
        message = Twist()
        image = self.msg
        h, w = image.shape
        if w != 0:
            x_c, y_c = w // 2, h // 2
            num_dots = 10
            points = []
            # Берем 10 пикселей по эллиппсу
            for i in range(num_dots):
                angle = 2 * np.pi * i / num_dots
                y = int(y_c + 0.8 * y_c * np.sin(angle))
                x = int(x_c + 0.8 * x_c * np.cos(angle))
                points.append((y, x))
            
            pixel_values = [image[point] for point in points]
            average_pixel_value = np.mean(pixel_values, axis=0)
            
            if average_pixel_value > 1.5:
                self.get_logger().info('Obstacle founded in distance: ' + str(average_pixel_value))
                message.linear.x = 0.1

            self.publisher.publish(message)              

def main(args=None):
    rclpy.init(args=args)
    publisher = Publisher()
    rclpy.spin(publisher)
    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
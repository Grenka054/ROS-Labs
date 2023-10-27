import rclpy
from rclpy.node import Node
import sys

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import atan2, sqrt, pow, pi
import time

class Turtle_to_Goal(Node):

    def __init__(self, x, y, theta):
        super().__init__('my_publisher')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.update_pose, 10)
        self.current_pose = Pose()
        self.goal_pose = Pose(x = float(x), y = float(y), theta = float(theta))

    def update_pose(self, pose):
        self.current_pose = pose
        self.move_to_goal(self.goal_pose)

    def find_distance(self, goal_pose):
        return sqrt(pow(goal_pose.x - self.current_pose.x, 2) + pow(goal_pose.y - self.current_pose.y, 2))

    def find_angular(self, goal_pose):
        return atan2(goal_pose.y - self.current_pose.y, goal_pose.x - self.current_pose.x)

    def move_to_goal(self, goal_pose):
        tw = Twist()
        # Вычисляем угол, на который нужно развернуться
        alpha = self.find_angular(goal_pose)
        angle = alpha - self.current_pose.theta
        self.current_pose.theta += angle
        tw.angular.z = angle

        # Поворот
        self.publisher.publish(tw)
        time.sleep(1)
        tw.angular.z = 0.0

        # Прохать прямо на посчитанное расстояние
        tw.linear.x = self.find_distance(goal_pose)
        self.publisher.publish(tw)
        time.sleep(1)
        tw.linear.x = 0.0
        tw.linear.y = 0.0
		
        # [0, 360] -> [-180, 180]
        goal_pose.theta = (goal_pose.theta + 180) % 360 - 180
        # Повернуться на заданный пользователем угол
        goal_pose.theta *= pi / 180
        tw.angular.z = goal_pose.theta - self.current_pose.theta
        self.publisher.publish(tw)
        time.sleep(1)

def main():
    rclpy.init()

    turtle_to_goal = Turtle_to_Goal(sys.argv[1], sys.argv[2], sys.argv[3])
    rclpy.spin_once(turtle_to_goal)

    turtle_to_goal.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
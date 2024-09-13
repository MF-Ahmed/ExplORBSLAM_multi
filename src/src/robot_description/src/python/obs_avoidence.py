#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance:
    def __init__(self):
        rospy.init_node('obstacle_avoidance_node', anonymous=True)

        self.cmd_vel_pub = rospy.Publisher('/robot_1/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/robot_1/scan', LaserScan, self.scan_callback)

    def scan_callback(self, data):
        # Adjust these values based on your robot and environment
        min_distance = 0.5
        max_distance = 2.0

        # Determine if an obstacle is too close
        if min(data.ranges) < min_distance:
            rospy.loginfo(f"Obsticle detected at dictance {min_distance}")
            #self.avoid_obstacle()
        else:
            pass
            self.move_forward()

    def avoid_obstacle(self):
        # Stop the robot and turn away from the obstacle
        cmd_vel = Twist()
        cmd_vel.linear.x = 0.0
        cmd_vel.angular.z = 0.5  # Adjust the angular velocity as needed
        self.cmd_vel_pub.publish(cmd_vel)

    def move_forward(self):
        # Move the robot forward
        cmd_vel = Twist()
        cmd_vel.linear.x = 0.2  # Adjust the linear velocity as needed
        cmd_vel.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd_vel)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    obstacle_avoidance = ObstacleAvoidance()
    rospy.loginfo("obsticle avoidence node started")
    obstacle_avoidance.run()

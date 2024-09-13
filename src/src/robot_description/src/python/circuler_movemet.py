#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from hector_uav_msgs.srv import EnableMotors

#This node is served only for testing purpose so that the user doesn't have
# to manually control the leader by publishing velocity commands.
#The node publishes velocity messages to move the leader drone in
#a circular pattern. 
class Flight_tester:
    def __init__(self):
        rospy.init_node('flight_test_node', anonymous=True)
        self.vel_pub = rospy.Publisher("drone_1/cmd_vel", Twist, queue_size = 1, latch=True)
        self.motors_enable_srv = rospy.ServiceProxy('drone_1/enable_motors', EnableMotors)
        self.motors_enable_srv(True)
        self.cmd_task = rospy.Timer(rospy.Duration(1), self.command_loop)
        self.timestep = 0
    
    def command_loop(self, ev):
        rospy.loginfo("before if = {}.".format(self.timestep))
        if self.timestep < 20:
            rospy.loginfo("In if = {}.".format(self.timestep))
            vel_msg = Twist()
            vel_msg.linear.y = 0
            vel_msg.linear.x = 0
            vel_msg.linear.z = 0.2
            vel_msg.angular.z = 0
            self.vel_pub.publish(vel_msg)
        else:

            vel_msg = Twist()
            vel_msg.linear.y = 0
            vel_msg.linear.x = 0.1
            vel_msg.linear.z = 0
            vel_msg.angular.z = 0.1
            self.vel_pub.publish(vel_msg)
        self.timestep += 1

if __name__ == '__main__':
    try:
        tester = Flight_tester()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from hector_uav_msgs.srv import EnableMotors
import time

class LawnMowerControl:
    def __init__(self):
        rospy.init_node('lawn_mower_control', anonymous=False)
        self.rate = rospy.Rate(1)  # Adjust the rate according to your needs
        self.cmd_vel_pub = rospy.Publisher('/drone_0/cmd_vel', Twist, queue_size=10)

        self.motors_enable_srv = rospy.ServiceProxy('drone_0/enable_motors', EnableMotors)
        self.motors_enable_srv(True)
        # Enable motors        
        rospy.sleep(3)  # Wait for the drone to stabilize after enabling motors
        self.cmd_task = rospy.Timer(rospy.Duration(1), self.command_loop)
        self.timestep = 0
                 


    def command_loop(self, ev):
        rospy.loginfo(f"timestep = {self.timestep} \n")
        if self.timestep == 0:
            self.drone_takeoff(2)
        if self.timestep == 1:
            self.drone_hover(30)    

        self.timestep += 1    

        
    def drone_takeoff(self, val):
        for i in range(val):
            self.vel_msg = Twist()
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.x = 0
            self.vel_msg.linear.z = 0.5
            self.vel_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(self.vel_msg)
            time.sleep(1)

    def drone_hover(self, val):
        for i in range(val):
            self.vel_msg = Twist()
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.x = 0
            self.vel_msg.linear.z = 0.5
            self.vel_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(self.vel_msg)
            time.sleep(1)            

    def drone_rotateCCW(self,val):
        for i in range(val):            
            self.vel_msg = Twist()
            self.vel_msg.linear.x = 0.0
            self.vel_msg.linear.z = 0.0
            self.vel_msg.angular.z = self.vel_msg.angular.z 
            self.cmd_vel_pub.publish(self.vel_msg)
            time.sleep(1)
        

    def drone_rotateCW(self,val): 
        for i in range(val):    
            self.vel_msg = Twist()
            self.vel_msg.linear.x = 0.0
            self.vel_msg.linear.z = 0.0
            self.vel_msg.angular.z = -1.0
            self.cmd_vel_pub.publish(self.vel_msg)                  
            time.sleep(1)
    

    def drone_moveforward(self,val):
        for i in range(val):  
            self.vel_msg = Twist()
            self.vel_msg.linear.x = 0.5
            self.vel_msg.linear.z = 0.0
            self.vel_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(self.vel_msg)
            time.sleep(1)
                
    def drone_land(self,val):    
        for i in range(val):  
            self.vel_msg = Twist()
            self.vel_msg.linear.x = 0
            self.vel_msg.linear.z = -0.5
            self.vel_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(self.vel_msg)        
            time.sleep(1)


    def publish_velocity(self, linear_x, angular_z):
        twist_msg = Twist()
        twist_msg.linear.x = linear_x
        twist_msg.linear.y = 0
        twist_msg.angular.z = angular_z
        self.cmd_vel_pub.publish(twist_msg)


if __name__ == '__main__':
    try:
        lawn_mower_controller = LawnMowerControl()
        #lawn_mower_controller.move_lawn_mower_pattern()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logerr(str(e))
    finally:
        pass
        

#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from hector_uav_msgs.srv import EnableMotors

def takeoff():
    rospy.init_node('quadrotor_takeoff_node', anonymous=True)
    pose_publisher = rospy.Publisher('/drone_0/command/pose', PoseStamped, queue_size=10)
    motors_enable_srv = rospy.ServiceProxy('drone_0/enable_motors', EnableMotors)
    motors_enable_srv(True)
    # Enable motors        
    rospy.sleep(3)  # Wait for the drone to stabilize after enabling motors

    rospy.loginfo("Sending takeoff command to Hector Quadrotor...")
    

    takeoff_pose = PoseStamped()
    takeoff_pose.header.frame_id = 'drone_0/map'
    takeoff_pose.pose.position.x = 0.0
    takeoff_pose.pose.position.y = 0.0
    
    takeoff_pose.pose.position.z = 2.5  # Adjust the height for desired takeoff

    takeoff_pose.pose.orientation.w = 1.0 

    rate = rospy.Rate(1)  # Frequency of commands

    while not rospy.is_shutdown():
        takeoff_pose.header.stamp = rospy.Time.now()
        pose_publisher.publish(takeoff_pose)
        rate.sleep()

if __name__ == '__main__':
    try:
        takeoff()
    except rospy.ROSInterruptException:
        pass


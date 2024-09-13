#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion
from hector_uav_msgs.srv import EnableMotors

def send_goal():
    rospy.init_node('send_goal_node')
    motors_enable_srv = rospy.ServiceProxy('drone_0/enable_motors', EnableMotors)
    motors_enable_srv(True)
    # Enable motors        
    rospy.sleep(3)  # Wait for the drone to stabilize after enabling motors
    
    # Create a SimpleActionClient for the move_base action
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
##    
    # Wait for the action server to come up
    client.wait_for_server()
    rospy.loginfo("Got server!")

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'drone_1/map'  # Change 'map' to your desired frame_id
    goal.target_pose.header.stamp = rospy.Time.now()

    # Define the goal pose (position and orientation)
    goal.target_pose.pose.position = Point(x=0.0, y=0.0, z=3.5)  # Adjust the coordinates
   
    goal.target_pose.pose.orientation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)  # Adjust the orientation
    
    # Send the goal
    rospy.loginfo("Sending the Goal......")
    client.send_goal(goal)

    # Wait for the result, with a timeout of, for example, 60 seconds
    client.wait_for_result(rospy.Duration(60))

    if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Goal reached successfully!")
        rospy.loginfo(client.get_state())
        
    else:
        rospy.logwarn("Failed to reach the goal!")

if __name__ == '__main__':
    try:
        send_goal()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python3

import rospy
import actionlib
from hector_uav_msgs.msg import PoseAction, PoseGoal

def active_cb():
    rospy.loginfo("Goal is active.")

def feedback_cb(feedback):
    rospy.loginfo("Received feedback: %s", feedback)

def done_cb(status, result):
    if status == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Action finished successfully. Result: %s", result)
    else:
        rospy.loginfo("Action did not finish successfully. Status: %s", status)

def send_pose_goal():
    rospy.init_node('pose_client')
    
    # Create a SimpleActionClient
    pose_client = actionlib.SimpleActionClient('drone_0/action/pose', PoseAction)

    rospy.loginfo("Waiting for action server to start.")
    # wait for the action server to start
    pose_client.wait_for_server()
    rospy.loginfo("Action server started, sending goal.")

    # Create a PoseGoal
    pose_goal = PoseGoal()
    # You may need to set the fields of pose_goal as per your requirements
    pose_goal.target_pose.pose.position.z = 1.0
    pose_goal.target_pose.pose.position.x = 0.0
    pose_goal.target_pose.pose.position.y = 0.0
    
    pose_goal.target_pose.header.frame_id = "drone_0/world"
    pose_goal.target_pose.pose.orientation.x = 0.0    
    pose_goal.target_pose.pose.orientation.y = 0.0
    pose_goal.target_pose.pose.orientation.z = 0.0
    pose_goal.target_pose.pose.orientation.w = 1.0

    # Send the goal to the action server
    pose_client.send_goal(pose_goal, done_cb=done_cb, active_cb=active_cb, feedback_cb=feedback_cb)

    # Wait for the result with a timeout of 30 seconds
    pose_client.wait_for_result(rospy.Duration(10.0))

    # Check the final state of the action
    if pose_client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Action finished successfully.")
    else:
        rospy.loginfo("Action did not finish before the timeout.")

if __name__ == '__main__':
    try:
        send_pose_goal()
    except rospy.ROSInterruptException:
        pass

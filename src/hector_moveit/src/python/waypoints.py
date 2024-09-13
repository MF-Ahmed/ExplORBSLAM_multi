#!/usr/bin/env python3

import rospy
import moveit_commander
from geometry_msgs.msg import Pose
import sys

def move_to_goal(goal_pose):
    rospy.init_node('moveit_goal_sender', anonymous=True)
    
    # Initialize MoveIt Commander
    moveit_commander.roscpp_initialize(sys.argv)
    
    # Instantiate a RobotCommander object
    robot = moveit_commander.RobotCommander()
    
    # Instantiate a PlanningSceneInterface object
    scene = moveit_commander.PlanningSceneInterface()
    
    # Instantiate a MoveGroupCommander object for the drone
    group_name = "drone_moveit"  # Replace with your MoveIt planning group
    move_group = moveit_commander.MoveGroupCommander(group_name)
    
    # Set the planning time
    move_group.set_planning_time(5)
    
    # Set the goal position and orientation
    move_group.set_pose_target(goal_pose)
    
    # Plan the trajectory
    plan = move_group.go(wait=True)
    
    if plan:
        print("Movement to goal position successful!")
    else:
        print("Failed to reach the goal position.")
    
    # Clean up MoveIt Commander
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        goal_pose = Pose()
        # Define your goal position and orientation here
        # For example:
        # goal_pose.position.x = 1.0
        # goal_pose.position.y = 0.5
        # goal_pose.position.z = 0.8
        # goal_pose.orientation.w = 1.0
        
        move_to_goal(goal_pose)
    except rospy.ROSInterruptException:
        pass

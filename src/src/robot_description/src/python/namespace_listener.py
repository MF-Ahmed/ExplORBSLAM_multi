#!/usr/bin/env python3
import rospy
from rosgraph_msgs.msg import Log

def callback(msg):
    # Extract the namespace from the log message
    namespace = msg.name
    print("Node in namespace:", namespace)

if __name__ == '__main__':
    # Initialize the ROS node
    rospy.init_node('namespace_listener', anonymous=True)

    # Define a subscriber to listen to the /rosout_agg topic
    rospy.Subscriber('/rosout_agg', Log, callback)

    # Spin to keep the script alive and receive messages
    rospy.spin()

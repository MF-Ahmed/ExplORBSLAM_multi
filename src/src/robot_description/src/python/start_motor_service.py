#!/usr/bin/env python3

import rospy
from std_srvs.srv import SetBool

rospy.init_node('enable_motors_client')  # Initialize the ROS node

# Manually set the MD5 checksum for the service
enable_motors = rospy.ServiceProxy('/enable_motors', SetBool)
enable_motors._type = 'std_srvs/SetBool'
enable_motors._md5sum = '6a0b406242562fc416b2c9c8a3efb051'  # Replace with the correct MD5 checksum

try:
    # Call the service with the argument 'enable: true'
    response = enable_motors(True)
    if response.success:
        rospy.loginfo("Motors enabled successfully!")
    else:
        rospy.logwarn("Failed to enable motors.")
except rospy.ServiceException as e:
    rospy.logerr("Service call failed: %s" % e)

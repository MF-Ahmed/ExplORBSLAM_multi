#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CameraInfo


def callback(data, pub):
    # Process the received CameraInfo data as needed
    # For demonstration, we're just republishing it

    # Publish the received message to the remapped topic
    pub.publish(data)

def my_node():
    rospy.init_node('my_node', anonymous=True)

    # Specify the remapped topic name when creating the publisher
    pub = rospy.Publisher('/orb_slam2_rgbd/camera_info', CameraInfo, queue_size=10)

    # Subscribe to the original topic and pass the 'pub' variable to the callback
    rospy.Subscriber('/camera/rgb/camera_info', CameraInfo, callback, pub)

    rospy.spin()

if __name__ == '__main__':
    try:
        my_node()
    except rospy.ROSInterruptException:
        pass

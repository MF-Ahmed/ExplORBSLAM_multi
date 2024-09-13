#!/usr/bin/env python3

import rospy
import tf2_ros

def tf_frame_printer():
    rospy.init_node('tf_frame_printer', anonymous=True)

    # Create a TF2 buffer and listener
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)

    rate = rospy.Rate(1)  # 1 Hz, adjust the rate as needed

    while not rospy.is_shutdown():
        try:
            # Get the list of all available frames in the TF tree
            all_frames = tf_buffer.all_frames_as_string()
            rospy.loginfo("Available TF Frames: %s", all_frames)

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.logwarn("An error occurred while retrieving frame IDs.")

        rate.sleep()

if __name__ == '__main__':
    try:
        tf_frame_printer()
    except rospy.ROSInterruptException:
        pass

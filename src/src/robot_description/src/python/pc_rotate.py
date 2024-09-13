#!/usr/bin/env python3

import rospy
import pcl
import sensor_msgs.point_cloud2 as pc2
import numpy as np
from sensor_msgs.msg import PointCloud2
from pcl import PointCloud

def rotate_point_cloud(cloud):
    pc = PointCloud()
    points_list = list(pc2.read_points(cloud, field_names=("x", "y", "z"), skip_nans=True))  # Convert generator to list

    # Check if there are points in the list
    if not points_list:
        return

    # Extract the number of points in the point cloud
    num_points = len(points_list)

    # Rotate the point cloud by 90 degrees around the Z-axis
    # In this example, we rotate around the Z-axis by 90 degrees.
    # You can modify this rotation according to your needs.
    theta = -np.pi/2   # 90 degrees in radians

    rotation_matrix_z = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0],
                                [0, 0, 1]])
    
    rotation_matrix_x = np.array([[1, 0, 0],
                                [0, np.cos(theta), -np.sin(theta)],
                                [0, np.sin(theta), np.cos(theta)]])
    
    rotation_matrix_y = np.array([[np.cos(theta), 0, np.sin(theta)],
                            [0, 1, 0],
                            [-np.sin(theta), 0, np.cos(theta)]])




    # Cast the points to 'float32' before applying rotation
    points_array = np.array(points_list, dtype=np.float32)
    
    # Perform the rotation
    rotated_points = np.dot(points_array[:, :3], rotation_matrix_x.T)

    # Create a new PointCloud with the rotated points
    rotated_pc = PointCloud()
    
    # Explicitly cast the NumPy array to 'float32' to avoid data type mismatch
    rotated_pc.from_array(np.column_stack((rotated_points, points_array[:, 3:])).astype(np.float32))

    # Convert the PointCloud back to a PointCloud2 message
    rotated_cloud_msg = pc2.create_cloud_xyz32(cloud.header, rotated_pc.to_array()[:, :3])

    # Publish the rotated point cloud
    rotated_cloud_pub.publish(rotated_cloud_msg)

def point_cloud_callback(msg):
    rotate_point_cloud(msg)

if __name__ == "__main__":
    rospy.init_node("point_cloud_rotator")
    rospy.loginfo("point cloud rotate mode started")

    # Replace these with your input and output topic names
    input_topic = "/orb_slam3/all_points"
    output_topic = "/rotated_point_cloud"

    rotated_cloud_pub = rospy.Publisher(output_topic, PointCloud2, queue_size=10)
    rospy.Subscriber(input_topic, PointCloud2, point_cloud_callback)

    rospy.spin()

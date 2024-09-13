#!/usr/bin/env python

import rospy
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
import math
from Functions import *
from frontier_detector.msg import PointArray
from std_msgs.msg import Int32



# Global variables to store the latest markers from both topics
marker1_points = []
marker2_points = []

# Minimum distance threshold in grid cell coordinates
DISTANCE_THRESHOLD = 1.0  # Adjust as needed

def euclidean_distance_grid(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def callback_marker1(data):
    global marker1_points
    if data.type == Marker.POINTS or data.type == Marker.LINE_STRIP:
        marker1_points = [(int(point.x), int(point.y)) for point in data.points]
        #rospy.loginfo("/robot_0/filter/centroids with %d points", len(marker1_points))
    else:
        rospy.logwarn("/robot_0/filter/centroids of type %d, which is not POINTS or LINE_STRIP", data.type)

def callback_marker2(data):
    global marker2_points
    if data.type == Marker.POINTS or data.type == Marker.LINE_STRIP:
        marker2_points = [(int(point.x), int(point.y)) for point in data.points]
        #rospy.loginfo("/opencv_shapes_iou with %d points", len(marker2_points))
        filtered_points = process_markers()        
        publish_filtered_markers(filtered_points)
        publish_filtered_pointarray(filtered_points)
        #rospy.loginfo("Published %d filtered points as markers", len(filtered_points))
        #rospy.loginfo(f"which are {filtered_points}")

    else:
        rospy.logwarn("/opencv_shapes_iou  of type %d, which is not POINTS or LINE_STRIP", data.type)

def process_markers():
    global marker1_points, marker2_points
    distance_threshold = rospy.get_param('~distance_threshold', 5.0)
    if not marker1_points or not marker2_points:
        return []    
    all_points = marker1_points + marker2_points
    all_points_pub.publish(len(all_points))

    filtered_points = []
    for point in all_points:
        too_close = False
        for filtered_point in filtered_points:
            if euclidean_distance_grid(point, filtered_point) < distance_threshold:
                too_close = True
                break
        if not too_close:
            filtered_points.append(point)
    if len(filtered_points) == 0:
        rospy.logwarn(f"No filtered points found and robot points are : {marker1_points}, while iou map points are : {marker2_points} ")

    num_iou_filters_pub.publish(len(filtered_points))
    return filtered_points

def publish_filtered_markers(points):
    robot_ns = rospy.get_param('~robot_ns', "map")
    color0 =  rospy.get_param('~color0', 0)
    color1 =  rospy.get_param('~color1', 0)
    color2 =  rospy.get_param('~color2', 0)
    markerArray2 = MarkerArray()
    marker2=Marker()        
    #rospy.loginfo(f"points = {points}")
    for ip in range(0, len(points)):
        p_frontier = np.array([points[ip][0], points[ip][1]])                      
        marker2 = draw_marker(robot_ns+"/map", p_frontier[0], p_frontier[1], [float(color0),float(color1),float(color2)] ,"cube", 0.4,"iou")   
        marker2.id = ip       
        markerArray2.markers.append(marker2) 
    iou_frontiers_filtered_pub.publish(markerArray2) 

def publish_filtered_pointarray(points):
    point_array_msg = PointArray()
    for point in points:
        p = Point()
        p.x = point[0]
        p.y = point[1]
        p.z = 0  # Assuming z=0, adjust if necessary
        point_array_msg.points.append(p)
    iou_filters_pub.publish(point_array_msg)

def marker_listener():
    rospy.init_node('iou_filter_node', anonymous=True)
    robot_topic = rospy.get_param('~robot_topic', 'visualization_marker1')
    rospy.Subscriber(robot_topic, Marker, callback_marker1)
    map_topic= rospy.get_param('~map_topic', 'visualization_marker2')
    rospy.Subscriber(map_topic, Marker, callback_marker2)
    rospy.spin()

if __name__ == '__main__':
    global iou_frontiers_filtered_pub, all_points_pub, num_iou_filters_pub   
    iou_frontiers_filtered_pub = rospy.Publisher("iou/iou_frontiers_filtered", MarkerArray, queue_size=10)  
    iou_filters_pub = rospy.Publisher("iou/iou_frontiers_filtered/points", PointArray, queue_size=10) # the filtered points will eventually be used by the robots 
    num_iou_filters_pub = rospy.Publisher("iou/num_frontiers_filtered/", Int32, queue_size=10) # the number of filtered points will eventually be used by the robots 
    all_points_pub =  rospy.Publisher("iou/all_points/", Int32, queue_size=10) # the number of inital points before IOU filtering (robot+iou frontiers) 
    marker_listener()

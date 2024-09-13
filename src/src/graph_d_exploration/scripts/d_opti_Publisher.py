#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import tf
import heapq
import numpy as np
import dynamic_reconfigure.client

from numpy import array
from copy import deepcopy, copy
from scipy.spatial.transform import Rotation

from frontier_detector.msg import PointArray
from nav_msgs.msg import OccupancyGrid
from WeightedPoseGraph import WeightedPoseGraph
import time




"""
from sensor_msgs.msg import PointCloud2
"""
from graph_d_exploration.msg import PointArray, InfoMatrix, BoolArray
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Pose, PoseStamped, Point
from visualization_msgs.msg import MarkerArray, Marker
from actionlib_msgs.msg import GoalID
from orb_slam2_ros.msg import ORBState
from std_msgs.msg import Bool, Int32, Float32

from Functions import *
from Robot import Robot
from Map import Map
from WeightedPoseGraph import WeightedPoseGraph
from actionlib_msgs.msg import GoalStatusArray




frontiers_ = []
mapPoints_ = []
vertices_ = []
edges_ = []

# Getting the robot name
_name_ = Robot.__name__

is_lost_ = False
is_relocalizing_ = False

def mapPointsCallBack(data):
    global mapPoints_

    mapPoints_ = []
    temp = []
    for i in range(0, len(data.data)):
        if data.data[i] == -1.0:
            mapPoints_.append(temp)
            temp = []
        else:
            temp.append(data.data[i])



def vertexCallBack(data):
    global vertices_
    n = data.layout.dim[0].stride

    vertices_ = []
    for i in range(0, len(data.data), n):
        vertices_.append(data.data[i:i + n])


def edgesCallBack(data):
    global edges_
    n = data.layout.dim[0].stride

    edges_ = []
    for i in range(0, len(data.data), n):
        edges_.append(data.data[i:i + n])



def statusCallBack(data):
    """
    UNKNOWN=0, SYSTEM_NOT_READY=1, NO_IMAGES_YET=2, NOT_INITIALIZED=3, OK=4, LOST=5
    """
    global is_lost_, is_relocalizing_
    if data.state == 4:
        is_lost_ = False
        if is_relocalizing_:  # Stop trying to re localize if already OK
            msg = GoalID()
            #goal_cancel_pub_.publish(msg)
            is_relocalizing_ = False
            rospy.loginfo(rospy.get_name() + ': ORB-SLAM re localized successfully.')
    elif data.state == 5 and not is_relocalizing_:  # If lost, cancel current goal and send best re localization goal
        # Empty stamp, empty ID -> cancels ALL goals.
        # https://wiki.ros.org/actionlib/DetailedDescription
        msg = GoalID()
        #goal_cancel_pub_.publish(msg)
        is_lost_ = True
        rospy.logwarn_throttle(1, rospy.get_name() + ': ORB-SLAM status is LOST. Robot stopped.'
                                                     ' Sending robot to best re localization pose.')
    elif data.state == 0:  # Stop robot
        msg = GoalID()
        #goal_cancel_pub_.publish(msg)
        rospy.logwarn_throttle(1, rospy.get_name() + ': ORB-SLAM status is UNKNOWN. Robot stopped.')



def node():

    global saved_goals, frontiers_, merged_frontiers_, mapPoints_, vertices_, edges_, gridMap_data_, is_relocalizing_, robot_, rec_centroids_flag, rec_goal_flag, goal_coordinates, arrAck, status, server_status, markerArray_pu,marker_pub
    rospy.init_node('d_opti', anonymous=False)
    rospy.loginfo(rospy.get_name() + ": Initializing...")

    Nodename = "/d_opti_node: "

    #if SHOW_DEBUG_PATH_:
        #global marker_hallucinated_graph_pub_

    namespace = rospy.get_param('~namespace')

    global _namespace
    _namespace = namespace

    rate_hz = rospy.get_param('~rate', 100)
    rate_hz = 10
    use_gpu = rospy.get_param('~enable_gpu_comp', True)
    camera_type = rospy.get_param('~camera_type', 'rgbd')      

    rospy.Subscriber("/orb_slam2_" + camera_type + "/info/state", ORBState, statusCallBack)

    rospy.Subscriber("/orb_slam2_" + camera_type + "/vertex_list", Float64MultiArray, vertexCallBack)
    rospy.Subscriber("/orb_slam2_" + camera_type + "/edge_list", Float64MultiArray, edgesCallBack)
    rospy.Subscriber("/orb_slam2_" + camera_type + "/point_list", Float64MultiArray, mapPointsCallBack)

    # ORB-SLAM map
    map_ = Map(_namespace)
    # Create a publisher object
 
    d_opt_pub = rospy.Publisher("d_optimality_publisher/Dopt", Float32, queue_size=10)  

    # Set the loop rate
    rate = rospy.Rate(rate_hz)

    while not rospy.is_shutdown():
       # Get SLAM graph
        map_.setNodes(vertices_)
        map_.setEdges(edges_)
        map_.setMapPoints(mapPoints_)
        nodes, edges = map_.getNodesEdges()
        #rospy.loginfo(_namespace +f" No. of nodes = {len(nodes)} and edges is {len(edges)}")
        # Build nx graph              
        start = time.perf_counter()     
        G = WeightedPoseGraph(_namespace, nodes, edges, 'd_opt')
        end = time.perf_counter()
        rospy.loginfo(rospy.get_name() + f" D-optimality  = {G.get_opti_total()}, No. of nodes = {len(nodes)}, No. of edges = {len(edges)}")
        elapsed = end - start
        rospy.loginfo(f' {_namespace} Time taken for D-Optimality computation is: {elapsed:.6f} seconds')
        edge_d_opti = G.get_opti_total()
        d_opt_pub.publish(edge_d_opti)
        # Sleep to maintain the loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass

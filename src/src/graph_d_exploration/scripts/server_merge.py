#!/usr/bin/env python3

# s4636216@studenti.unige.it
# 2023, Università degli Studi di Genova, LS2N Ecole Centrale de Nantes

# This script is the server class. Its task is to take the centroids of all the
# agents, passed through a client, merge into a single list, delete the redundant
# points, if any, and pass the list back to the client

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Include modules~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import rospy
import actionlib
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import PointStamped

import itertools
from graph_d_exploration.msg import MergePointsAction, MergePointsResult, MergePointsFeedback
from constants import RADIUS_BORDER_, PERCENTAGE_UNKNOWN_, NUMBER_POINTS_LIST_, MIN_NUMBER_POINTS_LIST_
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Float32
import numba as nb
import numpy as np
import time



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Callbacks~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to store the map discovered by all the agents together
def map_occupation(msg):
    global merged_map
    merged_map = msg



@nb.jit(nb.boolean(nb.float64, nb.int64, nb.float64, nb.float64, nb.int8[:], nb.float64, nb.float64, nb.float64, nb.int64, nb.int64), nopython=True)
def is_near_border_jit(resolution, map_width, origin_x, origin_y, grid, point_x, point_y, percentage, radius, map_height):
    cell_x = int((point_x - origin_x) / resolution)
    cell_y = int((point_y - origin_y) / resolution)

    radius_in_cells = int(radius / resolution)
    cells_in_circumference = set()
    unknown_count = 0
    total_cells = 0

    for i in range(-radius_in_cells, radius_in_cells + 1):
        for j in range(-radius_in_cells, radius_in_cells + 1):
            cell_i = cell_x + i
            cell_j = cell_y + j
            if 0 <= cell_i < map_width and 0 <= cell_j < map_height:
                index = cell_i + cell_j * map_width
                cells_in_circumference.add((cell_i, cell_j))
                if grid[index] == -1:
                    unknown_count += 1
                total_cells += 1

    if total_cells != 0:
        unknown_percentage = (unknown_count / total_cells) * 100
        if unknown_percentage !=0:
            return unknown_percentage >= percentage
      

    return False


class MergePointsServer:
    def __init__(self, servername):
        global merged_map
        self.ServerName_ = '/'+servername+':'
       

        # Variable to store the merged map until that moment
        merged_map = OccupancyGrid()

        self.num_clients = 0
        self.r = rospy.Rate(0.5)  # Hz
        self.server = actionlib.SimpleActionServer(
            'merge_points', MergePointsAction, self.execute_callback, False)

        # Subscriber for the merged map
        rospy.Subscriber('/mergedmap', OccupancyGrid, map_occupation)       

        # Start the server
        self.server.start()
        rospy.loginfo(f'{self.ServerName_} Merge Points Server started')

    def execute_callback(self, goal):
        rospy.loginfo(f'{self.ServerName_}  ******  Received {len(goal.points)} points from client {goal.client_id} **** !!!')

        result = MergePointsResult()
        result.merged_points, result.percentage_used, result.radius_used = self.merge_points(goal.points)
        rospy.loginfo(f'{self.ServerName_} **** Merged {len(result.merged_points)} points from all clients with radius : {result.radius_used } and percentage : {result.percentage_used} **** ')

        self.server.set_succeeded(result)

        if self.server.is_preempt_requested():
            rospy.loginfo(f'{self.ServerName_} Goal was preempted')
            self.server.set_preempted()
        elif rospy.is_shutdown():
            rospy.loginfo(f'{self.ServerName_} Node was shutdown')
            self.server.set_aborted()

    def merge_points(self, list):
        rospy.loginfo(f'{self.ServerName_}  Merging points ...')
        feedback_msg = MergePointsFeedback()
        feedback_msg.percent_completed = 0
        
        
        if len(list) == 0:
                return [], PERCENTAGE_UNKNOWN_, RADIUS_BORDER_
        else:
            # remove duplicate points with the same x and y coordinates
            unique_points = []
            #rospy.loginfo(f'{self.ServerName_} list has  : {len(list)} which are {list}).')
            radius_ = RADIUS_BORDER_
            
            for point in list:               
                if self.is_near_border(point, merged_map, PERCENTAGE_UNKNOWN_, RADIUS_BORDER_):
                    # Check that the point has not alrady been chosen
                    if point not in unique_points:
                        unique_points.append(point)

                       
            radius_ = RADIUS_BORDER_
            percentage_ = PERCENTAGE_UNKNOWN_
            rospy.loginfo(f"{self.is_near_border(point, merged_map, PERCENTAGE_UNKNOWN_, RADIUS_BORDER_)}")

            rospy.loginfo(f'{self.ServerName_} Unique points found  : {len(unique_points)}).')

        #while(len(unique_points) <= MIN_NUMBER_POINTS_LIST_ or len(unique_points) >= NUMBER_POINTS_LIST_+1):

        while (len(unique_points) >= NUMBER_POINTS_LIST_+1):           
            rospy.logwarn(f'{self.ServerName_} Recomputing list since {len(unique_points)} points found).')
            _unique_points_ = unique_points
            unique_points = []
            # increase the radius to use fewer points
            if(radius_ <=0):
                radius_ =  RADIUS_BORDER_
            else:    
                radius_ -= 0.5

            #rospy.logwarn(f'{self.ServerName_} radius changed to  {radius_} ).')
            # Perform the computation with a higher percentage
            for point in _unique_points_:
                if self.is_near_border(point, merged_map, PERCENTAGE_UNKNOWN_, radius_):
                    if point not in unique_points:
                        unique_points.append(point)

        return unique_points, percentage_, radius_
    
    def transform_point_server(self, point, from_frame, to_frame):

        rospy.loginfo(f"point passed is {point} of type {type(point)}")

        # Ensure the point is a tuple or list
        if not (isinstance(point, tuple) or isinstance(point, list)):
            raise ValueError("Point must be a tuple or list containing two elements (x, y)")

        if len(point) != 2:
            raise ValueError("Point must contain exactly two elements (x, y)")
        
        # Create a tf2_ros Buffer and TransformListener
        tf_buffer = tf2_ros.Buffer()
        tf_listener = tf2_ros.TransformListener(tf_buffer)

        # Create a PointStamped object
        point_stamped = PointStamped()
        point_stamped.header.frame_id = from_frame
        point_stamped.header.stamp = rospy.Time.now()
        point_stamped.point.x = point[0]
        point_stamped.point.y = point[1]
        point_stamped.point.z = 0.0  # Assuming 2D points

        # Wait for the transform to become available
        try:
            # Adding some delay to ensure the transform listener has time to buffer transforms
            rospy.sleep(1.0)
            transform = tf_buffer.lookup_transform(to_frame, from_frame, rospy.Time(0), rospy.Duration(0.2))
            transformed_point = tf2_geometry_msgs.do_transform_point(point_stamped, transform)
            return (transformed_point.point.x, transformed_point.point.y)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            rospy.logerr(f"Transform error: {e}")
            return None

    def is_near_border(self, point, merged_map, percentage, radius):
        grid = np.array(merged_map.data, dtype=np.int8)
        resolution = merged_map.info.resolution if merged_map.info.resolution else 0.05
        map_width = merged_map.info.width
        map_height = merged_map.info.height
        origin_x = merged_map.info.origin.position.x
        origin_y = merged_map.info.origin.position.y     
      

        return is_near_border_jit(resolution, map_width, origin_x, origin_y, grid, point.x, point.y, percentage, radius, map_height)
    

        


if __name__ == '__main__':
    rospy.init_node('merge_points_server')
    server = MergePointsServer('merge_points_server')
    rospy.spin()

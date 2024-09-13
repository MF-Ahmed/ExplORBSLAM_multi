#!/usr/bin/env python3

# jplaced
# 2022, Universidad de Zaragoza

# The filter nodes receives the detected frontier points from all the detectors,
# filters the points, and passes them to the assigner node to command the robots.
# Filtration includes the deletion of old and invalid points, and it also
# discards redundant points.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Include modules~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import rospy
import tf
import dynamic_reconfigure.client

import numpy as np
from sklearn.cluster import MeanShift
from copy import copy, deepcopy
from scipy.spatial.transform import Rotation

from Functions import gridValue, createMarker, informationGain, informationGain_NUMBA, yawBtw2Points

from SimpleRobot import Robot

from frontier_detector.msg import PointArray
from visualization_msgs.msg import Marker

from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Point, PointStamped, Pose
from dynamic_reconfigure.server import Server
from std_msgs.msg import Int32

from frontier_detector.cfg import informationGainConfig

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Callbacks~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
map_data_ = OccupancyGrid()
collab_map_data_ = OccupancyGrid()
frontiers_ = []
f_timestamps_ = []
global_map_ = []
max_t_ = 0

INFORMATION_THRESHOLD_ = 0.45  # 0.5


def reconfigureCallback(config, level=0):
    global INFORMATION_THRESHOLD_
    rospy.logwarn_throttle(0.5, rospy.get_name() + """: Reconfigure Request! InfoGain threshold changed to: {ig_threshold}""".format(**config))
    INFORMATION_THRESHOLD_ = config["ig_threshold"]
    return config

# TODO check why the transformation looks into the future
def frontiersCallBack(data, args):
    global frontiers_, f_timestamps_

    transformed_point = args[0].transformPoint(args[1], data)
    x = np.array([transformed_point.point.x, transformed_point.point.y])
    x_t = data.header.stamp.to_sec()

    # Only add if not already there
    # Use temp variables to avoid errors due to global variables dimension (multiple ROS cb same time)
    temp_black = copy(x.tolist())
    temp_array = np.asarray(copy(frontiers_)).tolist()
    temp_time = copy(f_timestamps_)
    try:

        if len(temp_array) == len(temp_time):
            assert (len(temp_array) == len(temp_time))
            if temp_black in temp_array:
                repeated_idx = temp_array.index(temp_black)
                temp_time[repeated_idx] = x_t
            else:  # Otherwise, update timestamp
                temp_array.append(x)
                temp_time.append(x_t)

            # Delete too old points
            original_len = len(temp_array)
            assert original_len == len(temp_time)
            for ip in range(0, original_len):
                i = ip - original_len + len(temp_array)
                t_diff = np.abs(temp_time[i] - rospy.get_time())
                if t_diff > max_t_:
                    rospy.logdebug(rospy.get_name() + ': Deleted a frontier with timestamp diff = ' + str(t_diff))
                    del temp_array[i]
                    del temp_time[i]

            frontiers_ = copy(temp_array)
            f_timestamps_ = copy(temp_time)
            assert (len(frontiers_) == len(f_timestamps_))
    except:       
            rospy.logerr(rospy.get_name() + ': Frontier callback failed due to dimension mismatch of ' + str(
                len(temp_array) - len(temp_time)) + '. Skipping callback.')


def mapCallBack(data):
    global map_data_
    map_data_ = data
    


def mapCollabCallBack(data):
    global collab_map_data_
    collab_map_data_ = data


def globalMapCallback(data):
    global global_map_
    global_map_ = data


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Node~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def node():
    global frontiers_, map_data_, global_map_, max_t_
    rospy.init_node('filter', anonymous=False)
    rospy.loginfo("Filter node initialized")

    # Fetch all parameters
    map_topic = rospy.get_param('~map_topic')
    collab_map_topic = rospy.get_param('~collab_map_topic')
    threshold = rospy.get_param('~costmap_clearing_threshold', 70)
    # this can be smaller than the laser scanner range, >> smaller >>less computation time>> too small is not good,
    # info gain won't be accurate
    info_radius = rospy.get_param('~info_radius', 1.0)
    ig_th = rospy.get_param('~information_threshold', 1.0)
    goals_topic = rospy.get_param('~goals_topic')
    #n_robots = rospy.get_param('~n_robots', 1)
    namespace = rospy.get_param('~namespace')
    rate_hz = rospy.get_param('~rate', 1)
    robot_frame = rospy.get_param('~robot_frame')
    global_frame_ = rospy.get_param('~global_frame_')
    global_costmap_topic = rospy.get_param('~global_costmap_topic')
    use_gpu = rospy.get_param('~enable_gpu_comp', True)
    max_t_ = rospy.get_param('~maximum_time_f', 1.0)

    #rospy.loginfo(f"in filter.py map_topic = {map_topic},   collab_map_topic = {collab_map_topic},  namespace  = {namespace},  global_frame = {global_frame_}")

    srv = Server(informationGainConfig, reconfigureCallback)

    rate = rospy.Rate(rate_hz)
    rospy.Subscriber(map_topic, OccupancyGrid, mapCallBack)
    rospy.Subscriber(collab_map_topic, OccupancyGrid, mapCollabCallBack)

    global_map_ = OccupancyGrid()

    rospy.Subscriber(global_costmap_topic, OccupancyGrid, globalMapCallback)

    # Robot
    robot_name = namespace #+ str(n_robots)
    robot = Robot(robot_name)

    # Wait if map map has not been received yet
    while len(map_data_.data) < 1:
        rospy.loginfo(rospy.get_name() + ': Filter is waiting for the map.')
        rospy.sleep(0.5)
        pass

    # Wait if global costmap map has not been received yet
    while len(global_map_.data) < 1:
        
        rospy.loginfo(rospy.get_name() + ': Filter is waiting for the global costmap.')
        rospy.sleep(0.5)
        pass

    rospy.loginfo(rospy.get_name() + ': Filter received local and global costmaps.')

    global_frame = "/" + map_data_.header.frame_id


    tf_lstnr = tf.TransformListener()
    tf_lstnr.waitForTransform(global_frame[1:], robot_frame, rospy.Time(0), rospy.Duration(10))

    rospy.Subscriber(goals_topic, PointStamped, callback=frontiersCallBack, callback_args=[tf_lstnr, global_frame[1:]])

    # Publishers
    pub_frontiers = rospy.Publisher(rospy.get_name() + '/frontiers', Marker, queue_size=1)
    pub_centroids = rospy.Publisher(rospy.get_name() + '/centroids', Marker, queue_size=1)
    pub_len_centroids = rospy.Publisher(rospy.get_name() + '/len_centroids', Int32, queue_size=1)

    pub_filt_points = rospy.Publisher(rospy.get_name() + '/filtered_points', PointArray, queue_size=1)
    
    # Wait if no frontier is received yet
    counter = 0
    while len(frontiers_) < 1:
        if counter == 0:
            rospy.loginfo(rospy.get_name() + ': Filter is waiting for frontiers.')
            counter = 1

    rospy.loginfo(rospy.get_name() + ': Filter received frontiers.')

    points = createMarker(namespace, frame=map_data_.header.frame_id, ns="raw_frontiers", colors=[1.0, 1.0, 0.0], scale=0.2,
                          lifetime=1 / rate_hz)
    

    #points_clust = createMarker(namespace, frame=map_data_.header.frame_id, ns="filtered_frontiers", colors=[0.0, 1.0, 0.0],
    #                                lifetime=1 / rate_hz)



    if namespace  == 'robot_1':
        points_clust = createMarker(namespace, frame=map_data_.header.frame_id, ns="filtered_frontiers", colors=[50.0, 255, 0.0],lifetime=1 / rate_hz)            
    elif namespace  == 'robot_2':
        points_clust = createMarker(namespace, frame=map_data_.header.frame_id, ns="filtered_frontiers", colors=[100.0, 255, 100.0],lifetime=1 / rate_hz)
    elif namespace  == 'robot_3':
        points_clust = createMarker(namespace, frame=map_data_.header.frame_id, ns="filtered_frontiers", colors=[150.0, 255, 50.0],lifetime=1 / rate_hz)
    else: 
        points_clust = createMarker(namespace, frame=map_data_.header.frame_id, ns="filtered_frontiers", colors=[200.0, 255, 150.0],lifetime=1 / rate_hz)           




    p = Point()
    p.z = 0

    temp_point_stamped = PointStamped()
    temp_point_stamped.header.frame_id = map_data_.header.frame_id
    #rospy.loginfo(f"filter node I got temp_point_stamped.header.frame_id = {temp_point_stamped.header.frame_id}")
    temp_point_stamped.header.stamp = rospy.Time(0)
    temp_point_stamped.point.z = 0.0

    temp_point_array = PointArray()
    temp_point = Point()
    temp_point.z = 0.0

    client = dynamic_reconfigure.client.Client("filter", timeout=1, config_callback=reconfigureCallback)
    client.update_configuration({"ig_threshold": ig_th})

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    while not rospy.is_shutdown():

        # Check for the merged map availability
        if len(collab_map_data_.data) < 1:
            grid_map_ = map_data_
        else:
            grid_map_ = collab_map_data_
                
        # Clustering frontier points
        centroids = []
        front = deepcopy(frontiers_)

        if len(front) > 1:
            ms = MeanShift(bandwidth=1.5)
            ms.fit(front)
            centroids = ms.cluster_centers_
        elif len(front) == 1:  # If there is only one frontier no need for clustering
            centroids = front

        # frontiers_ = deepcopy(centroids)

        # Clearing frontiers
        original_centroids_len = len(centroids)
        for zp in range(0, original_centroids_len):
            z = zp - original_centroids_len + len(centroids)

            cond = False
            temp_point_stamped.point.x = centroids[z][0]
            temp_point_stamped.point.y = centroids[z][1]

            # Remove frontiers at ~(0,0) // probably errors of the RRT frontier detectors
            if abs(centroids[z][0]) + abs(centroids[z][1]) < .1:
                cond = True

            # Remove frontiers too close to the robot
            if not cond:
                distance = np.linalg.norm(robot.getPosition() - centroids[z])
                if distance < 0.25:
                    cond = True
                    # rospy.logwarn(rospy.get_name() + ": Will delete a centroid too close to the robot.")

            # Remove any frontier inside an occupied cell (threshold)
            if not cond:
                transformed_point = tf_lstnr.transformPoint(global_map_.header.frame_id, temp_point_stamped)
                x = np.array([transformed_point.point.x, transformed_point.point.y])
                gval = gridValue(global_map_, x)
                if gval >= threshold:
                    cond = True
                    # rospy.logwarn(rospy.get_name() + ': Will delete a frontier in occupied cell with value: '
                    #               + str(gval))

            # Remove frontiers with low information gain
            if not cond:
                if use_gpu:
                    ig = informationGain_NUMBA(grid_map_.info.resolution, grid_map_.info.width,
                                               grid_map_.info.origin.position.x,
                                               grid_map_.info.origin.position.y, np.array(grid_map_.data),
                                               centroids[z][0], centroids[z][1], 1.0)
                else:
                    ig = informationGain(grid_map_, [centroids[z][0], centroids[z][1]], 1.0)
                if ig < INFORMATION_THRESHOLD_:
                    cond = True
                    # rospy.logwarn(rospy.get_name() + ': Will delete a frontier with information gain = ' + str(ig))

            # Remove frontiers in unreachable locations
            if not cond:
                p_frontier = np.array([centroids[z][0], centroids[z][1]])
                pose_frontier = Pose()
                pose_frontier.position.x = p_frontier[0]
                pose_frontier.position.y = p_frontier[1]
                pose_frontier.position.z = 0
                # Add orientation at frontier's location
                R_frontier = Rotation.from_euler('xyz', [0., 0., yawBtw2Points(robot.getPosition(), p_frontier)],
                                                 degrees=False)
                q_frontier = R_frontier.as_quat()
                pose_frontier.orientation.x = q_frontier[0]
                pose_frontier.orientation.y = q_frontier[1]
                pose_frontier.orientation.z = q_frontier[2]
                pose_frontier.orientation.w = q_frontier[3]
                plan = robot.makePlan(robot.getPoseAsGeometryMsg(), pose_frontier)
                n_points = int(len(plan))
                if n_points == 0:
                    cond = True
                    # rospy.logwarn(rospy.get_name() + ': Will delete an unreachable frontier.')

            if cond:
                centroids = np.delete(centroids, z, axis=0)
                # rospy.logwarn(rospy.get_name() + ': Frontier deleted.')

        rospy.logdebug(rospy.get_name() + ': Frontier centroids len=' + str(len(centroids)) + ', frontiers len=' + str(
            len(front)) + '. Centroids: \n' + str(centroids))

        # Publishing
        temp_point_array.points = []
        pp = []
        if len(centroids) > 0:
            for i in centroids:
                temp_point.x = i[0]
                temp_point.y = i[1]
                temp_point_array.points.append(copy(temp_point))
                pp.append(copy(temp_point))

        points_clust.id += 1
        points_clust.points = pp
        points_clust.header.frame_id = global_map_.header.frame_id
        #rospy.loginfo(f"points_clust = {points_clust}")
        pub_centroids.publish(points_clust)
        pub_len_centroids.publish(len(points_clust.points))
        pub_filt_points.publish(temp_point_array)

        pp = []
        if len(front) > 0:
            for q in front:
                p.x = q[0]
                p.y = q[1]
                pp.append(copy(p))

        points.id += 1
        points.points = pp
        points.header.frame_id = global_map_.header.frame_id
        pub_frontiers.publish(points)

        rate.sleep()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass

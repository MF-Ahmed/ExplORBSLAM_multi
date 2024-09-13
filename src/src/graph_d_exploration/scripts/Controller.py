#!/usr/bin/env python3

# jplaced
# 2022, Universidad de Zaragoza

# This node receives target exploration goals, which are the filtered frontier
# points published by the filter node, and commands the robots accordingly. The
# controller node commands the robot through the move_base_node.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Include modules~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import rospy
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

from constants import WAIT_TO_REACHGOAL, DOPTI_MAX

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
from constants import DOPTI_MAX
from collections import Counter




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Callbacks~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variable to check the recevied merged frontiers
rec_centroids_flag = False
# Variable to check the recevied goal
rec_goal_flag = False

reloclaization_efforts = 0


gridMap_data_ = OccupancyGrid()
gridCollabMap_data_ = OccupancyGrid()
frontiers_ = []
mapPoints_ = []
vertices_ = []
edges_ = []
saved_goals = []
timer_callback_result = False

# Getting the robot name
_name_ = Robot.__name__

is_lost_ = False
is_relocalizing_ = False
goal_cancel_pub_ = rospy.Publisher('/move_base/cancel', GoalID, queue_size=10)

def frontiersCallBack(data):
    global frontiers_
    frontiers_ = []
    #rospy.loginfo(rospy.get_name() + " In frontiers callback")
    for point in data.points:
        frontiers_.append(array([point.x, point.y]))
        #rospy.loginfo(rospy.get_name() + f"frontiers_ = {frontiers_}")



def mapCallBack(data):
    global gridMap_data_
    gridMap_data_ = data


def mergedpointsCallback(data):
    global merged_frontiers_, rec_centroids_flag
    if not rec_centroids_flag:
        #rospy.loginfo(f"in merged points call back got : {merged_frontiers_} merged_frontiers_")
        merged_frontiers_ = [np.array([round(point.x, 2), round(point.y, 2)])
                             for point in data.points]
        rec_centroids_flag = True    


def serverBusyCallback(msg):
    global server_status
    server_status = msg.availability
    print(server_status)

def goalCallback(data):
    global rec_goal_flag, goal_coordinates
    goal_coordinates = []
    if not rec_goal_flag:
        goal_coordinates = data.points
        rec_goal_flag = True

def goalStatusCallback(msg):
    global status
    for goal_status in msg.status_list:
        status = goal_status.status

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
            goal_cancel_pub_.publish(msg)
            is_relocalizing_ = False
            rospy.loginfo(rospy.get_name() + ': ORB-SLAM re localized successfully.')
    elif data.state == 5 and not is_relocalizing_:  # If lost, cancel current goal and send best re localization goal
        # Empty stamp, empty ID -> cancels ALL goals.
        # https://wiki.ros.org/actionlib/DetailedDescription
        #msg = GoalID()
        #goal_cancel_pub_.publish(msg)
        is_lost_ = True
        rospy.logwarn_throttle(1, rospy.get_name() + ': ORB-SLAM status is LOST. Robot stopped.'
                                                     ' Sending robot to best re localization pose.')
    elif data.state == 0:  # Stop robot
        msg = GoalID()
        goal_cancel_pub_.publish(msg)
        rospy.logwarn_throttle(1, rospy.get_name() + ': ORB-SLAM status is UNKNOWN. Robot stopped.')


# Prototype of the callbacks used in an iterative way
def cncallbackReachedGoal(data, robot_id):
    global arrAck
    if not arrAck[robot_id]:
        arrAck[robot_id] = data.data

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to create callbacks and subscriber in a iterative way
# depending on the number of robots used
def create_callbacks(num_robots):
    callbacks = []
    for i in range(num_robots):
        def callback(data, i=i): return cncallbackReachedGoal(data, i)
        callbacks.append(callback)

    return callbacks




def timer_callback(event):    
    global timer_callback_result
    rospy.loginfo("Timer expired! Executing callback.")
    timer_callback_result = True



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Node~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
def node():
    global saved_goals, frontiers_, merged_frontiers_, mapPoints_, vertices_, edges_, gridMap_data_, is_relocalizing_
    global robot_, rec_centroids_flag, rec_goal_flag, goal_coordinates, arrAck, status, server_status, markerArray_pu,marker_pub 
    global is_lost_, is_relocalizing_, reloclaization_efforts, timer_callback_result
    rospy.init_node('decision_maker', anonymous=False)
    rospy.loginfo(rospy.get_name() + ": Initializing...")

    Nodename = "/Manager_node: "

    #if SHOW_DEBUG_PATH_:
        #global marker_hallucinated_graph_pub_

    # List for the merged frontiers
    merged_frontiers_ = []
    # List for the agents' goal
    goal_coordinates = []
    # Variable to take the goal status of the agent
    status = -1
    
    # Fetch all parameters
    map_topic = rospy.get_param('~map_topic')
    
    
    frontiers_topic = rospy.get_param('~frontiers_topic')
    n_robots = rospy.get_param('~n_robots', 1)
    namespace = rospy.get_param('~namespace')

    global _namespace
    _namespace = namespace

    rate_hz = rospy.get_param('~rate', 100)
    delay_after_assignment = rospy.get_param('~delay_after_assignment', 0.1)
    show_debug_path = rospy.get_param('~show_debug_path', False)
    exploring_time = rospy.get_param('~max_exploring_time', 9000)
    use_gpu = rospy.get_param('~enable_gpu_comp', True)
    camera_type = rospy.get_param('~camera_type', 'rgbd')
    color0 = rospy.get_param('~color0', 0)
    color1 = rospy.get_param('~color1', 0)
    color2 = rospy.get_param('~color2', 0)            


    rate = rospy.Rate(rate_hz)
    tf_listener = tf.TransformListener()

    rospy.Subscriber(_namespace+map_topic, OccupancyGrid, mapCallBack)
    
    rospy.Subscriber(frontiers_topic, PointArray, frontiersCallBack)
    rospy.Subscriber("/orb_slam2_" + camera_type + "/info/state", ORBState, statusCallBack)

    rospy.Subscriber("/orb_slam2_" + camera_type + "/vertex_list", Float64MultiArray, vertexCallBack)
    rospy.Subscriber("/orb_slam2_" + camera_type + "/edge_list", Float64MultiArray, edgesCallBack)
    rospy.Subscriber("/orb_slam2_" + camera_type + "/point_list", Float64MultiArray, mapPointsCallBack)


    # Creating the callbacks and the subcribers
    callbacks = create_callbacks(n_robots)
    # Create boolean variables to keep track of the robot reached or not the goal
    # Initialised to True since there is no goal to reach at the starting point of the program
    arrAck = [True] * n_robots

    # Array to take the server status
    server_status = [False] * n_robots

    # Create subscribers for each robot
    for i in range(n_robots):
        topic_name = f"/robot_{i}/reached_goal"
        message_type = Bool
        rospy.Subscriber(topic_name, message_type, callbacks[i])

    # Subscriber to retrieve the list of the merged points
    rospy.Subscriber("/merged_centroids", PointArray, mergedpointsCallback)
    # Subscriber to retrieve the list of the goals
    rospy.Subscriber("/chosen_points", PointArray, goalCallback)
    # SUbscriber to retrieve the result of the move base goal
    rospy.Subscriber("move_base/status", GoalStatusArray, goalStatusCallback)
    # SUbscriber to know if the central server is busy or not
    rospy.Subscriber("/central_sever_status", BoolArray, serverBusyCallback)

    # Publisher to pass the centroid of each agent to the manager node
    agent_centroids_publisher = rospy.Publisher(
        'agent_centroid', PointArray, queue_size=10)

    # Publisher to pass the matix [Reward, X, Y] to the manager node
    matrix_publisher = rospy.Publisher(
        'reward_information', InfoMatrix, queue_size=10)

    # Publisher to store if an agent has already reached the goal or not
    goal_reached_publisher = rospy.Publisher(
        'reached_goal', Bool, queue_size=10)
    
    # Publisher to inform if an agent has to get closer to a goal
    graph_start_publisher = rospy.Publisher(
        'graph_started', Bool, queue_size=10)
    
    # publisher to inform the server the robot-i is asking for the server
    request_server_publisher = rospy.Publisher('server_request', Bool, queue_size=10)

    #if SHOW_DEBUG_PATH_:
        #marker_hallucinated_graph_pub_ = rospy.Publisher(
            #'marker_hallucinated_graph', MarkerArray, queue_size=10)

    markerArray_pub = rospy.Publisher("visualization_markerArray/EntropyPath2", MarkerArray, queue_size=10)    
    saved_goalmarkerArray_pub = rospy.Publisher("visualization_markerArray/saved_goals", MarkerArray, queue_size=10)  
    marker_pub = rospy.Publisher("visualization_marker/EntropyPath", Marker, queue_size=10)
    d_opt_pub = rospy.Publisher("d_optimality_publisher/Dopt", Float32, queue_size=10)  
    num_reloc_efforts = rospy.Publisher("num_reloc_efforts", Int32, queue_size=10)  
    num_saved_goals = rospy.Publisher("num_saved_goals", Int32, queue_size=10)
   

    # Wait if no frontier is received yet
    #while len(frontiers_) < 1:
        #pass

    while len(gridMap_data_.data) < 1:
        pass

    rospy.loginfo(rospy.get_name() + ": Controller received map.")



    # Robot
    robot_name = _namespace #+ str(n_robots)
    robot_ = Robot(robot_name)

    if not robot_.sendGoal(robot_.getPosition()):
        robot_.cancelGoal()


    # ORB-SLAM map
    map_ = Map(_namespace)

    # Get ROS time in seconds
    t_0 = rospy.get_time()

    ig_changer = 0

    rospy.loginfo(rospy.get_name() + ": Initialized.")
    markerArray2 = MarkerArray()
    marker2=Marker()

    reloclaization_efforts=0
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    while not rospy.is_shutdown():

        rospy.sleep(1)
        #timer_duration = rospy.Duration(5)  # 5 seconds
         # Start the timer with the defined duration and the callback function
        #timer = rospy.Timer(timer_duration, timer_callback)

        #if timer_callback_result:
            #rospy.loginfo(rospy.get_name() + _namespace +"Timer callback returned True.")
        #else:
            #rospy.loginfo(rospy.get_name() + _namespace +" Timer callback returned False.")


        # Pub a True which means the robot is waiting for the server
        msg = Bool()
        msg = True
        request_server_publisher.publish(msg)

        # Check for the merged map availability
        if len(gridMap_data_.data) < 1:
            rospy.loginfo(rospy.get_name() + _namespace +" : map not avalible")            
        else:
            gridMap_ = gridMap_data_

        # Print log
        rospy.loginfo(rospy.get_name() + f' {robot_name}: is waiting for server and server status is {server_status}')
        # Check the server allows the robot to use it

        while not server_status[int(robot_name.split("_")[1])]:
            continue      

        rospy.loginfo(f'{robot_name}: processing points')    

        #if not is_lost_:  # ORB-SLAM OK
        centroids = deepcopy(frontiers_)
        tempPointArray = PointArray()
        tempPoint = Point()
        tempPoint.z = 0.0       

        # Reset the flag cause another previous publication may have triggered it
        rec_centroids_flag = False

        # Use the client to fuse the centroids and take the result
        for i in centroids:
            tempPoint.x = i[0]
            tempPoint.y = i[1]
            tempPointArray.points.append(copy(tempPoint))
        agent_centroids_publisher.publish(tempPointArray)

        # rospy.logwarn('published list for being merged')

        # Wait until the node recevied the merged frontiers
        while not rec_centroids_flag:
            continue
        # Reset the flag
        rec_centroids_flag = False

        # Print log
        centroids = merged_frontiers_
        rospy.loginfo(rospy.get_name() + ': received ' + str(len(merged_frontiers_)) + ' merged frontiers')

        # Replace the old centroids with the merged one
        centroids = merged_frontiers_

        originalLen = len(centroids)

        for ip in range(originalLen):
            i = ip - originalLen + len(centroids)
            if np.linalg.norm(robot_.getPosition() - centroids[i]) < 0.25:
                rospy.logwarn(f"{robot_name}: deleted a frontier too close to the robot.")
                del centroids[i]            

        n_centroids = len(centroids)
                
        if n_centroids <= 0:
            rospy.logwarn(rospy.get_name() + ": Got NO frontiers ")
            if robot_name == "robot_0":
                robot_.sendGoal(robot_.getPosition() + [0.2, 0.5])

            elif robot_name == "robot_1":
                robot_.sendGoal(robot_.getPosition() + [0.6, 0.3])
            else:
                robot_.sendGoal(robot_.getPosition() + [0.8, 0.2])      
                
            rospy.logwarn_throttle(0.5, rospy.get_name() + ": No frontiers.")
            if ig_changer < 10:
                ig_changer += 1
            client = dynamic_reconfigure.client.Client("/"+namespace+"/filter")
            if ig_changer > 10 and client.get_configuration(timeout=1)["ig_threshold"] != 0.1:
                client.update_configuration({"ig_threshold": 0.1})


        while vertices_ ==0 or edges_ ==0 or mapPoints_ == 0:
            rospy.logwarn(rospy.get_name() + f": Map Not started vertices:{len(vertices_)}, edges: {len(edges_)}, mapPoints: {len(mapPoints_)}")

        rospy.loginfo(rospy.get_name() + ": Map started")   

        # Get SLAM graph
        map_.setNodes(vertices_)
        map_.setEdges(edges_)
        map_.setMapPoints(mapPoints_)
        nodes, edges = map_.getNodesEdges()
        
        rospy.loginfo(rospy.get_name() + f" Nodes : {len(nodes)} and edges : {len(edges)}")
        # Build nx graph
        G = WeightedPoseGraph(_namespace, nodes, edges, 'd_opt')
        rospy.loginfo(rospy.get_name() + f"D-optimality from class  = {G.get_opti_total()}")
        edge_d_opti = G.get_opti_total()
        d_opt_pub.publish(edge_d_opti)

    

        # If no nodes (starting step) build graph with one edge at origin.
        n = float(G.getNNodes())
        m = float(G.getNEdges())

        if n < 1:
            G.graph.add_node(int(0), translation=[0, 0, 0], orientation=[0, 0, 0, 0])
            rospy.loginfo(rospy.get_name() + " :ORBSLAM Graph Not started yet")

        info_gain = []
        info_gain_saved_goals = []
        seen_cells_prec = []
        t_list= []
        closer_goal = False

        # If only one frontier no need to evaluate anything. Select that frontier
        if n_centroids == 1:
            rospy.logwarn(rospy.get_name() + ": Only one frontier detected. Selecting it.")
            info_gain.append(np.ndarray.flatten(np.random.rand(1, 1)))

        # If no edges (starting step) do not evaluate D-opt. Select random frontier
        if m < 1 or centroids == 0:
            rospy.logwarn("Graph not started yet, m < 1. Selecting goal +=[0.2,0.2].")
            closer_goal = True

        else:  # Otherwise
           
            rospy.loginfo(rospy.get_name() + ": Computing information gain of every frontier candidate.")
           
            all_frontiers = []
            unique_frontiers =[]
            if is_lost_:
                rospy.loginfo(rospy.get_name() + ": Robot is lost skippin the loop.")
                rospy.logwarn(rospy.get_name() + f": !!!!!!!!!!!!!!!!   ORBSALM Status is {is_lost_}. !!!!!!!!!!!!!!!!!!!!!!")
                for ip in range(0, n_centroids):
                    info_gain.append(0)
            else:

                for ip in range(0, n_centroids):
                    robotposxy = robot_.getPosition()      

                    # Get frontier goal
                    rospy.loginfo(rospy.get_name() + f"D-optimality from class  = {G.get_opti_total()}")
                    edge_d_opti = G.get_opti_total()
                    d_opt_pub.publish(edge_d_opti)             
                
                    p_frontier = np.array([centroids[ip][0], centroids[ip][1]])                     

                    entropy, markerArray, marker,distance =  compute_entropy(namespace+"/map", gridMap_,p_frontier[0],p_frontier[1],robotposxy) 
                    inv_entropy = 1 - entropy                  
                    markerArray_pub.publish(markerArray) 
                    marker_pub.publish(marker)
                    # Compute hallucinated pose graph
                    
                    if use_gpu:
                        seen_cells_pct = cellInformation_NUMBA(np.array(gridMap_.data),
                                                                gridMap_.info.resolution,
                                                                gridMap_.info.width,
                                                                gridMap_.info.origin.position.x,
                                                                gridMap_.info.origin.position.y,
                                                                p_frontier[0], p_frontier[1], 0.5)                

                    else:
                        seen_cells_pct = cellInformation(gridMap_, p_frontier, 0.5)
                    seen_cells_prec.append(seen_cells_pct)
                    hallucinated_path, G_frontier = G.hallucinateGraph(robot_name, robot_, map_, seen_cells_pct, p_frontier,True)

                    # Compute no. of spanning trees <=> D-opt(FIM)
                    n_frontier = float(G_frontier.getNNodes())

                    #rospy.loginfo(rospy.get_name() +  f" nodes {n_frontier}")              
                    if n_frontier > 0:
                        L_anchored = G_frontier.computeAnchoredL()              
                        _, log_determinant = np.linalg.slogdet(L_anchored.todense())                    

                        if log_determinant == -np.inf:
                            rospy.logwarn(rospy.get_name() + f" Log determinant is {log_determinant} applying regularization!")
                            # Matrix is singular or close to singular, apply regularization
                            epsilon = 1e-3  # Small positive value
                            modified_matrix = L_anchored.todense() + epsilon * np.eye(L_anchored.todense().shape[0])
                            determinant_sign, log_determinant = np.linalg.slogdet(modified_matrix)
                        #t_list.append(log_determinant)
                        #rospy.loginfo(rospy.get_name() +  f" t: {log_determinant} ")
                        n_spanning_trees = n_frontier ** (1 / n_frontier) * np.exp(log_determinant / n_frontier)

                        eta = count_digits_before_decimal(n_spanning_trees) 
                        ####eta_minus1 = 10**float(eta-2) # Will tune Later 
                        decay_factor = 0.1  # default 0.5 .. 0.05 not good(better coverage but less accuracy), 0.1 not good (less coverage but better accuracy)
                        gamma = np.exp(-(decay_factor) * distance)
                        #rospy.loginfo(rospy.get_name() + f" gamma  :  {gamma}")
                        #rospy.loginfo("distance = {}".format(distance))
                        #rospy.loginfo("eta_minus1 = {}".format(eta_minus1))
                        eta = 10**float(eta)
                        #rospy.loginfo(rospy.get_name() +  "eta = {}".format(eta))
                        #rospy.loginfo(rospy.get_name() +  "========= inv_entropy of forntier = {} is {}".format(ip,inv_entropy)) 
                        entropy = inv_entropy*eta                    
                        #rospy.loginfo(rospy.get_name() +  "========= No. of Spanning trees of forntier = {} are {}".format(ip,n_spanning_trees))  
                        #rospy.loginfo(rospy.get_name() +  "========= inv_entropy*eta of forntier = {} is {}".format(ip,entropy))  
                        #rospy.loginfo(rospy.get_name() +  "========= Distance of forntier No. = {} at {} are {} with gamma = {} ".format(ip, p_frontier, distance,gamma))                                             
                        info_gain.append(n_spanning_trees + entropy + gamma)
                        #rospy.loginfo(rospy.get_name() +  f"=========  and infogain of {ip} : {info_gain[ip]}")                                                                                     
                        #infoGain.append(spann)
                        #info_gain.append(n_spanning_trees)
                    
        # Goal sender
        if robot_.getState() == 1:
            rospy.logwarn(rospy.get_name() + ": Robot is not available.")
            
        elif closer_goal:            
            if not robot_.sendGoal(robot_.getPosition() + [0.2, 0.2]):
                robot_.cancelGoal()

        #elif single_goal:
            #rospy.loginfo(rospy.get_name() + ": " + format(robot_name) + " assigned to " + format(centroids[0]))
            #robot_.sendGoal(centroids[0], True)
        else: 

            info_gain_record = []
            centroid_record = []
            seen_cells_perc_record = []
            

            rospy.loginfo(rospy.get_name() + f": got {len(centroids)} centroids for processing .")
            rospy.loginfo(f"info_gain = {info_gain}")

            for ip in range(0, len(centroids)):                               
                    info_gain_record.append(info_gain[ip])
                    centroid_record.append(centroids[ip])
                #seen_cells_perc_record.append(seen_cells_prec[ip])


            #winner_id = info_gain_record.index(np.max(info_gain_record))
            
            rospy.loginfo(rospy.get_name() +" Information record: [Reward, X, Y] \n" +
                        format(np.column_stack((info_gain_record, centroid_record)))) #, seen_cells_perc_record))))
            
            # Reset the flag cause another previous publication may have triggered it
            rec_goal_flag = False

            # Crete a matrix by putting the nx1 array and the nx2 matrix alongside
            matrix = np.column_stack((info_gain_record, centroid_record))
            matrix_msg = InfoMatrix()
            matrix_msg.rows = len(info_gain_record)
            # flatten the matrix and store the data in the message
            matrix_msg.data = matrix.flatten().tolist()
            # Publish the list on the topic
            matrix_publisher.publish(matrix_msg)            
            # Wait until the goal is published
            while not rec_goal_flag:
                continue
            # Reset the flag
            rec_goal_flag = False 
            rospy.loginfo(rospy.get_name() + ": ! goal recieved ! \n")
            #rospy.loginfo(rospy.get_name() + f" D-optimality  = {G.get_opti_total()}, No. of nodes = {len(nodes)}, No. of edges = {len(edges)}")
            edge_d_opti = G.get_opti_total()
            d_opt_pub.publish(edge_d_opti)


            if goal_coordinates != [] :
                rospy.loginfo(rospy.get_name() + ": GOAL COORDINATES RECEIVED \n" + str(goal_coordinates))
                
                # Print log
                #rospy.loginfo('Received goals. Extracting the correct one')
                # The goal position is the first for each robot cause the server now
                # gives one goal after each execution casue only one robot at time 
                # is using it

                selected_point = goal_coordinates[0]

                # Fill the array for the goal coordinates
                _goal_ = []
                _goal_.append(selected_point.x)
                _goal_.append(selected_point.y)
               
                winner_frontier_marker = goal_marker(namespace, [float(color0),float(color1),float(color2)], _goal_[0] ,_goal_[1], "sphere",0.8, 2.0)             
                marker_pub.publish(winner_frontier_marker)

                saved_goals.append(_goal_)
                rospy.loginfo(rospy.get_name() + f" saved_goals = {saved_goals}")
                num_saved_goals.publish(len(saved_goals))
                
                n_saved_goals =  len(saved_goals)  
                for ip in range(0, n_saved_goals):
                    robotposxy = robot_.getPosition()  
                    # Get frontier goal
                    p_saved_goals = np.array([saved_goals[ip][0], saved_goals[ip][1]])
                    #rospy.loginfo(rospy.get_name() + f" p_saved_goals = {p_saved_goals}")                       
                    marker2 = draw_marker(namespace+"/map", p_saved_goals[0], p_saved_goals[1], [float(color0),float(color1),float(color2)],"sphere",0.4,"saved_goals")   
                    marker2.id = ip       
                    markerArray2.markers.append(marker2)      
                    
                saved_goalmarkerArray_pub.publish(markerArray2) 
                rospy.loginfo(rospy.get_name() + " Saved goals marker published ")

     
                rospy.loginfo(f"{robot_name} assigned to {str(_goal_)}")
                initial_plan_position = robot_.getPosition()

                 
                #if not robot_.sendGoal(_goal_, WAIT_TO_REACHGOAL):
                    #robot_.cancelGoal()

                if not robot_.sendGoal(_goal_):
                    robot_.cancelGoal()
                          
                if (len(saved_goals)>3 and is_lost_ ) or (len(saved_goals)>3 and edge_d_opti>DOPTI_MAX) :
                    n_saved_goals =  len(saved_goals)   
                    edge_d_opti = G.get_opti_total()
                    d_opt_pub.publish(edge_d_opti) 

                    rospy.logwarn(rospy.get_name() + f" !! D-Opti: {edge_d_opti} exceeded  limit of: {DOPTI_MAX} robot SLAM status : {is_lost_} relaying robot to previously selected goal !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")                   
                    for ip in range(0, n_saved_goals):
                        robotposxy = robot_.getPosition()  
                        # Get frontier goal
                        p_saved_goals = np.array([saved_goals[ip][0], saved_goals[ip][1]])
                        #rospy.loginfo(rospy.get_name() + f" p_saved_goals = {p_saved_goals}")                                               
                        saved_goals_entropy, _, _, _ =  compute_entropy(namespace+"/map", gridMap_,p_saved_goals[0],p_saved_goals[1],robotposxy)     
                        saved_goals_inv_entropy = 1 - saved_goals_entropy     
                        info_gain_saved_goals.append(saved_goals_inv_entropy)    
                 
                    rospy.loginfo(rospy.get_name() + f" info_gain_saved_goals  = {info_gain_saved_goals}")                    
                    max_ = info_gain_saved_goals.index(max(info_gain_saved_goals))

                    winner_goal  = np.array([saved_goals[max_][0], saved_goals[max_][1]]) 
                    rospy.loginfo(rospy.get_name() + f": Saved frontier winner_goal = {winner_goal}")

                    
                    if not robot_.sendGoal(winner_goal):
                        robot_.cancelGoal()
                    reloclaization_efforts += 1 
                    num_reloc_efforts.publish(reloclaization_efforts)
                    markerArray2 = MarkerArray()
                    marker2=Marker()
                    saved_goals.append([winner_goal[0],winner_goal[1]])


                    #rospy.loginfo(rospy.get_name() + f": markerArray2 = {markerArray2}")                        
                    
                else:
                    pass      
            

                # Print log
                rospy.loginfo(f"{robot_name} reached {str(_goal_)}")

                # If plan fails near to starting position, send new goal to the next best frontier
                if robot_.getState() != 3 and n_centroids != 1:
                    norm = np.linalg.norm(
                        robot_.getPosition() - initial_plan_position)
                    if norm <= 2.0:
                        try:
                            second_max = heapq.nlargest(2, info_gain_record)[1]
                            winner_id = info_gain_record.index(second_max)
                            rospy.logwarn(
                                f"Goal aborted near previous pose (eucl = {str(norm)}). Sending new goal to: {str(_goal_)}"
                            )
                            if not robot_.sendGoal(_goal_):
                                robot_.cancelGoal()
                        finally:
                            pass
                    else:
                        rospy.logwarn(
                            f"Goal aborted away from previous pose (eucl = {str(norm)}). Recomputing."
                        )

                rospy.sleep(delay_after_assignment)

            else:
                rospy.logwarn(f"{robot_name} did not receive any goal")                                                  
                    
            # If plan fails near to starting position, send new goal to the next best frontier

        rate.sleep()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass

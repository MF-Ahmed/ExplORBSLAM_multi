#!/usr/bin/env python3

import rospy
import os
import matplotlib.pyplot as plt
import numpy as np
import time
import psutil
import pynvml
import GPUtil
from graph_d_exploration.msg import PointArray
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Int32, Float32, Float64 
from rosgraph_msgs.msg import Log

USE_GPU_ = 1

# Get the absolute path to the package
package_path = os.path.dirname(os.path.abspath(__file__))

# File for the values of the environment
filename_area = os.path.join(package_path, '..', 'config', 'filename_area.txt')
# Key to look or the specific environment
# key = 'warehouse'
key = 'warehouse'

# Retrieve the number of agents as parameter
# Modify the value before running
num_robots = rospy.get_param('~num_robots', 2)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Callbacks~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to store the map discovered by all the agents together
def map_occupation(msg):
    global merged_x, merged_y
    area = map_area(msg)

    # Append the current time and area to the respective arrays
    merged_x.append(rospy.Time.now().to_sec())
    merged_y = np.append(merged_y, area)

def intersection_areaCallback(msg):
    global intersection_x, intersection_y
    # Append the current time and area to the respective arrays
    intersection_x.append(rospy.Time.now().to_sec())
    intersection_y = np.append(intersection_y,msg.data)


def iou_scoreCallback(msg):
    global iou_score_x, iou_score_y
    # Append the current time and area to the respective arrays
    iou_score_x.append(rospy.Time.now().to_sec())
    iou_score_y = np.append(iou_score_y,msg.data)

def union_areaCallback(msg):
    global union_area_x, union_area_y
    # Append the current time and area to the respective arrays
    union_area_x.append(rospy.Time.now().to_sec())
    union_area_y = np.append(union_area_y,msg.data)

def mergedmapClearAreaCallback(msg):
    global MMClear_area_x, MMClear_area_y
    # Append the current time and area to the respective arrays
    MMClear_area_x.append(rospy.Time.now().to_sec())
    MMClear_area_y = np.append(MMClear_area_y,msg.data)
    


def mergedmapObsCallback(msg):
    global MMObs_area_x, MMObs_area_y
    # Append the current time and area to the respective arrays
    MMObs_area_x.append(rospy.Time.now().to_sec())
    MMObs_area_y = np.append(MMObs_area_y,msg.data)



def mergedmapTotAreaCallback(msg):
    global MM_area_x, MM_area_y
    # Append the current time and area to the respective arrays
    MM_area_x.append(rospy.Time.now().to_sec())
    MM_area_y = np.append(MM_area_y,msg.data)




def iou_opencvCallback(msg):
    global iou_num_frontiers_opncv_x, iou_num_frontiers_opncv_y
    # Append the current time and area to the respective arrays
    iou_num_frontiers_opncv_x.append(rospy.Time.now().to_sec())
    iou_num_frontiers_opncv_y = np.append(iou_num_frontiers_opncv_y,msg.data)

###################################################################
def num_saved_goalsCallback0(msg):
    global saved_goals0_x, saved_goals0_y
    # Append the current time and area to the respective arrays
    saved_goals0_x.append(rospy.Time.now().to_sec())
    saved_goals0_y = np.append(saved_goals0_y,msg.data)


def num_saved_goalsCallback1(msg):
    global saved_goals1_x, saved_goals1_y
    # Append the current time and area to the respective arrays
    saved_goals1_x.append(rospy.Time.now().to_sec())
    saved_goals1_y = np.append(saved_goals1_y,msg.data)


def num_saved_goalsCallback2(msg):
    global saved_goals2_x, saved_goals2_y
    # Append the current time and area to the respective arrays
    saved_goals2_x.append(rospy.Time.now().to_sec())
    saved_goals2_y = np.append(saved_goals2_y,msg.data)



#########################################################################

def num_reloc_effortsCallback0(msg):
    global num_reloc_efforts0_x, num_reloc_efforts0_y
    # Append the current time and area to the respective arrays
    num_reloc_efforts0_x.append(rospy.Time.now().to_sec())
    num_reloc_efforts0_y = np.append(num_reloc_efforts0_y,msg.data)



def num_reloc_effortsCallback1(msg):
    global num_reloc_efforts1_x, num_reloc_efforts1_y
    # Append the current time and area to the respective arrays
    num_reloc_efforts1_x.append(rospy.Time.now().to_sec())
    num_reloc_efforts1_y = np.append(num_reloc_efforts1_y,msg.data)


def num_reloc_effortsCallback2(msg):
    global num_reloc_efforts2_x, num_reloc_efforts2_y
    # Append the current time and area to the respective arrays
    num_reloc_efforts2_x.append(rospy.Time.now().to_sec())
    num_reloc_efforts2_y = np.append(num_reloc_efforts2_y,msg.data)

###################################################################

def DoptCallback0(msg):
    global Dopt0_x, Dopt0_y
    # Append the current time and area to the respective arrays
    Dopt0_x.append(rospy.Time.now().to_sec())
    Dopt0_y = np.append(Dopt0_y,msg.data)

def DoptCallback1(msg):
    global Dopt1_x, Dopt1_y
    # Append the current time and area to the respective arrays
    Dopt1_x.append(rospy.Time.now().to_sec())
    Dopt1_y = np.append(Dopt1_y,msg.data)    


def DoptCallback2(msg):
    global Dopt2_x, Dopt2_y
    # Append the current time and area to the respective arrays
    Dopt2_x.append(rospy.Time.now().to_sec())
    Dopt2_y = np.append(Dopt2_y,msg.data)    


# Callback to get the automatically generated map
def generated_map_callback(msg):
    global generated_map_area
    # Compute the total area of the environment
    generated_map_area = map_area(msg)

# Callback to get the total number of points passed to the server
def totalPointsCallback(data):
    global total_num_points, num_goals
    total_num_points.append(data.data)
    num_goals.append(len(total_num_points))

# Callback to get the actual number of points used for the reward computations
def actualPointsCallback(data):
    global actual_num_points
    actual_num_points.append(len(data.points))

def cpugpuCallback(msg):
    # Store also CPU and GPU usage
    monitor_cpu_usage()

    # Collect GPU data only if it is used
    if USE_GPU_:
        monitor_gpu_usage()

def radiusValueCallback(msg):
    # Store the radius value
    global radius_values
    radius_values.append(round(msg.data, 2))


def percentageValueCallback(msg):
    # Store the percentage value
    global percentage_values
    percentage_values.append(round(msg.data, 2))




def all_points0Callback(msg):
    global all_points0_x, all_points0_y
    # Append the current time and area to the respective arrays
    all_points0_x.append(rospy.Time.now().to_sec())
    all_points0_y = np.append(all_points0_y,msg.data)
        

def all_points1Callback(msg):
    global all_points1_x, all_points1_y
    # Append the current time and area to the respective arrays
    all_points1_x.append(rospy.Time.now().to_sec())
    all_points1_y = np.append(all_points1_y,msg.data)



def all_points2Callback(msg):
    global all_points2_x, all_points2_y
    # Append the current time and area to the respective arrays
    all_points2_x.append(rospy.Time.now().to_sec())
    all_points2_y = np.append(all_points2_y,msg.data)




def num_frontiers_filtered0Callback(msg):
    global num_frontiers_filtered0_x, num_frontiers_filtered0_y
    # Append the current time and area to the respective arrays
    num_frontiers_filtered0_x.append(rospy.Time.now().to_sec())
    num_frontiers_filtered0_y = np.append(num_frontiers_filtered0_y,msg.data)


def num_frontiers_filtered1Callback(msg):
    global num_frontiers_filtered1_x, num_frontiers_filtered1_y
    # Append the current time and area to the respective arrays
    num_frontiers_filtered1_x.append(rospy.Time.now().to_sec())
    num_frontiers_filtered1_y = np.append(num_frontiers_filtered1_y,msg.data)


def num_frontiers_filtered2Callback(msg):
    global num_frontiers_filtered2_x, num_frontiers_filtered2_y
    # Append the current time and area to the respective arrays
    num_frontiers_filtered2_x.append(rospy.Time.now().to_sec())
    num_frontiers_filtered2_y = np.append(num_frontiers_filtered2_y,msg.data)



def relocCallback0(msg):
    global reloc0_x, reloc0_y
    # Append the current time and area to the respective arrays
    reloc0_x.append(rospy.Time.now().to_sec())
    reloc0_y = np.append(reloc0_y,msg.data)


def relocCallback1(msg):
    global reloc1_x, reloc1_y
    # Append the current time and area to the respective arrays
    reloc1_x.append(rospy.Time.now().to_sec())
    reloc1_y = np.append(reloc1_y,msg.data)


def relocCallback2(msg):
    global reloc2_x, reloc2_y
    # Append the current time and area to the respective arrays
    reloc2_x.append(rospy.Time.now().to_sec())
    reloc2_y = np.append(reloc2_y,msg.data)    



#########################################################

def totareaCallback0(msg):
    global totarea0_x, totarea0_y
    # Append the current time and area to the respective arrays
    totarea0_x.append(rospy.Time.now().to_sec())
    totarea0_y = np.append(totarea0_y,msg.data)

def totareaCallback1(msg):
    global totarea1_x, totarea1_y
    # Append the current time and area to the respective arrays
    totarea1_x.append(rospy.Time.now().to_sec())
    totarea1_y = np.append(totarea1_y,msg.data)

def totareaCallback2(msg):
    global totarea2_x, totarea2_y
    # Append the current time and area to the respective arrays
    totarea2_x.append(rospy.Time.now().to_sec())
    totarea2_y = np.append(totarea2_y,msg.data)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to compute the total amount of area discovered
def map_area(map):
    discovered_cells = sum(1 for cell in map.data if (cell == 0 or cell == 100))
    return round(discovered_cells * (map.info.resolution ** 2), 2)


def monitor_cpu_usage():
    global cpu_time, cpu_percentages

    cpu_percent = psutil.cpu_percent(0.5)
    cpu_time.append(rospy.Time.now().to_sec())
    cpu_percentages = np.append(cpu_percentages, cpu_percent)


def monitor_gpu_usage():
    global gpu_time, gpu_percentages, gpu_memory

    gpu_list = GPUtil.getGPUs()
    for gpu in gpu_list:
        gpu_percent = float(gpu.load)*100
        gpu_mem = float(gpu.memoryUtil)*100
        gpu_time.append(rospy.Time.now().to_sec())
        gpu_percentages = np.append(gpu_percentages, gpu_percent)
        gpu_memory = np.append(gpu_memory, gpu_mem)


# Function to save the data for each simulation
def save_simulation_data(simulation_id):
    data = {
        'merged_x': merged_x,
        'merged_y': merged_y,
        'iou_area_time': intersection_x,
        'iou_area_value': intersection_y,
        'iou_score_time': iou_score_x,
        'iou_score_value': iou_score_y,
        'union_area_time': union_area_x,
        'union_area_value': union_area_y,
        'mergedMap_clearArea_time': MMClear_area_x,
        'mergedMap_clearArea_value': MMClear_area_y,
        'mergedMap_ObsArea_time': MMObs_area_x,
        'mergedMap_ObsArea_value': MMObs_area_y,
        'mergedMap_Area_time': MM_area_x,
        'mergedMap_Area_value': MM_area_y,
        'iou_frontiers_opencv_time': iou_num_frontiers_opncv_x,
        'iou_frontiers_opencv_value': iou_num_frontiers_opncv_y,

        'robot0_saved_goals_time': saved_goals0_x,
        'robot0_saved_goals_value': saved_goals0_y,

        'robot1_saved_goals_time': saved_goals1_x,
        'robot1_saved_goals_value': saved_goals1_y,        
  
        'robot2_saved_goals_time': saved_goals2_x,
        'robot2_saved_goals_value': saved_goals2_y,

        'robot0_num_reloc_efforts_time': num_reloc_efforts0_x,
        'robot0_num_reloc_efforts_value': num_reloc_efforts0_y,
 
        'robot1_num_reloc_efforts_time': num_reloc_efforts1_x,
        'robot1_num_reloc_efforts_value': num_reloc_efforts1_y,


        'robot2_num_reloc_efforts_time': num_reloc_efforts2_x,
        'robot2_num_reloc_efforts_value': num_reloc_efforts2_y,        
            
        'robot0_Dopt_time': Dopt0_x,
        'robot0_Dopt_value': Dopt0_y,

        'robot1_Dopt_time': Dopt1_x,
        'robot1_Dopt_value': Dopt1_y,

        'robot2_Dopt_time': Dopt2_x,
        'robot2_Dopt_value': Dopt2_y,             

        'robot0_all_points_time': all_points0_x,
        'robot0_all_points_value': all_points0_y,

        'robot1_all_points_time': all_points1_x,
        'robot1_all_points_value': all_points1_y,


        'robot2_all_points_time': all_points2_x,
        'robot2_all_points_value': all_points2_y,

        'robot0_num_frontiers_filtered_time' : num_frontiers_filtered0_x,
        'robot0_num_frontiers_filtered_value' : num_frontiers_filtered0_y,

        'robot1_num_frontiers_filtered_time' : num_frontiers_filtered1_x,
        'robot1_num_frontiers_filtered_value' : num_frontiers_filtered1_y,

        'robot2_num_frontiers_filtered_time' : num_frontiers_filtered2_x,
        'robot2_num_frontiers_filtered_value' : num_frontiers_filtered2_y,        
       

        'generated_map_area': generated_map_area,
        'cpu_time': cpu_time,
        'cpu_percentages': cpu_percentages,
        'gpu_time': gpu_time,
        'gpu_percentages': gpu_percentages,
        'gpu_memory': gpu_memory,
        'total_num_points': total_num_points,
        'actual_num_points': actual_num_points,
        'num_goals': num_goals,
        'radius_values': radius_values,
        'percentage_values': percentage_values,
        'totarea0_x': totarea0_x,
        'totarea0_y': totarea0_y,
        'totarea1_x': totarea1_x,
        'totarea1_y': totarea1_y,
        'totarea2_x': totarea2_x,
        'totarea2_y': totarea2_y,

        'reloc0_x': reloc0_x,
        'reloc1_x': reloc1_x,
        'reloc2_x': reloc2_x,                  


    }

   
    # Create the data directory if it doesn't exist
    data_directory = os.path.join(package_path, '..', 'data')
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    
    filename = os.path.join(data_directory, f'data-{simulation_id}_{key}.npy')
    np.save(filename, data)

def get_area_value(filename, key):
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                item = parts[0].strip()
                value = parts[1].strip()
                if item == key:
                    return float(value)
                
            
        # Key not found
        return 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Node~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlotterNode(object):
    def __init__(self, simulation_id):
        global merged_x, merged_y, generated_map_area, cpu_percentages, gpu_percentages, gpu_memory, cpu_time, gpu_time 
        global actual_num_points, total_num_points, num_goals, radius_values, percentage_values
        global intersection_x, intersection_y, iou_score_x, iou_score_y, union_area_x, union_area_y
        global MMClear_area_x, MMClear_area_y, MMObs_area_x, MMObs_area_y, MM_area_x, MM_area_y, iou_num_frontiers_opncv_x,iou_num_frontiers_opncv_y
        global saved_goals0_x, saved_goals0_y, saved_goals1_x, saved_goals1_y, saved_goals2_x, saved_goals2_y
        global num_reloc_efforts0_x, num_reloc_efforts0_y, num_reloc_efforts1_x, num_reloc_efforts1_y,num_reloc_efforts2_x, num_reloc_efforts2_y
        global Dopt0_x,Dopt0_y, Dopt1_x,Dopt1_y, Dopt2_x,Dopt2_y
        global all_points0_x,all_points0_y, all_points1_x,all_points1_y, all_points2_x,all_points2_y 
        global num_frontiers_filtered0_x,num_frontiers_filtered0_y, num_frontiers_filtered1_x,num_frontiers_filtered1_y, num_frontiers_filtered2_x,num_frontiers_filtered2_y
        global totarea0_x, totarea0_y, totarea1_x, totarea1_y,totarea2_x, totarea2_y
        global reloc0_x, reloc0_y, reloc1_x, reloc1_y, reloc2_x, reloc2_y  
 
  
        self.simulation_id = simulation_id

        rospy.init_node('plotter_node', anonymous=False)

        # Get initial time in seconds
        self.initial_time = rospy.Time.now().to_sec()

        # Subscriber for the merged map
        #rospy.Subscriber('/map', OccupancyGrid, map_occupation)
        rospy.Subscriber('/mergedmap_robots', OccupancyGrid, map_occupation)

        # Subscriber for the generated map
        rospy.Subscriber('/map2d', OccupancyGrid, generated_map_callback)

        # Subscriber to retrieve the list of the actual points used
        rospy.Subscriber("/merged_centroids", PointArray, actualPointsCallback)

        # Subscriber to retrieve the list of the total points used
        rospy.Subscriber("/list_points", Int32, totalPointsCallback)


        # Subscriber to retrieve the radius value used
        rospy.Subscriber("/radius_value", Float32, radiusValueCallback)

        # Subscriber to retrieve the radius value used
        rospy.Subscriber("/percentage_value", Float32, percentageValueCallback)

        # Subscriber to retrieve the CPU and GPU usage
        rospy.Subscriber("/rosout_agg", Log, cpugpuCallback)

        ###########################################################################
        
        rospy.Subscriber("/map_iou_calculator/intersection_area", Float64, intersection_areaCallback)
        rospy.Subscriber("/map_iou_calculator/iou_score", Float64, iou_scoreCallback)  
        rospy.Subscriber("/map_iou_calculator/union_area", Float64, union_areaCallback) 

        
        rospy.Subscriber("/known_clear_area", Float64, mergedmapClearAreaCallback)
        rospy.Subscriber("/obstacle_area", Float64, mergedmapObsCallback)  
        rospy.Subscriber("/total_area", Float64, mergedmapTotAreaCallback) 

        rospy.Subscriber("/num_opencv_iou", Int32, iou_opencvCallback) 


        rospy.Subscriber("/robot_0/num_saved_goals", Int32, num_saved_goalsCallback0)
        rospy.Subscriber("/robot_0/num_reloc_efforts", Int32, num_reloc_effortsCallback0)  
        rospy.Subscriber("/robot_0/d_optimality_publisher/Dopt", Float32, DoptCallback0) 



        rospy.Subscriber("/robot_0/num_saved_goals", Int32, num_saved_goalsCallback0)
        rospy.Subscriber("/robot_0/num_reloc_efforts", Int32, num_reloc_effortsCallback0)  
        rospy.Subscriber("/robot_0/d_optimality_publisher/Dopt", Float32, DoptCallback0) 

        
        rospy.Subscriber("/robot_1/num_saved_goals", Int32, num_saved_goalsCallback1)
        rospy.Subscriber("/robot_1/num_reloc_efforts", Int32, num_reloc_effortsCallback1)  
        rospy.Subscriber("/robot_1/d_optimality_publisher/Dopt", Float32, DoptCallback1) 

        rospy.Subscriber("/robot_2/num_saved_goals", Int32, num_saved_goalsCallback2)
        rospy.Subscriber("/robot_2/num_reloc_efforts", Int32, num_reloc_effortsCallback2)  
        rospy.Subscriber("/robot_2/d_optimality_publisher/Dopt", Float32, DoptCallback2)    


        rospy.Subscriber("/robot_0/iou/all_points", Int32, all_points0Callback) 
        rospy.Subscriber("/robot_0/iou/num_frontiers_filtered", Int32, num_frontiers_filtered0Callback) 


        rospy.Subscriber("/robot_1/iou/all_points", Int32, all_points1Callback) 
        rospy.Subscriber("/robot_1/iou/num_frontiers_filtered", Int32, num_frontiers_filtered1Callback) 



        rospy.Subscriber("/robot_2/iou/all_points", Int32, all_points2Callback) 
        rospy.Subscriber("/robot_2/iou/num_frontiers_filtered", Int32, num_frontiers_filtered2Callback)   



        rospy.Subscriber("/robot_0/total_area", Float64, totareaCallback0) 
        rospy.Subscriber("/robot_1/total_area", Float64, totareaCallback1) 
        rospy.Subscriber("/robot_2/total_area", Float64, totareaCallback2)


        rospy.Subscriber("/robot_0/num_reloc_efforts", Float64, relocCallback0) 
        rospy.Subscriber("/robot_1/num_reloc_efforts", Float64, relocCallback1) 
        rospy.Subscriber("/robot_2/num_reloc_efforts", Float64, relocCallback2) 


        '''
        * /map_iou_calculator/intersection_area [std_msgs/Float64]
        * /map_iou_calculator/iou_info [frontier_detector/iou]
        * /map_iou_calculator/iou_score [std_msgs/Float64]
        * /map_iou_calculator/union_area [std_msgs/Float64]
        

        Node [/occupancy_area_calculator]
        Publications: 
        * /known_clear_area [std_msgs/Float64]
        * /obstacle_area [std_msgs/Float64]
        * /total_area [std_msgs/Float64]

        Subscriptions: 
         * /mergedmap [nav_msgs/OccupancyGrid]

        '''
        """
        Node [/opencv_detector_iou]
        Publications: 
        * /num_opencv_iou [std_msgs/Int32]
        Subscriptions: 
        * /map_iou_calculator/iou_map [nav_msgs/OccupancyGrid]               
        
        """
        """
        Node [/robot_0/filter_iou]
        Publications: 
        * /robot_0/iou/all_points [std_msgs/Int32]   # points before filtering 
        * /robot_0/iou/num_frontiers_filtered [std_msgs/Int32]  # points afterfiltering    
        """
      
        """
        /robot_1/num_saved_goals [std_msgs/Int32]
        /robot_1/num_reloc_efforts [std_msgs/Int32]
        /robot_1/d_optimality_publisher/Dopt [std_msgs/Float32]       
        
        """

        """
        Node [/robot_0/occupancy_area_calculator]
        Publications: 
        * /robot_0/known_clear_area [std_msgs/Float64]
        * /robot_0/obstacle_area [std_msgs/Float64]
        * /robot_0/total_area [std_msgs/Float64]

        """

        """
        Node [/robot_1/occupancy_area_calculator]
        Publications: 
        * /robot_1/known_clear_area [std_msgs/Float64]
        * /robot_1/obstacle_area [std_msgs/Float64]
        * /robot_1/total_area [std_msgs/Float64]

        """

        """
        
        /robot_0/num_reloc_efforts
        /robot_0/num_reloc_efforts
        
        """


        intersection_x = []
        intersection_y = np.array([])


        iou_score_x = []
        iou_score_y = np.array([])


        union_area_x = []
        union_area_y = np.array([])


        MMClear_area_x = []
        MMClear_area_y = np.array([]) 

        MMObs_area_x = []
        MMObs_area_y = np.array([]) 


        MM_area_x = []
        MM_area_y = np.array([]) 

        iou_num_frontiers_opncv_x = []
        iou_num_frontiers_opncv_y = np.array([]) 
        ################################################
        saved_goals0_x = []
        saved_goals0_y = np.array([]) 

        saved_goals1_x = []
        saved_goals1_y = np.array([])   

        saved_goals2_x = []
        saved_goals2_y = np.array([])    

                   

        ################################################

        num_reloc_efforts0_x = []
        num_reloc_efforts0_y = np.array([])  

        num_reloc_efforts1_x = []
        num_reloc_efforts1_y = np.array([])          

        num_reloc_efforts2_x = []
        num_reloc_efforts2_y = np.array([])  

        ################################################

        Dopt0_x = []
        Dopt0_y = np.array([])   

        Dopt1_x = []
        Dopt1_y = np.array([])   

        Dopt2_x = []
        Dopt2_y = np.array([])   


        ###############################
        totarea0_x = []  
        totarea0_y = np.array([])          


        totarea1_x = []  
        totarea1_y = np.array([])        

        totarea2_x = []  
        totarea2_y = np.array([])             


        # Arrays to store x-values (time) and y-values (area)
        merged_x = []
        merged_y = np.array([])

        # Initialize generated_map_area
        generated_map_area = get_area_value(filename_area, key)

        # Arrays to store the values of usage for CPU ...
        cpu_time = []
        cpu_percentages = np.array([])
        # ... and GPU
        gpu_time = []
        gpu_percentages = np.array([])
        gpu_memory = np.array([])

        # Variables to store the number of goals, total and the actual number of points
        num_goals = []
        total_num_points = []
        actual_num_points = []

        # Variable to store the radius and percentage values used
        radius_values = []
        percentage_values = []


        all_points0_x = []
        all_points0_y = np.array([])   


        reloc0_x = []
        reloc0_y = np.array([])


        reloc1_x = []
        reloc1_y = np.array([])

        reloc2_x = []
        reloc2_y = np.array([])        


        all_points1_x = []
        all_points1_y = np.array([])   

        all_points2_x = []
        all_points2_y = np.array([])           

        num_frontiers_filtered0_x = []
        num_frontiers_filtered0_y = np.array([])  

        num_frontiers_filtered1_x = []
        num_frontiers_filtered1_y = np.array([])          

        num_frontiers_filtered2_x = []
        num_frontiers_filtered2_y = np.array([])       


        rospy.on_shutdown(self.shutdown)

        # Spin the node to prevent it from exiting immediately
        rospy.spin()

    def shutdown(self):
        rospy.loginfo("Shutting down the plotter node...")

        # Save the data for the current simulation
        save_simulation_data(self.simulation_id)

        self.plot_figure()

        rospy.sleep(1)

    def plot_figure(self):
        global merged_x, merged_y, generated_map_area

        plt.figure(figsize=(16, 9))
        # Plot the data
        plt.plot(np.array(merged_x)-merged_x[0], (merged_y/generated_map_area)*100, label='Percentage of area discovered over time')

        plt.xlabel('Time [s]')
        plt.ylabel('Percentage map discovered')
        plt.legend()
        plt.title('Merged map occupation over time')
        plt.grid(True)

        # Adjust the figure
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.4)

        # Check if the "figures" folder exists, and create it if it doesn't
        figure_path = os.path.join(package_path, '..', 'figures')
        if not os.path.exists(figure_path):
            os.makedirs(figure_path)

        # Read the current number from the config file
        # Construct the absolute path to the file
        filename = os.path.join(package_path, '..', 'config', 'number_figures.txt')
        with open(filename, 'r') as file:
            n = int(file.read())

        # Save image
        plt.savefig(f"{figure_path}/figure_{n}.png")

        # Save the updated number back to the file
        with open(filename, 'w') as file:
            file.write(str(n + 1))

        # Close the figure to release resources
        plt.close()


if __name__ == '__main__':
    # Create a unique ID for each simulation
    filename = os.path.join(package_path, '..', 'config', 'number_simulations.txt')
    with open(filename, 'r') as file:
        n = int(file.read())
    current_simulation_id = f"simulation_{n}_{num_robots}_robots"
    # Save the updated number back to the file
    with open(filename, 'w') as file:
        file.write(str(n + 1))

    node = PlotterNode(current_simulation_id)
    rospy.loginfo("Plotter Node Started")

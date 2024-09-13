#!/usr/bin/env python3

# jplaced
# 2022, Universidad de Zaragoza

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Include modules~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import rospy
import numpy as np

from nptyping import ndarray
from typing import Tuple
from geometry_msgs.msg import PoseStamped, Point
from visualization_msgs.msg import Marker, MarkerArray 
from nav_msgs.msg import OccupancyGrid
from numpy.linalg import norm
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.srv import GetPlan



import math
from constants import csv_path_1, csv_path_2, csv_path_3
from PIL import Image, ImageDraw
import csv



# NUMBA imports for GPU computations
try:
    import numba as nb
    from numba import cuda
    cuda.select_device(0)
except ModuleNotFoundError:
    print("Import error: Numba module not found")
except Exception as e:
    print("GPU not found: " + format(e))




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def waitEnterKey():
    input("Press Enter to continue...")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def euler2quaternion(roll: float, pitch: float, yaw: float) -> Tuple[float, float, float, float]:
    """
    Converts Euler angles (radians) to quaternion
    """
    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

    return qx, qy, qz, qw


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def quaternion2euler(w: float, x: float, y: float, z: float):
    """
    Converts quaternion to Euler angles (radians)
    """
    y2 = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y2)
    X = np.arctan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2 > +1.0, +1.0, t2)

    t2 = np.where(t2 < -1.0, -1.0, t2)
    Y = np.arcsin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y2 + z * z)
    Z = np.arctan2(t3, t4)

    return X, Y, Z


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def yawBtw2Points(pointA: np.array, pointB: np.array) -> float:
    """
    Computes angle between two 2-dimensional vectors (radians)
    """
    changeInX = pointB[0] - pointA[0]
    changeInY = pointB[1] - pointA[1]
    return np.arctan2(changeInY, changeInX)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def createMarker(namespace: str = "robot_1", locX: float=0, locY: float=0, mtype: str = "point", frame: str = "/map", ns: str = "marker_ns", lifetime: float = 0,
                 colors: ndarray = None, alpha: float = 1.0, scale: float = 0.3) -> Marker:
    """
    Initializes a ROS visualization_msgs Marker
    """
    if colors is None:
        colors = [255, 0, 0]

    marker = Marker()
    marker.header.frame_id = namespace+frame
    marker.header.stamp = rospy.Time.now()
    marker.ns = ns
    marker.id = 0
    marker.action = Marker.ADD
    marker.pose.orientation.w = 1.0
    marker.color.a = alpha
    marker.color.r = colors[0]
    marker.color.g = colors[1]
    marker.color.b = colors[2]
    marker.lifetime = rospy.Duration(lifetime)


    marker.pose.position.x = 0.0
    marker.pose.position.y = 0.0
    marker.pose.position.z = 0.0    

    marker.pose.orientation.x = locX
    marker.pose.orientation.y = locY
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    if mtype == "point":
        marker.type = Marker.POINTS
        marker.scale.x = marker.scale.y = scale
    elif mtype == "sphere":
        marker.type = Marker.SPHERE
        marker.scale.x = marker.scale.y = marker.scale.z = scale  # Diameter
    elif mtype == "arrow":
        marker.type = Marker.ARROW
        marker.scale.x = scale  # Arrow length
        marker.scale.y = marker.scale.z = 0.05  # Arrow head diameter and length
    elif mtype == "cube":
        marker.type = Marker.CUBE
        marker.scale.x = marker.scale.y = marker.scale.z = scale
    elif mtype == "circumference":
        marker.type = Marker.SPHERE
        marker.scale.x = marker.scale.y = scale
        marker.scale.z = 0.05
        marker.pose.position.z = 0.0
    elif mtype == "lines":
        marker.type = Marker.LINE_STRIP
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.0
        marker.scale.x = scale

    return marker


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cellInformation(mapData: OccupancyGrid, point: np.array, r: float):
    cells = [0, 0, 0]  # every cell, unknown cells, occupied cells
    index = index_of_point(mapData, point)
    r_region = int(r // mapData.info.resolution)
    init_index = index - r_region * (mapData.info.width + 1)

    for n in range(0, 2 * r_region + 1):
        start = n * mapData.info.width + init_index
        end = start + 2 * r_region
        limit = start + 2 * mapData.info.width
        for i in range(start, end + 1):
            if 0 <= i < np.min([limit, len(mapData.data)]) and \
                    np.linalg.norm(np.array(point) - point_of_index(mapData, i)) <= r:
                cells[0] += 1
                if mapData.data[i] == -1:
                    cells[1] += 1  # Unknown

    # Normalized information gain due to unknown region
    percentage_new_cells = (float(cells[1]) / float(cells[0]))

    return percentage_new_cells


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Returns the mapData's index of a given point (x,y) in the map
def index_of_point(mapData, Xp):
    resolution = mapData.info.resolution
    Xstartx = mapData.info.origin.position.x
    Xstarty = mapData.info.origin.position.y
    width = mapData.info.width
    index = int((np.floor((Xp[1] - Xstarty) // resolution) * width) + (np.floor((Xp[0] - Xstartx) // resolution)))
    return index


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Returns the point (x,y) of a given mapData's index
def point_of_index(mapData, i):
    y = mapData.info.origin.position.y + (i // mapData.info.width) * mapData.info.resolution
    x = mapData.info.origin.position.x + (
            i - (i // mapData.info.width) * mapData.info.width) * mapData.info.resolution
    return np.array([x, y])


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# NUMBA FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@nb.jit(nb.float64(nb.int64[:], nb.float64, nb.int64, nb.float64, nb.float64, nb.float64,
                   nb.float64, nb.float64), nopython=True)
def cellInformation_NUMBA(data, resolution, width, Xstartx, Xstarty, pointx, pointy, r):
    cells = [0, 0, 0]  # every cell, unknown cells, occupied cells
    index = int((np.floor((pointy - Xstarty) // resolution) * width) + (np.floor((pointx - Xstartx) // resolution)))
    r_region = int(r // resolution)
    init_index = index - r_region * (width + 1)

    for n in range(0, 2 * r_region + 1):
        start = n * width + init_index
        end = start + 2 * r_region
        limit = start + 2 * width
        for i in range(start, end + 1):
            if 0 <= i < len(data) and i < limit:
                y = Xstarty + (i // width) * resolution
                x = Xstartx + (i - (i // width) * width) * resolution
                poi = np.array([x, y])
                if np.linalg.norm(np.array([pointx, pointy]) - poi) <= r:
                    cells[0] += 1
                    if data[i] == -1:
                        cells[1] += 1  # Unknown

    if float(cells[0]) !=0:
        # Normalized information gain due to unknown region
        percentage_new_cells = (float(cells[1]) / float(cells[0]))
    else:
          percentage_new_cells=0  

    return percentage_new_cells


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# USED IN FRONTIER FILTERING
# Returns grid value at "Xp" location
# Map data:  100 occupied      -1 unknown       0 free
def gridValue(mapData, Xp):
    resolution = mapData.info.resolution
    Xstartx = mapData.info.origin.position.x
    Xstarty = mapData.info.origin.position.y
    width = mapData.info.width
    Data = mapData.data
    index = (np.floor((Xp[1] - Xstarty) // resolution) *
             width) + (np.floor((Xp[0] - Xstartx) // resolution))
    # return [100, Data[int(index)]][int(index) < len(Data) and int(index) >= 0]
    if int(index) < 0 or int(index) >= len(Data):
        return 100
    else:
        return Data[int(index)]


# ANSI color codes
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'



def draw_marker(namespace, x, y, color=[1.0,0.0,0.0], mtype="sphere", scale=0.1, ns='my_marker_ns'):
    # Create a Marker message
    #rospy.loginfo("got x at {} and y at {}".format(x,y))
    marker = Marker()
    marker.header.frame_id = namespace       
    marker.header.stamp = rospy.Time.now() 
    marker.action = marker.ADD
    #marker.id = 0
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = 0
    marker.pose.orientation.x = 0
    marker.pose.orientation.y = 0
    marker.pose.orientation.z = 0
    marker.pose.orientation.w = 1
    marker.scale.x = 0.5
    marker.scale.y = 0.5
    marker.scale.z = 0.5
    marker.color.a = 1.0
    marker.color.r = color[0]
    marker.color.g = color[1]
    marker.color.b = color[2]
    marker.lifetime = rospy.Duration(1.5)
    marker.ns = ns
    if mtype == "point":
        marker.type = Marker.POINTS
        marker.scale.x = marker.scale.y = scale
    elif mtype == "sphere":
        marker.type = Marker.SPHERE
        marker.scale.x = marker.scale.y = marker.scale.z = scale  # Diameter
    elif mtype == "arrow":
        marker.type = Marker.ARROW
        marker.scale.x = scale  # Arrow length
        marker.scale.y = marker.scale.z = 0.05  # Arrow head diameter and length
    elif mtype == "cube":
        marker.type = Marker.CUBE
        marker.scale.x = marker.scale.y = marker.scale.z = scale
    elif mtype == "circumference":
        marker.type = Marker.SPHERE
        marker.scale.x = marker.scale.y = scale
        marker.scale.z = 0.05
        marker.pose.position.z = 0.0
    elif mtype == "lines":
        marker.type = Marker.LINE_STRIP
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.0
        marker.scale
    return marker




def get_map_cell(mapData,point):
    """ Convert a point in the world coordinates to a cell in the occupancy grid map """       
    cell_x = int((point.x - mapData.info.origin.position.x) / mapData.info.resolution)
    cell_y = int((point.y - mapData.info.origin.position.y) / mapData.info.resolution)
    return (cell_x, cell_y)

def ray_tracing(mapData,start_point, end_point):
    """ Perform ray tracing from start_point to end_point """
    start_cell = get_map_cell(mapData,start_point)
    end_cell = get_map_cell(mapData,end_point)
    distance = math.sqrt(math.pow(end_cell[0] - start_cell[0], 2) + math.pow(end_cell[1] - start_cell[1], 2))  
    ray_cells = []
    occupancy_values=[]    
    x0, y0 = start_cell
    x1, y1 = end_cell       
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)    
    x = x0
    y = y0
    n = 1 + dx + dy

    x_inc = 1 if x1 > x0 else -1
    y_inc = 1 if y1 > y0 else -1
    
    error = dx - dy
    dx *= 2
    dy *= 2
    while n > 0:
        ray_cells.append((x, y))
        if error >= 0:
            x += x_inc
            error -= dy
        else:
            y += y_inc
            error += dx
        n -= 1 
    return distance, ray_cells



def compute_entropy(namespace,map_data_,p_frontier_x,p_frontier_y,robotposxy):            
    entropy=0        

    start_point = Point(robotposxy[0], robotposxy[1] , 0)
    end_point = Point( p_frontier_x,p_frontier_y, 0)

    distance, ray_cells = ray_tracing(map_data_,start_point, end_point) 
    
    markerArray = MarkerArray()
    marker=Marker()
    marker.id=0        
    occupency_values =[]
    map_res = map_data_.info.resolution        
    map_orig_x_loc = map_data_.info.origin.position.x 
    map_orig_y_loc = map_data_.info.origin.position.y    

    for i in range(0,len(ray_cells)):
        x = ray_cells[i][0]
        y = ray_cells[i][1]   
        X_w = map_data_.info.origin.position.x + x*map_data_.info.resolution  
        Y_w = map_data_.info.origin.position.y + y*map_data_.info.resolution                
        Xp =[X_w,Y_w]
        marker = draw_marker(namespace,(ray_cells[i][0]*map_res) +map_orig_x_loc ,(ray_cells[i][1]*map_res)+map_orig_y_loc , [0.4,0.1,0.5],"sphere", 0.1)                  
        marker.id = i       
        markerArray.markers.append(marker)  
        occupency_values.append(gridValue(map_data_, Xp)) 
           
    marker = draw_marker(namespace,p_frontier_x,p_frontier_y, [0.5,0.5,1],"sphere", 0.3)        
           
    occupancy_list = []

    try: 
        for occupancy_value in occupency_values:   
            occupancy_list.append(occupancy_value)                            
            if occupancy_value == -1:
                prob=0.100  # yeilds low entropy and high uncertinaty and low information gain
            elif occupancy_value == 0 or occupancy_value == 100:
                prob=0.450 #yields high entropy and low uncertinaty and high information gain
            else:
                rospy.loginfo("I got a different occupancy value of {}".format(occupancy_value))                               
            try:                                    
                entropy += (-((prob * math.log2(prob) + (1 - prob)*math.log2(1 - prob)))) #* np.exp(-0.25 * distance)     
               
            except Exception as e:                        
                rospy.logerr("problem computing the entropy {}".format(e))                
        # Do something with the occupancy value         
    except Exception as e:
        rospy.logerr("Error processing compute entropy method: {}".format(e))

     
    if entropy !=0 and len(occupency_values)!=0:    
        entropy = entropy/len(occupency_values)     

    return entropy,markerArray,marker,distance 


def savetofile(data,frontierID):
    try:
        with open(csv_path_1, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            rr,cc = np.shape(data)
            writer.writerow("Frontier No. "+str(frontierID)) 
            for i in range (0,cc):
                pose = [str(data[0,i]),str(data[1,i])]
                writer.writerow(pose)

    except IOError as e:
        rospy.logerr("Unable to write CSV file: %s", str(e))

    finally:
        file.close()

def euclidean_distance( x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))        
    return distance


def count_digits_before_decimal(number):
    number_str = str(number)
    if '.' in number_str:
        decimal_index = number_str.index('.')
        digits_before_decimal = decimal_index
    else:
        digits_before_decimal = len(number_str)
    return digits_before_decimal



def goal_marker(namespace, color=[1.0,0.0,0.0], x=0, y=0, mtype="sphere", scale=0.1, ns='GoalMarker_ns', lifetime = 1.0):
    # Create a Marker message
    #rospy.loginfo("got x at {} and y at {}".format(x,y))
    lifetime_ = lifetime
    marker = Marker()
    marker.header.frame_id = namespace+"/map"       
    marker.header.stamp = rospy.Time.now() 
    marker.action = marker.ADD
    #marker.id = 0
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = 0
    marker.pose.orientation.x = 0
    marker.pose.orientation.y = 0
    marker.pose.orientation.z = 0
    marker.pose.orientation.w = 1
    marker.scale.x = 0.5
    marker.scale.y = 0.5
    marker.scale.z = 0.5
    marker.color.a = 1.0

    marker.color.r = color[0]
    marker.color.g = color[1]
    marker.color.b = color[2]

    marker.lifetime = rospy.Duration(lifetime_)

    if mtype == "point":
        marker.type = Marker.POINTS
        marker.scale.x = marker.scale.y = scale
    elif mtype == "sphere":
        marker.type = Marker.SPHERE
        marker.scale.x = marker.scale.y = marker.scale.z = scale  # Diameter
    elif mtype == "arrow":
        marker.type = Marker.ARROW
        marker.scale.x = scale  # Arrow length
        marker.scale.y = marker.scale.z = 0.05  # Arrow head diameter and length
    elif mtype == "cube":
        marker.type = Marker.CUBE
        marker.scale.x = marker.scale.y = marker.scale.z = scale
    elif mtype == "circumference":
        marker.type = Marker.SPHERE
        marker.scale.x = marker.scale.y = scale
        marker.scale.z = 0.05
        marker.pose.position.z = 0.0
    elif mtype == "lines":
        marker.type = Marker.LINE_STRIP
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.0
        marker.scale.x = scale
    return marker








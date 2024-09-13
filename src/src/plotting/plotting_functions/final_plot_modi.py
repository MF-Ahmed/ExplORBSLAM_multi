import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import pandas as pd

# Define the directory where the data files are located
file_path = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(file_path,'..','data')
print(data_directory)


# Get a list of all the data files in the directory and sort them based on the simulation number
data_files = sorted([file for file in os.listdir(data_directory) if file.startswith('data-simulation')], key=lambda x: int(x.split("_")[1]))

# Initialize lists to store the data from each simulation
merged_x_list = []
merged_y_list = []
generated_map_area_list = []


iou_area_time_list = []
iou_area_value_list = []

iou_score_time_list = []
iou_score_value_list = []


union_area_time_list =[]
union_area_value_list =[]

mergedMap_clearArea_time_list = []
mergedMap_clearArea_value_list = []

mergedMap_ObsArea_time_list = []
mergedMap_ObsArea_value_list = []


mergedMap_Area_time_list = []
mergedMap_Area_value_list = []


iou_frontiers_opencv_time_list = []
iou_frontiers_opencv_value_list = []



totarea0_time_list = []
totarea0_value_list  = []


totarea1_time_list = []
totarea1_value_list  = []


totarea2_time_list = []
totarea2_value_list  = []




robot0_saved_goals_time_list = []
robot0_saved_goals_value_list = []


robot1_saved_goals_time_list = []
robot1_saved_goals_value_list = []


robot2_saved_goals_time_list = []
robot2_saved_goals_value_list = []


robot0_num_reloc_efforts_time_list = []
robot0_num_reloc_efforts_value_list = []

robot1_num_reloc_efforts_time_list = []
robot1_num_reloc_efforts_value_list = []

robot2_num_reloc_efforts_time_list= []
robot2_num_reloc_efforts_value_list = []


robot0_Dopt_time_list = []
robot0_Dopt_value_list = []


robot1_Dopt_time_list = []
robot1_Dopt_value_list = []


robot2_Dopt_time_list = []
robot2_Dopt_value_list = []


robot0_all_points_time_list = []
robot0_all_points_value_list = []



robot1_all_points_time_list = []
robot1_all_points_value_list = []


robot2_all_points_time_list = []
robot2_all_points_value_list = []


robot0_num_frontiers_filtered_time_list = []
robot0_num_frontiers_filtered_value_list = []


robot1_num_frontiers_filtered_time_list = []
robot1_num_frontiers_filtered_value_list = []


robot2_num_frontiers_filtered_time_list = []
robot2_num_frontiers_filtered_value_list = []






#cpu_time_list = []
#cpu_percentages_list = []
#gpu_time_list = []
#gpu_percentages_list = []
#gpu_memory_list = []
num_robots_list = []
num_goals_list = []
total_num_points_list = []
actual_num_points_list = []
radius_values_list = []
percentage_values_list = []
num_simulations = 0

method_list=[]

# Iterate over the data files
for file in data_files:

    num_simulations += 1
    # Load the data from the file
    data = np.load(os.path.join(data_directory, file), allow_pickle=True).item()
    merged_x = data['merged_x']       
    merged_y = data['merged_y']


    iou_area_time = data['iou_area_time']
    iou_area_value = data['iou_area_value']


    totarea0_time = data['totarea0_x']
    totarea0_value = data['totarea0_y']


    totarea1_time = data['totarea1_x']
    totarea1_value = data['totarea1_y']


    totarea2_time = data['totarea2_x']
    totarea2_value = data['totarea2_y']    


    iou_score_time = data['iou_score_time']
    iou_score_value = data['iou_score_value']


    union_area_time =data['union_area_time']
    union_area_value =data['union_area_value']

    mergedMap_clearArea_time = data['mergedMap_clearArea_time']
    mergedMap_clearArea_value = data['mergedMap_clearArea_value']

    mergedMap_ObsArea_time = data['mergedMap_ObsArea_time']
    mergedMap_ObsArea_value = data['mergedMap_ObsArea_value']


    mergedMap_Area_time = data['mergedMap_Area_time']
    mergedMap_Area_value = data['mergedMap_Area_value']


    iou_frontiers_opencv_time = data['iou_frontiers_opencv_time']
    iou_frontiers_opencv_value = data['iou_frontiers_opencv_value']

    robot0_saved_goals_time = data['robot0_saved_goals_time']
    robot0_saved_goals_value = data['robot0_saved_goals_value']

    robot1_saved_goals_time = data['robot1_saved_goals_time']
    robot1_saved_goals_value = data['robot1_saved_goals_value']

    robot2_saved_goals_time = data['robot2_saved_goals_time']
    robot2_saved_goals_value = data['robot2_saved_goals_value']


    robot0_num_reloc_efforts_time = data['robot0_num_reloc_efforts_time']
    robot0_num_reloc_efforts_value = data['robot0_num_reloc_efforts_value']

    robot1_num_reloc_efforts_time = data['robot1_num_reloc_efforts_time']
    robot1_num_reloc_efforts_value = data['robot1_num_reloc_efforts_value']

    robot2_num_reloc_efforts_time = data['robot2_num_reloc_efforts_time']
    robot2_num_reloc_efforts_value = data['robot2_num_reloc_efforts_value']


    robot0_Dopt_time = data['robot0_Dopt_time']
    robot0_Dopt_value = data['robot0_Dopt_value']

    robot1_Dopt_time = data['robot1_Dopt_time']
    robot1_Dopt_value = data['robot1_Dopt_value']

    robot2_Dopt_time = data['robot2_Dopt_time']
    robot2_Dopt_value = data['robot2_Dopt_value']

      
    robot0_all_points_time = data['robot0_all_points_time']
    robot0_all_points_value = data['robot0_all_points_value']


    robot1_all_points_time = data['robot1_all_points_time']
    robot1_all_points_value = data['robot1_all_points_value']

    robot2_all_points_time = data['robot2_all_points_time']
    robot2_all_points_value = data['robot2_all_points_value']      


    robot0_num_frontiers_filtered_time = data['robot0_num_frontiers_filtered_time']
    robot0_num_frontiers_filtered_value = data['robot0_num_frontiers_filtered_value']  


    robot1_num_frontiers_filtered_time = data['robot1_num_frontiers_filtered_time']
    robot1_num_frontiers_filtered_value = data['robot1_num_frontiers_filtered_value']  



    robot2_num_frontiers_filtered_time = data['robot2_num_frontiers_filtered_time']
    robot2_num_frontiers_filtered_value = data['robot2_num_frontiers_filtered_value']  



    # Extract the required data from the simulation
       
    generated_map_area = data['generated_map_area']
    #cpu_time = data['cpu_time']
    #cpu_percentages = data['cpu_percentages']
    #gpu_time = data['gpu_time']
    #gpu_percentages = data['gpu_percentages']
    #gpu_memory = data['gpu_memory']
    num_goals = data['num_goals']
    total_num_points = data['total_num_points']
    actual_num_points = data['actual_num_points']
    radius_values = data['radius_values']
    percentage_values = data['percentage_values']



    # Extract the number of robots from the file name
    num_robots = int(file.split('_')[2].split('.')[0])
    num_robots_list.append(num_robots)

    # Extract the Method the file name
    method = file.split('-')[1].split('.')[0]
    method_list.append(method)
    
    # Append the data to the respective lists
    merged_x_list.append(merged_x)
    merged_y_list.append(merged_y)


    totarea0_time_list.append(totarea0_time)
    totarea0_value_list.append(totarea0_value)


    totarea1_time_list.append(totarea1_time)
    totarea1_value_list.append(totarea1_value)


    totarea2_time_list.append(totarea2_time)
    totarea2_value_list.append(totarea2_value)

    iou_area_time_list.append(iou_area_time)
    iou_area_value_list.append(iou_area_value)

    iou_score_time_list.append(iou_score_time)
    iou_score_value_list.append(iou_score_value)

    union_area_time_list.append(union_area_time)
    union_area_value_list.append(union_area_value)

    mergedMap_clearArea_time_list.append(mergedMap_clearArea_time[5:])
    mergedMap_clearArea_value_list.append(mergedMap_clearArea_value[5:])

    mergedMap_ObsArea_time_list.append(mergedMap_ObsArea_time)
    mergedMap_ObsArea_value_list.append(mergedMap_ObsArea_value)


    mergedMap_Area_time_list.append(mergedMap_Area_time)
    mergedMap_Area_value_list.append(mergedMap_Area_value)


    iou_frontiers_opencv_time_list.append(iou_frontiers_opencv_time)
    iou_frontiers_opencv_value_list.append(iou_frontiers_opencv_value)


    robot0_saved_goals_time_list.append(robot0_saved_goals_time)
    robot0_saved_goals_value_list.append(robot0_saved_goals_value)


    robot1_saved_goals_time_list.append(robot1_saved_goals_time)
    robot1_saved_goals_value_list.append(robot1_saved_goals_value)    


    robot2_saved_goals_time_list.append(robot2_saved_goals_time)
    robot2_saved_goals_value_list.append(robot2_saved_goals_value)    


    robot0_num_reloc_efforts_time_list.append(robot0_num_reloc_efforts_time)
    robot0_num_reloc_efforts_value_list.append(robot0_num_reloc_efforts_value)


    robot1_num_reloc_efforts_time_list.append(robot1_num_reloc_efforts_time)
    robot1_num_reloc_efforts_value_list.append(robot1_num_reloc_efforts_value)


    robot2_num_reloc_efforts_time_list.append(robot2_num_reloc_efforts_time)
    robot2_num_reloc_efforts_value_list.append(robot2_num_reloc_efforts_value)



    robot1_num_reloc_efforts_time_list.append(robot1_num_reloc_efforts_time)
    robot1_num_reloc_efforts_value_list.append(robot1_num_reloc_efforts_value)

    robot2_num_reloc_efforts_time_list.append(robot2_num_reloc_efforts_time)
    robot2_num_reloc_efforts_value_list.append(robot2_num_reloc_efforts_value)


    robot0_Dopt_time_list.append(robot0_Dopt_time)
    robot0_Dopt_value_list.append(robot0_Dopt_value)


    robot1_Dopt_time_list.append(robot1_Dopt_time)
    robot1_Dopt_value_list.append(robot1_Dopt_value)

    robot2_Dopt_time_list.append(robot2_Dopt_time)
    robot2_Dopt_value_list.append(robot2_Dopt_value)


    robot0_all_points_time_list.append(robot0_all_points_time) 
    robot0_all_points_value_list.append(robot0_all_points_value) 


    robot1_all_points_time_list.append(robot1_all_points_time) 
    robot1_all_points_value_list.append(robot1_all_points_value) 

    robot2_all_points_time_list.append(robot2_all_points_time) 
    robot2_all_points_value_list.append(robot2_all_points_value)         

    robot0_num_frontiers_filtered_time_list.append(robot0_num_frontiers_filtered_time)
    robot0_num_frontiers_filtered_value_list.append(robot0_num_frontiers_filtered_value)

    robot1_num_frontiers_filtered_time_list.append(robot1_num_frontiers_filtered_time)
    robot1_num_frontiers_filtered_value_list.append(robot1_num_frontiers_filtered_value)

    robot2_num_frontiers_filtered_time_list.append(robot2_num_frontiers_filtered_time)
    robot2_num_frontiers_filtered_value_list.append(robot2_num_frontiers_filtered_value)        

    generated_map_area_list.append(generated_map_area)
    num_goals_list.append(num_goals)
    total_num_points_list.append(total_num_points)
    actual_num_points_list.append(actual_num_points)

    radius_values_list.append(radius_values)
    percentage_values_list.append(percentage_values)



################################## IOU Values ##################################
# Function to calculate the running average
def running_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

window_size = 10
# Plotting the data for the map occupancy
plt.figure(figsize=(16, 9))

# Plot the merged map occupation over time for each simulation
for i in range(num_simulations):
    _simulation_number = int(data_files[i].split("_")[1])
    # Compute running averages
    smoothed_iou_area_value = running_average(iou_area_value_list[i], window_size)
    smoothed_iou_score_value = running_average(iou_score_value_list[i], window_size)
    smoothed_union_area_value = running_average(union_area_value_list[i], window_size)
    
    # Adjust time lists to match the length of the running averages
    smoothed_time_list = np.array(iou_area_time_list[i][window_size-1:])
    
    plt.plot(smoothed_time_list - smoothed_time_list[0], smoothed_iou_area_value,
             label=f'Exp{_simulation_number} - IOU_Intersetion-Area', linewidth=3)
    
    plt.plot(smoothed_time_list - smoothed_time_list[0], smoothed_iou_score_value,
             label=f'New Exp{_simulation_number} - IOU_Score', linewidth=3)    
        
    #plt.plot(smoothed_time_list - smoothed_time_list[0], (smoothed_union_area_value/167)*100,
             #label=f'New Exp{_simulation_number} - Union Value', linewidth=3)
 
plt.xlabel('Time [s]')
plt.ylabel('IOU Map Area')
plt.legend()
plt.grid(True)

# Since the plot concern a percentage the graph will be from 0 to 100
plt.ylim(0, 5)
plt.xlim(0, 1200)  # 20 mins of simulation time 


# Adjust the figure
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.4)

# Show the plot
plt.show()

################################## Area Covered ##################################
"""
# Plotting the data for the map occupancy
plt.figure(figsize=(5, 4))

# Define the window size for the running average
window_size = 5
# Plot the merged map occupation over time for each simulation
for i in range(num_simulations):
    _simulation_number = int(data_files[i].split("_")[1])    
    # Compute running averages
    smoothed_totarea0_value = running_average(totarea0_value_list[i], window_size)
    smoothed_totarea1_value = running_average(totarea1_value_list[i], window_size)
    smoothed_total_area_value = smoothed_totarea0_value + smoothed_totarea1_value

    # Adjust time lists to match the length of the running averages
    smoothed_time_list = np.array(totarea0_time_list[i][window_size-1:])

    plt.plot(smoothed_time_list - smoothed_time_list[0], (smoothed_totarea0_value/167.0)*100,
                label=f'Exp{_simulation_number} - Running Avg Total_Area_Robot_0', linewidth=3)

    plt.plot(smoothed_time_list - smoothed_time_list[0], (smoothed_totarea1_value/167.0)*100,
                label=f'Exp{_simulation_number} - Running Avg Total_Area_Robot_1', linewidth=3)

    plt.plot(smoothed_time_list - smoothed_time_list[0], (smoothed_total_area_value/167.0)*100,
                label=f'Exp{_simulation_number} - Running Avg Total Area', linewidth=3, linestyle='--')

plt.xlabel('Time [s]')
plt.ylabel('Map Area')
plt.legend()
plt.grid(True)

# Since the plot concern a percentage the graph will be from 0 to 100
plt.ylim(0, 100)
plt.xlim(0, 500)

# Adjust the figure
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.4)
# Show the plot
plt.show()
"""

################################## IOU MAP OCCUPATION ##################################

# Function to calculate the running average
def running_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Function to normalize data
def normalize_data(data_list):
    max_values = np.max(data_list, axis=1)
    normalized_data = [data_list[i] / max_values[i] for i in range(len(data_list))]
    return normalized_data

# Assuming these are defined elsewhere
num_simulations = len(mergedMap_clearArea_value_list)

plt.figure(figsize=(12, 8))

for i in range(num_simulations):
    _simulation_number = int(data_files[i].split("_")[1])
    
    # Calculate running average for mergedMap_clearArea
    smoothed_clearArea_value = running_average(mergedMap_clearArea_value_list[i][5:], 5)
    smoothed_clearArea_time_list = mergedMap_clearArea_time_list[i][5 + (5-1):]  # Adjust time list for running average
    
    # Ensure time list length matches smoothed data length
    smoothed_clearArea_time_list = smoothed_clearArea_time_list[:len(smoothed_clearArea_value)]
    
    # Convert time list to numpy array
    smoothed_clearArea_time_array = np.array(smoothed_clearArea_time_list)

    # Normalize smoothed data for mergedMap_clearArea
    max_value = np.max(smoothed_clearArea_value)
    normalized_smoothed_clearArea_value = smoothed_clearArea_value / max_value

    # Calculate running average for mergedMap_ObsArea
    smoothed_ObsArea_value = running_average(mergedMap_ObsArea_value_list[i][5:], 5)
    smoothed_ObsArea_time_list = mergedMap_ObsArea_time_list[i][5 + (5-1):]  # Adjust time list for running average
    
    # Ensure time list length matches smoothed data length
    smoothed_ObsArea_time_list = smoothed_ObsArea_time_list[:len(smoothed_ObsArea_value)]
    
    # Convert time list to numpy array
    smoothed_ObsArea_time_array = np.array(smoothed_ObsArea_time_list)

    # Normalize smoothed data for mergedMap_ObsArea
    max_value_ObsArea = np.max(smoothed_ObsArea_value)
    normalized_smoothed_ObsArea_value = smoothed_ObsArea_value / max_value_ObsArea

    plt.plot(smoothed_ObsArea_time_array - smoothed_ObsArea_time_array[0], normalized_smoothed_ObsArea_value,
             label=f'Exp{_simulation_number} - Running Avg Normalized MergedMap_ObsArea', linewidth=3)

    plt.plot(smoothed_clearArea_time_array - smoothed_clearArea_time_array[0], normalized_smoothed_clearArea_value,
             label=f'Exp{_simulation_number} - Running Avg Normalized MergedMap_clearArea', linewidth=3)

plt.xlabel('Time [s]')
plt.ylabel('Normalized Merged Map Area')
plt.legend()
plt.grid(True)

# Since the plot concerns a percentage, adjust the y-axis limits as needed
plt.ylim(0.9, 1.1)
plt.xlim(0, 1200)  # 20 mins of simulation time 


plt.title('Normalized Running Average of Merged Map Area over Time')
plt.tight_layout()
plt.show()

################################## Frontiers ##################################


num_simulations = len(robot0_all_points_value_list)  # Assuming all lists have the same length

# Initialize arrays to store average values
avg_robot0_all_points = np.zeros(num_simulations)
avg_robot0_num_frontiers_filtered = np.zeros(num_simulations)
avg_robot1_all_points = np.zeros(num_simulations)
avg_robot1_num_frontiers_filtered = np.zeros(num_simulations)

# Compute average values for each simulation
for i in range(num_simulations):
    avg_robot0_all_points[i] = np.mean(robot0_all_points_value_list[i])
    avg_robot0_num_frontiers_filtered[i] = np.mean(robot0_num_frontiers_filtered_value_list[i])
    avg_robot1_all_points[i] = np.mean(robot1_all_points_value_list[i])
    avg_robot1_num_frontiers_filtered[i] = np.mean(robot1_num_frontiers_filtered_value_list[i])

# Plotting bar plots for robot0 and robot1 averages
plt.figure(figsize=(12, 8))

bar_width = 0.2
index = np.arange(num_simulations)

colors = ['#377eb8', '#ff7f00', '#4daf4a', '#e41a1c']  # Blue, Orange, Green, Red


plt.bar(index, avg_robot0_all_points, bar_width, label='robot0_all_points', alpha=0.8, color = colors[0])
plt.bar(index + bar_width, avg_robot0_num_frontiers_filtered, bar_width, label='robot0_num_frontiers_filtered', alpha=0.8,color = colors[1])
plt.bar(index + 2*bar_width, avg_robot1_all_points, bar_width, label='robot1_all_points', alpha=0.8, color = colors[2])
plt.bar(index + 3*bar_width, avg_robot1_num_frontiers_filtered, bar_width, label='robot1_num_frontiers_filtered', alpha=0.8, color = colors[0])

plt.xlabel('Simulation')
plt.ylabel('Average Frontiers')
plt.title('Average Frontiers for robot0 and robot1')
plt.xticks(index + 1.5*bar_width, [f'Sim{i+1}' for i in range(num_simulations)])
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


################################## D-Optimality ##################################

# Plotting the data for the map occupancy
plt.figure(figsize=(16, 9))

# Plot the merged map occupation over time for each simulation
for i in range(num_simulations):
    _simulation_number = int(data_files[i].split("_")[1])
    #_method = str(data_files[i].split("-")[1])    
  
    plt.plot(np.array(robot0_Dopt_time_list[i]) - robot0_Dopt_time_list[i][0], ((robot0_Dopt_value_list[i])),
            label=f'New Exp{_simulation_number} - {"robot0_Dopt"}', linewidth=3)    
    
    plt.plot(np.array(robot1_Dopt_time_list[i]) - robot1_Dopt_time_list[i][0], ((robot1_Dopt_value_list[i])),
            label=f'New Exp{_simulation_number} - {"robot1_Dopt"}', linewidth=3)    
    


plt.xlabel('Time [s]')
plt.ylabel('D-Optimality')
plt.legend()
plt.grid(True)

# Since the plot concern a percentage the graph will be from 0 to 100
plt.ylim(0, 200)
plt.xlim(0, 1200)  # 20 mins of simulation time 

# Adjust the figure
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.4)
# Show the plot
plt.show()





################################## NUM POINTS USED ##################################

"""

plt.figure(figsize=(6, 3))
# Lists to store data for box plots
total_points_data = []
actual_points_data = []
num_robots_list = []

# Process data to prepare for box plots
for i, (_, total_points) in enumerate(zip(num_goals_list, total_num_points_list)):
    # Append data to the corresponding lists for box plots
    total_points_data.append(total_points)
    actual_points_data.append(actual_num_points_list[i])
    # Extract the number of robots from the file name
    num_robots = int(data_files[i].split("_")[2])
    num_robots_list.append(num_robots)



boxprops = dict(linewidth=2, color='black')  # Style for the box outline
whiskerprops = dict(linewidth=2, color='black')  # Style for the whiskers
medianprops = dict(linewidth=2, color='red')  # Style for the median line

# Calculate the x-axis positions for the boxes
x_positions_total = np.arange(1, len(total_points_data) * 4 + 1, 4)
x_positions_actual = np.arange(2, len(actual_points_data) * 4 + 2, 4)

# Create the box plots and get the artists
total_boxes = plt.boxplot(total_points_data, positions=x_positions_total,
                         patch_artist=True, boxprops=boxprops, whiskerprops=whiskerprops, medianprops=medianprops)

actual_boxes = plt.boxplot(actual_points_data, positions=x_positions_actual,
                          patch_artist=True, boxprops=boxprops, whiskerprops=whiskerprops, medianprops=medianprops)

# Set the colors of the box plots
for box in total_boxes['boxes']:
    box.set_facecolor('lightblue')
for box in actual_boxes['boxes']:
    box.set_facecolor('lightgreen')

# Set the labels for the x-axis based on the simulation number and number of robots
x_labels = []
for i, num_robots in enumerate(num_robots_list):
    simulation_label = f'S{int(data_files[i].split("_")[1])}'
    
    
    x_labels.append(f'{simulation_label}\n({num_robots}R)')

plt.xticks(np.mean([x_positions_total, x_positions_actual], axis=0), x_labels,fontsize=14)

# Create custom artists for the legend
total_patch = plt.Line2D([], [], color='lightblue', marker='o', markersize=14, label='Total Points Detected')
actual_patch = plt.Line2D([], [], color='lightgreen', marker='o', markersize=14, label='Actual Points Used')

# Set the legend with the custom artists and mean line
plt.legend(handles=[total_patch, actual_patch])

plt.xlabel('Simulations',fontsize=14)
plt.ylabel('# of points',fontsize=14)
plt.grid(True)
# Show the plot
plt.show()

"""


################################## RADIUS VALUES USED ##################################
# Plotting the data for the map occupancy
'''
plt.figure(figsize=(9, 6))

#plt.hlines(1.0, xmin=num_goals[0], xmax=num_goals[-1], color='r', label='First value of radius')


for i, (goals, radius_values) in enumerate(zip(num_goals_list, radius_values_list)):
    _simulation_number = int(data_files[i].split("_")[1])
    print(goals)
    print(radius_values)

    plt.scatter(goals, radius_values, marker='x', s=50,
                   label=f'Simulation {_simulation_number} - Radius Values')
    #plt.plot(goals, radius_values)

plt.xlabel('Number of goals')
plt.ylabel('Radius Values')
plt.legend()
plt.title('Radius Values and number of goals Used')
plt.grid(True)

# Min and max for plot
min_y = np.min([np.min(y) for y in radius_values])  # Minimum value over all simulations
max_y = np.max([np.max(y) for y in radius_values])  # Maximum value over all simulations

plt.ylim(min_y - 0.25, max_y + 0.25)

# Adjust the figure
#plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.4)

# Show the plot
plt.show()

'''

################################## PERCENTAGE VALUES USED ##################################
'''
# Plotting the data for the map occupancy
plt.figure(figsize=(16, 9))

plt.hlines(60.0, xmin=num_goals[0], xmax=num_goals[-1], color='r', label='First value of radius')
for i, (goals, percentage_values) in enumerate(zip(num_goals_list, percentage_values_list)):
    _simulation_number = int(data_files[i].split("_")[1])
    plt.scatter(goals, percentage_values, marker='x', s=50,
                   label=f'Simulation {_simulation_number} - Percentage Values')

plt.xlabel('Number of goals')
plt.ylabel('Percentage Values')
plt.legend()
plt.title('Percentage Values Used')
plt.grid(True)

# Min and max for plot
min_y = np.min([np.min(y) for y in percentage_values])  # Minimum value over all simulations
max_y = np.max([np.max(y) for y in percentage_values])  # Maximum value over all simulations

plt.ylim(min_y - 0.5, max_y + 0.5)

# Adjust the figure
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.4)

# Show the plot
plt.show()
'''

################################## RADIUS  and percentage values used percentage ##################################

def calculate_average(values):
    total = sum(values)
    average = total / len(values)
    return average
# Plotting the data for the map occupancy
"""

percentage_60_list =[]
percentage_50_list=[]
percentage_less_than_40_list=[]

percentage_1_00_list =[]
percentage_1_25_list=[]
percentage_greater_than_1_50_list=[]
percentage_less_than_0_list=[]


print(f"num_simulations = {num_simulations}")

for i in range(0, 1):
    for i, (perc_values_, radius_values_) in enumerate(zip(percentage_values_list, radius_values_list)):
        _simulation_number = int(data_files[i].split("_")[1])

        print(f"perc_values_ = {perc_values_} file = {_simulation_number} count = {i}")
        print(f"radius_values_= {radius_values_} file = {_simulation_number} count = {i}")
        #print(f"radius_values_ = {radius_values_}")
        # Count occurrences of each value
        count_60 = perc_values_.count(60)
        count_50 = perc_values_.count(50)
        count_less_than_40 = sum(1 for value in perc_values_ if value <= 40)

        count_1_00 = radius_values_.count(1.00)
        count_1_25 = radius_values_.count(1.25)
        count_greater_than_1_50 = sum(1 for value in radius_values_ if value >= 1.50)
        count_less_than_0 = sum(1 for value in radius_values_ if value <= 0.00)


        # Calculate percentages
        total_values = len(perc_values_)
        percentage_60 =  (count_60 / total_values) * 100
        percentage_50 = (count_50 / total_values) * 100
        percentage_less_than_40 = (count_less_than_40 / total_values) * 100


        # Calculate radius
        total_values = len(radius_values_)
        percentage_1_00 =  ( count_1_00 / total_values) * 100
        percentage_1_25 = ( count_1_25 / total_values) * 100
        percentage_greater_than_1_50 = (count_greater_than_1_50 / total_values) * 100
        percentage_less_than_0  = (count_less_than_0 / total_values) * 100
        
        percentage_60_list.append(percentage_60)
        percentage_50_list.append(percentage_50)
        percentage_less_than_40_list.append(percentage_less_than_40)

        percentage_1_00_list.append(percentage_1_00)
        percentage_1_25_list.append(percentage_1_25)
        percentage_greater_than_1_50_list.append(percentage_greater_than_1_50)
        percentage_less_than_0_list.append(percentage_less_than_0)


#print("Percentage of 60:", (percentage_60_list))
#print("Percentage of 50:", (percentage_50_list))
print("Percentage greater than 1.50:", (percentage_greater_than_1_50_list))
# Print results
print("Average Percentage of 60:", calculate_average(percentage_60_list))
print("Average Percentage of 50:", calculate_average(percentage_50_list))
print("Average Percentage less than 40:", calculate_average(percentage_less_than_40_list))

# Print results
print("Average Percentage of 1.00:", calculate_average(percentage_1_00_list))
print("Average Percentage of 1.25 :", calculate_average(percentage_1_25_list))
print("Average Percentage greater than 1.50:", calculate_average(percentage_greater_than_1_50_list))
print("Average Percentage  percentage_less_than_0:", calculate_average(percentage_less_than_0_list))

"""

################################## CPU USAGE ##################################
# Plotting the data for the map occupancy

'''
plt.figure(figsize=(16, 9))

# Plot the merged map occupation over time for each simulation
for i in range(num_simulations):
    _simulation_number = int(data_files[i].split("_")[1])
    plt.plot(np.array(cpu_time_list[i]) - cpu_time_list[i][0], cpu_percentages_list[i],
             label=f'Simulation {_simulation_number} - CPU Usage over time with {num_robots_list[i]} Robots')

plt.xlabel('Time [s]')
plt.ylabel('Percentage CPU used')
plt.legend()
plt.title('CPU Usage')
plt.grid(True)

plt.ylim(0, 100)

# Adjust the figure
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.4)

# Show the plot
plt.show()

################################## GPU USAGE ##################################

if gpu_time != []:
    # Plotting the data for the map occupancy
    plt.figure(figsize=(16, 9))

    # Plot the merged map occupation over time for each simulation
    for i in range(num_simulations):
        _simulation_number = int(data_files[i].split("_")[1])
        plt.plot(np.array(gpu_time_list[i]) - gpu_time_list[i][0], gpu_percentages_list[i],
                label=f'Simulation {_simulation_number} - GPU Usage over time with {num_robots_list[i]} Robots')
        plt.plot(np.array(gpu_time_list[i]) - gpu_time_list[i][0], gpu_memory_list[i],
                label=f'Simulation {_simulation_number} - GPU Memory Usage over time with {num_robots_list[i]} Robots')
        
    plt.xlabel('Time [s]')
    plt.ylabel('Percentage GPU used')
    plt.legend()
    plt.title('GPU Usage')
    plt.grid(True)

    plt.ylim(0, 100)

    # Adjust the figure
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.2, hspace=0.4)

    # Show the plot
    plt.show()
'''

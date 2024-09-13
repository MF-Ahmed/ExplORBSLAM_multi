import os
import time
import subprocess
import signal
simtime  = 16*60 # 45 mins
# Set the paths to the ROS1 and ROS2 installations
ros1_path_setup_distro = "/opt/ros/noetic"
ros1_path_setup_ws = "~/data/ExplOrbSLAM_working/devel"
ros2_path_setup_distro = "/opt/ros/foxy"
ros2_path_setup_ws = "~/data/ros2_ws/install"

# Define ROS1 commands
ros1_roscore_cmd = "roscore"
ros1_simulation_cmd = "roslaunch graph_d_exploration file_warehouse.launch"
ros1_karto_cmd = "roslaunch graph_d_exploration multiple.launch"
ros1_mergedmap_info = "roslaunch frontier_detector map_area.launch"
ros1_centralised = "roslaunch graph_d_exploration servers.launch"
ros1_plottingNode = "rosrun plotting plot.py"

ros1_killplotnode = "rosnode kill /plotter_node"
ros1_mapserver = "rosrun map_server map_server  /home/usr/data/ExplOrbSLAM_working/maps/warehouse/ware_house_map.yaml"
ros1_mapsaver = "rosrun map_server map_saver -f /home/usr/data/ExplOrbSLAM_working/OG_maps/warehouse/$map_$(date +'%Y%m%d_%H%M%S') map:=/mergedmap"

run_lawn_mover = "python3 /home/usr/data/ExplOrbSLAM_working/src/src/robot_description/src/python/lawn_mower_warehouse.py"

ros1_iou_cmd = "roslaunch frontier_detector iou.launch"

ros1_map_merge_cmd = "rosrun frontier_detector frontier_detector_mapMerger 2"

# Define ROS2 commandss
ros2_bridge_cmd = "ros2 run ros1_bridge dynamic_bridge"
ros2_map_merge_cmd = "ros2 launch map_merge map_merge_launch.py num_robots:=3 num_drones:=1"


# Function to run each terminal
def launch_terminal(cmd, title=None, ros1=True):
    title_option = f'--title="{title}"' if title else ''
    if ros1:
        setup_distro_path = ros1_path_setup_distro
        setup_ws_path = ros1_path_setup_ws
    else:
        setup_distro_path = ros2_path_setup_distro
        setup_ws_path = ros2_path_setup_ws

    os.system(
        f"gnome-terminal {title_option} --window -- zsh -c 'source {setup_distro_path}/setup.zsh; source {setup_ws_path}/setup.zsh; {cmd}; exec zsh'")

def main():
    # Launch terminals and store the process objects
    launch_terminal(ros1_roscore_cmd, "ROSCORE", ros1=True) 
    time.sleep(2)


    launch_terminal(ros1_mapserver, "ros1_mapserver", ros1=True)
    print("ros1_mapserver  ...")

    time.sleep(2)

    print("[IMPORTANT] Plotting Node Started")
    launch_terminal(ros1_plottingNode, "Plotting Node Started", ros1=True) 
    time.sleep(10)
    #input("Press to start the simulation [Enter]: ")

    launch_terminal(ros1_simulation_cmd, "ROS1 SIMULATION", ros1=True)
    print("Simulation starting ...")
    time.sleep(5)
    time.sleep(5)
    
    # Wait for user input to kill all processes
    print("")
    print("")
    #input("Press to start the ROS bridge, the map merger node and the servers [Enter]: ")

    
    #time.sleep(10)
    #launch_terminal(run_lawn_mover, "lawn_mover", ros1=True)
    #print("lawn mover pattern ...")
    #print("")


    launch_terminal(ros1_map_merge_cmd, "ros1_map_merge_cmd", ros1=True)
    print("")
    print("ros1_map_merge_cmd ...")
    time.sleep(5)
    time.sleep(5)

    
    launch_terminal(ros2_bridge_cmd, "ROS2 BRIDGE", ros1=False)
    print("")
    print("ROS bridge starting ...")
    time.sleep(5)
    launch_terminal(ros2_map_merge_cmd, "ROS2 MAP MERGE", ros1=False)
    print("")
    print("Map merge starting ...")
    time.sleep(5)
   
  
    launch_terminal(ros1_centralised, "CENTRALISED SERVER", ros1=True)
    print("")
    print("Servers starting ...")
    time.sleep(5)
    time.sleep(5)
   
    print("")
    print("")

    launch_terminal(ros1_karto_cmd, "CONTROLLER", ros1=True)
    print("Controller starting ...")
    print("")
    print("")
    time.sleep(5)
    time.sleep(5)
    

    launch_terminal(ros1_mergedmap_info, "ros1_mergedmap_info", ros1=True)
    print("ros1_mergedmap_info...")
    print("")
    print("")
    time.sleep(5)

  
    launch_terminal(ros1_iou_cmd , "ros1_iou_cmd ", ros1=True)
    print("ros1_iou_cmd  ...")
    print("")  
    time.sleep(5)

            
    #print("[IMPORTANT] Stop the data collector before")
    input("Kill all processes [Enter]: ")
    time.sleep(5)
    
    #launch_terminal(ros1_killplotnode, "ros1_killplotnode", ros1=True)
    #print("ros1_killplotnode ...")
    #print("") 
    #time.sleep(5)   
    # 
    # 
    #print("Saving the Map before Exiting ...")
    #launch_terminal(ros1_mapsaver, "Save to Merged Map", ros1=True)
    #time.sleep(10) 

    os.system("pkill -f gnome-terminal")
    #Close all terminals
    #Kill all processes containing "gnome-terminal" in the name
    #input("Kill all processes [Enter]: ")   

if __name__ == "__main__":
    #for i in range(20):
        main()  
        #time.sleep(simtime)    
        #print("Saving the Map before Exiting ...")
        #launch_terminal(ros1_mapsaver, "Save to Merged Map", ros1=True)
        #time.sleep(10)
        #launch_terminal(ros1_killplotnode, "plotiing node kill", ros1=True)
        #time.sleep(10)  
        #os.system("pkill -f gnome-terminal")
        #time.sleep(10)
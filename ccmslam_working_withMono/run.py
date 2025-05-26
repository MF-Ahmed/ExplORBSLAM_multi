import os
import time
import subprocess
import signal

# Set the paths to the ROS1 and ROS2 installations
ros1_path_setup_distro = "/opt/ros/noetic"
ros1_path_setup_ws = "~/data/ExplOrbSLAM_working/devel"

# Define ROS1 commands
ros1_roscore_cmd = "roscore"
ros_simulation_cmd = "roslaunch robot_description single_house.launch"
ccmslam_server_cmd = "roslaunch ccmslam Server.launch"

client0_cmd = "roslaunch ccmslam Client0_euroc.launch"
client1_cmd = "roslaunch ccmslam Client1_euroc.launch"


#rosbag_agent0 = "rosbag play /home/usr/data/ExplOrbSLAM_working/rosbags/robot_1_camera.bag"
#rosbag_agent1 = "rosbag play /home/usr/data/ExplOrbSLAM_working/rosbags/robot_2_camera.bag cam0/image_raw:=/robot_2/camera/rgb/image_raw"

rosbag_agent0 = "rosbag play /media/usr/Data/DataSets/EuRoC/Rosbags/MH_01_easy.bag --start 45"
rosbag_agent1 = "rosbag play /media/usr/Data/DataSets/EuRoC/Rosbags/MH_02_easy.bag --start 35 /cam0/image_raw:=/cam0/image_raw1"

rviz_launch = "roslaunch ccmslam rviz.launch"

save_maps_ser = "rosservice call ccmslam/ccmslam_savemap 0"


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

    launch_terminal(ros_simulation_cmd, "ROS1 SIMULATION", ros1=True)
    print("Simulation starting  with 2 RosBots and 1 Drone  ...")
      
    # Wait for user input to kill all processes
    print("")
    print("")
    time.sleep(2)
    
    #time.sleep(10)
    #input("Press to start the simulation [Enter]: ")

    launch_terminal(ccmslam_server_cmd , "ccmslam_server_cmd ", ros1=True)
    print("ccmslam_server_cmd  ...")
      
    # Wait for user input to kill all processes
    #print("")
    #print("")
    time.sleep(5)
    
    launch_terminal(client0_cmd  , "client0_cmd", ros1=True)
    print("client0_cmd   ...")
      
    # Wait for user input to kill all processes
    #print("")
    #print("")    
    
    time.sleep(2)
    
    #launch_terminal(client1_cmd  , " client1_cmd", ros1=True)
    #print("client1_cmd   ...")
      
    # Wait for user input to kill all processes
    #print("")
    #print("")    
    
    time.sleep(2)      
   
   
    #launch_terminal(rosbag_agent0  , "rosbag_agent0", ros1=True)
    #print("rosbag_agent0  ...")
      
    # Wait for user input to kill all processes
    #print("")
    #print("")    
    
    #time.sleep(2)    
            
    #launch_terminal(rosbag_agent1  , "rosbag_agent1", ros1=True)
    #print("rosbag_agent1  ...")
      
    # Wait for user input to kill all processes

    launch_terminal(rviz_launch, "rviz_launch", ros1=True)
    print("rviz_launch  ...")
      
    # Wait for user input to kill all processes

             
    #input("Save maps [Enter]: ")
    #launch_terminal(save_maps_ser, "saving_the_maps", ros1=True)
    #print("saving the maps before exiting ......")
    
    #time.sleep(10)
    input("To exit hit [Enter]: ")
    print("Shutting down and exiting ......")
    os.system("pkill -f gnome-terminal")

if __name__ == "__main__":
    main()  

        



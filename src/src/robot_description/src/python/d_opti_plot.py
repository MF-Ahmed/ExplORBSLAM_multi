#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
from datetime import datetime


def callback(data, robot_num):
    values[robot_num].append(data.data)
    times[robot_num].append(rospy.Time.now().to_sec())  # Store the current ROS time
    rospy.loginfo(f"In d_opti_callback for robot_{robot_num} Got data = {data.data}")

    # Clear the plot
    plt.clf()

    # Plot all data again
    for i in range(len(topics)):
        plt.plot(times[i], values[i], 'o-', label=f'Robot {i}', linewidth=2, markersize=6)
      

    plt.ylim(0, 14) 
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Edge D-optimality', fontsize=12)
    plt.title('Uncertainaty evolution', fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()      
    plt.tight_layout()  # Improve spacing between subplots
    
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    file_name = f"/home/usr/data/ExplOrbSLAM_working/src/src/results/d_optiplot/d_opti_graph.png"
    plt.savefig(file_name, dpi=300)

if __name__ == '__main__':
    rospy.init_node('d_opti_plot')
    rospy.loginfo("d_opti_plot node initialized") 


    topics = [rospy.get_param('~topic_robot_0', 'robot_0/d_optimality_publisher/Dopt/'),
              rospy.get_param('~topic_robot_1', 'robot_1/d_optimality_publisher/Dopt/')]
    values = [[] for _ in range(len(topics))]  # Store the received values
    times = [[] for _ in range(len(topics))]

    plt.figure()  # Create a new figure
    for i, topic in enumerate(topics):
        rospy.Subscriber(topic, Float32, callback, callback_args=i)
        
    rospy.spin()

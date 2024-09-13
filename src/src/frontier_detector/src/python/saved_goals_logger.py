#!/usr/bin/env python3
#!/usr/bin/env python

import rospy
import csv
import os
from datetime import datetime
from visualization_msgs.msg import MarkerArray

# Calculate the relative path for the CSV file with date and time
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
relative_dir = os.path.join(os.path.dirname(__file__), '../../../saved_goals/')
relative_path = os.path.join(relative_dir, f'saved_goals_{timestamp}.csv')

# Ensure the directory exists
os.makedirs(relative_dir, exist_ok=True)

# Initialize the CSV file with header if it doesn't exist
with open(relative_path, mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Topic', 'X', 'Y'])  # CSV header

# Callback function for robot_0
def callback_robot_0(data):
    with open(relative_path, mode='a') as file:
        writer = csv.writer(file)
        for marker in data.markers:  # Iterate over markers in MarkerArray
            position = marker.pose.position
            writer.writerow(['robot_0', position.x, position.y])

# Callback function for robot_1
def callback_robot_1(data):
     with open(relative_path, mode='a') as file:
        writer = csv.writer(file)
        for marker in data.markers:  # Iterate over markers in MarkerArray
            position = marker.pose.position
            writer.writerow(['robot_1', position.x, position.y])

def listener():
    rospy.init_node('saved_goals_to_csv', anonymous=True)
    
    rospy.Subscriber('/robot_0/visualization_markerArray/saved_goals', MarkerArray, callback_robot_0)
    rospy.Subscriber('/robot_1/visualization_markerArray/saved_goals', MarkerArray, callback_robot_1)
                       



    
    rospy.spin()

if __name__ == '__main__':
    listener()

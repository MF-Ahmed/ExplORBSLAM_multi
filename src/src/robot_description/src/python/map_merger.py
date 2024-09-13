#!/usr/bin/env python3


import rospy
import tf2_ros
from tf2_geometry_msgs import PointStamped
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped, TransformStamped
import numpy as np

class MapMerger:
    def __init__(self):
        rospy.init_node('map_merger', anonymous=True)
        self.merged_map_pub = rospy.Publisher('/merged_map', OccupancyGrid, queue_size=10)
#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid

class MapMerger:
    def __init__(self):
        rospy.init_node('map_merger', anonymous=True)
        self.merged_map_pub = rospy.Publisher('/merged_map', OccupancyGrid, queue_size=10)
        self.map1_sub = rospy.Subscriber('/robot_1/gridmapper/projected_map', OccupancyGrid, self.map1_callback)
        self.map2_sub = rospy.Subscriber('/robot_2/gridmapper/projected_map', OccupancyGrid, self.map2_callback)
        self.merged_map = OccupancyGrid()

    def map1_callback(self, map1_msg):
        # If merged_map is not initialized, set it based on the first map
        if not self.merged_map.data:
            self.merged_map = map1_msg
        else:
            # Merge the two maps by taking the maximum probability value for each cell
            self.merged_map.data = [
                max(p1, p2) for p1, p2 in zip(self.merged_map.data, map1_msg.data)
            ]

        self.publish_merged_map()

    def map2_callback(self, map2_msg):
        # If merged_map is not initialized, set it based on the second map
        if not self.merged_map.data:
            self.merged_map = map2_msg
        else:
            # Merge the two maps by taking the maximum probability value for each cell
            self.merged_map.data = [
                max(p1, p2) for p1, p2 in zip(self.merged_map.data, map2_msg.data)
            ]

        self.publish_merged_map()

    def publish_merged_map(self):
        # Publish the merged map
        self.merged_map.header.stamp = rospy.Time.now()
        self.merged_map.header.frame_id = 'global_map'
        self.merged_map_pub.publish(self.merged_map)

if __name__ == '__main__':
    try:
        map_merger = MapMerger()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
import numpy as np

# Merge map function independet from the number of agents involved
def merge_maps(*maps):
    if not maps:
        return None

    # Get the min x-y and max x-y coordinates
    min_x = min(map_.info.origin.position.x for map_ in maps)
    min_y = min(map_.info.origin.position.y for map_ in maps)
    max_x = max(map_.info.origin.position.x + (map_.info.width * map_.info.resolution) for map_ in maps)
    max_y = max(map_.info.origin.position.y + (map_.info.height * map_.info.resolution) for map_ in maps)

    # Compute the resolution of the merged map
    merged_resolution = min(map_.info.resolution for map_ in maps)

    # Compute the dimensions of the merged map
    merged_width = int(np.ceil((max_x - min_x) / merged_resolution))
    merged_height = int(np.ceil((max_y - min_y) / merged_resolution))

    # Initialize the merged map
    merged_data = [-1] * (merged_width * merged_height)

    # Merge the maps
    for map_ in maps:
        for y in range(map_.info.height):
            for x in range(map_.info.width):
                i = x + y * map_.info.width
                merged_x = int(np.floor((map_.info.origin.position.x + x * map_.info.resolution - min_x) / merged_resolution))
                merged_y = int(np.floor((map_.info.origin.position.y + y * map_.info.resolution - min_y) / merged_resolution))
                merged_i = merged_x + merged_y * merged_width
                if merged_data[merged_i] == -1:
                    merged_data[merged_i] = map_.data[i]

    # Create the merged map message
    merged_map = OccupancyGrid()
    merged_map.header = maps[0].header
    merged_map.header.frame_id = 'map'
    merged_map.info.origin.position.x = min_x
    merged_map.info.origin.position.y = min_y
    merged_map.info.resolution = merged_resolution
    merged_map.info.width = merged_width
    merged_map.info.height = merged_height
    merged_map.data = merged_data

    return merged_map

class MapMerger(Node):
    def __init__(self):
        super().__init__('merge_map_node')

        self.declare_parameter('num_robots', 0)

        # Get the number of robots parameter
        num_robots = self.get_parameter('num_robots').get_parameter_value().integer_value

        # Print Log
        self.get_logger().info(f"Merging maps from {num_robots} robots.")
        
        # Subscribers
        self.subscribers = []
        for i in range(num_robots):
            callback_method = self.create_callback(i)
            subscriber = self.create_subscription(
                OccupancyGrid,
                f'/robot_{i}/map',
                callback_method,
                10
            )
            self.subscribers.append(subscriber)

        # Publisher
        self.merged_pub = self.create_publisher(OccupancyGrid, '/map', 10)

        # Variables to monitor data storage
        self.maps_received = [False] * num_robots
        self.maps = [None] * num_robots

    # Create callbacks in a dynamic way
    def create_callback(self, robot_id):
        def callback(msg):
            self.map_callback(msg, robot_id)
        return callback

    # Function to store the information of each callback related to the correct subscriber
    def map_callback(self, msg, robot_id):
        self.maps[robot_id] = msg
        self.maps_received[robot_id] = True

        if all(self.remove_element(self.maps_received, robot_id)):
            merged_map = merge_maps(*self.maps)
            self.merged_pub.publish(merged_map)

    # Remove the element in the robot_id position in order to analyse all the other easily
    def remove_element(self, arr, robot_id):
        return np.delete(arr, robot_id, axis=0)


# main
def main(args=None):
    rclpy.init(args=args)
    map_merger = MapMerger()
    rclpy.spin(map_merger)
    map_merger.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


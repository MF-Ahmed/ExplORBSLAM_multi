#!/usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np
import cv2
import yaml

class MapRotator:
    def __init__(self):
        rospy.init_node('map_rotator')
        rospy.loginfo("Map rotate node started")
        self.map_sub = rospy.Subscriber('/drone_map', OccupancyGrid, self.map_callback)
        self.rotation_angle_degrees = 45  # Set the rotation angle in degrees

    def map_callback(self, original_map):
        rospy.loginfo("In map callback")
        rospy.loginfo(f"Original map header frame_id: {original_map.header.frame_id}")

        # Convert OccupancyGrid data to a 2D numpy array
        map_data = np.array(original_map.data).reshape((original_map.info.height, original_map.info.width))
        rospy.loginfo(f"Map data shape: {map_data.shape}")

        # Rotate the map data
        rotated_map_data = self.rotate_map(map_data, self.rotation_angle_degrees)

        # Save rotated map as .pgm file
        map_filename = 'rotated_map.pgm'
        self.save_pgm(map_filename, rotated_map_data)

        # Save map metadata as .yaml file
        yaml_filename = 'rotated_map.yaml'
        self.save_yaml(yaml_filename, original_map, rotated_map_data)

    def rotate_map(self, map_data, rotation_angle_degrees):
        # Perform map rotation using OpenCV
        center = tuple(np.array(map_data.shape[::-1]) / 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle_degrees, 1.0)
        rotated_map_data = cv2.warpAffine(map_data.astype(np.uint8), rotation_matrix, map_data.shape[::-1], flags=cv2.INTER_NEAREST)
        return rotated_map_data

    def save_pgm(self, filename, map_data):
        # Save map data as .pgm image file
        with open(filename, 'wb') as f:
            f.write(b'P5\n')
            f.write(b'# Occupancy Grid Map\n')
            f.write(f"{map_data.shape[1]} {map_data.shape[0]}\n".encode())
            f.write(b'255\n')
            np.flipud(map_data).tofile(f)

    def save_yaml(self, filename, original_map, rotated_map_data):
        # Save map metadata as .yaml file
        resolution = original_map.info.resolution
        origin = original_map.info.origin.position
        yaml_data = {
            'image': 'rotated_map.pgm',
            'resolution': resolution,
            'origin': {'x': origin.x, 'y': origin.y},
            'negate': False,
            'occupied_thresh': 0.65,
            'free_thresh': 0.196
        }
        with open(filename, 'w') as f:
            yaml.dump(yaml_data, f)

if __name__ == '__main__':
    MapRotator()
    rospy.spin()

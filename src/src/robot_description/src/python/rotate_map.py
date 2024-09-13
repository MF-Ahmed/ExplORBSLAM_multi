#!/usr/bin/env python3
import numpy as np
from PIL import Image
import yaml

def rotate_image(image_path, angle):
    # Open an image file
    with Image.open(image_path) as img:
        # Rotate image
        rotated_img = img.rotate(angle, expand=True)
        # Save rotated image
        rotated_img.save(image_path)

def update_yaml(yaml_path):
    with open(yaml_path, 'r') as file:
        map_data = yaml.safe_load(file)

    # Flip the origin coordinates
    map_data['origin'][0] = -map_data['origin'][0]
    map_data['origin'][1] = -map_data['origin'][1]

    with open(yaml_path, 'w') as file:
        yaml.dump(map_data, file)

if __name__ == '__main__':
    image_path = 'my_map.pgm'
    yaml_path = 'my_map.yaml'
    angle = 180

    rotate_image(image_path, angle)
    update_yaml(yaml_path)


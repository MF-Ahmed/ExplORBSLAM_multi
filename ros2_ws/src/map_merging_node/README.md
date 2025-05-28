# Map merging node

Refer to this [README](https://github.com/mmatteo-hub/thesis_ws/blob/karto_slam/README.md) to sintall and use it.

Reger to [this](https://github.com/ros2/ros1_bridge/tree/foxy) repository to download and install the ros bridge. You find the submodule attached [here](https://github.com/mmatteo-hub/map_merging_node/tree/main/src)


# Run the code
To run the code it is needed:
* run the ros bridge (here from ROS1 Noetic and ROS2 Foxy)
```bash
ros2 run ros1_bridge dynamic_bridge
```
* run the map merging node
```bash
ros2 launch merge_map merge_map_launch.py num_robots:={num_robots}
```
where `num_robots` is an integer value which represent the number of agents currectly eorking in the simulation. <br>
It is important to set is correctly because:
* if it is less than the real number of agents, then the map will miss some parts;
* if it is higher thatn the real number of agents, then the code will wait until it has enough agents.
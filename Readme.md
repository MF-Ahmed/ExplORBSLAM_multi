# Active Collaborative Visual SLAM Exploiting ORB Features

This branch implements the work presented in our paper cited below, in which we present an efficient visual AC-SLAM method using aerial and ground robots for environment exploration and mapping. We propose an efficient frontier filtering method that takes into account the common IoU map frontiers and reduces the frontiers for each robot. Additionally, we present an approach to guide robots to previously visited goal positions to promote loop closure and reduce SLAM uncertainty.

**M. F. Ahmed, V. Frémont, and I. Fantoni, "Active Collaborative Visual SLAM Exploiting ORB Features," 2024 18th International Conference on Control, Automation, Robotics and Vision (ICARCV), Dubai, United Arab Emirates, 2024, pp. 966-971, doi: 10.1109/ICARCV63323.2024.10821699.**

Kindly cite this paper if you use this implementation.

## Overview
This implementation works with multiple robots and includes:
1. Matrix regularization.
2. Path entropy incorporation.

This branch is set up for ROS Noetic and Ubuntu 20.04.

## Dependencies
To install the necessary dependencies, run the following commands:

### General Dependencies
1. `pip install scipy==1.5.2`
2. `pip install networkx==2.6.3`
3. `sudo apt-get install python3-pybind11`
4. `pip install sophuspy==0.0.8`
5. `pip install numba==0.57.1`
6. `pip install numpy==1.21.1`

### ORB-SLAM2 Dependencies
1. Clone the ORB-SLAM2 repository and follow its installation instructions:
   ```bash
   git clone https://github.com/raulmur/ORB_SLAM2.git
   cd ORB_SLAM2
   ./build.sh

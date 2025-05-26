# Install script for directory: /home/farhan/data/ExplOrbSLAM_ws/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/farhan/data/ExplOrbSLAM_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/farhan/data/ExplOrbSLAM_ws/install/_setup_util.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/farhan/data/ExplOrbSLAM_ws/install" TYPE PROGRAM FILES "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/_setup_util.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/farhan/data/ExplOrbSLAM_ws/install/env.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/farhan/data/ExplOrbSLAM_ws/install" TYPE PROGRAM FILES "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/env.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/farhan/data/ExplOrbSLAM_ws/install/setup.bash;/home/farhan/data/ExplOrbSLAM_ws/install/local_setup.bash")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/farhan/data/ExplOrbSLAM_ws/install" TYPE FILE FILES
    "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/setup.bash"
    "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/local_setup.bash"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/farhan/data/ExplOrbSLAM_ws/install/setup.sh;/home/farhan/data/ExplOrbSLAM_ws/install/local_setup.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/farhan/data/ExplOrbSLAM_ws/install" TYPE FILE FILES
    "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/setup.sh"
    "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/local_setup.sh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/farhan/data/ExplOrbSLAM_ws/install/setup.zsh;/home/farhan/data/ExplOrbSLAM_ws/install/local_setup.zsh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/farhan/data/ExplOrbSLAM_ws/install" TYPE FILE FILES
    "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/setup.zsh"
    "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/local_setup.zsh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/farhan/data/ExplOrbSLAM_ws/install/setup.fish;/home/farhan/data/ExplOrbSLAM_ws/install/local_setup.fish")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/farhan/data/ExplOrbSLAM_ws/install" TYPE FILE FILES
    "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/setup.fish"
    "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/local_setup.fish"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/farhan/data/ExplOrbSLAM_ws/install/.rosinstall")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/farhan/data/ExplOrbSLAM_ws/install" TYPE FILE FILES "/home/farhan/data/ExplOrbSLAM_ws/build/catkin_generated/installspace/.rosinstall")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/farhan/data/ExplOrbSLAM_ws/build/gtest/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/catkin_simple/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_models/hector_components_description/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_models/hector_models/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_moveit/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector-moveit-working/src/hector_moveit_gazebo/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector-moveit-working/src/hector_moveit_gazebo_worlds/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector-moveit-working/src/hector_moveit_perception/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_demo/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_description/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_models/hector_sensors_description/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_models/hector_xacro_tools/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_uav_msgs/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector-moveit-working/src/hector_moveit_actions/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector-moveit-working/src/hector_moveit_gazebo_plugins/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_model/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/src/plotting/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/src/graph_d_exploration/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_gazebo_plugins/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_pose_estimation/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/src/3dParty/orb_slam_2_ros/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/src/frontier_detector/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_interface/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_actions/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_controllers/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_teleop/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_controller_gazebo/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector_quadrotor/hector_quadrotor_gazebo/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/src/3dParty/kobuki_plugins/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector-moveit-working/src/hector_moveit_rviz_plugins/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector-moveit-working/src/hector_moveit_exploration/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/hector-moveit-working/src/hector_moveit_config/cmake_install.cmake")
  include("/home/farhan/data/ExplOrbSLAM_ws/build/src/robot_description/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/farhan/data/ExplOrbSLAM_ws/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")

# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/usr/data/ExplOrbSLAM_working/src/navigation/map_server

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/usr/data/ExplOrbSLAM_working/build/map_server

# Utility rule file for clean_test_results_map_server.

# Include the progress variables for this target.
include CMakeFiles/clean_test_results_map_server.dir/progress.make

CMakeFiles/clean_test_results_map_server:
	/usr/bin/python3 /opt/ros/noetic/share/catkin/cmake/test/remove_test_results.py /home/usr/data/ExplOrbSLAM_working/build/map_server/test_results/map_server

clean_test_results_map_server: CMakeFiles/clean_test_results_map_server
clean_test_results_map_server: CMakeFiles/clean_test_results_map_server.dir/build.make

.PHONY : clean_test_results_map_server

# Rule to build all files generated by this target.
CMakeFiles/clean_test_results_map_server.dir/build: clean_test_results_map_server

.PHONY : CMakeFiles/clean_test_results_map_server.dir/build

CMakeFiles/clean_test_results_map_server.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/clean_test_results_map_server.dir/cmake_clean.cmake
.PHONY : CMakeFiles/clean_test_results_map_server.dir/clean

CMakeFiles/clean_test_results_map_server.dir/depend:
	cd /home/usr/data/ExplOrbSLAM_working/build/map_server && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/usr/data/ExplOrbSLAM_working/src/navigation/map_server /home/usr/data/ExplOrbSLAM_working/src/navigation/map_server /home/usr/data/ExplOrbSLAM_working/build/map_server /home/usr/data/ExplOrbSLAM_working/build/map_server /home/usr/data/ExplOrbSLAM_working/build/map_server/CMakeFiles/clean_test_results_map_server.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/clean_test_results_map_server.dir/depend


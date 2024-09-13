#include <ros/ros.h>
#include <nav_msgs/OccupancyGrid.h>
#include <vector>
#include <algorithm>
#include <cmath>

using nav_msgs::OccupancyGrid;

class MapMerger {
public:
    MapMerger(int num_robots) : num_robots_(num_robots) {
        ros::NodeHandle nh("~");

        //ROS_INFO("Merging maps from %d robots.", num_robots_);

        // Subscribe to robot/gridmapper/projected_map topics dynamically
        for (int i = 0; i < num_robots_; ++i) {
            std::string topic_name = "/robot_" + std::to_string(i) + "/gridmapper/projected_map";
            ros::Subscriber sub = nh.subscribe<OccupancyGrid>(topic_name, 10, boost::bind(&MapMerger::mapCallback, this, _1, i));
            subscribers_.push_back(sub);
        }

        merged_pub_ = nh.advertise<OccupancyGrid>("/mergedmap_robots", 10);
        maps_received_ = std::vector<bool>(num_robots_, false);
        maps_ = std::vector<OccupancyGrid::ConstPtr>(num_robots_, nullptr);
    }

private:
    void mapCallback(const OccupancyGrid::ConstPtr& msg, int robot_id) {
        maps_[robot_id] = msg;
        maps_received_[robot_id] = true;

        //ROS_INFO("In Map callback for robot %d.", robot_id);
        for (int i = 0; i < maps_received_.size(); ++i) {
            //ROS_INFO("Robot %d: %s", i, maps_received_[i] ? "Received" : "Not received");
        }

        if (std::all_of(maps_received_.begin(), maps_received_.end(), [](bool received) { return received; })) {
            //ROS_INFO("All maps received. Merging maps...");
            OccupancyGrid merged_map = mergeMaps(maps_);
            merged_pub_.publish(merged_map);
            //ROS_INFO("Merged Map published !!");
        }
    }

    OccupancyGrid mergeMaps(const std::vector<OccupancyGrid::ConstPtr>& maps) {
        if (maps.empty()) {
            ROS_INFO("Input map is empty !!");
            return OccupancyGrid();
        }
        double min_x = std::numeric_limits<double>::max();
        double min_y = std::numeric_limits<double>::max();
        double max_x = std::numeric_limits<double>::lowest();
        double max_y = std::numeric_limits<double>::lowest();
        float merged_resolution =  std::numeric_limits<float>::max();

        for (const auto& map : maps) {
            min_x = std::min(min_x, map->info.origin.position.x);
            min_y = std::min(min_y, map->info.origin.position.y);
            max_x = std::max(max_x, map->info.origin.position.x + map->info.width * map->info.resolution);
            max_y = std::max(max_y, map->info.origin.position.y + map->info.height * map->info.resolution);
            merged_resolution = std::min(merged_resolution, map->info.resolution);
        }

        int merged_width = static_cast<int>(std::ceil((max_x - min_x) / merged_resolution));
        int merged_height = static_cast<int>(std::ceil((max_y - min_y) / merged_resolution));

        std::vector<int8_t> merged_data(merged_width * merged_height, -1);

        for (const auto& map : maps) {
            for (int y = 0; y < map->info.height; ++y) {
                for (int x = 0; x < map->info.width; ++x) {
                    int i = x + y * map->info.width;
                    int merged_x = static_cast<int>(std::floor((map->info.origin.position.x + x * map->info.resolution - min_x) / merged_resolution));
                    int merged_y = static_cast<int>(std::floor((map->info.origin.position.y + y * map->info.resolution - min_y) / merged_resolution));
                    int merged_i = merged_x + merged_y * merged_width;
                    if (merged_data[merged_i] == -1) {
                        merged_data[merged_i] = map->data[i];
                    }
                }
            }
        }

        OccupancyGrid merged_map;
        merged_map.header = maps[0]->header;
        merged_map.header.frame_id = "mergedmap_robots";
        merged_map.info.origin.position.x = min_x;
        merged_map.info.origin.position.y = min_y;
        merged_map.info.resolution = merged_resolution;
        merged_map.info.width = merged_width;
        merged_map.info.height = merged_height;
        merged_map.data = merged_data;

        return merged_map;
    }

    int num_robots_;
    ros::Publisher merged_pub_;
    std::vector<ros::Subscriber> subscribers_;
    std::vector<bool> maps_received_;
    std::vector<OccupancyGrid::ConstPtr> maps_;
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "map_merger_node");

    int num_robots = 0;

    // Check if argument for num_robots is provided
    if (argc >= 2) {
        num_robots = std::stoi(argv[1]);
    } else {
        ROS_WARN("Usage: rosrun your_package_name map_merger_node <num_robots>");
        return 1;
    }

    MapMerger map_merger(num_robots);
    ros::spin();
    return 0;
}

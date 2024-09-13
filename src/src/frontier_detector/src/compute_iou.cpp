#include <ros/ros.h>
#include <nav_msgs/OccupancyGrid.h>
#include <geometry_msgs/Point.h>
#include <visualization_msgs/Marker.h>
#include <vector>
#include <algorithm>
#include <cmath>
#include "frontier_detector/iou.h"
#include <std_msgs/Float64.h>

using nav_msgs::OccupancyGrid;
using geometry_msgs::Point;
using visualization_msgs::Marker;

struct IoUResult {
    nav_msgs::OccupancyGrid::Ptr iou_map;
    frontier_detector::iou iou_information;
};

class FrontierDetector {
public:
    FrontierDetector() {
        ros::NodeHandle nh("~");

        std::string topic1, topic2, topic3;
        nh.param("map_topic1", topic1, std::string("/map1"));
        nh.param("map_topic2", topic2, std::string("/map2"));
           
        sub1_ = nh.subscribe<OccupancyGrid>(topic1, 10, &FrontierDetector::mapCallback1, this);
        sub2_ = nh.subscribe<OccupancyGrid>(topic2, 10, &FrontierDetector::mapCallback2, this);

        marker_pub_ = nh.advertise<Marker>("frontiers", 10);
        iou_map_pub_ = nh.advertise<OccupancyGrid>("iou_map", 10);
        iou_pub_ = nh.advertise<frontier_detector::iou>("iou_info", 10); // Updated publisher
        iou_score_pub_ = nh.advertise<std_msgs::Float64>("iou_score", 10);
        intersection_area_pub_ = nh.advertise<std_msgs::Float64>("intersection_area", 10);
        union_area_pub_ = nh.advertise<std_msgs::Float64>("union_area", 10);

    }

private:
    void mapCallback1(const OccupancyGrid::ConstPtr& msg) {
        map1_ = msg;
        if (map2_) {
            processMaps();
        }
    }

    void mapCallback2(const OccupancyGrid::ConstPtr& msg) {
        map2_ = msg;
        if (map1_) {
            processMaps();
        }
    }

    void processMaps() {
        if (!map1_ || !map2_) return;

        IoUResult result = computeIoU(map1_, map2_);
        if (result.iou_map) {
            std::vector<Point> frontiers = detectFrontiers(result.iou_map);
            publishFrontiers(frontiers, result.iou_map->header);
            publishIoUMap(result.iou_map);
            publishIoUInfo(result.iou_information); // Publish IoU information
            publishIntersectionArea(result.iou_information.Intersection);
            publishUnionArea(result.iou_information.Union);
            publishScore(result.iou_information.IouScore);

        }
    }

    IoUResult computeIoU(const OccupancyGrid::ConstPtr& map1, const OccupancyGrid::ConstPtr& map2) {
        IoUResult result;
        float resolution = std::max(map1->info.resolution, map2->info.resolution);
        float min_x = std::max(map1->info.origin.position.x, map2->info.origin.position.x);
        float min_y = std::max(map1->info.origin.position.y, map2->info.origin.position.y);
        float max_x = std::min(map1->info.origin.position.x + map1->info.width * map1->info.resolution,
                               map2->info.origin.position.x + map2->info.width * map2->info.resolution);
        float max_y = std::min(map1->info.origin.position.y + map1->info.height * map1->info.resolution,
                               map2->info.origin.position.y + map2->info.height * map2->info.resolution);

        if (min_x >= max_x || min_y >= max_y) {
            ROS_WARN("No overlapping region between maps.");
            return result;
        }

        int width = static_cast<int>((max_x - min_x) / resolution);
        int height = static_cast<int>((max_y - min_y) / resolution);

        result.iou_map = boost::make_shared<OccupancyGrid>();
        result.iou_map->header = map1->header;
        result.iou_map->header.frame_id = "iou_map";
        result.iou_map->info.resolution = resolution;
        result.iou_map->info.width = width;
        result.iou_map->info.height = height;
        result.iou_map->info.origin.position.x = min_x;
        result.iou_map->info.origin.position.y = min_y;

        result.iou_map->data.resize(width * height, -1); // default value is -1 (unknown)

        int intersection_count = 0;
        int union_count = 0;

        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                float wx = min_x + x * resolution;
                float wy = min_y + y * resolution;

                int idx1 = mapIndex(map1, wx, wy);
                int idx2 = mapIndex(map2, wx, wy);
                int idx_iou = x + y * width;

                if (idx1 != -1 && idx2 != -1) {
                    if (map1->data[idx1] == 0 && map2->data[idx2] == 0) {
                        result.iou_map->data[idx_iou] = 0; // free
                    } else if (map1->data[idx1] == 100 && map2->data[idx2] == 100) {
                        result.iou_map->data[idx_iou] = 100; // occupied in both maps
                        intersection_count++;
                        union_count++;
                    } else if (map1->data[idx1] == 100 || map2->data[idx2] == 100) {
                        result.iou_map->data[idx_iou] = 100; // occupied in either map
                        union_count++;
                    }
                }
            }
        }

        double intersection_area = intersection_count * resolution * resolution;
        double union_area = union_count * resolution * resolution;

        double iou_score = 0.0;
        try {
            if (union_area > 0) {
                iou_score = intersection_area / union_area;
            } else {
                throw std::runtime_error("Division by zero in union_area computation.");
            }
        } catch (const std::runtime_error& e) {
            ROS_ERROR("%s", e.what());
        }

        result.iou_information.IouScore = iou_score;
        result.iou_information.Intersection = intersection_area;
        result.iou_information.Union = union_area;      

        //ROS_INFO("IoU Score: %f (Intersection Area: %f m^2, Union Area: %f m^2)", iou_score, intersection_area, union_area);

        return result;
    }

    int mapIndex(const OccupancyGrid::ConstPtr& map, float wx, float wy) {
        int x = static_cast<int>((wx - map->info.origin.position.x) / map->info.resolution);
        int y = static_cast<int>((wy - map->info.origin.position.y) / map->info.resolution);

        if (x >= 0 && x < map->info.width && y >= 0 && y < map->info.height) {
            return x + y * map->info.width;
        } else {
            return -1;
        }
    }

    std::vector<Point> detectFrontiers(const OccupancyGrid::ConstPtr& map) {
        std::vector<Point> frontiers;

        for (int y = 1; y < map->info.height - 1; ++y) {
            for (int x = 1; x < map->info.width - 1; ++x) {
                int idx = x + y * map->info.width;
                if (map->data[idx] == 0) {
                    bool is_frontier = false;
                    for (int dy = -1; dy <= 1 && !is_frontier; ++dy) {
                        for (int dx = -1; dx <= 1 && !is_frontier; ++dx) {
                            if (map->data[idx + dx + dy * map->info.width] == -1) {
                                is_frontier = true;
                            }
                        }
                    }
                    if (is_frontier) {
                        Point pt;
                        pt.x = map->info.origin.position.x + x * map->info.resolution;
                        pt.y = map->info.origin.position.y + y * map->info.resolution;
                        pt.z = 0;
                        frontiers.push_back(pt);
                    }
                }
            }
        }

        return frontiers;
    }

    void publishFrontiers(const std::vector<Point>& frontiers, const std_msgs::Header& header) {
        Marker marker;
        marker.header = header;
        marker.ns = "frontiers";
        marker.id = 0;
        marker.type = Marker::POINTS;
        marker.action = Marker::ADD;
        marker.pose.orientation.w = 1.0;
        marker.scale.x = 0.1;
        marker.scale.y = 0.1;
        marker.color.a = 1.0;
        marker.color.r = 1.0;
        marker.color.g = 0.0;
        marker.color.b = 0.0;

        for (const auto& pt : frontiers) {
            marker.points.push_back(pt);
        }

        marker_pub_.publish(marker);
    }

    void publishIoUMap(const OccupancyGrid::ConstPtr& iou_map) {
        iou_map_pub_.publish(iou_map);
    }

    void publishIoUInfo(const frontier_detector::iou& iou_info) {
        iou_pub_.publish(iou_info);
    }

    void publishIntersectionArea(double intersection_area) {
        std_msgs::Float64 msg;
        msg.data = intersection_area;
        intersection_area_pub_.publish(msg);
    }

    void publishUnionArea(double union_area) {
        std_msgs::Float64 msg;
        msg.data = union_area;
        union_area_pub_.publish(msg);
    }

    void publishScore(double score) {
    std_msgs::Float64 msg;
    msg.data = score;
    iou_score_pub_.publish(msg);
}


    ros::Subscriber sub1_;
    ros::Subscriber sub2_;
 
    ros::Publisher marker_pub_;
    ros::Publisher iou_map_pub_;
    ros::Publisher iou_pub_; // Added publisher
    ros::Publisher iou_score_pub_; // Added publisher
    ros::Publisher intersection_area_pub_; // Added publisher
    ros::Publisher union_area_pub_; // Added publisher


    OccupancyGrid::ConstPtr map1_;
    OccupancyGrid::ConstPtr map2_;
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "frontier_detector_iou");
    FrontierDetector detector;
    ros::spin();
    return 0;
}

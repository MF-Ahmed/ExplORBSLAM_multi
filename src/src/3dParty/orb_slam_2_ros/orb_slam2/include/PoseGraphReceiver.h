#pragma once

#include <ros/ros.h>
#include <orb_slam2_ros/PoseGraphKeyFrame.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/PoseArray.h>
#include <visualization_msgs/MarkerArray.h>
#include <map>
#include <string>
#include <vector>

class PoseGraphReceiver {
public:
    PoseGraphReceiver(ros::NodeHandle& nh, const std::vector<std::string>& robot_namespaces);

    void Callback(const orb_slam2_ros::PoseGraphKeyFrame::ConstPtr& msg, const std::string& source_robot);

    const std::map<std::string, std::map<int, geometry_msgs::Pose>>& GetReceivedKeyframes() const;

    bool CheckForLoopClosure(const geometry_msgs::Pose& my_pose, double distance_threshold);

    void PublishPoseGraph();

private:
    std::map<std::string, ros::Subscriber> subscribers_;
    std::map<std::string, std::map<int, geometry_msgs::Pose>> received_keyframes_;
    std::map<std::string, ros::Publisher> pose_array_publishers_;
    ros::Publisher edge_marker_pub_;
};
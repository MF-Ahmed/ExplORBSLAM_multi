#include "PoseGraphReceiver.h"
#include <cmath>

static double PoseDistance(const geometry_msgs::Pose& a, const geometry_msgs::Pose& b) {
    double dx = a.position.x - b.position.x;
    double dy = a.position.y - b.position.y;
    double dz =  0;//a.position.z - b.position.z;
    return std::sqrt(dx*dx + dy*dy);
}

PoseGraphReceiver::PoseGraphReceiver(ros::NodeHandle& nh, const std::vector<std::string>& robot_namespaces) {
    for (const auto& ns : robot_namespaces) {
        std::string topic = "/" + ns + "/orb_slam2_rgbd/pose_graph";
        subscribers_[ns] = nh.subscribe<orb_slam2_ros::PoseGraphKeyFrame>(topic, 100, 
            boost::bind(&PoseGraphReceiver::Callback, this, _1, ns));
        //ROS_INFO_STREAM("Subscribed to: " << topic);

        std::string pub_topic = "/" + ns + "/orb_slam2_rgbd/pose_graph_array";
        pose_array_publishers_[ns] = nh.advertise<geometry_msgs::PoseArray>(pub_topic, 1);
        //ROS_INFO_STREAM("Advertising pose graph array for: " << pub_topic);
    }

    edge_marker_pub_ = nh.advertise<visualization_msgs::MarkerArray>("/pose_graph_edges", 1);
}

void PoseGraphReceiver::Callback(const orb_slam2_ros::PoseGraphKeyFrame::ConstPtr& msg, const std::string& source_robot) {
    received_keyframes_[source_robot][msg->keyframe_id] = msg->pose;
    ROS_INFO_STREAM("Received keyframe " << msg->keyframe_id << " from " << source_robot);
}

const std::map<std::string, std::map<int, geometry_msgs::Pose>>& PoseGraphReceiver::GetReceivedKeyframes() const {
    return received_keyframes_;
}

bool PoseGraphReceiver::CheckForLoopClosure(const geometry_msgs::Pose& my_pose, double distance_threshold) {
    bool matched = false;
    for (const auto& robot_data : received_keyframes_) {
        ROS_INFO_STREAM("Checking " << robot_data.second.size() << " keyframes from " << robot_data.first);

        for (const auto& [kf_id, pose] : robot_data.second) {
            double dist = PoseDistance(my_pose, pose);
            if (dist < distance_threshold) {
                ROS_WARN_STREAM("Loop closure candidate: " << robot_data.first
                                << " keyframe " << kf_id
                                << " at distance " << dist);
                matched = true;
            }
        }
    }
    return matched;
}

void PoseGraphReceiver::PublishPoseGraph() {
    visualization_msgs::MarkerArray edge_markers;
    int marker_id = 0;

    for (const auto& [robot, keyframes] : received_keyframes_) {
        geometry_msgs::PoseArray pose_array;
        pose_array.header.stamp = ros::Time::now();
        pose_array.header.frame_id = robot+"/map";

        geometry_msgs::Point last_point;
        bool has_last = false;

        for (const auto& [id, pose] : keyframes) {
            pose_array.poses.push_back(pose);

            geometry_msgs::Point current;
            current.x = pose.position.x;
            current.y = pose.position.y;
            current.z = pose.position.z;

            if (has_last) {
                visualization_msgs::Marker line;
                line.header.frame_id = robot+"/map";
                line.header.stamp = ros::Time::now();
                line.ns = robot;
                line.id = marker_id++;
                line.type = visualization_msgs::Marker::LINE_STRIP;
                line.action = visualization_msgs::Marker::ADD;
                line.scale.x = 0.03;
                line.color.r = 1.0;
                line.color.g = 1.0;
                line.color.b = 0.0;
                line.color.a = 1.0;

                line.points.push_back(last_point);
                line.points.push_back(current);

                edge_markers.markers.push_back(line);
            }

            last_point = current;
            has_last = true;
        }

        pose_array_publishers_[robot].publish(pose_array);
    }

    edge_marker_pub_.publish(edge_markers);
}
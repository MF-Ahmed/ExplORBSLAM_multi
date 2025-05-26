#pragma once

#include <ros/ros.h>
#include <geometry_msgs/Pose.h>
#include <orb_slam2_ros/PoseGraphKeyFrame.h>
#include "KeyFrame.h"

class PoseGraphPublisher {
public:
    PoseGraphPublisher(ros::NodeHandle& nh, const std::string& topic);
    void PublishKeyFrame(ORB_SLAM2::KeyFrame* pKF);

private:
    ros::Publisher pub_;
};


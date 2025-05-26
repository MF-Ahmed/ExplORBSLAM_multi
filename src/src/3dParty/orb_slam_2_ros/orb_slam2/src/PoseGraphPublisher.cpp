#include "PoseGraphPublisher.h"
#include <orb_slam2_ros/PoseGraphKeyFrame.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>
#include <ros/ros.h>

PoseGraphPublisher::PoseGraphPublisher(ros::NodeHandle& nh, const std::string& topic) {
    std::string resolved_topic = nh.resolveName(topic);
    ROS_INFO_STREAM("[PoseGraphPublisher] Advertising topic: " << resolved_topic);
    pub_ = nh.advertise<orb_slam2_ros::PoseGraphKeyFrame>(topic, 10);
}

void PoseGraphPublisher::PublishKeyFrame(ORB_SLAM2::KeyFrame* pKF) {
    if (!pKF) return;

    cv::Mat Tcw = pKF->GetPose();
    cv::Mat Rwc = Tcw.rowRange(0, 3).colRange(0, 3).t();
    cv::Mat twc = -Rwc * Tcw.rowRange(0, 3).col(3);

    tf2::Matrix3x3 tf_R(
        Rwc.at<float>(0,0), Rwc.at<float>(0,1), Rwc.at<float>(0,2),
        Rwc.at<float>(1,0), Rwc.at<float>(1,1), Rwc.at<float>(1,2),
        Rwc.at<float>(2,0), Rwc.at<float>(2,1), Rwc.at<float>(2,2)
    );
    tf2::Quaternion q;
    tf_R.getRotation(q);

    orb_slam2_ros::PoseGraphKeyFrame msg;
    msg.header.stamp = ros::Time::now();
    ros::this_node::getNamespace(); 
    std::string ns = ros::this_node::getNamespace();  // e.g., "/robot_0/orb_slam2_rgbd"
    std::string robot_ns = ns.substr(0, ns.find("/orb_slam2_rgbd"));  // extract "/robot_0"
    msg.header.frame_id = robot_ns + "/map";
    msg.keyframe_id = pKF->mnId;
    msg.timestamp = pKF->mTimeStamp;

    msg.pose.position.x = twc.at<float>(0);
    msg.pose.position.y = twc.at<float>(1);
    msg.pose.position.z = twc.at<float>(2);
    msg.pose.orientation.x = q.x();
    msg.pose.orientation.y = q.y();
    msg.pose.orientation.z = q.z();
    msg.pose.orientation.w = q.w();

    if (pub_.getNumSubscribers() == 0) {
        ROS_WARN("[PoseGraphPublisher] No active subscribers to pose_graph.");
    } else {
        ROS_INFO_STREAM("[PoseGraphPublisher] Publishing keyframe ID: " << pKF->mnId);
        pub_.publish(msg);
    }
}

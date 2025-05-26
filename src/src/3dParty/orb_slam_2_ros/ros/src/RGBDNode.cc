#include "RGBDNode.h"
#include "PoseGraphPublisher.h"
#include "PoseGraphReceiver.h"
#include "KeyFrame.h"
#include <vector>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "RGBD");
    ros::start();

    if(argc > 1) {
        ROS_WARN("Arguments supplied via command line are neglected.");
    }

    ros::NodeHandle node_handle("~");
    image_transport::ImageTransport image_transport(node_handle);

    RGBDNode node(ORB_SLAM2::System::RGBD, node_handle, image_transport);
    node.Init();

    ros::spin();
    ros::shutdown();

    return 0;
}

RGBDNode::RGBDNode(const ORB_SLAM2::System::eSensor sensor, ros::NodeHandle &node_handle, image_transport::ImageTransport &image_transport)
: Node(sensor, node_handle, image_transport), last_published_kf_id_(-1)
{
    rgb_subscriber_ = new message_filters::Subscriber<sensor_msgs::Image>(node_handle, "/camera/rgb/image_raw", 1);
    depth_subscriber_ = new message_filters::Subscriber<sensor_msgs::Image>(node_handle, "/camera/depth_registered/image_raw", 1);
    camera_info_topic_ = "/camera/rgb/camera_info";

    sync_ = new message_filters::Synchronizer<sync_pol>(sync_pol(10), *rgb_subscriber_, *depth_subscriber_);
    sync_->registerCallback(boost::bind(&RGBDNode::ImageCallback, this, _1, _2));

    pose_graph_publisher_ = new PoseGraphPublisher(node_handle, "pose_graph");
    std::vector<std::string> other_robots = {"robot_0", "robot_1"};
    pose_graph_receiver_ = new PoseGraphReceiver(node_handle, other_robots);
}

RGBDNode::~RGBDNode()
{
    delete rgb_subscriber_;
    delete depth_subscriber_;
    delete sync_;
    delete pose_graph_publisher_;
    delete pose_graph_receiver_;
}

void RGBDNode::ImageCallback(const sensor_msgs::ImageConstPtr& msgRGB, const sensor_msgs::ImageConstPtr& msgD)
{
    cv_bridge::CvImageConstPtr cv_ptrRGB;
    try {
        cv_ptrRGB = cv_bridge::toCvShare(msgRGB);
    } catch (cv_bridge::Exception& e) {
        ROS_ERROR("cv_bridge exception: %s", e.what());
        return;
    }

    cv_bridge::CvImageConstPtr cv_ptrD;
    try {
        cv_ptrD = cv_bridge::toCvShare(msgD);
    } catch (cv_bridge::Exception& e) {
        ROS_ERROR("cv_bridge exception: %s", e.what());
        return;
    }

    current_frame_time_ = msgRGB->header.stamp;

    orb_slam_->TrackRGBD(cv_ptrRGB->image, cv_ptrD->image, cv_ptrRGB->header.stamp.toSec());

    ORB_SLAM2::Tracking* tracker = orb_slam_->GetTracker();
    ORB_SLAM2::KeyFrame* last_kf = tracker->GetLastKeyFrame();

    if (last_kf && last_kf->mnId != last_published_kf_id_) {
        //ROS_INFO_STREAM("[RGBDNode] Publishing KF ID " << last_kf->mnId);
        pose_graph_publisher_->PublishKeyFrame(last_kf);
        last_published_kf_id_ = last_kf->mnId;

        cv::Mat Tcw = last_kf->GetPose();
        cv::Mat Rwc = Tcw.rowRange(0, 3).colRange(0, 3).t();
        cv::Mat twc = -Rwc * Tcw.rowRange(0, 3).col(3);

        geometry_msgs::Pose pose_msg;
        pose_msg.position.x = twc.at<float>(0);
        pose_msg.position.y = twc.at<float>(1);
        pose_msg.position.z = twc.at<float>(2);

        tf2::Matrix3x3 tf_R(
            Rwc.at<float>(0,0), Rwc.at<float>(0,1), Rwc.at<float>(0,2),
            Rwc.at<float>(1,0), Rwc.at<float>(1,1), Rwc.at<float>(1,2),
            Rwc.at<float>(2,0), Rwc.at<float>(2,1), Rwc.at<float>(2,2)
        );
        tf2::Quaternion q;
        tf_R.getRotation(q);

        pose_msg.orientation.x = q.x();
        pose_msg.orientation.y = q.y();
        pose_msg.orientation.z = q.z();
        pose_msg.orientation.w = q.w();

        if (pose_graph_receiver_->CheckForLoopClosure(pose_msg, 2.0)) {
            ROS_WARN_STREAM("[RGBDNode] Inter-robot loop closure detected at keyframe " << last_kf->mnId);
        }
    }

    pose_graph_receiver_->PublishPoseGraph();

    Update();
}
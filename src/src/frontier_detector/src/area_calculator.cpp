#include <ros/ros.h>
#include <nav_msgs/OccupancyGrid.h>
#include <std_msgs/Float64.h>

class OccupancyAreaCalculator
{
public:
    OccupancyAreaCalculator(ros::NodeHandle& nh, const std::string& topic_name)
    {
        // Subscribe to the map topic
        map_sub_ = nh.subscribe(topic_name, 1, &OccupancyAreaCalculator::mapCallback, this);
        // Publishers for the areas
        known_clear_area_pub_ = nh.advertise<std_msgs::Float64>("known_clear_area", 1);
        obstacle_area_pub_ = nh.advertise<std_msgs::Float64>("obstacle_area", 1);
        total_area_pub_ = nh.advertise<std_msgs::Float64>("total_area", 1);
        prev_known_clear_area_ = 0.0;
        prev_obstacle_area_ = 0.0;

    }

    void mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg)
    {
        double resolution = msg->info.resolution;
        int width = msg->info.width;
        int height = msg->info.height;


        double known_clear_area = 0.0;
        double obstacle_area = 0.0;

        for (int i = 0; i < width * height; ++i)
        {
            int cell_value = msg->data[i];
            if (cell_value == 0)  // Known and clear cell
            {
                known_clear_area += resolution * resolution;
            }
            else if (cell_value == 100)  // Obstacle cell
            {
                obstacle_area += resolution * resolution;
            }
        }

        double total_area = known_clear_area + obstacle_area;

        // Publish the known clear area only if it is greater than the previous value
        //if (known_clear_area > prev_known_clear_area_)
        //{
        std_msgs::Float64 known_clear_area_msg;
        known_clear_area_msg.data = known_clear_area;
        known_clear_area_pub_.publish(known_clear_area_msg);
        prev_known_clear_area_ = known_clear_area;
        //}

        // Publish the obstacle area only if it is less than the previous value
        //if (obstacle_area < prev_obstacle_area_)
        //{
        std_msgs::Float64 obstacle_area_msg;
        obstacle_area_msg.data = obstacle_area;
        obstacle_area_pub_.publish(obstacle_area_msg);
        prev_obstacle_area_ = obstacle_area;
       // }

        std_msgs::Float64 total_area_msg;
        total_area_msg.data = total_area;
        total_area_pub_.publish(total_area_msg);

        //ROS_INFO("Known clear area: %f square meters", known_clear_area);
        //ROS_INFO("Obstacle area: %f square meters", obstacle_area);
        //ROS_INFO("Total area: %f square meters", total_area);

    }

private:
    ros::Subscriber map_sub_;
    ros::Publisher known_clear_area_pub_;
    ros::Publisher obstacle_area_pub_;
    ros::Publisher total_area_pub_;
    double prev_known_clear_area_;
    double prev_obstacle_area_;    
};

int main(int argc, char** argv)
{
    ros::init(argc, argv, "frontier_detector_area");
    ros::NodeHandle nh;
    ROS_INFO("area_calculator_node_initlalized");

    std::string topic_name;
    nh.param<std::string>("area_map_topic", topic_name, "");

    
    ROS_INFO("map topic name: [%s]", topic_name.c_str());

    OccupancyAreaCalculator occupancy_area_calculator(nh, topic_name);
    ROS_INFO("All node parameters:");
    ros::spin();
    return 0;
}

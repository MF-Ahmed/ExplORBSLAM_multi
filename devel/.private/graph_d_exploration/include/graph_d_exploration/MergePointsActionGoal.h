// Generated by gencpp from file graph_d_exploration/MergePointsActionGoal.msg
// DO NOT EDIT!


#ifndef GRAPH_D_EXPLORATION_MESSAGE_MERGEPOINTSACTIONGOAL_H
#define GRAPH_D_EXPLORATION_MESSAGE_MERGEPOINTSACTIONGOAL_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <actionlib_msgs/GoalID.h>
#include <graph_d_exploration/MergePointsGoal.h>

namespace graph_d_exploration
{
template <class ContainerAllocator>
struct MergePointsActionGoal_
{
  typedef MergePointsActionGoal_<ContainerAllocator> Type;

  MergePointsActionGoal_()
    : header()
    , goal_id()
    , goal()  {
    }
  MergePointsActionGoal_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , goal_id(_alloc)
    , goal(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef  ::actionlib_msgs::GoalID_<ContainerAllocator>  _goal_id_type;
  _goal_id_type goal_id;

   typedef  ::graph_d_exploration::MergePointsGoal_<ContainerAllocator>  _goal_type;
  _goal_type goal;





  typedef boost::shared_ptr< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> const> ConstPtr;

}; // struct MergePointsActionGoal_

typedef ::graph_d_exploration::MergePointsActionGoal_<std::allocator<void> > MergePointsActionGoal;

typedef boost::shared_ptr< ::graph_d_exploration::MergePointsActionGoal > MergePointsActionGoalPtr;
typedef boost::shared_ptr< ::graph_d_exploration::MergePointsActionGoal const> MergePointsActionGoalConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator1> & lhs, const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator2> & rhs)
{
  return lhs.header == rhs.header &&
    lhs.goal_id == rhs.goal_id &&
    lhs.goal == rhs.goal;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator1> & lhs, const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace graph_d_exploration

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "242fc1835c52357820aa19c444682014";
  }

  static const char* value(const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x242fc1835c523578ULL;
  static const uint64_t static_value2 = 0x20aa19c444682014ULL;
};

template<class ContainerAllocator>
struct DataType< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "graph_d_exploration/MergePointsActionGoal";
  }

  static const char* value(const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"\n"
"Header header\n"
"actionlib_msgs/GoalID goal_id\n"
"MergePointsGoal goal\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: actionlib_msgs/GoalID\n"
"# The stamp should store the time at which this goal was requested.\n"
"# It is used by an action server when it tries to preempt all\n"
"# goals that were requested before a certain time\n"
"time stamp\n"
"\n"
"# The id provides a way to associate feedback and\n"
"# result message with specific goal requests. The id\n"
"# specified must be unique.\n"
"string id\n"
"\n"
"\n"
"================================================================================\n"
"MSG: graph_d_exploration/MergePointsGoal\n"
"# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"# Define a message type for passing an array of points to the server and getting the merged points back\n"
"\n"
"# Define the action goal message\n"
"string client_id\n"
"Point2D[] points\n"
"string robot_id\n"
"\n"
"================================================================================\n"
"MSG: graph_d_exploration/Point2D\n"
"# Point for centroids\n"
"float32 x\n"
"float32 y\n"
;
  }

  static const char* value(const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.goal_id);
      stream.next(m.goal);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MergePointsActionGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::graph_d_exploration::MergePointsActionGoal_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "goal_id: ";
    s << std::endl;
    Printer< ::actionlib_msgs::GoalID_<ContainerAllocator> >::stream(s, indent + "  ", v.goal_id);
    s << indent << "goal: ";
    s << std::endl;
    Printer< ::graph_d_exploration::MergePointsGoal_<ContainerAllocator> >::stream(s, indent + "  ", v.goal);
  }
};

} // namespace message_operations
} // namespace ros

#endif // GRAPH_D_EXPLORATION_MESSAGE_MERGEPOINTSACTIONGOAL_H

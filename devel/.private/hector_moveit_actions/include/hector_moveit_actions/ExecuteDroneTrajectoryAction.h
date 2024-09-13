// Generated by gencpp from file hector_moveit_actions/ExecuteDroneTrajectoryAction.msg
// DO NOT EDIT!


#ifndef HECTOR_MOVEIT_ACTIONS_MESSAGE_EXECUTEDRONETRAJECTORYACTION_H
#define HECTOR_MOVEIT_ACTIONS_MESSAGE_EXECUTEDRONETRAJECTORYACTION_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <hector_moveit_actions/ExecuteDroneTrajectoryActionGoal.h>
#include <hector_moveit_actions/ExecuteDroneTrajectoryActionResult.h>
#include <hector_moveit_actions/ExecuteDroneTrajectoryActionFeedback.h>

namespace hector_moveit_actions
{
template <class ContainerAllocator>
struct ExecuteDroneTrajectoryAction_
{
  typedef ExecuteDroneTrajectoryAction_<ContainerAllocator> Type;

  ExecuteDroneTrajectoryAction_()
    : action_goal()
    , action_result()
    , action_feedback()  {
    }
  ExecuteDroneTrajectoryAction_(const ContainerAllocator& _alloc)
    : action_goal(_alloc)
    , action_result(_alloc)
    , action_feedback(_alloc)  {
  (void)_alloc;
    }



   typedef  ::hector_moveit_actions::ExecuteDroneTrajectoryActionGoal_<ContainerAllocator>  _action_goal_type;
  _action_goal_type action_goal;

   typedef  ::hector_moveit_actions::ExecuteDroneTrajectoryActionResult_<ContainerAllocator>  _action_result_type;
  _action_result_type action_result;

   typedef  ::hector_moveit_actions::ExecuteDroneTrajectoryActionFeedback_<ContainerAllocator>  _action_feedback_type;
  _action_feedback_type action_feedback;





  typedef boost::shared_ptr< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> const> ConstPtr;

}; // struct ExecuteDroneTrajectoryAction_

typedef ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<std::allocator<void> > ExecuteDroneTrajectoryAction;

typedef boost::shared_ptr< ::hector_moveit_actions::ExecuteDroneTrajectoryAction > ExecuteDroneTrajectoryActionPtr;
typedef boost::shared_ptr< ::hector_moveit_actions::ExecuteDroneTrajectoryAction const> ExecuteDroneTrajectoryActionConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator1> & lhs, const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator2> & rhs)
{
  return lhs.action_goal == rhs.action_goal &&
    lhs.action_result == rhs.action_result &&
    lhs.action_feedback == rhs.action_feedback;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator1> & lhs, const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace hector_moveit_actions

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >
{
  static const char* value()
  {
    return "af7148fd02416a846ae1d2ce2a783c36";
  }

  static const char* value(const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xaf7148fd02416a84ULL;
  static const uint64_t static_value2 = 0x6ae1d2ce2a783c36ULL;
};

template<class ContainerAllocator>
struct DataType< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >
{
  static const char* value()
  {
    return "hector_moveit_actions/ExecuteDroneTrajectoryAction";
  }

  static const char* value(const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"\n"
"ExecuteDroneTrajectoryActionGoal action_goal\n"
"ExecuteDroneTrajectoryActionResult action_result\n"
"ExecuteDroneTrajectoryActionFeedback action_feedback\n"
"\n"
"================================================================================\n"
"MSG: hector_moveit_actions/ExecuteDroneTrajectoryActionGoal\n"
"# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"\n"
"Header header\n"
"actionlib_msgs/GoalID goal_id\n"
"ExecuteDroneTrajectoryGoal goal\n"
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
"MSG: hector_moveit_actions/ExecuteDroneTrajectoryGoal\n"
"# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"# Goal definition\n"
"geometry_msgs/Pose[] trajectory\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Pose\n"
"# A representation of pose in free space, composed of position and orientation. \n"
"Point position\n"
"Quaternion orientation\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Point\n"
"# This contains the position of a point in free space\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Quaternion\n"
"# This represents an orientation in free space in quaternion form.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"float64 w\n"
"\n"
"================================================================================\n"
"MSG: hector_moveit_actions/ExecuteDroneTrajectoryActionResult\n"
"# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"\n"
"Header header\n"
"actionlib_msgs/GoalStatus status\n"
"ExecuteDroneTrajectoryResult result\n"
"\n"
"================================================================================\n"
"MSG: actionlib_msgs/GoalStatus\n"
"GoalID goal_id\n"
"uint8 status\n"
"uint8 PENDING         = 0   # The goal has yet to be processed by the action server\n"
"uint8 ACTIVE          = 1   # The goal is currently being processed by the action server\n"
"uint8 PREEMPTED       = 2   # The goal received a cancel request after it started executing\n"
"                            #   and has since completed its execution (Terminal State)\n"
"uint8 SUCCEEDED       = 3   # The goal was achieved successfully by the action server (Terminal State)\n"
"uint8 ABORTED         = 4   # The goal was aborted during execution by the action server due\n"
"                            #    to some failure (Terminal State)\n"
"uint8 REJECTED        = 5   # The goal was rejected by the action server without being processed,\n"
"                            #    because the goal was unattainable or invalid (Terminal State)\n"
"uint8 PREEMPTING      = 6   # The goal received a cancel request after it started executing\n"
"                            #    and has not yet completed execution\n"
"uint8 RECALLING       = 7   # The goal received a cancel request before it started executing,\n"
"                            #    but the action server has not yet confirmed that the goal is canceled\n"
"uint8 RECALLED        = 8   # The goal received a cancel request before it started executing\n"
"                            #    and was successfully cancelled (Terminal State)\n"
"uint8 LOST            = 9   # An action client can determine that a goal is LOST. This should not be\n"
"                            #    sent over the wire by an action server\n"
"\n"
"#Allow for the user to associate a string with GoalStatus for debugging\n"
"string text\n"
"\n"
"\n"
"================================================================================\n"
"MSG: hector_moveit_actions/ExecuteDroneTrajectoryResult\n"
"# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"# Result definition\n"
"int32 result_code\n"
"int32 SUCCESSFUL = 0\n"
"int32 INVALID_GOAL = -1\n"
"int32 PATH_TOLERANCE_VIOLATED = -2\n"
"int32 COLLISION_IN_FRONT = 3\n"
"\n"
"================================================================================\n"
"MSG: hector_moveit_actions/ExecuteDroneTrajectoryActionFeedback\n"
"# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"\n"
"Header header\n"
"actionlib_msgs/GoalStatus status\n"
"ExecuteDroneTrajectoryFeedback feedback\n"
"\n"
"================================================================================\n"
"MSG: hector_moveit_actions/ExecuteDroneTrajectoryFeedback\n"
"# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"#Feedback definition\n"
"geometry_msgs/Pose current_pose\n"
;
  }

  static const char* value(const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.action_goal);
      stream.next(m.action_result);
      stream.next(m.action_feedback);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ExecuteDroneTrajectoryAction_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::hector_moveit_actions::ExecuteDroneTrajectoryAction_<ContainerAllocator>& v)
  {
    s << indent << "action_goal: ";
    s << std::endl;
    Printer< ::hector_moveit_actions::ExecuteDroneTrajectoryActionGoal_<ContainerAllocator> >::stream(s, indent + "  ", v.action_goal);
    s << indent << "action_result: ";
    s << std::endl;
    Printer< ::hector_moveit_actions::ExecuteDroneTrajectoryActionResult_<ContainerAllocator> >::stream(s, indent + "  ", v.action_result);
    s << indent << "action_feedback: ";
    s << std::endl;
    Printer< ::hector_moveit_actions::ExecuteDroneTrajectoryActionFeedback_<ContainerAllocator> >::stream(s, indent + "  ", v.action_feedback);
  }
};

} // namespace message_operations
} // namespace ros

#endif // HECTOR_MOVEIT_ACTIONS_MESSAGE_EXECUTEDRONETRAJECTORYACTION_H

// Generated by gencpp from file graph_d_exploration/MergePointsFeedback.msg
// DO NOT EDIT!


#ifndef GRAPH_D_EXPLORATION_MESSAGE_MERGEPOINTSFEEDBACK_H
#define GRAPH_D_EXPLORATION_MESSAGE_MERGEPOINTSFEEDBACK_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace graph_d_exploration
{
template <class ContainerAllocator>
struct MergePointsFeedback_
{
  typedef MergePointsFeedback_<ContainerAllocator> Type;

  MergePointsFeedback_()
    : percent_completed(0.0)  {
    }
  MergePointsFeedback_(const ContainerAllocator& _alloc)
    : percent_completed(0.0)  {
  (void)_alloc;
    }



   typedef float _percent_completed_type;
  _percent_completed_type percent_completed;





  typedef boost::shared_ptr< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> const> ConstPtr;

}; // struct MergePointsFeedback_

typedef ::graph_d_exploration::MergePointsFeedback_<std::allocator<void> > MergePointsFeedback;

typedef boost::shared_ptr< ::graph_d_exploration::MergePointsFeedback > MergePointsFeedbackPtr;
typedef boost::shared_ptr< ::graph_d_exploration::MergePointsFeedback const> MergePointsFeedbackConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator1> & lhs, const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator2> & rhs)
{
  return lhs.percent_completed == rhs.percent_completed;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator1> & lhs, const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace graph_d_exploration

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "2cfbe45a73922160426e29b7a5f151e0";
  }

  static const char* value(const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x2cfbe45a73922160ULL;
  static const uint64_t static_value2 = 0x426e29b7a5f151e0ULL;
};

template<class ContainerAllocator>
struct DataType< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "graph_d_exploration/MergePointsFeedback";
  }

  static const char* value(const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"# Define the action feedback message\n"
"float32 percent_completed\n"
"\n"
;
  }

  static const char* value(const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.percent_completed);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MergePointsFeedback_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::graph_d_exploration::MergePointsFeedback_<ContainerAllocator>& v)
  {
    s << indent << "percent_completed: ";
    Printer<float>::stream(s, indent + "  ", v.percent_completed);
  }
};

} // namespace message_operations
} // namespace ros

#endif // GRAPH_D_EXPLORATION_MESSAGE_MERGEPOINTSFEEDBACK_H

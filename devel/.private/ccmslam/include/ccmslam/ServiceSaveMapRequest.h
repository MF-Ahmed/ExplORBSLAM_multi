// Generated by gencpp from file ccmslam/ServiceSaveMapRequest.msg
// DO NOT EDIT!


#ifndef CCMSLAM_MESSAGE_SERVICESAVEMAPREQUEST_H
#define CCMSLAM_MESSAGE_SERVICESAVEMAPREQUEST_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace ccmslam
{
template <class ContainerAllocator>
struct ServiceSaveMapRequest_
{
  typedef ServiceSaveMapRequest_<ContainerAllocator> Type;

  ServiceSaveMapRequest_()
    : map_id(0)  {
    }
  ServiceSaveMapRequest_(const ContainerAllocator& _alloc)
    : map_id(0)  {
  (void)_alloc;
    }



   typedef int64_t _map_id_type;
  _map_id_type map_id;





  typedef boost::shared_ptr< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> const> ConstPtr;

}; // struct ServiceSaveMapRequest_

typedef ::ccmslam::ServiceSaveMapRequest_<std::allocator<void> > ServiceSaveMapRequest;

typedef boost::shared_ptr< ::ccmslam::ServiceSaveMapRequest > ServiceSaveMapRequestPtr;
typedef boost::shared_ptr< ::ccmslam::ServiceSaveMapRequest const> ServiceSaveMapRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator1> & lhs, const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator2> & rhs)
{
  return lhs.map_id == rhs.map_id;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator1> & lhs, const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace ccmslam

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "9c1e1ce0f999abf593b8013f00455110";
  }

  static const char* value(const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x9c1e1ce0f999abf5ULL;
  static const uint64_t static_value2 = 0x93b8013f00455110ULL;
};

template<class ContainerAllocator>
struct DataType< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ccmslam/ServiceSaveMapRequest";
  }

  static const char* value(const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int64 map_id\n"
;
  }

  static const char* value(const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.map_id);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ServiceSaveMapRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ccmslam::ServiceSaveMapRequest_<ContainerAllocator>& v)
  {
    s << indent << "map_id: ";
    Printer<int64_t>::stream(s, indent + "  ", v.map_id);
  }
};

} // namespace message_operations
} // namespace ros

#endif // CCMSLAM_MESSAGE_SERVICESAVEMAPREQUEST_H

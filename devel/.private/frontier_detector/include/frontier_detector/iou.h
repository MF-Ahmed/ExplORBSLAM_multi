// Generated by gencpp from file frontier_detector/iou.msg
// DO NOT EDIT!


#ifndef FRONTIER_DETECTOR_MESSAGE_IOU_H
#define FRONTIER_DETECTOR_MESSAGE_IOU_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace frontier_detector
{
template <class ContainerAllocator>
struct iou_
{
  typedef iou_<ContainerAllocator> Type;

  iou_()
    : IouScore(0.0)
    , Intersection(0.0)
    , Union(0.0)  {
    }
  iou_(const ContainerAllocator& _alloc)
    : IouScore(0.0)
    , Intersection(0.0)
    , Union(0.0)  {
  (void)_alloc;
    }



   typedef double _IouScore_type;
  _IouScore_type IouScore;

   typedef double _Intersection_type;
  _Intersection_type Intersection;

   typedef double _Union_type;
  _Union_type Union;





  typedef boost::shared_ptr< ::frontier_detector::iou_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::frontier_detector::iou_<ContainerAllocator> const> ConstPtr;

}; // struct iou_

typedef ::frontier_detector::iou_<std::allocator<void> > iou;

typedef boost::shared_ptr< ::frontier_detector::iou > iouPtr;
typedef boost::shared_ptr< ::frontier_detector::iou const> iouConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::frontier_detector::iou_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::frontier_detector::iou_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::frontier_detector::iou_<ContainerAllocator1> & lhs, const ::frontier_detector::iou_<ContainerAllocator2> & rhs)
{
  return lhs.IouScore == rhs.IouScore &&
    lhs.Intersection == rhs.Intersection &&
    lhs.Union == rhs.Union;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::frontier_detector::iou_<ContainerAllocator1> & lhs, const ::frontier_detector::iou_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace frontier_detector

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::frontier_detector::iou_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::frontier_detector::iou_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::frontier_detector::iou_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::frontier_detector::iou_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::frontier_detector::iou_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::frontier_detector::iou_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::frontier_detector::iou_<ContainerAllocator> >
{
  static const char* value()
  {
    return "7cbdf3f3cf45675e88468517bea07534";
  }

  static const char* value(const ::frontier_detector::iou_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x7cbdf3f3cf45675eULL;
  static const uint64_t static_value2 = 0x88468517bea07534ULL;
};

template<class ContainerAllocator>
struct DataType< ::frontier_detector::iou_<ContainerAllocator> >
{
  static const char* value()
  {
    return "frontier_detector/iou";
  }

  static const char* value(const ::frontier_detector::iou_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::frontier_detector::iou_<ContainerAllocator> >
{
  static const char* value()
  {
    return "#iou meaage \n"
"float64 IouScore\n"
"float64 Intersection\n"
"float64 Union\n"
;
  }

  static const char* value(const ::frontier_detector::iou_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::frontier_detector::iou_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.IouScore);
      stream.next(m.Intersection);
      stream.next(m.Union);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct iou_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::frontier_detector::iou_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::frontier_detector::iou_<ContainerAllocator>& v)
  {
    s << indent << "IouScore: ";
    Printer<double>::stream(s, indent + "  ", v.IouScore);
    s << indent << "Intersection: ";
    Printer<double>::stream(s, indent + "  ", v.Intersection);
    s << indent << "Union: ";
    Printer<double>::stream(s, indent + "  ", v.Union);
  }
};

} // namespace message_operations
} // namespace ros

#endif // FRONTIER_DETECTOR_MESSAGE_IOU_H

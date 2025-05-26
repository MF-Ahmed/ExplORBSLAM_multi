;; Auto-generated. Do not edit!


(when (boundp 'orb_slam2_ros::PoseGraphKeyFrame)
  (if (not (find-package "ORB_SLAM2_ROS"))
    (make-package "ORB_SLAM2_ROS"))
  (shadow 'PoseGraphKeyFrame (find-package "ORB_SLAM2_ROS")))
(unless (find-package "ORB_SLAM2_ROS::POSEGRAPHKEYFRAME")
  (make-package "ORB_SLAM2_ROS::POSEGRAPHKEYFRAME"))

(in-package "ROS")
;;//! \htmlinclude PoseGraphKeyFrame.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass orb_slam2_ros::PoseGraphKeyFrame
  :super ros::object
  :slots (_header _keyframe_id _pose _timestamp ))

(defmethod orb_slam2_ros::PoseGraphKeyFrame
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:keyframe_id __keyframe_id) 0)
    ((:pose __pose) (instance geometry_msgs::Pose :init))
    ((:timestamp __timestamp) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _keyframe_id (round __keyframe_id))
   (setq _pose __pose)
   (setq _timestamp (float __timestamp))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:keyframe_id
   (&optional __keyframe_id)
   (if __keyframe_id (setq _keyframe_id __keyframe_id)) _keyframe_id)
  (:pose
   (&rest __pose)
   (if (keywordp (car __pose))
       (send* _pose __pose)
     (progn
       (if __pose (setq _pose (car __pose)))
       _pose)))
  (:timestamp
   (&optional __timestamp)
   (if __timestamp (setq _timestamp __timestamp)) _timestamp)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; int32 _keyframe_id
    4
    ;; geometry_msgs/Pose _pose
    (send _pose :serialization-length)
    ;; float64 _timestamp
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; int32 _keyframe_id
       (write-long _keyframe_id s)
     ;; geometry_msgs/Pose _pose
       (send _pose :serialize s)
     ;; float64 _timestamp
       (sys::poke _timestamp (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; int32 _keyframe_id
     (setq _keyframe_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; geometry_msgs/Pose _pose
     (send _pose :deserialize buf ptr-) (incf ptr- (send _pose :serialization-length))
   ;; float64 _timestamp
     (setq _timestamp (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get orb_slam2_ros::PoseGraphKeyFrame :md5sum-) "5bd14b990739982b06eb1cfab09a2dfe")
(setf (get orb_slam2_ros::PoseGraphKeyFrame :datatype-) "orb_slam2_ros/PoseGraphKeyFrame")
(setf (get orb_slam2_ros::PoseGraphKeyFrame :definition-)
      "Header header
int32 keyframe_id
geometry_msgs/Pose pose
float64 timestamp

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :orb_slam2_ros/PoseGraphKeyFrame "5bd14b990739982b06eb1cfab09a2dfe")



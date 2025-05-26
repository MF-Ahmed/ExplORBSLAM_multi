; Auto-generated. Do not edit!


(cl:in-package orb_slam2_ros-msg)


;//! \htmlinclude PoseGraphKeyFrame.msg.html

(cl:defclass <PoseGraphKeyFrame> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (keyframe_id
    :reader keyframe_id
    :initarg :keyframe_id
    :type cl:integer
    :initform 0)
   (pose
    :reader pose
    :initarg :pose
    :type geometry_msgs-msg:Pose
    :initform (cl:make-instance 'geometry_msgs-msg:Pose))
   (timestamp
    :reader timestamp
    :initarg :timestamp
    :type cl:float
    :initform 0.0))
)

(cl:defclass PoseGraphKeyFrame (<PoseGraphKeyFrame>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PoseGraphKeyFrame>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PoseGraphKeyFrame)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name orb_slam2_ros-msg:<PoseGraphKeyFrame> is deprecated: use orb_slam2_ros-msg:PoseGraphKeyFrame instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <PoseGraphKeyFrame>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader orb_slam2_ros-msg:header-val is deprecated.  Use orb_slam2_ros-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'keyframe_id-val :lambda-list '(m))
(cl:defmethod keyframe_id-val ((m <PoseGraphKeyFrame>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader orb_slam2_ros-msg:keyframe_id-val is deprecated.  Use orb_slam2_ros-msg:keyframe_id instead.")
  (keyframe_id m))

(cl:ensure-generic-function 'pose-val :lambda-list '(m))
(cl:defmethod pose-val ((m <PoseGraphKeyFrame>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader orb_slam2_ros-msg:pose-val is deprecated.  Use orb_slam2_ros-msg:pose instead.")
  (pose m))

(cl:ensure-generic-function 'timestamp-val :lambda-list '(m))
(cl:defmethod timestamp-val ((m <PoseGraphKeyFrame>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader orb_slam2_ros-msg:timestamp-val is deprecated.  Use orb_slam2_ros-msg:timestamp instead.")
  (timestamp m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PoseGraphKeyFrame>) ostream)
  "Serializes a message object of type '<PoseGraphKeyFrame>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let* ((signed (cl:slot-value msg 'keyframe_id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'pose) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'timestamp))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PoseGraphKeyFrame>) istream)
  "Deserializes a message object of type '<PoseGraphKeyFrame>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'keyframe_id) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'pose) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'timestamp) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PoseGraphKeyFrame>)))
  "Returns string type for a message object of type '<PoseGraphKeyFrame>"
  "orb_slam2_ros/PoseGraphKeyFrame")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PoseGraphKeyFrame)))
  "Returns string type for a message object of type 'PoseGraphKeyFrame"
  "orb_slam2_ros/PoseGraphKeyFrame")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PoseGraphKeyFrame>)))
  "Returns md5sum for a message object of type '<PoseGraphKeyFrame>"
  "5bd14b990739982b06eb1cfab09a2dfe")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PoseGraphKeyFrame)))
  "Returns md5sum for a message object of type 'PoseGraphKeyFrame"
  "5bd14b990739982b06eb1cfab09a2dfe")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PoseGraphKeyFrame>)))
  "Returns full string definition for message of type '<PoseGraphKeyFrame>"
  (cl:format cl:nil "Header header~%int32 keyframe_id~%geometry_msgs/Pose pose~%float64 timestamp~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PoseGraphKeyFrame)))
  "Returns full string definition for message of type 'PoseGraphKeyFrame"
  (cl:format cl:nil "Header header~%int32 keyframe_id~%geometry_msgs/Pose pose~%float64 timestamp~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PoseGraphKeyFrame>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'pose))
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PoseGraphKeyFrame>))
  "Converts a ROS message object to a list"
  (cl:list 'PoseGraphKeyFrame
    (cl:cons ':header (header msg))
    (cl:cons ':keyframe_id (keyframe_id msg))
    (cl:cons ':pose (pose msg))
    (cl:cons ':timestamp (timestamp msg))
))

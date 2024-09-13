; Auto-generated. Do not edit!


(cl:in-package frontier_detector-msg)


;//! \htmlinclude iou.msg.html

(cl:defclass <iou> (roslisp-msg-protocol:ros-message)
  ((IouScore
    :reader IouScore
    :initarg :IouScore
    :type cl:float
    :initform 0.0)
   (Intersection
    :reader Intersection
    :initarg :Intersection
    :type cl:float
    :initform 0.0)
   (Union
    :reader Union
    :initarg :Union
    :type cl:float
    :initform 0.0))
)

(cl:defclass iou (<iou>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <iou>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'iou)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name frontier_detector-msg:<iou> is deprecated: use frontier_detector-msg:iou instead.")))

(cl:ensure-generic-function 'IouScore-val :lambda-list '(m))
(cl:defmethod IouScore-val ((m <iou>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader frontier_detector-msg:IouScore-val is deprecated.  Use frontier_detector-msg:IouScore instead.")
  (IouScore m))

(cl:ensure-generic-function 'Intersection-val :lambda-list '(m))
(cl:defmethod Intersection-val ((m <iou>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader frontier_detector-msg:Intersection-val is deprecated.  Use frontier_detector-msg:Intersection instead.")
  (Intersection m))

(cl:ensure-generic-function 'Union-val :lambda-list '(m))
(cl:defmethod Union-val ((m <iou>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader frontier_detector-msg:Union-val is deprecated.  Use frontier_detector-msg:Union instead.")
  (Union m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <iou>) ostream)
  "Serializes a message object of type '<iou>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'IouScore))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'Intersection))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'Union))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <iou>) istream)
  "Deserializes a message object of type '<iou>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'IouScore) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'Intersection) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'Union) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<iou>)))
  "Returns string type for a message object of type '<iou>"
  "frontier_detector/iou")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'iou)))
  "Returns string type for a message object of type 'iou"
  "frontier_detector/iou")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<iou>)))
  "Returns md5sum for a message object of type '<iou>"
  "7cbdf3f3cf45675e88468517bea07534")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'iou)))
  "Returns md5sum for a message object of type 'iou"
  "7cbdf3f3cf45675e88468517bea07534")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<iou>)))
  "Returns full string definition for message of type '<iou>"
  (cl:format cl:nil "#iou meaage ~%float64 IouScore~%float64 Intersection~%float64 Union~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'iou)))
  "Returns full string definition for message of type 'iou"
  (cl:format cl:nil "#iou meaage ~%float64 IouScore~%float64 Intersection~%float64 Union~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <iou>))
  (cl:+ 0
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <iou>))
  "Converts a ROS message object to a list"
  (cl:list 'iou
    (cl:cons ':IouScore (IouScore msg))
    (cl:cons ':Intersection (Intersection msg))
    (cl:cons ':Union (Union msg))
))

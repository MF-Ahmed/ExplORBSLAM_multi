; Auto-generated. Do not edit!


(cl:in-package graph_d_exploration-msg)


;//! \htmlinclude BoolArray.msg.html

(cl:defclass <BoolArray> (roslisp-msg-protocol:ros-message)
  ((availability
    :reader availability
    :initarg :availability
    :type (cl:vector cl:boolean)
   :initform (cl:make-array 0 :element-type 'cl:boolean :initial-element cl:nil)))
)

(cl:defclass BoolArray (<BoolArray>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BoolArray>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BoolArray)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name graph_d_exploration-msg:<BoolArray> is deprecated: use graph_d_exploration-msg:BoolArray instead.")))

(cl:ensure-generic-function 'availability-val :lambda-list '(m))
(cl:defmethod availability-val ((m <BoolArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader graph_d_exploration-msg:availability-val is deprecated.  Use graph_d_exploration-msg:availability instead.")
  (availability m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BoolArray>) ostream)
  "Serializes a message object of type '<BoolArray>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'availability))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if ele 1 0)) ostream))
   (cl:slot-value msg 'availability))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BoolArray>) istream)
  "Deserializes a message object of type '<BoolArray>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'availability) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'availability)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:not (cl:zerop (cl:read-byte istream)))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BoolArray>)))
  "Returns string type for a message object of type '<BoolArray>"
  "graph_d_exploration/BoolArray")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BoolArray)))
  "Returns string type for a message object of type 'BoolArray"
  "graph_d_exploration/BoolArray")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BoolArray>)))
  "Returns md5sum for a message object of type '<BoolArray>"
  "31080b5ad54e6a85d10a027f73e819fc")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BoolArray)))
  "Returns md5sum for a message object of type 'BoolArray"
  "31080b5ad54e6a85d10a027f73e819fc")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BoolArray>)))
  "Returns full string definition for message of type '<BoolArray>"
  (cl:format cl:nil "# Arrays of booleans~%bool[] availability~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BoolArray)))
  "Returns full string definition for message of type 'BoolArray"
  (cl:format cl:nil "# Arrays of booleans~%bool[] availability~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BoolArray>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'availability) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BoolArray>))
  "Converts a ROS message object to a list"
  (cl:list 'BoolArray
    (cl:cons ':availability (availability msg))
))

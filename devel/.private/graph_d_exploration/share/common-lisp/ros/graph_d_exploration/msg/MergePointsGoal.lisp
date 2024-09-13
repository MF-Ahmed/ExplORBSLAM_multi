; Auto-generated. Do not edit!


(cl:in-package graph_d_exploration-msg)


;//! \htmlinclude MergePointsGoal.msg.html

(cl:defclass <MergePointsGoal> (roslisp-msg-protocol:ros-message)
  ((client_id
    :reader client_id
    :initarg :client_id
    :type cl:string
    :initform "")
   (points
    :reader points
    :initarg :points
    :type (cl:vector graph_d_exploration-msg:Point2D)
   :initform (cl:make-array 0 :element-type 'graph_d_exploration-msg:Point2D :initial-element (cl:make-instance 'graph_d_exploration-msg:Point2D)))
   (robot_id
    :reader robot_id
    :initarg :robot_id
    :type cl:string
    :initform ""))
)

(cl:defclass MergePointsGoal (<MergePointsGoal>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MergePointsGoal>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MergePointsGoal)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name graph_d_exploration-msg:<MergePointsGoal> is deprecated: use graph_d_exploration-msg:MergePointsGoal instead.")))

(cl:ensure-generic-function 'client_id-val :lambda-list '(m))
(cl:defmethod client_id-val ((m <MergePointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader graph_d_exploration-msg:client_id-val is deprecated.  Use graph_d_exploration-msg:client_id instead.")
  (client_id m))

(cl:ensure-generic-function 'points-val :lambda-list '(m))
(cl:defmethod points-val ((m <MergePointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader graph_d_exploration-msg:points-val is deprecated.  Use graph_d_exploration-msg:points instead.")
  (points m))

(cl:ensure-generic-function 'robot_id-val :lambda-list '(m))
(cl:defmethod robot_id-val ((m <MergePointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader graph_d_exploration-msg:robot_id-val is deprecated.  Use graph_d_exploration-msg:robot_id instead.")
  (robot_id m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MergePointsGoal>) ostream)
  "Serializes a message object of type '<MergePointsGoal>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'client_id))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'client_id))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'points))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'points))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'robot_id))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'robot_id))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MergePointsGoal>) istream)
  "Deserializes a message object of type '<MergePointsGoal>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'client_id) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'client_id) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'points) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'points)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'graph_d_exploration-msg:Point2D))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'robot_id) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'robot_id) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MergePointsGoal>)))
  "Returns string type for a message object of type '<MergePointsGoal>"
  "graph_d_exploration/MergePointsGoal")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MergePointsGoal)))
  "Returns string type for a message object of type 'MergePointsGoal"
  "graph_d_exploration/MergePointsGoal")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MergePointsGoal>)))
  "Returns md5sum for a message object of type '<MergePointsGoal>"
  "b2c66b8a0ad24cf595212d5c25aaea6b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MergePointsGoal)))
  "Returns md5sum for a message object of type 'MergePointsGoal"
  "b2c66b8a0ad24cf595212d5c25aaea6b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MergePointsGoal>)))
  "Returns full string definition for message of type '<MergePointsGoal>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Define a message type for passing an array of points to the server and getting the merged points back~%~%# Define the action goal message~%string client_id~%Point2D[] points~%string robot_id~%~%================================================================================~%MSG: graph_d_exploration/Point2D~%# Point for centroids~%float32 x~%float32 y~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MergePointsGoal)))
  "Returns full string definition for message of type 'MergePointsGoal"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Define a message type for passing an array of points to the server and getting the merged points back~%~%# Define the action goal message~%string client_id~%Point2D[] points~%string robot_id~%~%================================================================================~%MSG: graph_d_exploration/Point2D~%# Point for centroids~%float32 x~%float32 y~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MergePointsGoal>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'client_id))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'points) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     4 (cl:length (cl:slot-value msg 'robot_id))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MergePointsGoal>))
  "Converts a ROS message object to a list"
  (cl:list 'MergePointsGoal
    (cl:cons ':client_id (client_id msg))
    (cl:cons ':points (points msg))
    (cl:cons ':robot_id (robot_id msg))
))

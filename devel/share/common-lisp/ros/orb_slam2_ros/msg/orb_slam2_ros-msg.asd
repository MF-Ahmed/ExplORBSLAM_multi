
(cl:in-package :asdf)

(defsystem "orb_slam2_ros-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "ORBState" :depends-on ("_package_ORBState"))
    (:file "_package_ORBState" :depends-on ("_package"))
    (:file "PoseGraphKeyFrame" :depends-on ("_package_PoseGraphKeyFrame"))
    (:file "_package_PoseGraphKeyFrame" :depends-on ("_package"))
  ))
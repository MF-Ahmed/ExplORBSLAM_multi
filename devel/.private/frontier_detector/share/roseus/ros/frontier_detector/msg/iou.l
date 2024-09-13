;; Auto-generated. Do not edit!


(when (boundp 'frontier_detector::iou)
  (if (not (find-package "FRONTIER_DETECTOR"))
    (make-package "FRONTIER_DETECTOR"))
  (shadow 'iou (find-package "FRONTIER_DETECTOR")))
(unless (find-package "FRONTIER_DETECTOR::IOU")
  (make-package "FRONTIER_DETECTOR::IOU"))

(in-package "ROS")
;;//! \htmlinclude iou.msg.html


(defclass frontier_detector::iou
  :super ros::object
  :slots (_IouScore _Intersection _Union ))

(defmethod frontier_detector::iou
  (:init
   (&key
    ((:IouScore __IouScore) 0.0)
    ((:Intersection __Intersection) 0.0)
    ((:Union __Union) 0.0)
    )
   (send-super :init)
   (setq _IouScore (float __IouScore))
   (setq _Intersection (float __Intersection))
   (setq _Union (float __Union))
   self)
  (:IouScore
   (&optional __IouScore)
   (if __IouScore (setq _IouScore __IouScore)) _IouScore)
  (:Intersection
   (&optional __Intersection)
   (if __Intersection (setq _Intersection __Intersection)) _Intersection)
  (:Union
   (&optional __Union)
   (if __Union (setq _Union __Union)) _Union)
  (:serialization-length
   ()
   (+
    ;; float64 _IouScore
    8
    ;; float64 _Intersection
    8
    ;; float64 _Union
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _IouScore
       (sys::poke _IouScore (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _Intersection
       (sys::poke _Intersection (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _Union
       (sys::poke _Union (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _IouScore
     (setq _IouScore (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _Intersection
     (setq _Intersection (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _Union
     (setq _Union (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get frontier_detector::iou :md5sum-) "7cbdf3f3cf45675e88468517bea07534")
(setf (get frontier_detector::iou :datatype-) "frontier_detector/iou")
(setf (get frontier_detector::iou :definition-)
      "#iou meaage 
float64 IouScore
float64 Intersection
float64 Union

")



(provide :frontier_detector/iou "7cbdf3f3cf45675e88468517bea07534")



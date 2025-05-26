;; Auto-generated. Do not edit!


(when (boundp 'graph_d_exploration::BoolArray)
  (if (not (find-package "GRAPH_D_EXPLORATION"))
    (make-package "GRAPH_D_EXPLORATION"))
  (shadow 'BoolArray (find-package "GRAPH_D_EXPLORATION")))
(unless (find-package "GRAPH_D_EXPLORATION::BOOLARRAY")
  (make-package "GRAPH_D_EXPLORATION::BOOLARRAY"))

(in-package "ROS")
;;//! \htmlinclude BoolArray.msg.html


(defclass graph_d_exploration::BoolArray
  :super ros::object
  :slots (_availability ))

(defmethod graph_d_exploration::BoolArray
  (:init
   (&key
    ((:availability __availability) (let (r) (dotimes (i 0) (push nil r)) r))
    )
   (send-super :init)
   (setq _availability __availability)
   self)
  (:availability
   (&optional __availability)
   (if __availability (setq _availability __availability)) _availability)
  (:serialization-length
   ()
   (+
    ;; bool[] _availability
    (* 1    (length _availability)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool[] _availability
     (write-long (length _availability) s)
     (dotimes (i (length _availability))
       (if (elt _availability i) (write-byte -1 s) (write-byte 0 s))
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool[] _availability
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _availability (make-list n))
     (dotimes (i n)
     (setf (elt _availability i) (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
     ))
   ;;
   self)
  )

(setf (get graph_d_exploration::BoolArray :md5sum-) "31080b5ad54e6a85d10a027f73e819fc")
(setf (get graph_d_exploration::BoolArray :datatype-) "graph_d_exploration/BoolArray")
(setf (get graph_d_exploration::BoolArray :definition-)
      "# Arrays of booleans
bool[] availability
")



(provide :graph_d_exploration/BoolArray "31080b5ad54e6a85d10a027f73e819fc")



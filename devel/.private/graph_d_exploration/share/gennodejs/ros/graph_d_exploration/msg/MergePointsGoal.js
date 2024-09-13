// Auto-generated. Do not edit!

// (in-package graph_d_exploration.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Point2D = require('./Point2D.js');

//-----------------------------------------------------------

class MergePointsGoal {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.client_id = null;
      this.points = null;
      this.robot_id = null;
    }
    else {
      if (initObj.hasOwnProperty('client_id')) {
        this.client_id = initObj.client_id
      }
      else {
        this.client_id = '';
      }
      if (initObj.hasOwnProperty('points')) {
        this.points = initObj.points
      }
      else {
        this.points = [];
      }
      if (initObj.hasOwnProperty('robot_id')) {
        this.robot_id = initObj.robot_id
      }
      else {
        this.robot_id = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MergePointsGoal
    // Serialize message field [client_id]
    bufferOffset = _serializer.string(obj.client_id, buffer, bufferOffset);
    // Serialize message field [points]
    // Serialize the length for message field [points]
    bufferOffset = _serializer.uint32(obj.points.length, buffer, bufferOffset);
    obj.points.forEach((val) => {
      bufferOffset = Point2D.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [robot_id]
    bufferOffset = _serializer.string(obj.robot_id, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MergePointsGoal
    let len;
    let data = new MergePointsGoal(null);
    // Deserialize message field [client_id]
    data.client_id = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [points]
    // Deserialize array length for message field [points]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.points = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.points[i] = Point2D.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [robot_id]
    data.robot_id = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.client_id);
    length += 8 * object.points.length;
    length += _getByteLength(object.robot_id);
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'graph_d_exploration/MergePointsGoal';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b2c66b8a0ad24cf595212d5c25aaea6b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
    # Define a message type for passing an array of points to the server and getting the merged points back
    
    # Define the action goal message
    string client_id
    Point2D[] points
    string robot_id
    
    ================================================================================
    MSG: graph_d_exploration/Point2D
    # Point for centroids
    float32 x
    float32 y
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MergePointsGoal(null);
    if (msg.client_id !== undefined) {
      resolved.client_id = msg.client_id;
    }
    else {
      resolved.client_id = ''
    }

    if (msg.points !== undefined) {
      resolved.points = new Array(msg.points.length);
      for (let i = 0; i < resolved.points.length; ++i) {
        resolved.points[i] = Point2D.Resolve(msg.points[i]);
      }
    }
    else {
      resolved.points = []
    }

    if (msg.robot_id !== undefined) {
      resolved.robot_id = msg.robot_id;
    }
    else {
      resolved.robot_id = ''
    }

    return resolved;
    }
};

module.exports = MergePointsGoal;

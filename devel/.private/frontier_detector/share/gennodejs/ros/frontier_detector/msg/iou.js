// Auto-generated. Do not edit!

// (in-package frontier_detector.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class iou {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.IouScore = null;
      this.Intersection = null;
      this.Union = null;
    }
    else {
      if (initObj.hasOwnProperty('IouScore')) {
        this.IouScore = initObj.IouScore
      }
      else {
        this.IouScore = 0.0;
      }
      if (initObj.hasOwnProperty('Intersection')) {
        this.Intersection = initObj.Intersection
      }
      else {
        this.Intersection = 0.0;
      }
      if (initObj.hasOwnProperty('Union')) {
        this.Union = initObj.Union
      }
      else {
        this.Union = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type iou
    // Serialize message field [IouScore]
    bufferOffset = _serializer.float64(obj.IouScore, buffer, bufferOffset);
    // Serialize message field [Intersection]
    bufferOffset = _serializer.float64(obj.Intersection, buffer, bufferOffset);
    // Serialize message field [Union]
    bufferOffset = _serializer.float64(obj.Union, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type iou
    let len;
    let data = new iou(null);
    // Deserialize message field [IouScore]
    data.IouScore = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [Intersection]
    data.Intersection = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [Union]
    data.Union = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'frontier_detector/iou';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7cbdf3f3cf45675e88468517bea07534';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    #iou meaage 
    float64 IouScore
    float64 Intersection
    float64 Union
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new iou(null);
    if (msg.IouScore !== undefined) {
      resolved.IouScore = msg.IouScore;
    }
    else {
      resolved.IouScore = 0.0
    }

    if (msg.Intersection !== undefined) {
      resolved.Intersection = msg.Intersection;
    }
    else {
      resolved.Intersection = 0.0
    }

    if (msg.Union !== undefined) {
      resolved.Union = msg.Union;
    }
    else {
      resolved.Union = 0.0
    }

    return resolved;
    }
};

module.exports = iou;

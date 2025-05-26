// Auto-generated. Do not edit!

// (in-package graph_d_exploration.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class BoolArray {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.availability = null;
    }
    else {
      if (initObj.hasOwnProperty('availability')) {
        this.availability = initObj.availability
      }
      else {
        this.availability = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type BoolArray
    // Serialize message field [availability]
    bufferOffset = _arraySerializer.bool(obj.availability, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type BoolArray
    let len;
    let data = new BoolArray(null);
    // Deserialize message field [availability]
    data.availability = _arrayDeserializer.bool(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.availability.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'graph_d_exploration/BoolArray';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '31080b5ad54e6a85d10a027f73e819fc';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # Arrays of booleans
    bool[] availability
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new BoolArray(null);
    if (msg.availability !== undefined) {
      resolved.availability = msg.availability;
    }
    else {
      resolved.availability = []
    }

    return resolved;
    }
};

module.exports = BoolArray;

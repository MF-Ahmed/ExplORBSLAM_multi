
"use strict";

let Compass = require('./Compass.js');
let MotorPWM = require('./MotorPWM.js');
let Altimeter = require('./Altimeter.js');
let RawImu = require('./RawImu.js');
let RawMagnetic = require('./RawMagnetic.js');
let RawRC = require('./RawRC.js');
let Supply = require('./Supply.js');
let PositionXYCommand = require('./PositionXYCommand.js');
let VelocityZCommand = require('./VelocityZCommand.js');
let ServoCommand = require('./ServoCommand.js');
let ThrustCommand = require('./ThrustCommand.js');
let ControllerState = require('./ControllerState.js');
let RuddersCommand = require('./RuddersCommand.js');
let AttitudeCommand = require('./AttitudeCommand.js');
let MotorStatus = require('./MotorStatus.js');
let YawrateCommand = require('./YawrateCommand.js');
let HeightCommand = require('./HeightCommand.js');
let MotorCommand = require('./MotorCommand.js');
let VelocityXYCommand = require('./VelocityXYCommand.js');
let HeadingCommand = require('./HeadingCommand.js');
let RC = require('./RC.js');
let PoseResult = require('./PoseResult.js');
let LandingActionFeedback = require('./LandingActionFeedback.js');
let LandingAction = require('./LandingAction.js');
let LandingActionResult = require('./LandingActionResult.js');
let TakeoffActionResult = require('./TakeoffActionResult.js');
let PoseGoal = require('./PoseGoal.js');
let LandingGoal = require('./LandingGoal.js');
let TakeoffResult = require('./TakeoffResult.js');
let PoseActionResult = require('./PoseActionResult.js');
let PoseActionFeedback = require('./PoseActionFeedback.js');
let TakeoffActionFeedback = require('./TakeoffActionFeedback.js');
let LandingResult = require('./LandingResult.js');
let PoseFeedback = require('./PoseFeedback.js');
let TakeoffGoal = require('./TakeoffGoal.js');
let PoseActionGoal = require('./PoseActionGoal.js');
let LandingActionGoal = require('./LandingActionGoal.js');
let TakeoffAction = require('./TakeoffAction.js');
let PoseAction = require('./PoseAction.js');
let LandingFeedback = require('./LandingFeedback.js');
let TakeoffActionGoal = require('./TakeoffActionGoal.js');
let TakeoffFeedback = require('./TakeoffFeedback.js');

module.exports = {
  Compass: Compass,
  MotorPWM: MotorPWM,
  Altimeter: Altimeter,
  RawImu: RawImu,
  RawMagnetic: RawMagnetic,
  RawRC: RawRC,
  Supply: Supply,
  PositionXYCommand: PositionXYCommand,
  VelocityZCommand: VelocityZCommand,
  ServoCommand: ServoCommand,
  ThrustCommand: ThrustCommand,
  ControllerState: ControllerState,
  RuddersCommand: RuddersCommand,
  AttitudeCommand: AttitudeCommand,
  MotorStatus: MotorStatus,
  YawrateCommand: YawrateCommand,
  HeightCommand: HeightCommand,
  MotorCommand: MotorCommand,
  VelocityXYCommand: VelocityXYCommand,
  HeadingCommand: HeadingCommand,
  RC: RC,
  PoseResult: PoseResult,
  LandingActionFeedback: LandingActionFeedback,
  LandingAction: LandingAction,
  LandingActionResult: LandingActionResult,
  TakeoffActionResult: TakeoffActionResult,
  PoseGoal: PoseGoal,
  LandingGoal: LandingGoal,
  TakeoffResult: TakeoffResult,
  PoseActionResult: PoseActionResult,
  PoseActionFeedback: PoseActionFeedback,
  TakeoffActionFeedback: TakeoffActionFeedback,
  LandingResult: LandingResult,
  PoseFeedback: PoseFeedback,
  TakeoffGoal: TakeoffGoal,
  PoseActionGoal: PoseActionGoal,
  LandingActionGoal: LandingActionGoal,
  TakeoffAction: TakeoffAction,
  PoseAction: PoseAction,
  LandingFeedback: LandingFeedback,
  TakeoffActionGoal: TakeoffActionGoal,
  TakeoffFeedback: TakeoffFeedback,
};

#Default start up parameters
#DO NOT TOUCH!

from odrive.enums import *
import odrive

AXIS0_CURRENT_LIM = 15 #[A]
AXIS1_CURRENT_LIM = 15 #[A]

AXIS0_VEL_LIMIT = 100000 #[Counts/S]
AXIS1_VEL_LIMIT = 100000 #[Counts/S]

AXIS0_CALIBRATION_CURRENT = 15 #[A]
AXIS1_CALIBRATION_CURRENT = 15 #[A]

AXIS0_POLE_PAIRS = 7 #
AXIS1_POLE_PAIRS = 7 #

AXIS0_MOTOR_TYPE = MOTOR_TYPE_HIGH_CURRENT # = 0
AXIS1_MOTOR_TYPE = MOTOR_TYPE_HIGH_CURRENT # = 0

AXIS0_CPR = 8192 #2048*4
AXIS1_CPR = 8192 #2048*4

AXIS0_ENCODER_MODE = ENCODER_MODE_INCREMENTAL
AXIS1_ENCODER_MODE = ENCODER_MODE_INCREMENTAL

ODRV0_BRAKE_RESISTANCE = 0.5 #[Ohm]


def sendParameters(objectOdrv):
        #Current
    objectOdrv.axis0.motor.config.current_lim = AXIS0_CURRENT_LIM
    objectOdrv.axis1.motor.config.current_lim = AXIS1_CURRENT_LIM
    #Max velocity
    objectOdrv.axis0.controller.config.vel_limit = AXIS0_VEL_LIMIT
    objectOdrv.axis1.controller.config.vel_limit = AXIS1_VEL_LIMIT
    #Calibration current
    objectOdrv.axis0.motor.config.calibration_current = AXIS0_CALIBRATION_CURRENT
    objectOdrv.axis1.motor.config.calibration_current = AXIS1_CALIBRATION_CURRENT
    #Number od motor pole pairs
    objectOdrv.axis0.motor.config.pole_pairs = AXIS0_POLE_PAIRS
    objectOdrv.axis1.motor.config.pole_pairs = AXIS1_POLE_PAIRS
    #Motor type
    objectOdrv.axis0.motor.config.motor_type = AXIS0_MOTOR_TYPE
    objectOdrv.axis1.motor.config.motor_type = AXIS1_MOTOR_TYPE
    #Encoder CPR
    objectOdrv.axis0.encoder.config.cpr = AXIS0_CPR
    objectOdrv.axis1.encoder.config.cpr = AXIS1_CPR
    #Encoder mode
    objectOdrv.axis0.encoder.config.mode = AXIS0_ENCODER_MODE
    objectOdrv.axis0.encoder.config.mode = AXIS1_ENCODER_MODE
    #Brake resistance
    objectOdrv.config.brake_resistance = ODRV0_BRAKE_RESISTANCE
    #Go to trayectory control mode
    objectOdrv.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
    objectOdrv.axis1.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
    #TODO: Motor parameter, Check if need to be implemented and checked later
    """
    objectOdrv.axis0.motor.config.resistance_calib_max_voltage = 4
    objectOdrv.axis1.motor.config.resistance_calib_max_voltage = 4
    objectOdrv.axis0.motor.config.requested_current_range = 25 #Requires config save and reboot
    objectOdrv.axis1.motor.config.requested_current_range = 25 #Requires config save and reboot+
    objectOdrv.axis0.motor.config.current_control_bandwidth = 100
    objectOdrv.axis1.motor.config.current_control_bandwidth = 100
    """
    #TODO: Encoder parameter, Check if need to be implemented and checked later
    """
    odrv0.axis1.config.calibration_lockin.vel
    odrv0.axis1.config.calibration_lockin.ramp_distance
    odrv0.axis1.config.calibration_lockin.accel
    """


def checkParameters(objectOdrv):
    if(not(objectOdrv.axis0.motor.config.current_lim == AXIS0_CURRENT_LIM) or not(objectOdrv.axis1.motor.config.current_lim == AXIS1_CURRENT_LIM)):
        return False
    if(not(objectOdrv.axis0.controller.config.vel_limit == AXIS0_VEL_LIMIT) or not(objectOdrv.axis1.controller.config.vel_limit == AXIS1_VEL_LIMIT)):
        return False
    if(not(objectOdrv.axis0.motor.config.calibration_current == AXIS0_CALIBRATION_CURRENT) and not(objectOdrv.axis1.motor.config.calibration_current == AXIS1_CALIBRATION_CURRENT)):
        return False
    if(not(objectOdrv.axis0.motor.config.pole_pairs == AXIS0_POLE_PAIRS) or not(objectOdrv.axis1.motor.config.pole_pairs == AXIS1_POLE_PAIRS)):
        return False
    if(not(objectOdrv.axis0.motor.config.motor_type == AXIS0_MOTOR_TYPE) or not(objectOdrv.axis1.motor.config.motor_type == AXIS1_MOTOR_TYPE)):
        return False
    if(not(objectOdrv.axis0.encoder.config.cpr == AXIS0_CPR) or not(objectOdrv.axis1.encoder.config.cpr == AXIS1_CPR)):
        return False
    if(not(objectOdrv.axis0.encoder.config.mode == AXIS0_ENCODER_MODE) or not(objectOdrv.axis0.encoder.config.mode == AXIS1_ENCODER_MODE)):
        return False
    if(not(objectOdrv.config.brake_resistance == ODRV0_BRAKE_RESISTANCE)):
        return False
    if(not(objectOdrv.axis0.motor.config.pre_calibrated == True) or not(objectOdrv.axis1.motor.config.pre_calibrated == True)):
        return False
    if(not(objectOdrv.axis0.encoder.config.use_index == True) or not(objectOdrv.axis1.encoder.config.use_index == True)):
        return False
    if(not(objectOdrv.axis0.controller.config.control_mode == CTRL_MODE_POSITION_CONTROL) or not(objectOdrv.axis1.controller.config.control_mode == CTRL_MODE_POSITION_CONTROL)):
        return False
    else:
        return True
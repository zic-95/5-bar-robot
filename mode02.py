#full calibration gui
from tkinter import *
import time
import math
import odrive
from odrive.enums import *
import defaultParameters as dP

delayLength = 3 # [s], time to read messages
backgroundColor = '#293134'
lettersColor = '#E7E6DE'

calibrationSuccesful02 = False

def mode02init(objectOdrv):
    root02 = Tk()
    root02.title("5-Bar Robot")
    root02.iconbitmap("C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotIcon.ico")
    root02.configure(background = backgroundColor)

    mode01Txt1 = StringVar()
    mode01Txt1.set("Welcome to the calibration sequence.")
    mode01Msg1 = Message(root02, width = 1000, textvariable = mode01Txt1, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "24", "bold"), relief = FLAT, justify = CENTER)
    mode01Msg1.pack()

    mode01Txt2 = StringVar()
    mode01Txt2.set("Please remove robot arm linkages as photo is showing and press Arm linkages are removed button.")
    mode01Msg2 = Message(root02, width = 1000, textvariable = mode01Txt2, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), relief = FLAT, justify = CENTER)
    mode01Msg2.pack()

    photoFrame = Frame(root02,bd = 0, bg = backgroundColor , highlightbackground = backgroundColor)
    photoFrame.pack(expand = True, fill = X)
    photoCanvas1 = Canvas(photoFrame, width=700, height=490, bg = backgroundColor , highlightbackground = backgroundColor, bd = 0)
    img1 = PhotoImage(file = "C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotPositionFull.gif")
    photoCanvas1.create_image(700/2, 490/2, image = img1)
    photoCanvas1.pack(side = TOP, expand = True, fill = X)

    armLinkagesRemovedB = Button(root02, text = "Arm linkages removed", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = lambda: enableFullCalibration(fullCalibrationB))
    fullCalibrationB = Button(root02, text = "Start calibration", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = lambda: startFullCalibration(root02 ,objectOdrv, fullCalibrationB), state = DISABLED)
    armLinkagesRemovedB.pack(expand = True, fill = X)
    fullCalibrationB.pack(expand = True, fill = X)

    root02.mainloop()


def enableFullCalibration(buttonPass):
    buttonPass.config(state = NORMAL)

def startFullCalibration(objectRoot, objectOdrv, buttonPass):
    buttonPass.config(state = DISABLED)
    mode01Txt3 = StringVar()
    mode01Txt3.set("Calibration has started, please wait for it to finish.")
    mode01Msg3 = Message(objectRoot,width = 1000, textvariable = mode01Txt3, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "24", "bold"), relief = FLAT, justify = CENTER)
    mode01Msg3.pack(expand = True, fill = X)
    fullCalibrationSequence(objectRoot, objectOdrv)

def fullCalibrationSequence(objectRoot, objectOdrv):
    global calibrationSuccesful02
    mode01Txt4 = StringVar()
    mode01Txt4.set("Sending motor parameters to driver")
    mode01Msg4 = Message(objectRoot,width = 1000, textvariable = mode01Txt4, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), relief = FLAT, justify = CENTER)
    mode01Msg4.pack(expand = True, fill = X)
    objectRoot.update()
    ###Send parameters###
    dP.sendParameters(objectOdrv)
    time.sleep(delayLength)
    ###Check parameters###
    mode01Txt4.set("Checking if parameters were send succesfully.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    if(not(dP.checkParameters(objectOdrv))):
        calibrationSuccesful02 = False
        return
    time.sleep(delayLength)
    ###Motor calibration###
    mode01Txt4.set("Calibrating motor.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    objectOdrv.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
    while objectOdrv.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    objectOdrv.axis1.requested_state = AXIS_STATE_MOTOR_CALIBRATION
    while objectOdrv.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    objectOdrv.axis0.motor.config.pre_calibrated = True
    objectOdrv.axis1.motor.config.pre_calibrated = True
    time.sleep(delayLength)
    ###Z index search###
    mode01Txt4.set("Finding Encoder Z index.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    objectOdrv.axis0.encoder.config.use_index = True 
    objectOdrv.axis1.encoder.config.use_index = True 
    objectOdrv.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while objectOdrv.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    objectOdrv.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while objectOdrv.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    time.sleep(delayLength)
    ###Encoder offset calibration###
    mode01Txt4.set("Encoder offset calibration")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    objectOdrv.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
    while objectOdrv.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    objectOdrv.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
    while objectOdrv.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    objectOdrv.axis0.encoder.config.pre_calibrated = True
    objectOdrv.axis1.encoder.config.pre_calibrated = True
    time.sleep(delayLength)
    ###Check encoder calibration###
    mode01Txt4.set("Checking if encoder calibration was succesful.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    objectOdrv.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while objectOdrv.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    objectOdrv.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while objectOdrv.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    #using min, max becuase of noise, check later
    minEncoderVal = -1000 #in counts 
    maxEncoderVal = 9000 #in counts
    if(not(objectOdrv.axis0.encoder.pos_estimate > minEncoderVal) and not(objectOdrv.axis0.encoder.pos_estimate < maxEncoderVal) and not(objectOdrv.axis1.encoder.pos_estimate > minEncoderVal) and not(objectOdrv.axis1.encoder.pos_estimate < maxEncoderVal)):
        ###Calibration was not succesful###
        mode01Txt4.set("Calibration was not succesful")
        mode01Msg4.configure(text = mode01Txt4)
        objectRoot.update()
        time.sleep(delayLength)
        calibrationSuccesful02 = False
        return
    time.sleep(delayLength)
    ###Calibration was succesful###
    mode01Txt4.set("Calibration was succesful, saving configuration.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    objectOdrv.save_configuration()
    time.sleep(delayLength)
    ###Going to IDLE###
    mode01Txt4.set("End of calibration. Going to IDLE.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    objectOdrv.axis0.requested_state = AXIS_STATE_IDLE
    objectOdrv.axis1.requested_state = AXIS_STATE_IDLE
    time.sleep(delayLength)
    calibrationSuccesful02 = True
    objectRoot.destroy()
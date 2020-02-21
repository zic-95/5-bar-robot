#normal calibration gui
from tkinter import *
import time
import math
import odrive
from odrive.enums import *
import defaultParameters as dP

delayLength = 3 # [s], time to read messages
backgroundColor = '#293134'
lettersColor = '#E7E6DE'

calibrationSuccesful01 = False

def mode01init(objectOdrv):
    root01 = Tk()
    root01.title("5-Bar Robot")
    root01.iconbitmap("C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotIcon.ico")
    root01.configure(background = backgroundColor)
    
    mode01Txt1 = StringVar()
    mode01Txt1.set("Welcome to the calibration sequence.")
    mode01Msg1 = Message(root01,width = 1000, textvariable = mode01Txt1, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "24", "bold"), relief = FLAT, justify = CENTER)
    mode01Msg1.pack()

    mode01Txt2 = StringVar()
    mode01Txt2.set("Please put the robot in place as photo is showing and press Robot is in place button.")
    mode01Msg2 = Message(root01,width = 1000, textvariable = mode01Txt2, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), relief = FLAT, justify = CENTER)
    mode01Msg2.pack()

    photoFrame = Frame(root01,bd = 0, bg = backgroundColor , highlightbackground = backgroundColor)
    photoFrame.pack(expand = True, fill = X)
    photoCanvas1 = Canvas(photoFrame, width=700, height=490, bg = backgroundColor , highlightbackground = backgroundColor, bd = 0)
    photoCanvas2 = Canvas(photoFrame, width=700, height=490, bg = backgroundColor , highlightbackground = backgroundColor, bd = 0)
    img1 = PhotoImage(file = "C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotPosition.gif")
    img2 = PhotoImage(file = "C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotPins.gif")
    photoCanvas1.create_image(700/2, 490/2, image = img1)
    photoCanvas2.create_image(700/2, 490/2, image = img2)
    photoCanvas1.pack(side = LEFT, expand = True, fill = X)
    photoCanvas2.pack(side = RIGHT, expand = True, fill = X)

    robotInPlaceB = Button(root01, text = "Robot is in place", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = lambda: enableHandCalibration(handCalibrationB))
    handCalibrationB = Button(root01, text = "Start calibration", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = lambda: startNormalCalibration(root01 ,objectOdrv, handCalibrationB), state = DISABLED)
    cameraCalibrationB = Button(root01, text = "Camera Calibration Sequence", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor, highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = startCameraCalibration, state = DISABLED)
    robotInPlaceB.pack(expand = True, fill = X)
    handCalibrationB.pack(expand = True, fill = X)
    cameraCalibrationB.pack(expand = True, fill = X)

    root01.mainloop()

def enableHandCalibration(buttonPass):
    buttonPass.config(state = NORMAL)

def startNormalCalibration(objectRoot, objectOdrv, buttonPass):
    buttonPass.config(state = DISABLED)
    mode01Txt3 = StringVar()
    mode01Txt3.set("Calibration has started, please wait for it to finish.")
    mode01Msg3 = Message(objectRoot,width = 1000, textvariable = mode01Txt3, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "24", "bold"), relief = FLAT, justify = CENTER)
    mode01Msg3.pack(expand = True, fill = X)
    normalCalibrationSequence(objectRoot, objectOdrv)

def normalCalibrationSequence(objectRoot, objectOdrv):
    global calibrationSuccesful01
    mode01Txt4 = StringVar()
    mode01Txt4.set("Sending motor parameters to driver")
    mode01Msg4 = Message(objectRoot,width = 1000, textvariable = mode01Txt4, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), relief = FLAT, justify = CENTER)
    mode01Msg4.pack(expand = True, fill = X)
    ###Send parameters###
    dP.sendParameters(objectOdrv)
    objectRoot.update()
    time.sleep(delayLength)
    ###Check parameters###
    mode01Txt4.set("Checking if parameters were send succesfully and motor is precalibrated.")
    mode01Msg4.configure(text = mode01Txt4)
    if(not(dP.checkParameters(objectOdrv))):
        calibrationSuccesful01 = False
        return
    objectRoot.update()
    time.sleep(delayLength)
    ###Z-pulse search###
    mode01Txt4.set("Finding Encoder Z pulse.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    objectOdrv.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while objectOdrv.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    objectOdrv.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while objectOdrv.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    time.sleep(delayLength)
    ###Check encoder calibration###
    mode01Txt4.set("Checking if encoder calibration was succesful.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    time.sleep(delayLength)
    #using min, max becuase of noise, check later
    minEncoderVal = -1000 #in counts 
    maxEncoderVal = 9000 #in counts
    if(not(objectOdrv.axis0.encoder.pos_estimate > minEncoderVal) and not(objectOdrv.axis0.encoder.pos_estimate < maxEncoderVal) and not(objectOdrv.axis1.encoder.pos_estimate > minEncoderVal) and not(objectOdrv.axis1.encoder.pos_estimate < maxEncoderVal)):
        ###Calibration was not succesful###
        mode01Txt4.set("Calibration was not succesful")
        mode01Msg4.configure(text = mode01Txt4)
        objectRoot.update()
        time.sleep(delayLength)
        calibrationSuccesful01 = False
        return
    ###Calibration was succesful###
    mode01Txt4.set("Calibration was succesful!")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    time.sleep(delayLength)
    ###Going to IDLE###
    mode01Txt4.set("End of calibration. Going to IDLE.")
    mode01Msg4.configure(text = mode01Txt4)
    objectRoot.update()
    objectOdrv.axis0.requested_state = AXIS_STATE_IDLE
    objectOdrv.axis1.requested_state = AXIS_STATE_IDLE
    time.sleep(delayLength)
    calibrationSuccesful01 = True
    objectRoot.destroy()

############### TODO ###############
def startCameraCalibration():
    pass #TODO: implement camera calibraiton, now it has to be done by hand

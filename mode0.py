#welcome window, used for calibration
from tkinter import *
import mode01
import mode02

backgroundColor = '#293134'
lettersColor = '#E7E6DE'

def mode0init(objectOdrv):
    root0 = Tk()
    root0.title("5-Bar Robot")
    root0.iconbitmap("C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotIcon.ico")
    root0.configure(background = backgroundColor)
    startMsgTxt1 = StringVar()
    startMsgTxt2 = StringVar()
    startMsgTxt1.set("5-BAR PARALLEL ROBOT")
    startMsgTxt2.set("Press Normal Calibration Sequence if robot has been calibrated before. Otherwise press Full Calibration Sequence.")
    startMsg1 = Message(root0, pady = 50, textvariable = startMsgTxt1, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "24", "bold"), relief = FLAT, justify = CENTER)
    startMsg2 = Message(root0, pady = 50, textvariable = startMsgTxt2, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "12") , relief = FLAT)
    startMsg1.pack()
    startMsg2.pack()

    normalCalibrationButton = Button(root0, text = "Normal Calibration Sequence", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold") , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = lambda: callMode01(root0, objectOdrv))
    fullCalibrationButton = Button(root0, text = "Full Calibration Sequence", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = lambda: callMode02(root0, objectOdrv))
    normalCalibrationButton.pack(expand = True, fill = X)
    fullCalibrationButton.pack(expand = True, fill = X)
    root0.mainloop()
    if(mode01.calibrationSuccesful01 or mode02.calibrationSuccesful02):
        return True
    else:
        return False

def callMode01(objectRoot, objectOdrv):
    objectRoot.destroy() #kills mode0
    mode01.mode01init(objectOdrv)

def callMode02(objectRoot, objectOdrv):
    objectRoot.destroy() #kills mode0
    mode02.mode02init(objectOdrv)

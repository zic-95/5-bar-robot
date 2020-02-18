from tkinter import *
import time
import mode0
import mode1
import odrive
from odrive.enums import *

odrv0 = odrive.find_any()

backgroundColor = '#293134'
lettersColor = '#E7E6DE'

def quitRoot(objectRoot):
    objectRoot.destroy()

def succesfulCalibration(objectRoot):
    objectRoot.title("5-Bar Robot")
    objectRoot.iconbitmap("C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotIcon.ico")
    objectRoot.configure(background = backgroundColor)
    startMsgTxt1 = StringVar()
    startMsgTxt1.set("Calibration was successful, press Open aplication to start robot.")
    startMsg1 = Message(objectRoot, pady = 50, textvariable = startMsgTxt1, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "24", "bold"), relief = FLAT, justify = CENTER)
    startMsg1.pack()
    openButton = Button(objectRoot, text = "Open aplication", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold") , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = lambda: quitRoot(objectRoot))
    openButton.pack(expand = True, fill = X)
    objectRoot.mainloop()

def unSuccesfulCalibration(objectRoot):
    objectRoot.title("5-Bar Robot")
    objectRoot.iconbitmap("C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotIcon.ico")
    objectRoot.configure(background = backgroundColor)
    startMsgTxt1 = StringVar()
    startMsgTxt1.set("Unfortunately, calibration was not succesful, please try again.")
    startMsg1 = Message(objectRoot, pady = 50, textvariable = startMsgTxt1, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "24", "bold"), relief = FLAT, justify = CENTER)
    startMsg1.pack()
    quitButton = Button(objectRoot, text = "Quit", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold") , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, command = lambda: quitRoot(objectRoot))
    quitButton.pack(expand = True, fill = X)
    objectRoot.mainloop()

def main():
    
    if(mode0.mode0init(odrv0)):
        rootMS = Tk()
        succesfulCalibration(rootMS)
        mode1.mode1init(odrv0)
    else:
        rootMUS = Tk()
        unSuccesfulCalibration(rootMUS)

main()




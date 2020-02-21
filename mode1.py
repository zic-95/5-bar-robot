from tkinter import *
import odrive
from odrive.enums import *
import time
from numpy import pi, sqrt
import mode1Helpers as m1H

backgroundColor = '#293134'
lettersColor = '#E7E6DE'
#odrv0 = odrive.find_any()


global_xTcp = 0.0 #home position x
global_yTcp = 268.627 #home postion y
global_theta0 = 1/4 * pi #home position theta0(right motor)
global_theta1 = 3/4 * pi #home postion theta0(left motor)

##When in idle, and goes to closed loop, convert from encoder estimate pos to abscnt
global_absCnt0 = 0 #encoder absoulte counts for home position, motor0, right
global_absCnt1 = 0 #encoder absoulte counts for home position, motor1, left
maxCurrent = 0.0 #motor max current
maxVel = 0.0 #motor max velocity
"""Keep in mind that you must still set your safety limits as before. I recommend you set these a little higher ( > 10%) than the planner values, to give the controller enough control authority."""
trapVelLimit = 50000 #trajectory control velocity limit
trapAccLimit = 10000 #trajectory control acceleration limit
trapDeccLimit = 10000 #trajectory control decceleration limit

joggIncrement = 0 #Used for Jogg mode, can be 1, 2, 5, 10 mm
cprCount = 8192

def mode1init(objectOdrv):
    root1 = Tk()
    root1.title("5-Bar Robot")
    root1.iconbitmap("C:/Users/Matej/Desktop/5_Bar_Robot/photo_gif/robotIcon.ico")
    root1.configure(background = backgroundColor)
    
    ##Draw robot positon
    robotPosition = Canvas(root1, width=750, height=500, bg = backgroundColor , cursor = "dot", highlightbackground = backgroundColor)
    robotPosition.pack(expand = True, fill = "both")
    ##Jogging mode
    joggMode = LabelFrame(root1, text = "Jogg mode", bd = 0, bg = backgroundColor , highlightbackground = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"))
    joggMode.pack(expand = True, fill = "both")
    joggModeInit(joggMode, objectOdrv)
    ##GoTo mode
    goToMode = LabelFrame(root1, text = "GoTo mode", bd = 0, bg = backgroundColor , highlightbackground = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"))
    goToMode.pack(expand = True, fill = "both")
    goToModeInit(goToMode, objectOdrv)

    #quit
    quitButton = Button(root1, text = "QUIT", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: quitFunc(objectOdrv, root1))
    #idle
    idleRightButton = Button(root1, text = "IDLE", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: idleFunc(objectOdrv))
    #closed loop
    cloosedLoopButton = Button(root1, text = "CLOSED LOOP", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: closedLoopFunc(objectOdrv))
    quitButton.pack()
    idleRightButton.pack()
    cloosedLoopButton.pack()
    root1.mainloop()

##TEMP---START
def quitFunc(objectOdrv, objectRoot):
    objectOdrv.axis0.requested_state = AXIS_STATE_IDLE
    objectOdrv.axis1.requested_state = AXIS_STATE_IDLE
    objectRoot.destroy()

def idleFunc(objectOdrv):
    objectOdrv.axis0.requested_state = AXIS_STATE_IDLE
    objectOdrv.axis1.requested_state = AXIS_STATE_IDLE

def closedLoopFunc(objectOdrv):
    global global_xTcp, global_yTcp, global_theta0, global_theta1, global_absCnt0, global_absCnt1
    global_xTcp = 0.0 #home position x
    global_yTcp = 268.627 #home postion y
    global_theta0 = 1/4 * pi #home position theta0(right motor)
    global_theta1 = 3/4 * pi #home postion theta0(left motor)
    objectOdrv.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
    objectOdrv.axis1.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
    ##When in idle, and goes to closed loop, convert from encoder estimate pos to abscnt
    global_absCnt0 = 0 #encoder absoulte counts for home position, motor0, right
    global_absCnt1 = 0 #encoder absoulte counts for home position, motor1, left
    objectOdrv.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while objectOdrv.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.2)
    objectOdrv.axis1.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
    while objectOdrv.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.2)
    objectOdrv.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    objectOdrv.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
##TEMP---END

def paint(event):
    w.delete('my_tag')
    global global_Theta0
    global global_Theta1
    global global_absCnt0
    global global_absCnt1
    x3, y3 = (event.x - 375), (400 - event.y) 
    t0, t1 = kin.inverseKinematics(x3, y3)
    x2, y2 = -l0 + l1*math.cos(t0), l1*math.sin(t0)
    x4, y4 = l0 + l1*math.cos(t1), l1*math.sin(t1)
    coordinates = [x1, y1, x2 + 375, 400 - y2, x3 + 375, 400 - y3, x4 + 375, 400 - y4, x5, y5 ]
    w.create_line(coordinates, width = 10, fill = "#19a4bf", tags='my_tag')

def drawRobot(passCanvas):
    passCanvas.create_line(20, 20, 730, 20, 730, 480, 20, 480, 20, 20, width = 5, fill = lettersColor)
    passCanvas.create_line(270, 337.5, 480, 337.5, 480, 480, 270, 480, 270, 337.5, width = 3, fill = lettersColor)
    passCanvas.create_arc(-47.5, 20, 712.5, 780, start = -12.5, extent = 97, style = ARC, width = 3, outline = lettersColor)
    passCanvas.create_arc(37.5, 20, 797.5, 780, start = 192.5, extent = -97, style = ARC, width = 3, outline = lettersColor)
    passCanvas.create_line(start_coordinates, width = 10, fill = "#19a4bf", tags='killOld')
    passCanvas.grid(row = 0, column = 0)
    passCanvas.bind("<B1-Motion>", paint)

def radioButtonSelection(passVar):
    global joggIncrement
    joggIncrement = passVar.get()

def joggModeInit(objectFrame, objectOdrv):
    var = IntVar()
    r1 = Radiobutton(objectFrame, text = "1 mm", variable=var, value=1, bd = 0, command = lambda: radioButtonSelection(var))
    r2 = Radiobutton(objectFrame, text = "2 mm", variable=var, value=2, bd = 0, command = lambda: radioButtonSelection(var))
    r5 = Radiobutton(objectFrame, text = "5 mm", variable=var, value=5, bd = 0, command = lambda: radioButtonSelection(var))
    r10 = Radiobutton(objectFrame, text = "10 mm", variable=var, value=10, bd = 0, command = lambda: radioButtonSelection(var))
    r1.grid(row = 0, column = 0)
    r2.grid(row = 0, column = 1)
    r5.grid(row = 0, column = 2)
    r10.grid(row = 0, column = 3)
    upLeftButton = Button(objectFrame, text = "UP LEFT", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: joggModeFunc(objectOdrv, "UL"))
    upButton = Button(objectFrame, text = "UP", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: joggModeFunc(objectOdrv, "U"))
    upRightButton = Button(objectFrame, text = "UP RIGHT", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: joggModeFunc(objectOdrv, "UR"))
    leftButton = Button(objectFrame, text = "LEFT", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: joggModeFunc(objectOdrv, "L"))
    middleButton = Button(objectFrame, text = "", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = DISABLED)
    rightButton = Button(objectFrame, text = "RIGHT", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: joggModeFunc(objectOdrv, "R"))
    downLeftButton = Button(objectFrame, text = "DOWN LEFT", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: joggModeFunc(objectOdrv, "DL"))
    downButton = Button(objectFrame, text = "DOWN", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: joggModeFunc(objectOdrv, "D"))
    downRightButton = Button(objectFrame, text = "DOWN RIGHT", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "16", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: joggModeFunc(objectOdrv, "DR"))

    upLeftButton.grid(row = 1, column = 0)
    upButton.grid(row = 1, column = 1)
    upRightButton.grid(row = 1, column = 2)
    leftButton.grid(row = 2, column = 0)
    middleButton.grid(row = 2, column = 1)
    rightButton.grid(row = 2, column = 2)
    downLeftButton.grid(row = 3, column = 0)
    downButton.grid(row = 3, column = 1)
    downRightButton.grid(row = 3, column = 2)

def joggModeFunc(objectOdrv, direction):
    #CHANGES global_xTcp, global_yTcp
    #finds endpoint at fixed distance(choosed by radiobutton, and direction button), checks if newpoint is in working distance,
    #finds set of points between start and end point, finds motor angles for set of points, makes conversion from degrees to absoulte ecnoder counts,
    #sends absoulte enoder counts to drivers, updates x,y TCP
    global joggIncrement, global_xTcp, global_yTcp
    pointsResolution = joggIncrement #1 point per 1 mm
    directionFactor = m1H.directionToFactor[direction]
    startPoint = (global_xTcp, global_yTcp)
    endPoint = (startPoint[0] + joggIncrement * directionFactor[0], startPoint[1] + joggIncrement * directionFactor[1])
    if(not(m1H.isInWorkSpace(endPoint[0], endPoint[1]))): #Check if end point is in workspace
        return
    vecOfPoints = m1H.getEquidistantPoints(startPoint, endPoint, pointsResolution )
    for i in vecOfPoints:
        newTheta0, newTheta1 = m1H.inverseKinematics(i[0], i[1]) #theta0, theta1 from x,y coordinate
        newPos0, newPos1 = thetaToCnt(newTheta0, newTheta1)
        trapMoving(objectOdrv, newPos0, newPos1)
    global_xTcp, global_yTcp= endPoint[0], endPoint[1] #update global TCP
    print("TCP: ", global_xTcp, global_yTcp)

def goToModeInit(objectFrame, objectOdrv):
    global global_xTcp, global_yTcp
    oldXtext, oldYtext= global_xTcp, global_yTcp
    xLabel = Label(objectFrame, text = "new X:", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor)
    yLabel = Label(objectFrame, text = "new Y:", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor)
    xLabel.grid(row = 0, column = 0)
    yLabel.grid(row = 1, column = 0)
    
    xEntry = Entry(objectFrame, bg  = lettersColor, fg = backgroundColor, font =("Helvetica", "10", "bold"), highlightbackground= lettersColor , highlightcolor = lettersColor, relief = FLAT)
    yEntry = Entry(objectFrame, bg  = lettersColor, fg = backgroundColor, font =("Helvetica", "10", "bold"), highlightbackground= lettersColor , highlightcolor = lettersColor, relief = FLAT)
    xEntry.grid(row = 0, column = 1)
    yEntry.grid(row = 1, column = 1)
    
    jointButton = Button(objectFrame, text = "JOINT", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: gotoModeFunc(objectOdrv, objectFrame, "JOINT", xEntry, yEntry, oldXLabelValue, oldYLabelValue))
    linearButton = Button(objectFrame, text = "LINEAR", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor, state = NORMAL, command = lambda: gotoModeFunc(objectOdrv, objectFrame, "LINEAR", xEntry, yEntry, oldXLabelValue, oldYLabelValue))
    jointButton.grid(row = 0, column = 2, rowspan = 2)
    linearButton.grid(row = 0, column = 3, rowspan = 2)
    
    oldXLabelTxt = Label(objectFrame, text = "current X:", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor)
    oldYLabelTxt = Label(objectFrame, text = "current Y:", bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor)
    oldXLabelTxt.grid(row = 0, column = 4)
    oldYLabelTxt.grid(row = 1, column = 4)
    oldXLabelValue = Label(objectFrame, text = oldXtext, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor)
    oldYLabelValue = Label(objectFrame, text = oldYtext, bg  = backgroundColor, fg = lettersColor, font =("Helvetica", "10", "bold"), highlightbackground= backgroundColor , highlightcolor = backgroundColor, relief = FLAT, activebackground = backgroundColor)
    oldXLabelValue.grid(row = 0, column = 5)
    oldYLabelValue.grid(row = 1, column = 5)

def gotoModeFunc(objectOdrv, cobjectFrame, mvmtType, xEntry, yEntry, oldXLabelValueUpdate, oldYLabelValueUpdate):
    global joggIncrement, global_xTcp, global_yTcp
    if(xEntry.get() == "" or yEntry.get() == ""):
        xEntry.delete(0, 'end') #clears entry area before exiting
        yEntry.delete(0, 'end') #clears entry area before exiting
        return
    startPoint = [global_xTcp, global_yTcp]
    endPoint = [float(xEntry.get()), float(yEntry.get())]
    if(not(m1H.isInWorkSpace(endPoint[0], endPoint[1]))): #Check if end point is in workspace
        xEntry.delete(0, 'end') #clears entry area before exiting
        yEntry.delete(0, 'end') #clears entry area before exiting
        return
    if(mvmtType == "JOINT"):
        newTheta0, newTheta1 = m1H.inverseKinematics(endPoint[0], endPoint[1]) #theta0, theta1 from x,y coordinate
        newPos0, newPos1 = thetaToCnt(newTheta0, newTheta1)
        trapMoving(objectOdrv, newPos0, newPos1)
    if(mvmtType == "LINEAR"):
        pointsResolution = sqrt((startPoint[0]-endPoint[0])*(startPoint[0]-endPoint[0]) + (startPoint[1]-endPoint[1])*(startPoint[1]-endPoint[1]))  #1 point per 1 mm
        pointsResolutionINT = int(pointsResolution * 2)
        vecOfPoints = m1H.getEquidistantPoints(startPoint, endPoint, pointsResolutionINT )
        for i in vecOfPoints:
            newTheta0, newTheta1 = m1H.inverseKinematics(i[0], i[1]) #theta0, theta1 from x,y coordinate
            newPos0, newPos1 = thetaToCnt(newTheta0, newTheta1)
            trapMoving(objectOdrv, newPos0, newPos1)
    global_xTcp, global_yTcp= endPoint[0], endPoint[1] #update global TCP
    xEntry.delete(0, 'end') #clears entry area when finished
    yEntry.delete(0, 'end') #clears entry area when finished
    oldXLabelValueUpdate.config(text = endPoint[0])
    oldYLabelValueUpdate.config(text = endPoint[1])





def thetaToCnt(newTheta0, newTheta1):
    #calculates new absolute position, CHANGES global_theta0, global_theta1, global_absCnt0, global_absCnt1
    #updates global abscnt0 and 1 and global theta0 and 1
    global global_theta0, global_theta1, global_absCnt0, global_absCnt1
    localTheta0 = newTheta0 - global_theta0
    localTheta1 = newTheta1 - global_theta1
    if localTheta0 < 0:
        global_absCnt0 -= abs(localTheta0) * 8192/(2*pi)
    elif localTheta0 > 0:
        global_absCnt0 += localTheta0 * 8192/(2*pi)
    if localTheta1 < 0:
        global_absCnt1 -= abs(localTheta1) * 8192/(2*pi)
    elif localTheta1 > 0:
        global_absCnt1 += localTheta1 * 8192/(2*pi)
    print(global_absCnt0, global_absCnt1)
    global_theta0 = newTheta0
    global_theta1 = newTheta1
    return (global_absCnt0, global_absCnt1)

def trapMoving(objectOdrv, newPos0, newPos1):
    global trapVelLimit, trapAccLimit, trapDeccLimit #controled with slider
    #objectOdrv.axis0.trap_traj.config.vel_limit = trapVelLimit       #is the maximum planned trajectory speed, sets coasting speed, value must be positive(>=0)
    #objectOdrv.axis1.trap_traj.config.vel_limit = trapVelLimit       #is the maximum planned trajectory speed, sets coasting speed, value must be positive(>=0)
    #objectOdrv.axis0.trap_traj.config.accel_limit = trapAccLimit     #the maximum acceleration [counts / sec^2], value must be positive(>=0)
    #objectOdrv.axis1.trap_traj.config.accel_limit = trapAccLimit     #the maximum acceleration [counts / sec^2], value must be positive(>=0)
    #objectOdrv.axis0.trap_traj.config.decel_limit = trapDeccLimit     #is the maximum deceleration [counts / sec^2], value must be positive(>=0)
    #objectOdrv.axis1.trap_traj.config.decel_limit = trapDeccLimit     #is the maximum deceleration [counts / sec^2], value must be positive(>=0)
    #actual moving
    #objectOdrv.axis0.controller.move_to_pos(newPos0)
    #objectOdrv.axis1.controller.move_to_pos(newPos1)
    objectOdrv.axis0.controller.pos_setpoint = newPos0
    objectOdrv.axis1.controller.pos_setpoint = newPos1


mode1init(5)
import math
from numpy import pi, sqrt, linspace
import matplotlib.pyplot as plt
import sys

l0 = 42.5   # Length between origin and the two motors      [mm]
l1 = 160    # Length from motor to passive joints           [mm]
l2 = 220    # Length from passive joints to end effector    [mm]

directionToFactor = {
    "UL"    : (-(sqrt(2)/2), (sqrt(2)/2)),
    "U"     : (0, 1),
    "UR"    : ((sqrt(2)/2), (sqrt(2)/2)),
    "L"     : (-1, 0),
    "R"     : (1, 0),
    "DL"    : (-(sqrt(2)/2), -(sqrt(2)/2)),
    "D"     : (0, -1),
    "DR"    : ((sqrt(2)/2), -(sqrt(2)/2)),
}

def inverseKinematics(x, y):

    if(not(isInWorkSpace(x, y))):
        quit()
    beta0 = math.atan2( y, (l0 - x) )
    beta1 = math.atan2( y, (l0 + x) )
    alpha0_calc = (l1**2 + ( (l0 - x)**2 + y**2 ) - l2**2) / (2*l1*math.sqrt( (l0 - x)**2 + y**2 ))  
    alpha1_calc = (l1**2 + ( (l0 + x)**2 + y**2 ) - l2**2) / (2*l1*math.sqrt( (l0 + x)**2 + y**2 ))  

    # If calculations > 1, will fail acos function
    if alpha0_calc > 1 or alpha1_calc > 1:
        print("Unreachable coordinates")
        quit()

    alpha1 = math.acos(alpha1_calc)
    alpha0 = math.acos(alpha0_calc)

    returnTheta0 = math.pi - beta0 - alpha0
    returnTheta1 = beta1 + alpha1

    return(returnTheta0, returnTheta1)
##TODO: FIX FK
""" def forwardKinematics(t1, t2):
    m = 2*l0 + l2 * (math.cos(t2) - math.cos(t1))
    n = l1 * abs(math.sin(t1) - math.sin(t2))
    print(n, "  ", m, "  ")
    fi1 = math.acos(math.sqrt(m**2 + n**2) / 2 * l2)
    fi2 = math.atan(n / m)

    p1 = fi1 + fi2
    p2 = math.pi - fi1 + fi2

    returnX = l0 + l1 * math.cos(t1) + l2 * math.cos(p1)
    returnY = l1 * math.sin(t2) + l2 * math.sin(p2)

    return(returnX, returnY)
 """
def radToDeg(t1,t2):
    return( t1 * 180 / math.pi, t2 * 180 / math.pi)

def degToRad(t1,t2):
    return( t1 * math.pi / 180, t2 * math.pi / 180)

def isInWorkSpace(x, y):
    if(not(((x - 42.5)**2 + (y - 0)**2) < 380**2)):
        return False
    if(not(((x + 42.5)**2 + (y - 0)**2) < 380**2)):
        return False
    if((-105 < x < 105 ) and (-78 < y < 63)):
        return False
    if(not((-355 < x < 355 ) and (-78 < y < 382))):
        return False
    return True


def getEquidistantPoints(p1, p2, parts):
    return zip(linspace(p1[0], p2[0], parts+1),
               linspace(p1[1], p2[1], parts+1))


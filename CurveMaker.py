# OMRANE005

import matplotlib.pyplot as plt
import math
import numpy as np


def join(cord_y_1, cord_x_1, cord_y_2, cord_x_2):

    dy = cord_y_2-cord_y_1
    dx = cord_x_2-cord_x_1

    angle = math.atan(dy/dx)

    angle = np.degrees(angle)

    if dx < 0 and dy < 0:
        finalangle = angle + 360

    if dx >= 0 and dy < 0:

        finalangle = angle + 180

    if dx < 0 and dy > 0:

        finalangle = angle+180

    if dx > 0 and dy > 0:
        finalangle = angle

    distance = np.sqrt(dy**2+dx**2)

    if finalangle > 360:

        return finalangle-360, distance

    elif finalangle < 0:

        return finalangle+360, distance

    else:
        return finalangle, distance

# calcualtes a polar given co-oridnates for one point and a direction and distance to the next point


def polar(y1, x1, distance, direction):

    x2 = x1 + distance*np.cos(np.radians(direction))
    y2 = y1 + distance*np.sin(np.radians(direction))
    return (y2, x2)

# converts from decimal degrees to dms


def dec2dms(Dec):

    d = int(Dec)
    m = int(abs(Dec - d) * 60)
    s = round((((abs(Dec - d) * 60)-m)*60), 0)

    return d, m, s

# converts from dms to decimal degrees


def dms2dec(dms):
    degrees, minutes, seconds = dms.split(",")
    degrees = eval(degrees)
    minutes = eval(minutes)
    seconds = eval(seconds)
    decimal_degrees = degrees + minutes / 60 + seconds / 3600
    return decimal_degrees


userInput = False

# manual input
if userInput == False:
    Radius = 15
    Velocity = 25
    CRA = 2
    Width = 6
    ChainageInterval = 4

    StraightA = "-32529.87 11326.83 125,27,30"

    StraightB = "-32526.67 11281.83 53,54,6"
# user input
else:
    Radius = input("Enter Radius :")
    Velocity = input("Enter Velocity : ")
    CRA = input("Enter Change in radial acceleration: ")
    Width = input("Enter road width: ")
    ChainageInterval = input("Enter chainage interval: ")

    StraightA = input("Enter first straight in form (y x dms): ")

    StraightB = input("Enter first straight in form (y x dms): ")

# process input
StraightA = StraightA.split(' ')
straightAY = eval(StraightA[0])
straightAX = eval(StraightA[1])
straightAAngle = math.radians(dms2dec(StraightA[2]))

StraightB = StraightB.split(' ')
straightBY = eval(StraightB[0])
straightBX = eval(StraightB[1])
straightBAngle = math.radians(dms2dec(StraightB[2]))


# question 1
print("Question 1")
# intersection to get IP


XIP = (straightAX) + ((straightBY - straightAY)-((straightBX-straightAX) *
                                                 math.tan(straightBAngle)))/(math.tan(straightAAngle) - math.tan(straightBAngle))

YIP = straightAY + ((XIP-straightAX)*(math.tan(straightAAngle)))

print("Y           X")
print("A", straightAY, "   ", straightAX)
print("B", straightBY, "   ", straightBX)
print("     ", round(straightBY-straightAY, 2), "    ", straightBX-straightAX)
print("A-N  ", StraightA[2])
print("B-N  ", StraightB[2])
print("co-ordinates of IP (y,x): ", round(YIP, 2), ",", round(XIP, 2))

intersectionAngle = 180-(math.degrees(straightAAngle) -
                         math.degrees(straightBAngle))

print("Intersection angle: ", dec2dms(intersectionAngle))
print()

# calculates super elevation

superElevation = (Width*(Velocity**2))/(282.8*Radius)

print("Super Elevation :", round(superElevation, 3))
print()

# calculates length of curver

L = (Velocity**3)/((3.6**3)*CRA*Radius)
L = ChainageInterval * round(L / ChainageInterval)
print("length of curve : ", L, "m")
print()

# calculates the shift

shift = ((L**2)/(24*Radius))-((L**4)/(2688*(Radius**3)))
print("Shift: ", round(shift, 3))

apexDistance = (L/2)+((Radius+shift) *
                      (math.tan(math.radians(intersectionAngle/2))))-((L**3)/(240*(Radius**2)))
print("Apex distance: ", round(apexDistance, 3))
print()


IPA_Angle = straightAAngle + math.radians(180)
IPB_Angle = straightBAngle + math.radians(180)

polarTP1 = polar(YIP, XIP, apexDistance, math.degrees(IPA_Angle))
polarTP2 = polar(YIP, XIP, apexDistance, math.degrees(IPB_Angle))

TP1X = polarTP1[1]
TP1Y = polarTP1[0]

TP2X = polarTP2[1]
TP2Y = polarTP2[0]

print("TP1: ", round(TP1Y, 3), ",", round(TP1X, 3)+3800000)
print("TP2: ", round(TP2Y, 3), ",", round(TP2X, 3)+3800000)
print()


tanAngle = L/(2*Radius)
print("Tangential angle: ", dec2dms(math.degrees(tanAngle)))
print()


lenTranCurv = (Radius*math.radians(intersectionAngle)) + L

print("Length of combined curve: ", round(lenTranCurv, 3), "m")
print()

chainX = []
chainY = []

print("Transitional Points")
for i in range(ChainageInterval, ChainageInterval*4, ChainageInterval):
    y = (1/6)*(i**3/(Radius*L)) - (1/336)*((i**7)/((Radius*L)**3)) + \
        (1/42240)*((i**11)/((Radius*L)**5))
    x = i - ((1/40)*((i**5/((Radius*L)**2)))) + \
        ((1/3456)*(i**9/((Radius*L)**4)))

    distance = np.sqrt(y**2+x**2)
    direction = math.degrees(straightAAngle)+math.degrees(math.atan(y/x))
    polarPoint_i = polar(TP1Y, TP1X, distance, direction)
    polarPoint_iX = polarPoint_i[1]
    polarPoint_iY = polarPoint_i[0]
    chainX.append(polarPoint_iX)
    chainY.append(polarPoint_iY)

    print()

    print("Chainage: ", i)
    print("co-ordinates: ", round(polarPoint_iY, 2),
          ",", round(polarPoint_iX, 2))

    print("Polar from TP1 to Chainage:")
    print()

    print("                     ", "y                       x")
    print(round(distance, 2), " m        ", round(TP1Y, 2),
          "               ", round(TP1X, 2))
    print(dec2dms(direction), "   ", round(distance*math.sin(math.radians(direction)), 2),
          "                  ", round(distance*math.cos(math.radians(direction))), 2)
    print("                 ", "----------------------------------------------")
    print("                ",
          round(polarPoint_iY, 2), "                  ", round(polarPoint_iX, 2)+3800000)
    print("                 ", "----------------------------------------------")

    print()

betas = []
distances = []

# points for circular curves

print("Circular Points")

for i, k in zip(range(1, 5, 1), range(16, 32, 4)):

    beta = ChainageInterval/(2*Radius)
    gamma = beta
    beta1 = beta + (i-1)*gamma
    distanceC = (2*Radius)*math.sin(beta1)
    directionC = (straightAAngle)+(tanAngle)+beta1
    betas.append(beta1)
    distances.append(distanceC)
    polar16toChainage = polar(
        chainY[2], chainX[2], distanceC, math.degrees(directionC))
    chainX.append(polar16toChainage[1])
    chainY.append(polar16toChainage[0])

    print("Polar from Chainage 16 to Chainage", k, ":")
    print()

    print("                     ", "y                       x")
    print(round(distanceC, 2), " m        ", round(chainY[2], 2),
          "               ", round(chainX[2], 2))
    print(dec2dms(directionC), "   ", round(distanceC*math.sin(math.radians(directionC)), 2),
          "                  ", round(distanceC*math.cos(math.radians(directionC))), 2)
    print("                 ", "----------------------------------------------")
    print("                ",
          round(polar16toChainage[0], 3), "                  ", round(polar16toChainage[1], 3))
    print("                 ", "----------------------------------------------")

    print()

# points for transitional curves
print("Transitional Points")
print()

d = [12, 8.390, 4.390, 0.390]

for i, k in zip(d, range(28, 44, 4)):

    y = (1/6)*(i**3/(Radius*L)) - (1/336)*((i**7)/((Radius*L)**3)) + \
        (1/42240)*((i**11)/((Radius*L)**5))

    x = i - ((1/40)*((i**5/((Radius*L)**2)))) + \
        ((1/3456)*(i**9/((Radius*L)**4)))

    distance = np.sqrt(y**2+x**2)
    direction = math.degrees(straightBAngle) - math.degrees(math.tan(y/x))
    polar_i = polar(TP2Y, TP2X, distance, direction)
    chainX.append(polar_i[1])
    chainY.append(polar_i[0])

    print("Polar from TP2 to Chainage", k, ":")
    print()

    print("                     ", "y                       x")
    print(round(distance, 2), " m        ", round(TP2Y, 2),
          "               ", round(TP2X+3800000, 2))
    print(dec2dms(direction), "   ", round(distance*math.sin(math.radians(direction)), 2),
          "                  ", round(distance*math.cos(math.radians(direction))), 2)
    print("                 ", "----------------------------------------------")
    print("                ",
          round(polar_i[0], 3), "                  ", round(polar_i[1]+3800000, 3))
    print("                 ", "----------------------------------------------")

    print()

print("setting out curve")

# tp1 to chainage
for i in range(1, 10, 1):
    joini = join(TP1Y, TP1X, chainY[i], chainX[i])

    print("join from TP1 to chainage: ", (i+1)*4)

    print("y                           x")
    print(round(TP1Y, 2), "           ", round(TP1X, 2), "        ", dec2dms(
        round(joini[0], 2)))
    print(round(chainY[i], 2), "           ", round(chainX[i], 2), "            ",
          round(joini[1], 3), "m")
    print("-----------------------------------")
    print(round(chainY[i]-TP1Y, 2),
          "             ", round(TP1X-chainX[i], 2))
    print("-----------------------------------")

for i in range(-1, -10, -1):

    print("join from TP2 to chainage: ", ((i+1)*4))
    joini = join(TP2Y, TP2X, chainY[i], chainX[i])

    print("y                           x")
    print(round(TP1Y, 2), "           ", round(TP1X, 2), "        ", dec2dms(
        round(joini[0], 2)))
    print(round(chainY[i], 2), "           ", round(chainX[i], 2), "            ",
          round(joini[1], 3), "m")
    print("-----------------------------------")
    print(round(chainY[i]-TP1Y, 2),
          "             ", round(TP1X-chainX[i], 2))
    print("-----------------------------------")


def to_coordinates(x_list, y_list):
    coordinates = []
    for i in range(len(x_list)):
        coordinates.append((y_list[i], x_list[i]))
    return coordinates


def plot_points(points):
    x = [p[1] for p in points]
    y = [p[0] for p in points]
    fig, ax = plt.subplots()
    ax.invert_yaxis()
    ax.plot(x, y, '-o')
    ax.annotate('T1', (x[0], y[0]))
    for i in range(1, len(points)-1):
        ax.annotate('C{}'.format(i*4), (x[i], y[i]))
    ax.annotate('T2', (x[-1], y[-1]))
    plt.show()


plot_points(to_coordinates(chainX, chainY))

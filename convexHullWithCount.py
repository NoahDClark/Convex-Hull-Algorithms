
import random
from tkinter import *
from matplotlib import pyplot as plt
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

class Points: #Object which stores x and y coordinates
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def get_x(self):
            return self.x
        def get_y(self):
            return self.y

def leftMost(point_list): #finds the starting point at the left most point

    min_val = 0
    for i in range(1, len(point_list)): #traverse input array of Points
        if point_list[i].x < point_list[min_val].x:
            min_val = i
        elif point_list[i].x == point_list[min_val].x: #If 2 left most x values set highest y coordiante point
            if point_list[i].y > point_list[min_val].y:
                min_val = i
    return min_val

def rightMost(point_list):
    
    max_val = 0
    for i in range(1, len(point_list)): #traverse input array of Points
        if point_list[i].x > point_list[max_val].x:
            max_val = i
        elif point_list[i].x == point_list[max_val].x: #If 2 left most x values set lowest y coordiante point
            if point_list[i].y < point_list[max_val].y:
                max_val = i
    return max_val

def slope_function(point1, nextPoint, testPoints):
    #inputs are of Points object
    #use expresion ax+by=c to find relative positions of testPoints
    cExpression= (nextPoint.y - point1.y) * (testPoints.x - nextPoint.x) - (nextPoint.x - point1.x) * (testPoints.y - nextPoint.y)

    if cExpression >= 0: #Points lie on the same line or clockwise position
        return False
    else: #Points in a counter clockwise position
        return True
    


def to2DList(pointsList): #takes list of Points objects and creates a 2D list to save x and y coordinates
    size = len(pointsList)
    rows = size
    cols = 2
    arr = [] #array to save rows and columns
    for i in range(rows):
        col = []
        for j in range(cols):
            if j % 2 == 0: #append x values to first position of each array
                col.append(pointsList[i].x)
            else: #append y values to second position of each array
                col.append(pointsList[i].y)
        arr.append(col)
    return arr

def toPointList(twoDList): #takes 2D list and returns a list of Points objects
    pointList = []
    for i in range(len(twoDList)):
        x = 0
        y = 0
        for j in range(len(twoDList[i])):
            if j % 2 == 0:
                x = twoDList[i][j]
            else:
                y = twoDList[i][j]
        point = Points(x, y)
        pointList.append(point)

    return pointList

#For most cases, it will create a partition for points on the right of P1 to Pn and then Points on the right of Pn to P2
#The if case will only trigger when Pn == P2 which only happens once at the start.
#This is because the algorithm starts with partitions P1 to P2 and P2 to P1.
def partitionPointList(point_list, P1, Pn, P2):
    partitionOne = []
    partitionTwo = []
    if(Pn == P2):
        Pn2 = P2
        Pn3 = P1
    else:
        Pn2 = Pn
        Pn3 = P2
    
    for i in range(len(point_list)):
        if (slope_function(P1,Pn,point_list[i])):
            partitionOne.append(point_list[i])
        elif (slope_function(Pn2, Pn3,point_list[i])):
            partitionTwo.append(point_list[i])
            
    return partitionOne, partitionTwo

def pointDistance(P1, P2, Pn):
    numerator = abs((P2.x - P1.x)*(P1.y-Pn.y) - (P1.x -Pn.x)*(P2.y-P1.y))
    distance = numerator/(((P2.x-P1.x)**2 + (P2.y - P1.y)**2)**0.5)
    return distance
    

    
def findHull(point_list, P1, P2, convexHull):
    #if point list is empty then return; otherwise recursively call code
    if not point_list:
        return
    else:
        #Finds farthest point from line
        maxIndex = 0
        maxDistance = pointDistance(P1, P2, point_list[0])
        for i in range(len(point_list)):
            if(pointDistance(P1, P2, point_list[i]) > pointDistance(P1, P2, point_list[maxIndex])):
                convexHull[0].y = convexHull[0].y + 2
                maxIndex = i
        #Deletes farthest point from list and adds it to convex hull
        nextPoint = point_list[maxIndex]
        del(point_list[maxIndex])
        convexHull.append(nextPoint)
        #new partition for points then recursively calls
        firstHalf, secondHalf = partitionPointList(point_list, P1, nextPoint, P2)
        convexHull[0].x = convexHull[0].x + 1
        findHull(firstHalf, P1, nextPoint, convexHull) 
        findHull(secondHalf, nextPoint, P2, convexHull)
    
            

def quickHull(in_list, size):
    #establishes required variables such as leftmost, rightmost, and the convexHull array
    point_list = toPointList(in_list)
    convexHull = []
    convexHull.append(Points(0,0))
    P1 = point_list[leftMost(point_list)]
    P2 = point_list[rightMost(point_list)]
    convexHull.append(P1)
    convexHull.append(P2)
    
    #partitions points based on which side of the line they're on
    firstHalf, secondHalf = partitionPointList(point_list, P1, P2, P2)
    convexHull[0].x = convexHull[0].x + 1
    
    #Calls findHull; passes convexHull by reference so new points can be added
    findHull(firstHalf, P1, P2, convexHull)
    findHull(secondHalf, P2, P1, convexHull)
    temp = convexHull.pop(0)
    count = temp.x + temp.y
    result_list = to2DList(convexHull)
    return result_list, count

def convexHull(point_list, size):
    #Minimum size 3 uses helper methods to create result list in counter clockwise order starting from leftmost point
    in_list = toPointList(point_list)

    if size < 3:
        return in_list
    firstL = leftMost(in_list) #get first point
    result = []
    currentP = firstL
    count = 0
    nextQ = 0
    while True:
        result.append(in_list[currentP]) #append current point to hull
        nextQ = (currentP + 1) % size
        for i in range(size): # test current and next point with all points
            count = count + 1
            if slope_function(in_list[currentP], in_list[i], in_list[nextQ]): # if next point is in the hull
                nextQ = i

        currentP = nextQ
        if currentP == firstL: #end case if the current point is the first point
            break

    #still need to work on getting output to 2d array
    result_list = to2DList(result)
    return result_list, count


  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  #Everything below is GUI

window = Tk()
fig = Figure(figsize = (5, 5),dpi = 100)
canvas = FigureCanvasTkAgg(fig, master = window)  

labelOne = Label(window, text="Current point list: ", font=("Times",14)).place(x=200,y=50)
labelTwo = Label(window, text="Points in convex hull: ", font=("Times",14)).place(x=700,y=50)
labelThree = Label(window, text="The order of points \n for quickHull Solution: ", font=("Times",14)).place(x=850,y=300)
labelFour = Label(window, text="Note: Lines drawn by \n quickHull are meant to \n demonstrate how it recursively \n solves the convex Hull problem.\n Brute force will output the array in \n counter clockwise order.", font=("Times",14)).place(x=850,y=600)

canvas.draw()
canvas.get_tk_widget().place(x=300,y=200)
toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
class temp():
    def __init__(self, inputArray):
        self.inputArray = inputArray
tempArray = [1]
newTemp = temp(tempArray)

    
#Set the geometry of tkinter frame
window.geometry("1200x800")

def plotPoints():
    points = []
    for i in range(20):
        point = Points(random.randint(-20,20),random.randint(-20,20))
        points.append(point)
    
    twoDPoints = to2DList(points)
    data = np.array(twoDPoints)
    x, y = data.T
    newTemp.tempArray = twoDPoints
    
    string = "Current point list: "
    for i in range(20):
        if(i%5 == 0):
            string = string + " \n"
        string = string + str(twoDPoints[i])
    labelOne = Label(window, text=string, font=("Times",14)).place(x=200,y=50)
    labelTwo = Label(window, text="Points in convex hull: UNKNOWN            \n\n\n", font=("Times",14)).place(x=700,y=50)
    
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),dpi = 100)
    plot1 = fig.add_subplot(111)
    plot1.spines[["left", "bottom"]].set_position(("data", 0))
    plot1.spines[["top", "right"]].set_visible(False)
    
    plot1.scatter(x, y)
  
    canvas = FigureCanvasTkAgg(fig, master = window)  
    # creating the Tkinter canvas
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().place(x=300,y=200)

def plotConvexHull():
    fig = Figure(figsize = (5, 5),dpi = 100)
    plot1 = fig.add_subplot(111)
    plot1.spines[["left", "bottom"]].set_position(("data", 0))
    plot1.spines[["top", "right"]].set_visible(False)
    points = newTemp.tempArray
    print(points)
    
    data = np.array(points)
    x,y = data.T
    plot1.scatter(x, y)
    output, count = convexHull(points, len(points))
    
    string = "Points in convex hull: "
    for i in range(len(output)):
        if(i%5 == 0):
            string = string + " \n"
        string = string + str(output[i])
    string = string + "\n COUNT:"
    string = string + str(count)
    labelTwo = Label(window, text=string, font=("Times",14)).place(x=700,y=50)
    
    output.append(output[0])
    data2 = np.array(output)
    x2, y2 = data2.T
    # the figure that will contain the plot
  
    plot1.plot(x2, y2)
    canvas = FigureCanvasTkAgg(fig, master = window)  
    # creating the Tkinter canvas
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().place(x=300,y=200)

def solveWithQuickHull():
    fig = Figure(figsize = (5, 5),dpi = 100)
    plot1 = fig.add_subplot(111)
    plot1.spines[["left", "bottom"]].set_position(("data", 0))
    plot1.spines[["top", "right"]].set_visible(False)
    points = newTemp.tempArray
    print(points)
    
    data = np.array(points)
    x,y = data.T
    plot1.scatter(x, y)
    output,count = quickHull(points, len(points))
    
    string = "The order of points \n for quickHull Solution: "
    for i in range(len(output)):
        if(i%5 == 0):
            string = string + " \n"
        string = string + str(output[i])
    
    string = string + "\n COUNT:"
    string = string + str(count)
    labelThree = Label(window, text=string, font=("Times",14)).place(x=850,y=300)
    
    output.append(output[0])
    data2 = np.array(output)
    x2, y2 = data2.T
    # the figure that will contain the plot
  
    plot1.plot(x2, y2)
    canvas = FigureCanvasTkAgg(fig, master = window)  
    # creating the Tkinter canvas
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().place(x=300,y=200)
    
    
    
buttonOne=Button(window, height = 4, width = 20, command = plotPoints, text="Display Random Points")
buttonOne.pack(ipadx=10)
buttonOne.place(x=50,y=250)

buttonTwo=Button(window, height = 4, width = 20, text="Solve Convex Hull", command= plotConvexHull)
buttonTwo.pack(ipadx=10)
buttonTwo.place(x=50,y=400)

buttonThree=Button(window, height = 4, width = 20, text="Solve With Quick Hull", command= solveWithQuickHull)
buttonThree.pack(ipadx=10)
buttonThree.place(x=50,y=550)

# place the button 
# in main window

window.bind('<Return>',lambda event:callback())
window.mainloop()

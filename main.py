import math

class Problem :
    def __init__(self, drivers,driversCoord,speed,cost,points,pointsCoord, rides):
        
        #Drivers initialization
        self.drivers = drivers
        self.driversCoord = driversCoord
        self.driversSpeed = speed
        self.driversCost = cost
        
        #Points initialization
        self.points = points
        self.pointsCoord = pointsCoord
        self.rides = rides
        
        
prob = Problem([0,1,2],[(23,23),(90,1),(1,2)],["Home","Work","School"],[(2,2),(9,19),(17,92)],[("Home","Work"),("School","Home"),("Work","School")])

class Solution :
    
    
    def __init__(self, driversRides, prob):
        self.driversRides = driversRides # list of tuples (driver,[rides])
        self.problem = prob
        self.ObjectiveFunction = 0
        
    def DistanceBetweenPoints(self,point1, point2):
            ind1 = self.problem.points.index(point1)
            ind2 = self.problem.points.index(point2)
            dist = math.sqrt((self.problem.pointsCoord[ind1][0]-self.problem.pointsCoord[ind2][0])**2 + 
                             (self.problem.pointsCoord[ind1][1]-self.problem.pointsCoord[ind2][1])**2)
            return dist
    
    def Feasability(self):
        #Also check if all the rides are dispatch and if the ride isnt already assigned to a driver
        if driver in self.problem.drivers and ride in self.problem.rides:
            return True
        else:
            return False
    
    def ObjectiveFunction(self, problem, driversRides):
        #Calculate the total distance and time for each driver and return the total cost in function of it
        return 0


#Do the class method to construct a solution and check if it is feasible


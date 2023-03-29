import math
import random


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
        
prob = Problem([1,2,3],[(0,0),(0,0),(0,0)],1,1,['Home','School','Work'],[(0,0),(0,0),(0,0)],[('Home','School'),('Work','Home'),('School','Work')])

class Solution :
    
    
    def __init__(self, driversRides, prob):
        self.driversRides = driversRides # list of tuples (driver,[rides])
        self.problem = prob
        self.objective = 0
        
    def DistanceBetweenPoints(self,point1, point2):
            ind1 = self.problem.points.index(point1)
            ind2 = self.problem.points.index(point2)
            dist = math.sqrt((self.problem.pointsCoord[ind1][0]-self.problem.pointsCoord[ind2][0])**2 + 
                             (self.problem.pointsCoord[ind1][1]-self.problem.pointsCoord[ind2][1])**2)
            return dist
    
    def Feasability(self, prob):
        #Also check if all the rides are dispatch and if the ride isnt already assigned to a driver
        feasible = True
        for i in range (0,len(self.driversRides)):
            if self.driversRides[i][0] not in self.problem.drivers :
                feasible = False
            for j in range (0,len(self.driversRides[i][1])):
                if self.driversRides[i][1][j] not in self.problem.rides :
                    feasible = False
        if prob.driver in self.problem.drivers and prob.ride in self.problem.rides :
            return True
        else:
            return False
    
    def ObjectiveFunction(self, problem, driversRides):
        #Calculate the total distance and time for each driver and return the total cost in function of it
        return 0


#Do the class method to construct a solution and check if it is feasible

class Method :
    
    def __init__(self, problem):
        self.problem = problem
    
    def RandomSolution(self): #Construct a random solution
        
        tupleList = []
        for i in range (0,len(self.problem.drivers)):
            tupleList.append((self.problem.drivers[i],[]))
            
        for i in range (0,len(self.problem.rides)):
            rand = random.randint(0,len(self.problem.drivers)-1)
            tupleList[rand][1].append(self.problem.rides[i])
    
        solution = Solution(tupleList, self.problem)
        return solution

    def SimpleSwap(self, solution):
        
        #Swap 2 rides between 2 drivers
        randDriver1 = randDriver2 = 0
        while randDriver1 == randDriver2 :
            randDriver1 = random.randint(0,len(self.problem.drivers)-1)
            randDriver2 = random.randint(0,len(self.problem.drivers)-1)
        
        if len(solution.driversRides[randDriver1][1]) > 0 and len(solution.driversRides[randDriver2][1]) > 0:
            randRide1 = random.randint(0,len(solution.driversRides[randDriver1][1])-1)
            randRide2 = random.randint(0,len(solution.driversRides[randDriver2][1])-1)
            solution.driversRides[randDriver1][1][randRide1], solution.driversRides[randDriver2][1][randRide2] = solution.driversRides[randDriver2][1][randRide2], solution.driversRides[randDriver1][1][randRide1]
        
        elif len(solution.driversRides[randDriver1][1]) > 0 and len(solution.driversRides[randDriver2][1]) == 0:
            randRide1 = random.randint(0,len(solution.driversRides[randDriver1][1])-1)
            solution.driversRides[randDriver2][1].append(solution.driversRides[randDriver1][1][randRide1])
            solution.driversRides[randDriver1][1].pop(randRide1)
        
        elif len(solution.driversRides[randDriver1][1]) == 0 and len(solution.driversRides[randDriver2][1]) > 0:
            randRide2 = random.randint(0,len(solution.driversRides[randDriver2][1])-1)
            solution.driversRides[randDriver1][1].append(solution.driversRides[randDriver2][1][randRide2])
            solution.driversRides[randDriver2][1].pop(randRide2)
        
        return solution

    def SwapAll(self, solution):
        
        #give all rides from a driver to another driver
        randDriver1 = randDriver2 = 0
        while randDriver1 == randDriver2 :
            randDriver1 = random.randint(0,len(self.problem.drivers)-1)
            randDriver2 = random.randint(0,len(self.problem.drivers)-1)
        
        if len(solution.driversRides[randDriver1][1]) > 0 :
            for i in range (0,len(solution.driversRides[randDriver1][1])):
                solution.driversRides[randDriver2][1].append(solution.driversRides[randDriver1][1][i])
            solution.driversRides[randDriver1][1].clear()
        
        elif len(solution.driversRides[randDriver1][1]) == 0 and len(solution.driversRides[randDriver2][1]) > 0:
            for i in range (0,len(solution.driversRides[randDriver2][1])):
                solution.driversRides[randDriver1][1].append(solution.driversRides[randDriver2][1][i])
            solution.driversRides[randDriver2][1].clear()
        
        elif len(solution.driversRides[randDriver1][1]) == 0 and len(solution.driversRides[randDriver2][1]) == 0:
            print("No rides to swap")
        
        return solution
        
    
method = Method(prob)
sol = method.RandomSolution()
print(sol.driversRides)
print(method.SimpleSwap(sol).driversRides)
print(method.SwapAll(sol).driversRides)
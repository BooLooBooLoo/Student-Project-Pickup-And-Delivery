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
        
prob = Problem([1,2,3],[(0,0),(0,0),(0,0)],1,1,['Home','School','Work'],[(2,2),(1,1),(3,3)],[('Home','School'),('Work','Home'),('School','Work')])

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
            print("Distance between " + point1 + " and " + point2 + " is " + str(dist))
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
        
        rideSum = []
        for i in range (0,len(self.driversRides)):
            rideSum.append(len(self.driversRides[i][1]))
        if sum(rideSum) != len(self.problem.rides):
            feasible = False
        
        return feasible
        
    
    def ObjectiveFunction(self, problem, driversRides):
        #Calculate the total cost of all the routes
        print(self.driversRides)
        for i in range (0,len(driversRides)):
            if len(driversRides[i][1]) != 0:
                ind = self.problem.points.index(driversRides[i][1][0][0])
                distance = math.sqrt((self.problem.driversCoord[i][0]-self.problem.pointsCoord[ind][0])**2 + 
                                (self.problem.driversCoord[i][1]-self.problem.pointsCoord[ind][1])**2)
                self.objective += distance
                print("Distance between driver ", driversRides[i][0]  ," and ", driversRides[i][1][0][0], " is ", distance)
                for j in range (0,len(driversRides[i][1])):
                    self.objective += self.DistanceBetweenPoints(driversRides[i][1][j][0],driversRides[i][1][j][1]) * self.problem.driversCost
                for j in range(0,len(driversRides[i][1])-1):
                    self.objective += self.DistanceBetweenPoints(driversRides[i][1][j][1],driversRides[i][1][j+1][0]) * self.problem.driversCost
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

    def SimpleSwapDriver(self, solution):
        
        #Swap 2 rides between 2 drivers
        randDriver1 = randDriver2 = 0
        #Takes 2 random drivers 
        while randDriver1 == randDriver2 :
            randDriver1 = random.randint(0,len(self.problem.drivers)-1)
            randDriver2 = random.randint(0,len(self.problem.drivers)-1)
        #If both drivers have rides, swap 2 random rides
        if len(solution.driversRides[randDriver1][1]) > 0 and len(solution.driversRides[randDriver2][1]) > 0:
            randRide1 = random.randint(0,len(solution.driversRides[randDriver1][1])-1)
            randRide2 = random.randint(0,len(solution.driversRides[randDriver2][1])-1)
            solution.driversRides[randDriver1][1][randRide1], solution.driversRides[randDriver2][1][randRide2] = solution.driversRides[randDriver2][1][randRide2], solution.driversRides[randDriver1][1][randRide1]
        #If one driver has rides and the other one doesnt, swap a random ride with an empty list
        elif len(solution.driversRides[randDriver1][1]) > 0 and len(solution.driversRides[randDriver2][1]) == 0:
            randRide1 = random.randint(0,len(solution.driversRides[randDriver1][1])-1)
            solution.driversRides[randDriver2][1].append(solution.driversRides[randDriver1][1][randRide1])
            solution.driversRides[randDriver1][1].pop(randRide1)
        #Same but with the other driver
        elif len(solution.driversRides[randDriver1][1]) == 0 and len(solution.driversRides[randDriver2][1]) > 0:
            randRide2 = random.randint(0,len(solution.driversRides[randDriver2][1])-1)
            solution.driversRides[randDriver1][1].append(solution.driversRides[randDriver2][1][randRide2])
            solution.driversRides[randDriver2][1].pop(randRide2)
        
        return solution

    def SwapAllDriver(self, solution):
        
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
    def OneSwapRide(self, solution):
        #Swap 2 rides of the same driver
        randDriver = random.randint(0,len(self.problem.drivers)-1)
        if len(solution.driversRides[randDriver][1]) > 1:
            randRide1 = random.randint(0,len(solution.driversRides[randDriver][1])-1)
            randRide2 = random.randint(0,len(solution.driversRides[randDriver][1])-1)
            solution.driversRides[randDriver][1][randRide1], solution.driversRides[randDriver][1][randRide2] = solution.driversRides[randDriver][1][randRide2], solution.driversRides[randDriver][1][randRide1]
        else:
            print("No rides to swap")
        return solution
    def SimulatedAnnealing(self, solution, maxIter):
        #Simulated Annealing
        for i in range (0,maxIter):
            solution2 = self.RandomSolution()
            delta = solution2.objective - solution.objective
            if delta < 0:
                solution = solution2
        return solution
    
method = Method(prob)
sol = method.RandomSolution()
sol.ObjectiveFunction(prob, sol.driversRides)
print(sol.objective)
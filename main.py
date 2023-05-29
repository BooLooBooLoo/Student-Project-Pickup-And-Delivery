import math
import random
<<<<<<< HEAD
from data import get_data
import pandas as pd
import numpy as np
import datetime
import pytz
import openrouteservice
=======
import data


>>>>>>> parent of c8f0183 (divers files)
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
<<<<<<< HEAD
data=get_data(datetime.datetime(2023, 1, 5, 0, 0, 0, 0,pytz.UTC),datetime.datetime(2023, 1, 5, 0, 30, 0, 0,pytz.UTC),0)
prob = Problem(data[3],data[4],50,1,data[0],data[1],data[2])        
=======
        
prob = Problem([1,2,3],[(0,0),(0,0),(0,0)],1,1,['Home','School','Work'],[(2,2),(1,1),(3,3)],[('Home','School'),('Work','Home'),('School','Work')])
>>>>>>> parent of c8f0183 (divers files)

class Solution :

    def __init__(self, driversRides, prob):
        self.driversRides = driversRides # list of tuples (driver,[rides])
        self.problem = prob
        self.objective = 0
        
    def DistanceBetweenPoints(self,point1, point2):
            ind1 = self.problem.points.index(point1)
            ind2 = self.problem.points.index(point2)
            lat_1 = self.problem.pointsCoord[ind1][0]
            lng_1 = self.problem.pointsCoord[ind1][1]
            lat_2 = self.problem.pointsCoord[ind2][0]
            lng_2 = self.problem.pointsCoord[ind2][1]
            lat_1, lng_1, lat_2, lng_2 = map(math.radians, [lat_1, lng_1, lat_2, lng_2])
            d_lat = lat_2 - lat_1
            d_lng = lng_2 - lng_1
            temp=(math.sin(d_lat / 2) ** 2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(d_lng / 2) ** 2)
            return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))
    
    def Feasability(self, prob):
        #Also check if all the rides are dispatch and if the ride isnt already assigned to a driver
        feasible = True
        for i in range (0,len(self.driversRides)):
            if self.driversRides[i][0] not in self.problem.drivers :
                feasible = False
            for j in range (0,len(self.driversRides[i][1])):
                if self.driversRides[i][1][j] not in self.problem.rides :
                    feasible = False
        
        #Check if all the rides are dispatched 
        rides = []
        for i in range (0,len(self.driversRides)):
            for j in range (0,len(self.driversRides[i][1])):
                rides.append(self.driversRides[i][1][j])
        for i in range (0,len(self.problem.rides)):
            if self.problem.rides[i] not in rides:
                print("ride not dispatched")
                feasible = False
        #Check if the rides are not assigned to multiple drivers
        for i in range (0,len(self.driversRides)):
            for j in range (0,len(self.driversRides[i][1])):
                for k in range (0,len(self.driversRides)):
                    if k != i:
                        if self.driversRides[i][1][j] in self.driversRides[k][1]:
                            feasible = False
        
        return feasible
        
    
    def ObjectiveFunction(self, problem, driversRides):
        #Calculate the total cost of all the routes
        for i in range (0,len(driversRides)):
            if len(driversRides[i][1]) != 0:
                ind = self.problem.points.index(driversRides[i][1][0][0])
                lat_1 = self.problem.pointsCoord[ind][1]
                lng_1 = self.problem.pointsCoord[ind][0]
                lat_2 = self.problem.driversCoord[i][0]
                lng_2 = self.problem.driversCoord[i][1]
                print(lat_1,lng_1,lat_2,lng_2)
                lat_1, lng_1, lat_2, lng_2 = map(math.radians, [lat_1, lng_1, lat_2, lng_2])
                d_lat = lat_2 - lat_1
                d_lng = lng_2 - lng_1
                temp=(math.sin(d_lat / 2) ** 2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(d_lng / 2) ** 2)
                distance = 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))
                print(distance)
                self.objective += distance
                for j in range (0,len(driversRides[i][1])):
                    self.objective += self.DistanceBetweenPoints(driversRides[i][1][j][0],driversRides[i][1][j][1]) * self.problem.driversCost
                for j in range(0,len(driversRides[i][1])-1):
                    self.objective += self.DistanceBetweenPoints(driversRides[i][1][j][1],driversRides[i][1][j+1][0]) * self.problem.driversCost
        return self.objective


#Do the class method to construct a solution and check if it is feasible

class Method :
    
    def __init__(self, problem):
        self.problem = problem
    
    def RandomSolution(self): #Construct a random solution
        feasible = False
        while  feasible == False:
            tupleList = []
            for i in range (0,len(self.problem.drivers)):
                tupleList.append((self.problem.drivers[i],[]))
                
            for i in range (0,len(self.problem.rides)):
                rand = random.randint(0,len(self.problem.drivers)-1)
                tupleList[rand][1].append(self.problem.rides[i])
        
            solution = Solution(tupleList, self.problem)
            feasible = solution.Feasability(self.problem)
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
        randDriver1 = randDriver2 = 0
        while randDriver1 == randDriver2 :
            randDriver1 = random.randint(0,len(self.problem.drivers)-1)
            randDriver2 = random.randint(0,len(self.problem.drivers)-1)
        if len(solution.driversRides[randDriver1][1]) > 0 and len(solution.driversRides[randDriver2][1]) > 0:
            if len(solution.driversRides[randDriver1][1]) > len(solution.driversRides[randDriver2][1]):
                for i in range (0,len(solution.driversRides[randDriver2][1])):
                    solution.driversRides[randDriver1][1][i], solution.driversRides[randDriver2][1][i] = solution.driversRides[randDriver2][1][i], solution.driversRides[randDriver1][1][i]
                for i in range (len(solution.driversRides[randDriver2][1]),len(solution.driversRides[randDriver1][1])):
                    solution.driversRides[randDriver2][1].append(solution.driversRides[randDriver1][1][i])
                    solution.driversRides[randDriver1][1].pop(i)
            if len(solution.driversRides[randDriver1][1]) < len(solution.driversRides[randDriver2][1]):
                for i in range (0,len(solution.driversRides[randDriver1][1])):
                    solution.driversRides[randDriver1][1][i], solution.driversRides[randDriver2][1][i] = solution.driversRides[randDriver2][1][i], solution.driversRides[randDriver1][1][i]
                for i in range (len(solution.driversRides[randDriver1][1]),len(solution.driversRides[randDriver2][1])):
                    solution.driversRides[randDriver1][1].append(solution.driversRides[randDriver2][1][i])
                    solution.driversRides[randDriver2][1].pop(i)
            if len(solution.driversRides[randDriver1][1]) == len(solution.driversRides[randDriver2][1]):
                for i in range (len(solution.driversRides[randDriver1][1])):
                    solution.driversRides[randDriver1][1][i], solution.driversRides[randDriver2][1][i] = solution.driversRides[randDriver2][1][i], solution.driversRides[randDriver1][1][i]
                
        elif len(solution.driversRides[randDriver1][1]) > 0 and len(solution.driversRides[randDriver2][1]) == 0:
            for i in range (0,len(solution.driversRides[randDriver1][1])):
                solution.driversRides[randDriver2][1].append(solution.driversRides[randDriver1][1][i])
            
            solution.driversRides[randDriver1][1].clear()
        elif len(solution.driversRides[randDriver1][1]) == 0 and len(solution.driversRides[randDriver2][1]) > 0:
            for i in range (0,len(solution.driversRides[randDriver2][1])):
                solution.driversRides[randDriver1][1].append(solution.driversRides[randDriver2][1][i])
            
            solution.driversRides[randDriver2][1].clear()
        return solution
    
    def GiveOneDriver(self, solution):
        randDriver1 = randDriver2 = 0
        while randDriver1 == randDriver2 :
            randDriver1 = random.randint(0,len(self.problem.drivers)-1)
            randDriver2 = random.randint(0,len(self.problem.drivers)-1)
        if len(solution.driversRides[randDriver1][1]) > 0 :
            randRide1 = random.randint(0,len(solution.driversRides[randDriver1][1])-1)
            solution.driversRides[randDriver2][1].append(solution.driversRides[randDriver1][1][randRide1])
            solution.driversRides[randDriver1][1].pop(randRide1)
        elif len(solution.driversRides[randDriver1][1]) == 0 and len(solution.driversRides[randDriver2][1]) > 0:
            randRide1 = random.randint(0,len(solution.driversRides[randDriver2][1])-1)
            solution.driversRides[randDriver1][1].append(solution.driversRides[randDriver2][1][randRide1])
            solution.driversRides[randDriver2][1].pop(randRide1)
        return solution
    
    def GiveAllDriver(self, solution):
        
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
        return solution
    
    def OneSwapRide(self, solution):
        #Swap 2 rides of the same driver
        randDriver = random.randint(0,len(self.problem.drivers)-1)
        if len(solution.driversRides[randDriver][1]) > 1:
            randRide1 = randRide2 = 0
            while randRide1 == randRide2 :
                randRide1 = random.randint(0,len(solution.driversRides[randDriver][1])-1)
                randRide2 = random.randint(0,len(solution.driversRides[randDriver][1])-1)
            solution.driversRides[randDriver][1][randRide1], solution.driversRides[randDriver][1][randRide2] = solution.driversRides[randDriver][1][randRide2], solution.driversRides[randDriver][1][randRide1]
        return solution
    
    def SimulatedAnnealing(self, maxIter, temp, alpha):
        #Simulated Annealing
        #Initialize a random solution and set it as the best solution
        ini_solution=self.RandomSolution()
        best_solution=ini_solution
        best_solution_cost=ini_solution.ObjectiveFunction(self.problem, ini_solution.driversRides)
        #Select a random neighbor solution
        for i in range (0,maxIter):
            ran=random.uniform(0,1)
            if ran<0.2:
                new_solution=self.GiveOneDriver(ini_solution)
            elif ran<0.4:
                new_solution=self.GiveAllDriver(ini_solution)
            elif ran<0.6:
                new_solution=self.OneSwapRide(ini_solution)
            elif ran<0.8:
                new_solution=self.SimpleSwapDriver(ini_solution)
            else:
                new_solution=self.SwapAllDriver(ini_solution)
            #Calculate the cost of the new solution and the initial solution
            new_solution_cost=new_solution.ObjectiveFunction(self.problem, new_solution.driversRides)
            ini_solution_cost=ini_solution.ObjectiveFunction(self.problem, ini_solution.driversRides)
            delta=new_solution_cost-ini_solution_cost
            #Check the feasibility of the new solution
            feasible=new_solution.Feasability(self.problem)
            if feasible==True:
                #If it's cheaper, replace the initial solution with the new solution
                if delta<0:
                    ini_solution=new_solution
                    #If it's the best solution, replace the best solution with the new solution
                    if new_solution_cost<best_solution_cost:
                        best_solution=new_solution
                        best_solution_cost=new_solution_cost
                #If delta>0, replace the initial solution with the new solution with a probability according to the temperature and the delta
                elif random.uniform(0.01,0.99)<math.exp(-delta/temp):
                    ini_solution=new_solution
                temp=temp*alpha
        return best_solution, best_solution_cost
#try the simulated annealing algorithm with prob
method=Method(prob)
<<<<<<< HEAD
best_solution, best_solution_cost=method.SimulatedAnnealing(100, 100, 0.99)
client = openrouteservice.Client(key='5b3ce3597851110001cf6248953dea1a63794872a30093a3907dfb03') # Specify your personal API key
print(best_solution_cost)
for i in range(len(best_solution.driversRides)):
    if len(best_solution.driversRides[i][1])>0:
        print(best_solution.driversRides[i])
#Use the API to calculate the time between the points
#for i in range(len(best_solution.driversRides)):
#    if len(best_solution.driversRides[i][1])>0:
#        coords=[]
#        coords.append(prob.driversCoord[i])
#        for j in range(len(best_solution.driversRides[i][1])):
#            coords.append(prob.pointsCoord[prob.points.index(best_solution.driversRides[i][1][j][0])])
#            coords.append(prob.pointsCoord[prob.points.index(best_solution.driversRides[i][1][j][1])])
#        routes = client.directions(coords)
#        print(routes['routes'][0]['summary']['duration'])
=======
sol=method.SimulatedAnnealing(1000,100,0.99)
print(sol[0].driversRides,sol[1])
>>>>>>> parent of c8f0183 (divers files)

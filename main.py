import math

class Problem :
    def __init__(self, drivers,driversCoord,points,pointsCoord, rides,dist):
        distBtwPoints = []
        self.drivers = drivers
        self.driversCoord = driversCoord
        self.points = points
        self.pointsCoord = pointsCoord
        self.rides = rides
        def DistanceBetweenPoints(self,point1, point2):
            ind1 = self.points.index(point1)
            ind2 = self.points.index(point2)
            dist = math.sqrt((pointsCoord[ind1][0]-pointsCoord[ind2][0])**2 + (pointsCoord[ind1][1]-pointsCoord[ind2][1])**2)
            distBtwPoints.append()
        

prob = Problem([0,1,2],['Casa','Marrakech','Tanger'],['Casa','Marrakech','Tanger'],[("Marrakech","Tanger"),("Casa","Marrakech")])

print(prob.rides[0])
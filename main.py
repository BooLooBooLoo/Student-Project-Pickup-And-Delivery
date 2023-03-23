import math

class Problem :
    def __init__(self, drivers,driversCoord,points,pointsCoord, rides):
        dist = 0
        self.drivers = drivers
        self.driversCoord = driversCoord
        self.points = points
        self.pointsCoord = pointsCoord
        self.rides = rides
        def DistanceBetweenPoints(self,point1, point2):
            ind1 = self.points.index(point1)
            ind2 = self.points.index(point2)
            dist = math.sqrt((pointsCoord[ind1][0]-pointsCoord[ind2][0])**2 + (pointsCoord[ind1][1]-pointsCoord[ind2][1])**2)
            return dist


prob = Problem([0,1,2],[(23,23),(90,1),(1,2)],["Home","Work","School"],[(2,2),(9,19),(17,92)],[("Home","Work"),("Work","School"),("School","Home")])


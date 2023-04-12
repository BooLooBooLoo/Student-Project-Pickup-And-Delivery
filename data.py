import pandas as pd
import numpy as np
import time
import datetime
import pytz
def get_data(debutTime,endTime):
    #select only the data between the two dates in hours
    df = pd.read_csv('data.csv')
    df['trip_requested_at_date'] = pd.to_datetime(df['trip_requested_at_date'])
    df = df[(df['trip_requested_at_date'] >= debutTime) & (df['trip_requested_at_date'] <= endTime)]   
    longDeparturePoint=df.pickup_lng.values.tolist()
    latDeparturePoint=df.pickup_lat.values.tolist()
    longArrivalPoint=df.destination_lng.values.tolist()
    latArrivalPoint=df.destination_lat.values.tolist()
    driverId=df.driver_id.values.tolist()
    points = []
    pointsCoords=[]
    rides = []
    drivers = []
    driverCoords = []
    j=0
    for i in range(len(longDeparturePoint)):
        if (longDeparturePoint[i],latDeparturePoint[i]) not in pointsCoords:
            points.append('Point'+str(j))
            j+=1
            pointsCoords.append((longDeparturePoint[i],latDeparturePoint[i]))
        if (longArrivalPoint[i],latArrivalPoint[i]) not in pointsCoords:
            points.append('Point'+str(j))
            j+=1
            pointsCoords.append((longArrivalPoint[i],latArrivalPoint[i]))
        if driverId[i] not in drivers:
            drivers.append(driverId[i])
            driverCoords.append((0,0))
        Begin = pointsCoords.index((longDeparturePoint[i],latDeparturePoint[i]))
        End = pointsCoords.index((longArrivalPoint[i],latArrivalPoint[i]))
        rides.append((points[Begin],points[End]))
        
    
    
    return [points, pointsCoords, rides, drivers, driverCoords]

#use datetime +utc as argument
get_data(datetime.datetime(2023, 1, 5, 0, 0, 0, 0,pytz.UTC),datetime.datetime(2023, 1, 5, 0, 7, 0, 0,pytz.UTC))
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
    #Read the drivers file
    df2=pd.read_csv('drivers_positions.csv')
    df2 = df2[df2['status'] == 'ONLINE']
    print('Step 1')
    #Convert the timestamp to datetime and select only the data between the two dates in hours
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])
    #Select Only the drivers online
    print('Step 2')
    df2 = df2[(df2['timestamp'] >= debutTime) & (df2['timestamp'] <= endTime)]
    print('Step 3')
    #Convert data to list
    longDeparturePoint=df.pickup_lng.values.tolist()
    latDeparturePoint=df.pickup_lat.values.tolist()
    longArrivalPoint=df.destination_lng.values.tolist()
    latArrivalPoint=df.destination_lat.values.tolist()
    driversId=df2.driver.values.tolist()
    print(len(driversId))
    driversLon=df2.lon.values.tolist()
    driversLat=df2.lat.values.tolist()
    points = []
    pointsCoords=[]
    rides = []
    driversIdCheck=[]
    drivers = []
    driverCoords = []
    j=0
    print('Step 4')
    #Create the list of drivers and their coordinates
    for i in range(len(driversId)):
        if driversId[i] not in driversIdCheck:
            driversIdCheck.append(driversId[i])
            drivers.append('Driver'+str(j))
            j+=1
            driverCoords.append((driversLon[i],driversLat[i]))
    j=0
    #Create the list of points and their coordinates
    print('Step 5')
    for i in range(len(longDeparturePoint)):
        if (longDeparturePoint[i],latDeparturePoint[i]) not in pointsCoords:
            points.append('Point'+str(j))
            j+=1
            pointsCoords.append((longDeparturePoint[i],latDeparturePoint[i]))
        if (longArrivalPoint[i],latArrivalPoint[i]) not in pointsCoords:
            points.append('Point'+str(j))
            j+=1
            pointsCoords.append((longArrivalPoint[i],latArrivalPoint[i]))
        Begin = pointsCoords.index((longDeparturePoint[i],latDeparturePoint[i]))
        End = pointsCoords.index((longArrivalPoint[i],latArrivalPoint[i]))
        if (points[Begin],points[End]) not in rides:
            rides.append((points[Begin],points[End]))
    print('Step 6')
    return [points, pointsCoords, rides, drivers, driverCoords]

#use datetime +utc as argument
get_data(datetime.datetime(2023, 1, 5, 0, 0, 0, 0,pytz.UTC),datetime.datetime(2023, 1, 5, 0, 7, 0, 0,pytz.UTC))
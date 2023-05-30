import pandas as pd
import numpy as np
import time
import datetime
import pytz
import math
def get_data(debutTime,endTime,hour):
    #select only the data between the two dates in hours
    df = pd.read_csv('data.csv')
    df['trip_requested_at_date'] = pd.to_datetime(df['trip_requested_at_date'])
    df = df[(df['trip_requested_at_date'] >= debutTime) & (df['trip_requested_at_date'] <= endTime)]
    #Read the drivers file
    df2=pd.read_csv('drivers_positions_modified_'+str(hour)+'.csv')
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
    driversLon=df2.lat.values.tolist()
    driversLat=df2.lon.values.tolist()
    points = []
    pointsCoords=[]
    rides = []
    driversIdCheck=[]
    drivers = []
    driversIdCheck = []
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
    #Keep only the drivers that are near enough to the points
    sortedDrivers=[]
    sortedDriversCoords=[]
    for i in range(len(pointsCoords)):
        for j in range(len(drivers)):
            lng_1 = pointsCoords[i][0]
            lat_1 = pointsCoords[i][1]
            lng_2 = driverCoords[j][0]
            lat_2 = driverCoords[j][1]
            lat_1, lng_1, lat_2, lng_2 = map(math.radians, [lat_1, lng_1, lat_2, lng_2])
            d_lat = lat_2 - lat_1
            d_lng = lng_2 - lng_1
            temp=(math.sin(d_lat / 2) ** 2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(d_lng / 2) ** 2)
            distance = 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))            
            if(distance<25):
                if drivers[j] not in sortedDrivers:
                    sortedDrivers.append(drivers[j])
                    sortedDriversCoords.append(driverCoords[j])
    print('Step 7')
    print(len(sortedDrivers))
    print(len(drivers))
    return [points, pointsCoords, rides, sortedDrivers, sortedDriversCoords]

#use datetime +utc as argument
def csv_creator():
    for i in range (24):
        df = pd.read_csv('drivers_positions_modified.csv')
        print(i)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[(df['timestamp'] >= datetime.datetime(2023, 1, 5, i, 0, 0, 0,pytz.UTC)) & (df['timestamp'] <= datetime.datetime(2023, 1, 5, i, 59, 59, 0,pytz.UTC))]
        df.to_csv('drivers_positions_modified_'+str(i)+'.csv')

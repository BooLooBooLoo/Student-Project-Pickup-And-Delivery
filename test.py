import plotly.express as px
import folium
from geopy.distance import distance
        
        
        #print(best_solution.driversRides[i])
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

col = []
for i in range (len(solution)):
    col.append(tuple(np.random.choice(range(255),size=3)))
fig = px.scatter_mapbox(solution,
                        lat=[x[1] for x in data[4] if data[3][data[4].index(x)] in [x[0] for x in solution]],
                        lon=[x[0] for x in data[4] if data[3][data[4].index(x)] in [x[0] for x in solution]],
                        zoom = 7,
                        color=col,
                        hover_name= [x for x in data[3] if x in [x[0] for x in solution]],
                        width=1000,
                        height=800,
                        title="Drivers Positions"
                        )

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
fig.show()
print(solution)
print('plot complete')

location = float(data[1][data[0].index(solution[0][1][0][0])][1]), float(data[1][data[0].index(solution[0][1][0][0])][0])
location2 = float(data[1][data[0].index(solution[0][1][0][1])][1]), float(data[1][data[0].index(solution[0][1][0][1])][0])

m = folium.Map(location=[location[0], location[1]], zoom_start=12)
folium.Marker(location).add_to(m)
folium.Marker(location2).add_to(m)

km = distance(location, location2).km
print(km)

folium.PolyLine(locations=[location, location2], color='red').add_to(m)
m.show_in_browser()
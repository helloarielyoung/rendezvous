#import requests, json

import json

# route for User1:
# r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=683+sutter+str+san+francisco&destination=3000+mission+str+san+francisco&mode=driving&key=AIzaSyAQebJTWGOQmOsuTYscQ5bjCVjBenHOgC0')

# route for User2:
# r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=Lafayette+Park+Gough+Street+San+Francisco&destination=683+sutter+str+san+francisco&mode=driving&key=AIzaSyAQebJTWGOQmOsuTYscQ5bjCVjBenHOgC0')

#user3 origin:  37.786493, -122.416289
#route for User 3:
#r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=37.786493, -122.416289&destination=683+sutter+str+san+francisco&mode=driving&key=AIzaSyAQebJTWGOQmOsuTYscQ5bjCVjBenHOgC0')

f = open('user3data3.json')
data = f.read()

data = json.loads(data)

# data = r.json()

# This is actually not quite right.  It's missing the start location,
# and starts at the first turn of the route!
# new_data = [item['end_location'] for item in data['routes'][0]['legs'][0]['steps']]
# data =[{'lat':item['lat'], 'lng':item['lng']} for item in new_data]

#corrected way to do it:
start_location = [item['start_location'] for item in data['routes'][0]['legs']]

rest_of_route = [item['end_location'] for item in data['routes'][0]['legs'][0]['steps']]

whole = start_location + rest_of_route

route = [{'lat':item['lat'], 'lng':item['lng']} for item in whole]

print route

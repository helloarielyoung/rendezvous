"""Helper Functions"""
import json
import requests


def get_route_data(start, end):
    """Returns formatted list of waypoints between start and end

    expects street address and city name for start and end points

    example call:

    helper_functions.get_route_data('221 4th St San Francisco', '683 Sutter St San Francisco')

    passes the request:
    'https://maps.googleapis.com/maps/api/directions/json?origin=221+4th+St+San+Francisco&destination=683+Sutter+St+San+Francisco&mode=driving&key=AIzaSyAQebJTWGOQmOsuTYscQ5bjCVjBenHOgC0'

    """

    # format the addresses
    formatted_start = start.replace(' ', '+')
    formatted_end = end.replace(' ', '+')

    r = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + \
        formatted_start + '&destination=' + formatted_end + \
        '&mode=driving&key=AIzaSyAQebJTWGOQmOsuTYscQ5bjCVjBenHOgC0'

    #for testing:
    print r

    result = requests.get(r)
    result = result.json()

    start_location = [item['start_location'] for item in result['routes'][0]['legs']]
    rest_of_route = [item['end_location'] for item in result['routes'][0]['legs'][0]['steps']]

    whole = start_location + rest_of_route

    #format the way "path" for google maps API wants them:
    route = [{'lat':item['lat'], 'lng':item['lng']} for item in whole]

    print route

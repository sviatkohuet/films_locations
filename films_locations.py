import folium
import requests
import pandas as pd
import urllib.parse
import random
from math import *


def calculate_distance(locations):
    lat1 = locations[0][0]
    lat2 = locations[1][0]
    lon1 = locations[1][0]
    lon2 = locations[1][1]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return 13400- (c * r)

def get_locations(file):
    with open(file, 'rb') as f:
        films_locations = {}
        for _ in range(14):
            f.readline()
        for line in f.readlines():
            try:
                info = line.decode('utf-8').split('\t')
                location = info[-1]
                if info[-1].startswith('('):
                    location = info[-2]
                if info[0] not in films_locations.keys():
                    films_locations[info[0]] = []
                films_locations[info[0]].append(location.strip())
            except UnicodeDecodeError:
                pass
    return films_locations


def create_df(locations):
    return pd.DataFrame(locations)


def get_coordinates(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    try:
        response = requests.get(url).json()[0]
        return [float(response['lat']), float(response['lon'])]
    except IndexError:
        return [0, 0]


# def sort_by_distance(locations):
#     pass

def generate_map(start_location, file):
    locations = get_locations(file)
    # sorted_locations = sort_by_distance(locations)
    map = folium.Map(tiles="Stamen Terrain",
                location=start_location,
                zoom_control=3)
    fg = folium.FeatureGroup(name="Films map")
    number = 0
    for index, element in enumerate(locations.keys()):
        if number >= 20:
            break
        for location in locations[element]:
            coordinates = get_coordinates(location)
            if coordinates != [0, 0] and calculate_distance([start_location, coordinates]) <= 3000:
                fg.add_child(folium.Marker(location=[coordinates[0], coordinates[1]],
                                    popup=element,
                                    icon=folium.Icon()))
                number += 1
    map.add_child(fg)
    map.save("Map.html")


generate_map([34.0536909, -118.242766], 'locations.list')
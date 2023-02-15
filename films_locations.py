import folium
import pandas
from geopy.geocoders import Nominatim
from math import *


def calculate_distance(locations):
    lat1 = locations[0][0]
    lat2 = locations[1][0]
    lon1 = locations[1][0]
    lon2 = locations[1][1]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    a=sin((lat2-lat1)/2.0)**2+\
            cos(lat1)*cos(lat2)*\
            sin((lon2-lon1)/2.0)**2
    dist=2*atan2(sqrt(a), sqrt(1-a))

    return dist


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


def get_coordinates(location):
    try:
        geolocator = Nominatim(user_agent="name")
        location = geolocator.geocode(location)
        return [location.latitude, location.longitude]
    except AttributeError:
        return [0, 0]


def generate_map(location, file):
    locations = get_locations(file)
    map = folium.Map(tiles="Stamen Terrain",
                location=[49.817545, 24.023932],
                zoom_control=3)
    fg = folium.FeatureGroup(name="Films map")
    for index, element in enumerate(locations.keys()):
        if index >= 10:
            break
        for location in locations[element]:
            print(location)
            coordinates = get_coordinates(location)
            if coordinates != [0, 0]:
                fg.add_child(folium.Marker(location=[coordinates[0], coordinates[1]],
                                    popup=element,
                                    icon=folium.Icon()))
    map.add_child(fg)
    map.save("Map.html")


# generate_map(1, 'locations.list')
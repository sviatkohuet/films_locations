""" This module generates map with films locations and save it to Map.html file """

import argparse
import math
import json
import urllib.parse
import requests
import pycountry
import folium
from geopy.geocoders import Nominatim


def calculate_distance(locations):
    """Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) and return it in km
    
    :param locations: list of two lists with lat and lon

    :return: distance in km
    """
    lat1, lon1 = locations[0]
    lat2, lon2 = locations[1]

    radius = 6371  # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def get_country_from_coordinates(coordinates):
    """Get country from coordinates

    :param coordinates: list with lat and lon

    :return: country
    """
    country_codes = {country.alpha_2: country.name for country in pycountry.countries}
    other_names = {'United States': 'USA', 'United Kingdom': 'UK', 'Russian Federation': 'Russia'}
    try:
        geolocator = Nominatim(user_agent="name")
        location = geolocator.reverse(coordinates)

        if country_codes[location.raw['address']['country_code'].upper()] in other_names.keys():
            return other_names[country_codes[location.raw['address']['country_code'].upper()]]
        return country_codes[location.raw['address']['country_code'].upper()]
    except (IndexError, json.decoder.JSONDecodeError, KeyError):
        return None


def get_locations(file, year, country):
    """Get locations of films from file and sort them by distance from start location

    :param file: file with locations

    :return: dictionary with films and locations
    """
    used_locations = set()
    with open(file, 'rb') as f:
        films_locations = {}
        for _ in range(14):
            f.readline()
        for line in f.readlines():
            if len(used_locations) >= 150:
                break
            try:
                info = line.decode('utf-8').split('\t')
                location = info[-1]
                if info[-1].startswith('('):
                    location = info[-2]
                if str(year) in info[0] and location.strip() not in used_locations\
                    and country in location:
                    if info[0] not in films_locations.keys():
                        films_locations[info[0]] = []
                    else:
                        continue
                    films_locations[info[0]].append(location.strip())
                    used_locations.add(location.strip())
            except UnicodeDecodeError:
                pass
    return films_locations


def get_coordinates(address):
    """Get coordinates of address from OpenStreetMap

    :param address: address

    :return: list with lat and lon
    """
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    try:
        response = requests.get(url).json()[0]
        return [float(response['lat']), float(response['lon'])]
    except (IndexError, json.decoder.JSONDecodeError):
        return [0, 0]


def get_year(film):
    """Get year of film

    :param film: film

    :return: year of film
    """
    return film.split('(')[1].split(')')[0]


def sort_by_distance(locations, start_location):
    """Sort locations by distance from start location

    :param locations: list of locations
    :param start_location: start location

    :return: sorted list of locations
    """
    return {k: v for k, v in sorted(locations.items(), key=lambda item: calculate_distance([start_location, get_coordinates(item[1][0])]))}


def generate_map(start_location, file, year):
    """Generate map with films locations and save it to Map.html file

    :param start_location: start location
    :param file: file with locations
    :param radius: radius of search

    :return: 1 if success
    """
    country = get_country_from_coordinates(start_location)
    locations = get_locations(file, year, country)
    locations = sort_by_distance(locations, start_location)
    map = folium.Map(tiles="Stamen Terrain",
                location=start_location,
                zoom_control=3)
    fg = folium.FeatureGroup(name="Films map")
    fg1 = folium.FeatureGroup(name="Beatiful layer")
    fg1.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read()))
    number = 0

    for _, element in enumerate(locations.keys()):
        if number >= 10:
            break
        for location in locations[element]:
            coordinates = get_coordinates(location)
            if coordinates != [0, 0]:
                fg.add_child(folium.Marker(location=[coordinates[0], coordinates[1]],
                                    popup=element,
                                    icon=folium.Icon()))
                number += 1
    map.add_child(fg1)
    map.add_child(fg)
    map.save("Map1.html")
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, default='locations.list')
    parser.add_argument('year', type=int, default=2016)
    parser.add_argument("lat", type=float, default=34.0536909)
    parser.add_argument("lon", type=float, default=-118.242766)
    all_args = parser.parse_args()
    generate_map([all_args.lat, all_args.lon], all_args.file, all_args.year)

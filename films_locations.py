import folium
import pandas
from geopy.geocoders import Nominatim


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
                    location = info[-2]+' '+info[-1]
                if info[0] not in films_locations.keys():
                    films_locations[info[0]] = []
                films_locations[info[0]].append(location.strip())
            except UnicodeDecodeError:
                pass
    return films_locations

def get_coordinates(location):
    geolocator = Nominatim(user_agent="name")
    location = geolocator.geocode(location)
    return [location.latitude, location.longitude]


def generate_map(location, file):
    locations = get_locations(file)
    map = folium.Map(tiles="Stamen Terrain",
                location=[49.817545, 24.023932],
                zoom_control=3)

    fg = folium.FeatureGroup(name="Films map")
    for i, x in enumerate(locations.keys()):
        print(x)
        if i >= 2:
            break
        for location in locations[x]:
            coordinates = get_coordinates(location)
            fg.add_child(folium.Marker(location=[coordinates[0], coordinates[1]],
                                    popup=x,
                                    icon=folium.Icon()))
    map.add_child(fg)
    map.save("Map.html")



# generate_map(1, 'locations.list')
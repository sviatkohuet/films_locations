import folium
import pandas


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
                films_locations[info[0]] = location.strip()
            except UnicodeDecodeError:
                pass
    return films_locations

def get_coordinates(location):
    return []


def generate_map(location, file):
    locations = get_locations(file)
    map = folium.Map(tiles="Stamen Terrain",
                location=[49.817545, 24.023932],
                zoom_control=3)

    fg = folium.FeatureGroup(name="Films map")
    for i, x in enumerate(locations.keys()):
        if i >= 2:
            break
        coordinates = get_coordinates(locations[x])
        fg.add_child(folium.Marker(location=[coordinates[0], coordinates[1]],
                                popup=x,
                                icon=folium.Icon()))
    map.add_child(fg)
    map.save("Map.html")
    # for i, x in enumerate(locations.keys()):
    #     if i >= 10:
    #         break
    #     print(locations[x])

        


# print(generate_map(1, 'locations.list'))
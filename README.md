# films_locations
 
 This module is for creating html file, which contains map and  markers, that represent places where some film episodes were filmed.
 You have to input file, yearof film, your location and then map will be generated with nearest 10 places from your location.
 
 ```python films_locations.py locations.list 2016 34.0536909 -118.242766```
 
 # instalation
 
 For this module you need to install: folium, argparse, requests, urllib.parse, json, pycountry and from geopy.geocoders import Nominatim
 
 ```pip install folium
 pip install geopy
 pip install pycountry
 pip install requests
 ```
 
# Usage

Just run terminal and paste

 ```python films_locations.py locations.list 2016 34.0536909 -118.242766``` with your arguments
 
 After that you have to wait 2-3 minutes, then you get html file, which you can open in google or somewhere.

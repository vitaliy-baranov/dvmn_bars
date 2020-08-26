import json

import folium
import requests
from flask import Flask
from geopy import distance

API_KEY = "3cdef1e4-b3f0-4276-86e0-9fcb8524fbbe"
BARS_FILE = 'bars.json'
DEBUG = True
HTML_FILE = 'index.html'


def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_user_coordinates():
    if DEBUG:
        return ('37.432672', '55.845067') #  Москва Аэродромная 4
    else:
        place_start = input("Где вы находитесь? ")
        return fetch_coordinates(API_KEY, place_start)


def count_distance(start_coordinates, finish_coordinates):
    return distance.distance(tuple(reversed(start_coordinates)), tuple(reversed(finish_coordinates))).km


def convert_with_distance(bar, user_coordinates):
    return {
        'title': bar['Name'],
        'longitude': bar['Longitude_WGS84'],
        'latitude': bar['Latitude_WGS84'],
        'distance': count_distance(bar['geoData']['coordinates'], user_coordinates)
    }


def fetch_bars_with_distance(user_coordinates):
    with open("bars.json", "r", encoding="CP1251") as f:
        bars_raw = f.read()
    bars = json.loads(bars_raw)
    bars_with_distance = []
    for bar in bars:
        bars_with_distance.append(convert_with_distance(bar, user_coordinates))
    return bars_with_distance


def print_to_map(user_coordinates, closest_bars):
    map = folium.Map(location=[user_coordinates[1], user_coordinates[0]])
    folium.Marker(
        location=[user_coordinates[1], user_coordinates[0]],
        popup='Your location',
        icon=folium.Icon(color="red")
    ).add_to(map)
    for bar in closest_bars:
        folium.Marker(
            location=[bar['latitude'], bar['longitude']],
            popup=bar['title'],
            icon=folium.Icon(color="green", icon='info-sign')
        ).add_to(map)
    map.save(HTML_FILE)


def get_closests_bars():
    with open(HTML_FILE, "r") as f:
        return f.read()


if __name__ == '__main__':
    user_coordinates = get_user_coordinates()
    bars_with_distance = fetch_bars_with_distance(user_coordinates)
    closest_bars = sorted(bars_with_distance, key=lambda bar: bar['distance'])[0:5]
    print_to_map(user_coordinates, closest_bars)
    app = Flask(__name__)
    app.add_url_rule('/', 'Closests bars', get_closests_bars)
    app.run('0.0.0.0')

import json
import os

import folium
import requests
from dotenv import load_dotenv
from flask import Flask
from geopy import distance

BARS_FILE = 'bars.json'
BARS_QUANTITY = 5
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


def get_user_coordinates(api_key):
    place_start = input("Где вы находитесь? ")
    return fetch_coordinates(api_key, place_start)


def fetch_bars_with_distance(bars, user_coordinates):
    bars_with_distance = []
    for bar in bars:
        bars_with_distance.append(
            {
                'title': bar['Name'],
                'longitude': bar['Longitude_WGS84'],
                'latitude': bar['Latitude_WGS84'],
                'distance': distance.distance(tuple(reversed(bar['geoData']['coordinates'])),
                                              tuple(reversed(user_coordinates)))
            })
    return bars_with_distance


def get_bars_from_file(bars):
    with open(bars, "r", encoding="CP1251") as f:
        bars_raw = f.read()
    return json.loads(bars_raw)


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
    load_dotenv()
    user_coordinates = get_user_coordinates(os.getenv("API_KEY"))
    bars = get_bars_from_file(BARS_FILE)
    bars_with_distance = fetch_bars_with_distance(bars, user_coordinates)
    closest_bars = sorted(bars_with_distance, key=lambda bar: bar['distance'])[0:BARS_QUANTITY]
    print_to_map(user_coordinates, closest_bars)
    app = Flask(__name__)
    app.add_url_rule('/', 'Closests bars', get_closests_bars)
    app.run('0.0.0.0')

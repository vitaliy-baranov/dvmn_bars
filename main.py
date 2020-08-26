import json
import requests
from geopy import distance

API_KEY = "3cdef1e4-b3f0-4276-86e0-9fcb8524fbbe"
BARS_FILE = 'bars.json'

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


if __name__ == '__main__':
    user_coordinates = get_user_coordinates()
    bars_with_distance = fetch_bars_with_distance(user_coordinates)
    print(bars_with_distance)

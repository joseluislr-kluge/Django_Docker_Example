import requests
import os

# Archivo que funciona como proxy con nuestro servicio del clima

API_URL = os.environ.get('WEATHER_API_URL', 'http://127.0.0.1:8001')

def get_all_places():
    try:
        response = requests.get(f"{API_URL}/places")
        response.raise_for_status()
        return response.json().get("places", [])
    except requests.RequestException:
        return None # Indicate an error

def get_place_details(name: str):
    try:
        response = requests.get(f"{API_URL}/places/{name}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def get_weather_for_place(name: str):
    try:
        response = requests.get(f"{API_URL}/weather/{name}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return 500, {"detail": str(e)}


def create_place(name: str, latitude: float, longitude: float):
    payload = {"name": name, "latitude": latitude, "longitude": longitude}
    try:
        response = requests.post(f"{API_URL}/places", json=payload)
        return response.status_code, response.json()
    except requests.RequestException as e:
        return 500, {"detail": str(e)}

def update_place(original_name: str, name: str, latitude: float, longitude: float):
    payload = {"name": name, "latitude": latitude, "longitude": longitude}
    try:
        response = requests.put(f"{API_URL}/places/{original_name}", json=payload)
        return response.status_code, response.json()
    except requests.RequestException as e:
        return 500, {"detail": str(e)}

def delete_place(name: str):
    try:
        response = requests.delete(f"{API_URL}/places/{name}")
        return response.status_code == 200
    except requests.RequestException:
        return False
import requests
import os
from dotenv import load_dotenv

load_dotenv()

OW_KEY = os.getenv("OWAPI")
WB_KEY = os.getenv("WBAPI")

def fetch_openweather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OW_KEY}&units=metric"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()  # Raise an exception for HTTP errors
        data = resp.json()

        # Check if 'coord' exists
        if "coord" not in data:
            return {"error": "Coordinates not found", "response": data}

        return data

    except requests.HTTPError as e:
        return {"error": f"HTTP error {e.response.status_code}", "response": {}}
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}", "response": {}}


def fetch_weatherbit(lat, lon):
    url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={WB_KEY}&units=M"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if "data" not in data or not data["data"]:
            return {"error": "No data from Weatherbit", "response": data}
        return data["data"][0]

    except requests.HTTPError as e:
        return {"error": f"HTTP error {e.response.status_code}", "response": {}}
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}", "response": {}}

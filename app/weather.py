import requests
import os
from dotenv import load_dotenv

load_dotenv()

OW_KEY = os.getenv("OWAPI")
WB_KEY = os.getenv("WBAPI")

def fetch_openweather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OW_KEY}"
    return requests.get(url).json()

def fetch_weatherbit(lat, lon):
    url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={WB_KEY}"
    resp = requests.get(url).json()
    return resp["data"][0]

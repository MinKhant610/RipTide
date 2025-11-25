from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from app.weather import fetch_openweather, fetch_weatherbit
from app.flood_model import build_flood_input
from app.gemini import ask_gemini
import requests

app = FastAPI()

class LocationOnly(BaseModel):
    location: str


@app.get("/")
def home():
    return {"message": "Flood Detection API working"}


def geocode_location(location: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    res = requests.get(url).json()

    if "results" not in res:
        raise HTTPException(status_code=400, detail="Location not found")

    info = res["results"][0]
    return info["latitude"], info["longitude"]


@app.post("/predict_location")
def predict_location(data: LocationOnly):

    lat, lon = geocode_location(data.location)
    ow = fetch_openweather(data.location)
    wb = fetch_weatherbit(lat, lon)

    flood_input = build_flood_input(data.location, lat, lon, ow, wb)

    result = ask_gemini(flood_input)

    return {
        "location": data.location,
        "latitude": lat,
        "longitude": lon,
        "prediction": result
    }

@app.get("/predict")
def predict(city: str, lat: float, lon: float):

    ow = fetch_openweather(city)
    wb = fetch_weatherbit(lat, lon)

    flood_input = build_flood_input(city, lat, lon, ow, wb)

    result = ask_gemini(flood_input)

    return {
        "city": city,
        "prediction": result
    }

class FloodInput(BaseModel):
    date: str
    location: str
    lat: float
    lon: float
    openweather_like: dict
    weatherbit_like: dict


@app.post("/predict_json")
def predict_json(data: FloodInput):

    result = ask_gemini(data.model_dump())

    return {
        "city": data.location,
        "prediction": result
    }

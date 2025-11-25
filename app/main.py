from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.weather import fetch_openweather, fetch_weatherbit
from app.flood_model import build_flood_input
from app.gemini import ask_gemini

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all domains
    allow_credentials=True,
    allow_methods=["*"],          # allow POST, GET, etc.
    allow_headers=["*"],
)

class LocationInput(BaseModel):
    location: str


@app.get("/")
def home():
    return {"message": "Flood Detection API working"}

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

@app.post("/predict_location")
def predict_location(data: LocationInput):

    city = data.location

    # Fetch weather from your existing functions
    ow = fetch_openweather(city)

    # Weatherbit requires lat/lon → get from OpenWeather data
    lat = ow["coord"]["lat"]
    lon = ow["coord"]["lon"]

    wb = fetch_weatherbit(lat, lon)

    # Build ML model input
    flood_input = build_flood_input(city, lat, lon, ow, wb)

    # Run Gemini
    result = ask_gemini(flood_input)

    return {
        "city": city,
        "lat": lat,
        "lon": lon,
        "prediction": result
    }

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.weather import fetch_openweather, fetch_weatherbit
from app.flood_model import build_flood_input
from app.gemini import ask_gemini

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LocationInput(BaseModel):
    location: str

@app.get("/")
def home():
    return {"message": "Flood Detection API working"}

@app.post("/predict_location")
def predict_location(data: LocationInput):
    city = data.location

    # Fetch OpenWeather data
    ow = fetch_openweather(city)

    # Check if 'coord' exists
    coord = ow.get("coord")
    if not coord:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Coordinates not found. Check the location name or API response.",
                "response": ow
            }
        )

    lat = coord.get("lat")
    lon = coord.get("lon")

    if lat is None or lon is None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Incomplete coordinates in OpenWeather response.",
                "response": ow
            }
        )

    # Fetch Weatherbit using lat/lon
    wb = fetch_weatherbit(lat, lon)

    # Build input for ML/Gemini
    flood_input = build_flood_input(city, lat, lon, ow, wb)

    # Run Gemini model
    result = ask_gemini(flood_input)

    return {
        "city": city,
        "lat": lat,
        "lon": lon,
        "prediction": result
    }

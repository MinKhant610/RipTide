from pydantic import BaseModel
from fastapi import FastAPI
from app.weather import fetch_openweather, fetch_weatherbit
from app.flood_model import build_flood_input
from app.gemini import ask_gemini

app = FastAPI()

# ----------------------------
# 1. Input model for JSON test
# ----------------------------
class FloodInput(BaseModel):
    date: str
    location: str
    lat: float
    lon: float
    openweather_like: dict
    weatherbit_like: dict


@app.get("/")
def home():
    return {"message": "Flood Detection API working"}


# ----------------------------
# 2. Existing GET version
# ----------------------------
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


# ----------------------------
# 3. New POST version for JSON
# ----------------------------
@app.post("/predict_json")
def predict_json(data: FloodInput):

    # Pass JSON directly to Gemini
    result = ask_gemini(data.model_dump())

    return {
        "city": data.location,
        "prediction": result
    }

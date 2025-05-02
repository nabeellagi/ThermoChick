from fastapi import APIRouter, Query, HTTPException
import os
import requests
from core.userdata import get_latest_location
from core.sensor import get_latest_data

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

router = APIRouter(
    tags=["GPS Weather Data"]
)

def interpret_pressure(pressure_mb):
    if pressure_mb < 1000:
        return "Tekanan Rendah : Kemungkinan Hujan"
    elif 1000 <= pressure_mb <= 1020:
        return "Tekanan Normal: Cuaca Stabil"
    else:
        return "Tekanan Tinggi: Cuaca Tenang"

def interpret_gb(index):
    if 1 <= index <= 3:
        return {
            "level": "Rendah 🟢",
            "pesan": "Udara sekitar kandang oke!"
        }
    elif 4 <= index <= 6:
        return {
            "level": "Sedang 🟡",
            "pesan": "Mulai waspada. Cek ventilasi, pastikan kipas menyala. Jangan sampai amonia naik!"
        }
    elif 7 <= index <= 9:
        return {
            "level": "Tinggi 🔴",
            "pesan": "Bahaya! Amonia tinggi bisa bikin ayam stres & nafsu makan turun. Segera tambah ventilasi, semprot air, atau buka kandang!"
        }
    elif index == 10:
        return {
            "level": "Sangat Tinggi 🟣",
            "pesan": "Kondisi gawat! Risiko kematian ayam tinggi. Segera evakuasi, atau lakukan penanganan darurat udara!"
        }
    else:
        return {
            "level": "Tidak Valid ❓",
            "pesan": "Index nggak sesuai"
        }

@router.get("/weather")
def get_weather(device_id: str = Query(...)):
    location_data = get_latest_location(device_id)
    cage_data = get_latest_data(device_id)
    
    if not location_data:
        raise HTTPException(status_code=404, detail="Location not found for device.")

    latitude = location_data["latitude"]
    longitude = location_data["longitude"]

    try:
        weather_response = requests.get(
            WEATHER_API_URL,
            params={
                "key": WEATHER_API_KEY,
                "q": f"{latitude},{longitude}",
                "aqi": "yes"
            }
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        result = {
            "name": weather_data["location"]["name"],
            "region": weather_data["location"]["region"],
            "country": weather_data["location"]["country"],
            "outside_temp": weather_data["current"]["temp_c"],
            "outside_feelslike": weather_data["current"]["feelslike_c"],
            "difference": {
                "amount": abs(round(weather_data["current"]["temp_c"] - cage_data["temperature"], 3)),
                "interpret": (
                    "Suhu di luar lebih tinggi dibandingkan suhu yang di dalam"
                    if weather_data["current"]["temp_c"] > cage_data["temperature"]
                    else "Suhu di dalam lebih tinggi dibandingkan suhu yang di luar"
                )
            },
            "wind" : weather_data["current"]["wind_kph"],
            "pressure":{
                "mb" : weather_data["current"]["pressure_mb"],
                "interpret":interpret_pressure(weather_data["current"]["pressure_mb"])
            },
            "gbdefra":{
                "index" : weather_data["current"]["air_quality"]["gb-defra-index"],
                "interpret":interpret_gb(weather_data["current"]["air_quality"]["gb-defra-index"])
            },
            "text" : weather_data["current"]["condition"]["text"],
        }

        return result

    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Weather API request failed: {str(e)}")
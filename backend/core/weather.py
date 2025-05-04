import os
import requests
from fastapi import HTTPException
from core.userdata import get_latest_location
from core.sensor import get_latest_data

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

WEATHER_TRANSLATIONS = {
    "Sunny": "Cerah",
    "Partly Cloudy": "Berawan sebagian",
    "Cloudy": "Berawan",
    "Overcast": "Mendung",
    "Mist": "Berkabut",
    "Patchy Rain Possible": "Hujan ringan mungkin",
    "Light Rain": "Hujan ringan",
    "Heavy Rain": "Hujan deras",
    "Thunderstorm": "Badai petir",
    # Add more as needed
}

def translate_condition(condition_en: str) -> str:
    return WEATHER_TRANSLATIONS.get(condition_en, f"Teks tidak diterjemahkan: {condition_en}")


def fetch_weather(latitude: float, longitude: float) -> dict:
    try:
        response = requests.get(
            WEATHER_API_URL,
            params={
                "key": WEATHER_API_KEY,
                "q": f"{latitude},{longitude}",
                "aqi": "yes"
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Weather API request failed: {str(e)}")

def interpret_pressure(pressure_mb: float) -> str:
    if pressure_mb < 1000:
        return "Tekanan Rendah : Kemungkinan Hujan"
    elif 1000 <= pressure_mb <= 1020:
        return "Tekanan Normal: Cuaca Stabil"
    else:
        return "Tekanan Tinggi: Cuaca Tenang"

def interpret_gb(index: int) -> dict:
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

def get_weather_data(device_id: str) -> dict:
    location_data = get_latest_location(device_id)
    cage_data = get_latest_data(device_id)

    if not location_data:
        raise HTTPException(status_code=404, detail="Location not found for device.")

    latitude = location_data["latitude"]
    longitude = location_data["longitude"]

    try:
        weather_data = fetch_weather(latitude, longitude)

        outside_temp = weather_data["current"]["temp_c"]
        cage_temp = cage_data["temperature"]
        pressure_mb = weather_data["current"]["pressure_mb"]
        gb_index = weather_data["current"]["air_quality"]["gb-defra-index"]

        return {
            "name": weather_data["location"]["name"],
            "region": weather_data["location"]["region"],
            "country": weather_data["location"]["country"],
            "outside_temp": outside_temp,
            "outside_feelslike": weather_data["current"]["feelslike_c"],
            "difference": {
                "amount": abs(round(outside_temp - cage_temp, 3)),
                "interpret": (
                    "Suhu di luar lebih tinggi dibandingkan suhu yang di dalam"
                    if outside_temp > cage_temp
                    else "Suhu di dalam lebih tinggi dibandingkan suhu yang di luar"
                )
            },
            "wind": weather_data["current"]["wind_kph"],
            "pressure": {
                "mb": pressure_mb,
                "interpret": interpret_pressure(pressure_mb)
            },
            "gbdefra": {
                "index": gb_index,
                "interpret": interpret_gb(gb_index)
            },
            "text": translate_condition(weather_data["current"]["condition"]["text"]),
        }

    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

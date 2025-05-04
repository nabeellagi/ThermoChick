from fastapi import APIRouter, Query
from core.weather import get_weather_data

router = APIRouter(tags=["GPS Weather Data"])

@router.get("/weather")
def get_weather(device_id: str = Query(...)):
    return get_weather_data(device_id)

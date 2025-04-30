from fastapi import APIRouter, Query
from pydantic import BaseModel
import requests

from core.sensor import save_sensor_data, get_latest_data, get_recent_sensor_data

router = APIRouter()

class SensorData(BaseModel):
    device_id : str
    temperature: float
    humidity: float

class DataID(BaseModel):
    device_id : str

# Ubidots Configuration
UBIDOTS_TOKEN = "BBUS-MT0TtGV0niggXIlCYujJkIMHhE1bht"
DEVICE_LABEL = "thermochick-proto"  # You can change this label based on your setup
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"

HEADERS = {
    "X-Auth-Token": UBIDOTS_TOKEN,
    "Content-Type": "application/json"
}

@router.post("/sensor")
def post_sensor_data(data: SensorData):
    # Save data locally
    result = save_sensor_data(data.device_id, data.temperature, data.humidity)

    # Prepare payload for Ubidots
    payload = {
        "temperature": data.temperature,
        "humidity": data.humidity
    }

    # Post to Ubidots (asynchronously or silently, without affecting return schema)
    try:
        requests.post(UBIDOTS_URL, headers=HEADERS, json=payload)
    except requests.exceptions.RequestException:
        pass  # Fail silently or log it if needed

    # Return standard response schema
    return {
        "status": "success",
        "data": {
            "temperature": data.temperature,
            "humidity": data.humidity
        }
    }

@router.get("/sensor")
def get_sensor_data(
    device_id: str = Query(..., description="ID of the IoT device"),
):
    result = get_latest_data(device_id)
    return {"status": "success", "data": result}

# @router.get("/sensor/recent")
# def get_recent_data(data : DataID):
#     result = get_recent_sensor_data(data.device_id)
#     return {
#         "status": "success",
#         "data": result
#     }
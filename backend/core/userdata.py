from supabase import create_client, Client
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_temperature(device_id: str, temperature: Optional[float] = 26.0):
    data = {
        "device_id": device_id,
        "temperature": temperature or 26.0
    }
    response = supabase.table("temperature_set").upsert(data, on_conflict=["device_id"]).execute()
    return response.data


def insert_location(device_id: str, longitude: float, latitude: float, altitude: float):
    data = {
        "device_id": device_id,
        "longitude": longitude,
        "latitude": latitude,
        "altitude": altitude
    }
    response = supabase.table("location_set").upsert(data, on_conflict=["device_id"]).execute()
    return response.data

def get_latest_temperature(device_id: str):
    response = (
        supabase.table("temperature_set")
        .select("*")
        .eq("device_id", device_id)
        .limit(1)
        .execute()
    )
    if response.data:
        return response.data[0]
    return None

def get_latest_location(device_id: str):
    response = (
        supabase.table("location_set")
        .select("*")
        .eq("device_id", device_id)
        .limit(1)
        .execute()
    )
    if response.data:
        return response.data[0]
    return None


def insert_fire_detection(device_id: str, fire_detected: bool):
    data = {
        "device_id": device_id,
        "fire_detected": fire_detected
    }
    response = supabase.table("fire_detection").upsert(data, on_conflict=["device_id"]).execute()
    return response.data

def get_fire_detection(device_id: str):
    response = (
        supabase.table("fire_detection")
        .select("*")
        .eq("device_id", device_id)
        .limit(1)
        .execute()
    )
    if response.data:
        return response.data[0]
    return None

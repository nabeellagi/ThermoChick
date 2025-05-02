from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
from core import userdata

router = APIRouter(
    tags=["Handle User Data"]
)

class TemperaturePayload(BaseModel):
    temperature: Optional[float] = 26.0

class LocationPayload(BaseModel):
    longitude: float
    latitude: float
    altitude: float

@router.post("/temperature-set")
def post_temperature(payload: TemperaturePayload, device_id: str = Query(...)):
    try:
        data = userdata.insert_temperature(device_id=device_id, temperature=payload.temperature)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert temperature: {e}")

@router.post("/location")
def post_location(payload: LocationPayload, device_id: str = Query(...)):
    try:
        data = userdata.insert_location(
            device_id=device_id,
            longitude=payload.longitude,
            latitude=payload.latitude,
            altitude=payload.altitude
        )
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert location: {e}")

@router.get("/temperature-set")
def get_temperature(device_id: str = Query(...)):
    try:
        data = userdata.get_latest_temperature(device_id)
        if not data:
            raise HTTPException(status_code=404, detail="Temperature data not found")
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve temperature: {e}")


@router.get("/location")
def get_location(device_id: str = Query(...)):
    try:
        data = userdata.get_latest_location(device_id)
        if not data:
            raise HTTPException(status_code=404, detail="Location data not found")
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve location: {e}")

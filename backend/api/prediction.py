from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from core.prediction import TempHumidPredictor
from typing import Optional

router = APIRouter(
    tags=["Prediction"]
)

@router.get("/predict")
def get_prediction(
    device_id: str = Query(..., description="ID of the IoT device"),
    seconds_ahead: int = Query(10, ge=1, le=86400, description="How many seconds into the future to predict")
):
    try:
        predictor = TempHumidPredictor(device_id=device_id)
        prediction = predictor.predict_future(seconds_ahead)
        return {
            "status": "success",
            "data": {
                "timestamp": prediction["timestamp"],
                "temperature": prediction["predicted_temperature"],
                "humidity": prediction["predicted_humidity"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plot")
def get_plot(
    device_id: str = Query(..., description="ID of the IoT device")
):
    try:
        predictor = TempHumidPredictor(device_id=device_id)
        img_bytes = predictor.get_plot_bytes()
        return StreamingResponse(img_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

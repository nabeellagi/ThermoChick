from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from core.prediction import TempHumidPredictor

router = APIRouter()
predictor = TempHumidPredictor(csv_path="data/sensor_data.csv")  # Load once on startup

@router.get("/predict")
def get_prediction(seconds_ahead: int = Query(10, description="Seconds ahead from the last timestamp")):
    try:
        prediction = predictor.predict_future(seconds_ahead)
        return {
            "status": "success",
            "data": {
                "temperature": prediction["predicted_temperature"],
                "humidity": prediction["predicted_humidity"]
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/plot")
def get_plot():
    try:
        img_bytes = predictor.get_plot_bytes()
        return StreamingResponse(img_bytes, media_type="image/png")
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

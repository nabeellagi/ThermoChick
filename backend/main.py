from fastapi import FastAPI
from api import qa, sensor, prediction, vtt
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="FAQ Assistant")

app.include_router(qa.router)
app.include_router(sensor.router)
app.include_router(prediction.router)
app.include_router(vtt.router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your device IP for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the FAQ Assistant API"}

import pandas as pd
from datetime import datetime
import os

CSV_FILE = "data/sensor_data.csv"
MAX_ROWS = 200  # Limit for the number of rows

def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["timestamp", "temperature", "humidity"])
        df.to_csv(CSV_FILE, index=False)

def save_sensor_data(temperature: float, humidity: float):
    init_csv()
    timestamp = datetime.now().isoformat()
    
    # Append new data
    new_data = pd.DataFrame([{
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity
    }])
    new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
    
    # Clean the file if it exceeds MAX_ROWS
    df = pd.read_csv(CSV_FILE)
    if len(df) > MAX_ROWS:
        # Keep only the latest MAX_ROWS
        df = df.tail(MAX_ROWS)
        df.to_csv(CSV_FILE, index=False)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "last_updated": timestamp
    }

def get_latest_data():
    init_csv()
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        return {"message": "No data available"}
    last_row = df.iloc[-1]
    return {
        "temperature": last_row["temperature"],
        "humidity": last_row["humidity"],
        "last_updated": last_row["timestamp"]
    }

def get_recent_sensor_data(n: int = 10):
    init_csv()
    df = pd.read_csv(CSV_FILE)

    if df.empty:
        return {"message": "No data available"}

    # Get last n values for temperature and humidity
    last_rows = df.tail(n)
    temperatures = last_rows["temperature"].tolist()
    humidities = last_rows["humidity"].tolist()
    timestamps = last_rows["timestamp"].tolist()

    return {
        "temperatures": temperatures,
        "humidities": humidities,
        "timestamps": timestamps
    }


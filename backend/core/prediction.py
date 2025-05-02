import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import timedelta
import psycopg2

# --- QuestDB Configuration ---
QUESTDB_CONFIG = {
    "host": "localhost",
    "port": 8812,
    "user": "admin",
    "password": "quest",
    "dbname": "qdb"
}

def get_connection():
    return psycopg2.connect(**QUESTDB_CONFIG)

# --- Predictor Class ---
class TempHumidPredictor:
    def __init__(self, device_id: str, degree: int = 5, max_rows: int = 200):
        self.device_id = device_id
        self.table_name = self._sanitize_table_name(device_id)
        self.degree = degree
        self.poly = PolynomialFeatures(degree)
        self.temperature_model = LinearRegression()
        self.humidity_model = LinearRegression()
        self.df = self._fetch_data(max_rows)
        self._prepare_data()
        self._train_models()

    def _sanitize_table_name(self, name: str) -> str:
        """
        Prevents SQL injection by allowing only alphanumeric and underscore in table names.
        """
        import re
        if not re.match(r'^[A-Za-z0-9_]+$', name):
            raise ValueError("Invalid device_id: must contain only letters, numbers, and underscores")
        return name

    def _fetch_data(self, limit=200) -> pd.DataFrame:
        query = f"""
        SELECT timestamp, temperature, humidity
        FROM {self.table_name}
        ORDER BY timestamp DESC
        LIMIT %s;
        """
        with get_connection() as conn:
            df = pd.read_sql(query, conn, params=(limit,))

        if df.empty:
            raise ValueError(f"No sensor data found for device '{self.device_id}'")

        return df.sort_values('timestamp')  # ensure chronological order

    def _prepare_data(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.x = (self.df['timestamp'] - self.df['timestamp'].min()).dt.total_seconds().values.reshape(-1, 1)
        self.x_poly = self.poly.fit_transform(self.x)
        self.y_temp = self.df['temperature'].values
        self.y_humid = self.df['humidity'].values

    def _train_models(self):
        self.temperature_model.fit(self.x_poly, self.y_temp)
        self.humidity_model.fit(self.x_poly, self.y_humid)

    def predict_future(self, seconds_ahead: int):
        last_time = self.df['timestamp'].max()
        future_time = last_time + timedelta(seconds=seconds_ahead)
        x_future = (future_time - self.df['timestamp'].min()).total_seconds()
        x_future_poly = self.poly.transform(np.array([[x_future]]))

        temp_pred = self.temperature_model.predict(x_future_poly)[0]
        humid_pred = self.humidity_model.predict(x_future_poly)[0]

        return {
            "timestamp": future_time.isoformat(),
            "predicted_temperature": round(temp_pred, 2),
            "predicted_humidity": round(humid_pred, 2)
        }

    def get_plot_bytes(self) -> BytesIO:
        # Predict using the trained models
        temp_pred = self.temperature_model.predict(self.x_poly)
        humid_pred = self.humidity_model.predict(self.x_poly)

        # Plotting
        plt.figure(figsize=(14, 6))

        # Temperature subplot
        plt.subplot(1, 2, 1)
        plt.plot(self.df['timestamp'], self.y_temp, label='Actual Temperature', color='orange')
        plt.plot(self.df['timestamp'], temp_pred, label='Predicted Temperature', color='red', linestyle='--')
        plt.xlabel('Timestamp')
        plt.ylabel('Temperature')
        plt.title('Temperature: Actual vs Predicted')
        plt.xticks(rotation=45)
        plt.legend()

        # Humidity subplot
        plt.subplot(1, 2, 2)
        plt.plot(self.df['timestamp'], self.y_humid, label='Actual Humidity', color='skyblue')
        plt.plot(self.df['timestamp'], humid_pred, label='Predicted Humidity', color='blue', linestyle='--')
        plt.xlabel('Timestamp')
        plt.ylabel('Humidity')
        plt.title('Humidity: Actual vs Predicted')
        plt.xticks(rotation=45)
        plt.legend()

        plt.tight_layout()

        # Save to buffer
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf
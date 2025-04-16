import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime, timedelta

class TempHumidPredictor:
    def __init__(self, csv_path: str, degree: int = 6):
        self.degree = degree
        self.poly = PolynomialFeatures(degree)
        self.temperature_model = LinearRegression()
        self.humidity_model = LinearRegression()
        self.df = pd.read_csv(csv_path)
        self._prepare_data()
        self._train_models()

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
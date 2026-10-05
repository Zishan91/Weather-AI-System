from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import xgboost as xgb
import joblib

from tensorflow.keras.models import load_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Load trained models
# ==========================================

xgb_model = xgb.XGBRegressor()
xgb_model.load_model("models/xgboost_aqi.json")

lstm_model = load_model("models/lstm_weather.keras")

lstm_scaler = joblib.load(
    "models/lstm_scaler.pkl"
)


# ==========================================
# Input models
# ==========================================

class AQIInput(BaseModel):

    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    precipitation: float

    pm10: float
    pm2_5: float
    carbon_monoxide: float
    nitrogen_dioxide: float
    sulphur_dioxide: float
    ozone: float

    hour: int
    day: int
    month: int
    day_of_week: int

    aqi_lag_1: float
    aqi_lag_24: float

    pm25_lag_1: float
    pm25_lag_24: float


class WeatherInput(BaseModel):

    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    precipitation: float


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Weather AI System API is running"
    }


# ==========================================
# Health
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "OK",
        "xgboost": "loaded",
        "lstm": "loaded",
        "scaler": "loaded"
    }


# ==========================================
# Models
# ==========================================

@app.get("/models")
def models():

    return {
        "aqi_model": "XGBoost",
        "weather_model": "LSTM"
    }


# ==========================================
# AQI Prediction
# ==========================================

@app.post("/predict/aqi")
def predict_aqi(data: AQIInput):

    features = np.array([[
        data.temperature,
        data.humidity,
        data.pressure,
        data.wind_speed,
        data.precipitation,

        data.pm10,
        data.pm2_5,
        data.carbon_monoxide,
        data.nitrogen_dioxide,
        data.sulphur_dioxide,
        data.ozone,

        data.hour,
        data.day,
        data.month,
        data.day_of_week,

        data.aqi_lag_1,
        data.aqi_lag_24,

        data.pm25_lag_1,
        data.pm25_lag_24
    ]])

    prediction = xgb_model.predict(features)[0]

    return {
        "predicted_aqi": round(
            float(prediction), 2
        )
    }


# ==========================================
# Weather Prediction
# ==========================================

@app.post("/predict/weather")
def predict_weather(data: WeatherInput):

    # Create one weather observation
    current_data = np.array([[
        data.temperature,
        data.humidity,
        data.pressure,
        data.wind_speed,
        data.precipitation
    ]])

    # Scale using the SAME scaler used during training
    scaled_data = lstm_scaler.transform(
        current_data
    )

    # Repeat observation to create
    # a 24-hour input sequence
    sequence = np.repeat(
        scaled_data[np.newaxis, :, :],
        24,
        axis=1
    )

    # LSTM prediction
    prediction_scaled = lstm_model.predict(
        sequence,
        verbose=0
    )[0][0]

    # Convert temperature back
    # to Celsius
    dummy = np.zeros(
        (1, 5)
    )

    dummy[0][0] = prediction_scaled

    prediction = lstm_scaler.inverse_transform(
        dummy
    )[0][0]

    return {
        "predicted_temperature": round(
            float(prediction), 2
        )
    }
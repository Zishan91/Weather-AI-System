"use client";

import { useState } from "react";

export default function Home() {
  const [weather, setWeather] = useState({
    temperature: 25,
    humidity: 60,
    pressure: 1010,
    wind_speed: 10,
    precipitation: 0,
  });

  const [aqi, setAqi] = useState({
    temperature: 25,
    humidity: 60,
    pressure: 1010,
    wind_speed: 10,
    precipitation: 0,
    pm10: 40,
    pm2_5: 25,
    carbon_monoxide: 200,
    nitrogen_dioxide: 20,
    sulphur_dioxide: 5,
    ozone: 80,
    hour: 12,
    day: 15,
    month: 10,
    day_of_week: 1,
    aqi_lag_1: 60,
    aqi_lag_24: 60,
    pm25_lag_1: 25,
    pm25_lag_24: 25,
  });

  const [weatherResult, setWeatherResult] = useState(null);
  const [aqiResult, setAqiResult] = useState(null);

  const [loadingWeather, setLoadingWeather] = useState(false);
  const [loadingAqi, setLoadingAqi] = useState(false);

  // ---------------- WEATHER PREDICTION ----------------

  const predictWeather = async () => {
    setLoadingWeather(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/predict/weather",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(weather),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail
            ? JSON.stringify(data.detail)
            : "Weather prediction failed"
        );
      }

      setWeatherResult(data);
    } catch (error) {
      alert(error.message);
    }

    setLoadingWeather(false);
  };

  // ---------------- AQI PREDICTION ----------------

  const predictAQI = async () => {
    setLoadingAqi(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/predict/aqi",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(aqi),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail
            ? JSON.stringify(data.detail)
            : "AQI prediction failed"
        );
      }

      setAqiResult(data);
    } catch (error) {
      alert(error.message);
    }

    setLoadingAqi(false);
  };

  return (
    <main
      style={{
        minHeight: "100vh",
        background: "#f4f7fb",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          maxWidth: "1100px",
          margin: "auto",
        }}
      >
        {/* HEADER */}

        <div
          style={{
            textAlign: "center",
            marginBottom: "40px",
          }}
        >
          <h1
            style={{
              fontSize: "36px",
              marginBottom: "10px",
              color: "#111827",
            }}
          >
            🌤️ AI Weather & AQI Prediction
          </h1>

          <p
            style={{
              color: "#4b5563",
              fontSize: "17px",
            }}
          >
            AI-powered weather forecasting and air quality prediction
          </p>
        </div>

        {/* MAIN CARDS */}

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "25px",
          }}
        >
          {/* WEATHER CARD */}

          <div
            style={{
              background: "white",
              padding: "25px",
              borderRadius: "15px",
              boxShadow:
                "0 4px 15px rgba(0,0,0,0.08)",
            }}
          >
            <h2
              style={{
                color: "#111827",
                marginBottom: "8px",
              }}
            >
              🌡️ Weather Prediction
            </h2>

            <p
              style={{
                color: "#6b7280",
                marginBottom: "25px",
              }}
            >
              Predict future temperature using LSTM
            </p>

            {/* Temperature */}

            <label style={labelStyle}>
              Temperature (°C)
            </label>

            <input
              type="number"
              value={weather.temperature}
              onChange={(e) =>
                setWeather({
                  ...weather,
                  temperature: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* Humidity */}

            <label style={labelStyle}>
              Humidity (%)
            </label>

            <input
              type="number"
              value={weather.humidity}
              onChange={(e) =>
                setWeather({
                  ...weather,
                  humidity: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* Pressure */}

            <label style={labelStyle}>
              Pressure (hPa)
            </label>

            <input
              type="number"
              value={weather.pressure}
              onChange={(e) =>
                setWeather({
                  ...weather,
                  pressure: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* Wind Speed */}

            <label style={labelStyle}>
              Wind Speed (km/h)
            </label>

            <input
              type="number"
              value={weather.wind_speed}
              onChange={(e) =>
                setWeather({
                  ...weather,
                  wind_speed: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* Precipitation */}

            <label style={labelStyle}>
              Precipitation (mm)
            </label>

            <input
              type="number"
              value={weather.precipitation}
              onChange={(e) =>
                setWeather({
                  ...weather,
                  precipitation: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            <button
              onClick={predictWeather}
              style={buttonStyle}
            >
              {loadingWeather
                ? "Predicting..."
                : "Predict Temperature"}
            </button>

            {/* WEATHER RESULT */}

            {weatherResult && (
              <div style={resultStyle}>
                <h3
                  style={{
                    color: "#111827",
                    marginBottom: "10px",
                  }}
                >
                  Predicted Temperature
                </h3>

                <div
                  style={{
                    fontSize: "32px",
                    fontWeight: "bold",
                    color: "#111827",
                  }}
                >
                  {Number(
                    weatherResult.predicted_temperature
                  ).toFixed(2)}{" "}
                  °C
                </div>
              </div>
            )}
          </div>

          {/* AQI CARD */}

          <div
            style={{
              background: "white",
              padding: "25px",
              borderRadius: "15px",
              boxShadow:
                "0 4px 15px rgba(0,0,0,0.08)",
            }}
          >
            <h2
              style={{
                color: "#111827",
                marginBottom: "8px",
              }}
            >
              🌫️ AQI Prediction
            </h2>

            <p
              style={{
                color: "#6b7280",
                marginBottom: "25px",
              }}
            >
              Predict air quality using XGBoost
            </p>

            {/* Temperature */}

            <label style={labelStyle}>
              Temperature (°C)
            </label>

            <input
              type="number"
              value={aqi.temperature}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  temperature: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* Humidity */}

            <label style={labelStyle}>
              Humidity (%)
            </label>

            <input
              type="number"
              value={aqi.humidity}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  humidity: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* Pressure */}

            <label style={labelStyle}>
              Pressure (hPa)
            </label>

            <input
              type="number"
              value={aqi.pressure}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  pressure: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* Wind */}

            <label style={labelStyle}>
              Wind Speed (km/h)
            </label>

            <input
              type="number"
              value={aqi.wind_speed}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  wind_speed: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* Precipitation */}

            <label style={labelStyle}>
              Precipitation (mm)
            </label>

            <input
              type="number"
              value={aqi.precipitation}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  precipitation: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* PM10 */}

            <label style={labelStyle}>
              PM10
            </label>

            <input
              type="number"
              value={aqi.pm10}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  pm10: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* PM2.5 */}

            <label style={labelStyle}>
              PM2.5
            </label>

            <input
              type="number"
              value={aqi.pm2_5}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  pm2_5: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            {/* CO */}

            <label style={labelStyle}>
              CO
            </label>

            <input
              type="number"
              value={aqi.carbon_monoxide}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  carbon_monoxide: Number(
                    e.target.value
                  ),
                })
              }
              style={inputStyle}
            />

            {/* NO2 */}

            <label style={labelStyle}>
              NO₂
            </label>

            <input
              type="number"
              value={aqi.nitrogen_dioxide}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  nitrogen_dioxide: Number(
                    e.target.value
                  ),
                })
              }
              style={inputStyle}
            />

            {/* SO2 */}

            <label style={labelStyle}>
              SO₂
            </label>

            <input
              type="number"
              value={aqi.sulphur_dioxide}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  sulphur_dioxide: Number(
                    e.target.value
                  ),
                })
              }
              style={inputStyle}
            />

            {/* O3 */}

            <label style={labelStyle}>
              O₃
            </label>

            <input
              type="number"
              value={aqi.ozone}
              onChange={(e) =>
                setAqi({
                  ...aqi,
                  ozone: Number(e.target.value),
                })
              }
              style={inputStyle}
            />

            <button
              onClick={predictAQI}
              style={buttonStyle}
            >
              {loadingAqi
                ? "Predicting..."
                : "Predict AQI"}
            </button>

            {/* AQI RESULT */}

            {aqiResult && (
              <div style={resultStyle}>
                <h3
                  style={{
                    color: "#111827",
                    marginBottom: "10px",
                  }}
                >
                  Predicted AQI
                </h3>

                <div
                  style={{
                    fontSize: "32px",
                    fontWeight: "bold",
                    color: "#111827",
                  }}
                >
                  {Number(
                    aqiResult.predicted_aqi
                  ).toFixed(2)}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* FOOTER */}

        <div
          style={{
            textAlign: "center",
            marginTop: "40px",
            color: "#6b7280",
          }}
        >
          <p>
            Powered by <b>XGBoost</b> & <b>LSTM</b> |
            FastAPI + Next.js
          </p>
        </div>
      </div>
    </main>
  );
}

// ---------------- STYLES ----------------

const labelStyle = {
  display: "block",
  color: "#374151",
  fontWeight: "500",
  marginBottom: "6px",
};

const inputStyle = {
  width: "100%",
  padding: "10px",
  marginBottom: "15px",
  border: "1px solid #d1d5db",
  borderRadius: "8px",
  background: "white",
  color: "#111827",
  fontSize: "15px",
  boxSizing: "border-box",
};

const buttonStyle = {
  width: "100%",
  padding: "12px",
  border: "none",
  borderRadius: "8px",
  background: "#111827",
  color: "white",
  fontSize: "16px",
  cursor: "pointer",
  marginTop: "5px",
};

const resultStyle = {
  marginTop: "20px",
  padding: "18px",
  background: "#eef6ff",
  borderRadius: "10px",
  textAlign: "center",
};
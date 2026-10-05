import requests
import pandas as pd

# ==========================================
# Pune Location
# ==========================================
latitude = 18.5204
longitude = 73.8567

# ==========================================
# Open-Meteo Air Quality API
# ==========================================
url = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",

    "hourly": [
        "pm10",
        "pm2_5",
        "carbon_monoxide",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "ozone",
        "us_aqi"
    ],

    "timezone": "Asia/Kolkata"
}

# ==========================================
# Send request
# ==========================================
response = requests.get(url, params=params)

# ==========================================
# Check response
# ==========================================
if response.status_code == 200:

    data = response.json()

    # Convert API data into DataFrame
    df = pd.DataFrame(data["hourly"])

    # Save CSV
    df.to_csv("data/air_quality_data.csv", index=False)

    # Display information
    print("\nAir quality data downloaded successfully!")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nDataset shape:")
    print(df.shape)

else:

    print("Error:", response.status_code)
    print(response.text)
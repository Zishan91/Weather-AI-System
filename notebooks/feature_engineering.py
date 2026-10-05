import pandas as pd

# ==========================================
# 1. Load combined dataset
# ==========================================

df = pd.read_csv("data/combined_data.csv")

# Convert time to datetime
df["time"] = pd.to_datetime(df["time"])

# Sort by time
df = df.sort_values("time").reset_index(drop=True)


# ==========================================
# 2. Create time-based features
# ==========================================

df["hour"] = df["time"].dt.hour
df["day"] = df["time"].dt.day
df["month"] = df["time"].dt.month
df["day_of_week"] = df["time"].dt.dayofweek


# ==========================================
# 3. Create weather lag features
# ==========================================

df["temperature_lag_1"] = df["temperature_2m"].shift(1)
df["temperature_lag_24"] = df["temperature_2m"].shift(24)

df["humidity_lag_1"] = df["relative_humidity_2m"].shift(1)
df["humidity_lag_24"] = df["relative_humidity_2m"].shift(24)


# ==========================================
# 4. Create air-quality lag features
# ==========================================

df["aqi_lag_1"] = df["us_aqi"].shift(1)
df["aqi_lag_24"] = df["us_aqi"].shift(24)

df["pm25_lag_1"] = df["pm2_5"].shift(1)
df["pm25_lag_24"] = df["pm2_5"].shift(24)


# ==========================================
# 5. Create future prediction targets
# ==========================================

# Next-hour temperature
df["future_temperature"] = df["temperature_2m"].shift(-1)

# Next-hour AQI
df["future_aqi"] = df["us_aqi"].shift(-1)


# ==========================================
# 6. Remove rows created by lag/shift
# ==========================================

df = df.dropna().reset_index(drop=True)


# ==========================================
# 7. Save processed dataset
# ==========================================

df.to_csv("data/processed_data.csv", index=False)


# ==========================================
# 8. Display information
# ==========================================

print("Feature engineering completed successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nNew columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())
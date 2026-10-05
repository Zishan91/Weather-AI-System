import pandas as pd
import matplotlib.pyplot as plt

# Load combined dataset
df = pd.read_csv("data/combined_data.csv")

# Convert time to datetime
df["time"] = pd.to_datetime(df["time"])

# Basic information
print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nStatistical Summary:")
print(df.describe())

# -----------------------------
# Temperature graph
# -----------------------------
plt.figure(figsize=(12, 5))
plt.plot(df["time"], df["temperature_2m"])
plt.title("Temperature Over Time")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------------------
# AQI graph
# -----------------------------
plt.figure(figsize=(12, 5))
plt.plot(df["time"], df["us_aqi"])
plt.title("AQI Over Time")
plt.xlabel("Time")
plt.ylabel("AQI")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------------------
# PM2.5 graph
# -----------------------------
plt.figure(figsize=(12, 5))
plt.plot(df["time"], df["pm2_5"])
plt.title("PM2.5 Over Time")
plt.xlabel("Time")
plt.ylabel("PM2.5")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
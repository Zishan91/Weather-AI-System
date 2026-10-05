import pandas as pd

# Load weather data
weather = pd.read_csv("data/weather_data.csv")

# Load air quality data
air_quality = pd.read_csv("data/air_quality_data.csv")

# Convert time column to datetime
weather["time"] = pd.to_datetime(weather["time"])
air_quality["time"] = pd.to_datetime(air_quality["time"])

# Merge both datasets using time
combined = pd.merge(
    weather,
    air_quality,
    on="time",
    how="inner"
)

# Sort by time
combined = combined.sort_values("time")

# Save combined dataset
combined.to_csv("data/combined_data.csv", index=False)

# Display results
print("\nData combined successfully!")

print("\nFirst 5 rows:")
print(combined.head())

print("\nColumns:")
print(combined.columns.tolist())

print("\nDataset shape:")
print(combined.shape)

print("\nMissing values:")
print(combined.isnull().sum())
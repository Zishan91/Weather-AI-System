import pandas as pd
import numpy as np

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# 1. Load processed data
# ==========================================

df = pd.read_csv("data/processed_data.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ==========================================
# 2. Select features
# ==========================================

features = [
    "temperature_2m",
    "relative_humidity_2m",
    "surface_pressure",
    "wind_speed_10m",
    "precipitation",
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "hour",
    "day",
    "month",
    "day_of_week",
    "aqi_lag_1",
    "aqi_lag_24",
    "pm25_lag_1",
    "pm25_lag_24"
]

target = "future_aqi"


# ==========================================
# 3. Create X and y
# ==========================================

X = df[features]
y = df[target]


# ==========================================
# 4. Time-based train/test split
# ==========================================

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 5. Create XGBoost model
# ==========================================

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)


# ==========================================
# 6. Train model
# ==========================================

print("\nTraining XGBoost model...")

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 7. Make predictions
# ==========================================

predictions = model.predict(X_test)


# ==========================================
# 8. Evaluate model
# ==========================================

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)


print("\n========== MODEL RESULTS ==========")

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R²  :", round(r2, 2))


# ==========================================
# 9. Show sample predictions
# ==========================================

results = pd.DataFrame({
    "Actual AQI": y_test.values[:10],
    "Predicted AQI": predictions[:10]
})

print("\nSample Predictions:")
print(results)


# ==========================================
# 10. Save model
# ==========================================

model.save_model("models/xgboost_aqi.json")

print("\nModel saved successfully!")
print("Location: models/xgboost_aqi.json")
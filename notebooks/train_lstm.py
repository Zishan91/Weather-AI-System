import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


# ==========================================
# 1. Load processed data
# ==========================================

df = pd.read_csv("data/processed_data.csv")

df["time"] = pd.to_datetime(df["time"])

df = df.sort_values("time").reset_index(drop=True)

print("Dataset loaded!")
print("Shape:", df.shape)


# ==========================================
# 2. Select weather features
# ==========================================

features = [
    "temperature_2m",
    "relative_humidity_2m",
    "surface_pressure",
    "wind_speed_10m",
    "precipitation"
]

data = df[features].values


# ==========================================
# 3. Scale the data
# ==========================================

scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(data)

joblib.dump(scaler, "models/lstm_scaler.pkl")
# ==========================================
# 4. Create sequences
# ==========================================

sequence_length = 24

X = []
y = []

for i in range(sequence_length, len(scaled_data)):

    X.append(
        scaled_data[i - sequence_length:i]
    )

    # Temperature is column 0
    y.append(
        scaled_data[i, 0]
    )

X = np.array(X)
y = np.array(y)


print("\nSequence shape:", X.shape)
print("Target shape:", y.shape)


# ==========================================
# 5. Time-based train/test split
# ==========================================

split_index = int(len(X) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 6. Build LSTM model
# ==========================================

model = Sequential([
    
    LSTM(
        64,
        return_sequences=True,
        input_shape=(X_train.shape[1], X_train.shape[2])
    ),

    Dropout(0.2),

    LSTM(32),

    Dropout(0.2),

    Dense(1)
])


# ==========================================
# 7. Compile
# ==========================================

model.compile(
    optimizer="adam",
    loss="mean_squared_error"
)


# ==========================================
# 8. Train
# ==========================================

print("\nTraining LSTM model...")

history = model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.1,
    verbose=1
)

print("\nTraining completed!")


# ==========================================
# 9. Prediction
# ==========================================

predictions_scaled = model.predict(
    X_test,
    verbose=0
)


# ==========================================
# 10. Convert predictions back
#     to temperature scale
# ==========================================

dummy_actual = np.zeros(
    (len(y_test), len(features))
)

dummy_prediction = np.zeros(
    (len(predictions_scaled), len(features))
)

dummy_actual[:, 0] = y_test

dummy_prediction[:, 0] = predictions_scaled[:, 0]


actual_values = scaler.inverse_transform(
    dummy_actual
)[:, 0]

predicted_values = scaler.inverse_transform(
    dummy_prediction
)[:, 0]


# ==========================================
# 11. Evaluate
# ==========================================

mae = mean_absolute_error(
    actual_values,
    predicted_values
)

rmse = np.sqrt(
    mean_squared_error(
        actual_values,
        predicted_values
    )
)

r2 = r2_score(
    actual_values,
    predicted_values
)


print("\n========== LSTM RESULTS ==========")

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R²  :", round(r2, 2))


# ==========================================
# 12. Sample predictions
# ==========================================

results = pd.DataFrame({
    "Actual Temperature": actual_values[:10],
    "Predicted Temperature": predicted_values[:10]
})

print("\nSample Predictions:")
print(results)


# ==========================================
# 13. Save LSTM model
# ==========================================

model.save(
    "models/lstm_weather.keras"
)

print("\nLSTM model saved successfully!")

print(
    "Location: models/lstm_weather.keras"
)
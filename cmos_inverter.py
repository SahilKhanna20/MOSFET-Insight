# -*- coding: utf-8 -*-
# Load Libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from google.colab import files

print("✅ Libraries Loaded")

"""# Upload Dataset"""

file_path = '/content/CMOS_VTC_Dataset.csv'
df = pd.read_csv(file_path)
df.head()

"""# Preprocess Data"""

X = df[['Vdd', 'Vin', 'Vtn', 'Vtp', 'Wn', 'Ln', 'Wp', 'Lp']]
y = df[['Vout']]

scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)
print("✅ Data Preprocessed")

"""# Train Model

"""

model = Sequential([
    Dense(64, activation='relu', input_shape=(8,)),
    Dense(128, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])
model.fit(X_train, y_train, epochs=100, validation_split=0.1, verbose=0)
print("✅ Model Trained")

"""# User Input and Prediction"""

Vdd = float(input("Enter Vdd (e.g., 5): "))
Vtn = float(input("Enter Vtn (e.g., 0.7): "))
Vtp = float(input("Enter Vtp (e.g., -0.7): "))
Wn = float(input("Enter Wn (e.g., 2): "))
Ln = float(input("Enter Ln (e.g., 0.18): "))
Wp = float(input("Enter Wp (e.g., 4): "))
Lp = float(input("Enter Lp (e.g., 0.18): "))
Vin_start = float(input("Enter Vin start value (e.g., 0): "))
Vin_end = float(input("Enter Vin end value (e.g., 5): "))
step = float(input("Enter step size (e.g., 0.05): "))

Vin_vals = np.arange(Vin_start, Vin_end + step, step)

input_data = pd.DataFrame({
    'Vdd': [Vdd] * len(Vin_vals),
    'Vin': Vin_vals,
    'Vtn': [Vtn] * len(Vin_vals),
    'Vtp': [Vtp] * len(Vin_vals),
    'Wn': [Wn] * len(Vin_vals),
    'Ln': [Ln] * len(Vin_vals),
    'Wp': [Wp] * len(Vin_vals),
    'Lp': [Lp] * len(Vin_vals)
})

X_input_scaled = scaler_X.transform(input_data)

Vout_pred_scaled = model.predict(X_input_scaled)
Vout_pred = scaler_y.inverse_transform(Vout_pred_scaled).flatten()
Vout_pred = np.clip(Vout_pred, 0, Vdd)

"""# Plot Graph"""

plt.figure(figsize=(8, 5))
plt.plot(Vin_vals, Vout_pred, label='Predicted VTC',marker='o', color='blue')
plt.plot(Vin_vals, Vin_vals, '--', label='Vin Reference Line', color='gray')
plt.xlabel("Vin (V)")
plt.ylabel("Vout (V)")
plt.title("CMOS Inverter VTC")
plt.legend()
plt.grid(True)
plt.show()

"""# Critical Voltages"""

VOH = max(Vout_pred)
VOL = min(Vout_pred)

diff = np.abs(Vin_vals - Vout_pred)
VTH = Vin_vals[np.argmin(diff)]

dVout_dVin = np.gradient(Vout_pred, step)
VIL = Vin_vals[np.argmin(dVout_dVin)]
VIH = Vin_vals[np.argmax(dVout_dVin)]

print(f"VOH: {VOH:.3f} V")
print(f"VOL: {VOL:.3f} V")
print(f"VTH (Vin = Vout): {VTH:.3f} V")
print(f"VIL (Max -ve slope): {VIL:.3f} V")
print(f"VIH (Max +ve slope): {VIH:.3f} V")

# -*- coding: utf-8 -*-
"""CMOS_Inverter_Transient

# Load Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

print("✅ Libraries Loaded")

"""# Upload Dataset

"""

file_path = '/content/final_cmos_inverter_corrected_resave (1).csv'  

df = pd.read_csv(file_path)
df.head()

"""# Preprocess Data

"""

X = df[['time_ns', 'Vin', 'Vdd']].values
y = df['Vout'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

window_size = 5
X_seq = []
y_seq = []
for i in range(len(X_scaled) - window_size):
    X_seq.append(X_scaled[i:i+window_size])
    y_seq.append(y[i+window_size])

X_seq = np.array(X_seq)
y_seq = np.array(y_seq)

X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

print("✅ Data Preprocessed")

"""# Train Model"""

model = Sequential([
    LSTM(64, activation='tanh', input_shape=(window_size, 3)),
    Dense(32, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.summary()

history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

print("✅ Model Trained")

"""# User Input and Prediction"""

user_vdd = float(input("Enter Vdd (example 1.8): "))


time_ns_user = np.arange(0, 40, 0.005)


pulse_period = 10
pulse_width = 5

Vin_user = np.zeros_like(time_ns_user)
for i, t in enumerate(time_ns_user):
    if (t % pulse_period) < pulse_width:
        Vin_user[i] = user_vdd
    else:
        Vin_user[i] = 0


X_user = np.column_stack((time_ns_user, Vin_user, np.full_like(time_ns_user, user_vdd)))
X_user_scaled = scaler.transform(X_user)


X_user_seq = []
for i in range(len(X_user_scaled) - window_size):
    X_user_seq.append(X_user_scaled[i:i+window_size])

X_user_seq = np.array(X_user_seq)


Vout_predicted = model.predict(X_user_seq)


time_ns_user_aligned = time_ns_user[window_size:]
Vin_user_aligned = Vin_user[window_size:]

"""# Plot Graph"""

plt.figure(figsize=(12, 6))
plt.plot(time_ns_user_aligned, Vin_user_aligned, label="Vin", linestyle="--", linewidth=2)
plt.plot(time_ns_user_aligned, Vout_predicted.flatten(), label="Predicted Vout", linewidth=2)
plt.title("Predicted CMOS Inverter Transient Response")
plt.xlabel("Time (ns)")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.legend()
plt.xlim(0, 40)
plt.ylim(-0.2, user_vdd + 0.5)
plt.show()

"""# Propagation Delays Calculation"""

def find_crossing(time_array, signal, target):
    idx = np.where(np.diff(np.sign(signal - target)))[0]
    if len(idx) == 0:
        return None

    i = idx[0]
    t0, t1 = time_array[i], time_array[i+1]
    y0, y1 = signal[i], signal[i+1]
    return t0 + (target - y0) * (t1 - t0) / (y1 - y0)

target_50 = 0.5 * user_vdd

vin_50_rise_time = find_crossing(time_ns_user_aligned, Vin_user_aligned, target_50)
vin_50_fall_time = find_crossing(time_ns_user_aligned[::-1], Vin_user_aligned[::-1], target_50)

vout_50_rise_time = find_crossing(time_ns_user_aligned, Vout_predicted.flatten(), target_50)
vout_50_fall_time = find_crossing(time_ns_user_aligned[::-1], Vout_predicted.flatten()[::-1], target_50)

tpLH = None
if vin_50_rise_time is not None and vout_50_fall_time is not None:
    tpLH = vout_50_fall_time - vin_50_rise_time

tpHL = None
if vin_50_fall_time is not None and vout_50_rise_time is not None:
    tpHL = vout_50_rise_time - vin_50_fall_time

target_10 = 0.1 * user_vdd
target_90 = 0.9 * user_vdd

t_rise_start = find_crossing(time_ns_user_aligned, Vout_predicted.flatten(), target_10)
t_rise_end = find_crossing(time_ns_user_aligned, Vout_predicted.flatten(), target_90)

t_fall_start = find_crossing(time_ns_user_aligned[::-1], Vout_predicted.flatten()[::-1], target_90)
t_fall_end = find_crossing(time_ns_user_aligned[::-1], Vout_predicted.flatten()[::-1], target_10)

t_rise = None
if t_rise_start is not None and t_rise_end is not None:
    t_rise = t_rise_end - t_rise_start

t_fall = None
if t_fall_start is not None and t_fall_end is not None:
    t_fall = t_fall_start - t_fall_end

print("\n--- Performance Metrics ---")
if tpLH is not None:
    print(f"tpLH (Low to High Propagation Delay): {tpLH:.3f} ns")
if tpHL is not None:
    print(f"tpHL (High to Low Propagation Delay): {tpHL:.3f} ns")
if t_rise is not None:
    print(f"Rise Time (10% to 90%): {t_rise:.3f} ns")
if t_fall is not None:
    print(f"Fall Time (90% to 10%): {t_fall:.3f} ns")

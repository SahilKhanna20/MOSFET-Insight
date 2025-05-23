# 🔌 CMOS Inverter Analysis using Machine Learning

A Python-based application that predicts the DC and transient behavior of a CMOS inverter using machine learning models like neural networks and LSTM. It offers fast, SPICE-like simulation results using trained models and realistic datasets.

## 📊 DC Transfer Analysis
- Predicts `Vout` using CMOS parameters:
  - `Vdd`, `Vin`, `Vtn`, `Vtp`, `Wn`, `Wp`, `Ln`, `Lp`
- Generates the **Voltage Transfer Characteristic (VTC)** curve.
- Computes critical voltages:
  - `VOH`, `VOL`, `VIL`, `VIH`, `VTH`
- Uses polynomial regression and dense neural networks.

## 🔁 Transient Response Prediction
- Simulates transient `Vout` for square-wave `Vin` inputs.
- Accepts user inputs:
  - Pulse width, period, rise/fall times (in ns/ps)
- LSTM model trained on SPICE-like waveform datasets.
- Visualizes output waveform over time under capacitive load.

## 🧠 Machine Learning Models
- Uses:
  - `Sequential` dense models for DC regression.
  - `LSTM` networks for time-series transient prediction.
- Data preprocessing with:
  - `MinMaxScaler`, `train_test_split`
- Training and evaluation using:
  - `TensorFlow`, `Keras`, `Scikit-learn`

## 📁 Dataset and Input
- Accepts CSV datasets with Vdd, Vin, Vtn, Vtp, W/L ratios, and Vout.
- SPICE-like datasets generated using sigmoid-based modeling and RC-delay simulations.
- Supports waveform plotting and dataset visualization.

## 📦 Libraries Used
- `NumPy`, `Pandas`, `Matplotlib`
- `Scikit-learn`, `TensorFlow`, `Keras`

## ✅ Output Features
- DC Analysis: VTC plot, critical voltage extraction.
- Transient Analysis: Time vs Vout waveform simulation.
- Clipping to valid CMOS voltage levels (0 to Vdd).
- User-interactive input and automatic scaling.

---

> ⚠️ **Note**: Ensure dataset files (e.g. `Realistic_CMOS_VTC_HighRes.csv`) are available in the working directory. Run on Google Colab or local Python environment with the listed dependencies installed.

---

## 📸 Preview
![VTC_Plot](https://github.com/user-attachments/assets/example-vtc-plot.png)
![Transient_Plot](https://github.com/user-attachments/assets/example-transient-plot.png)

---

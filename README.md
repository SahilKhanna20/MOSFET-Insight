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

> ⚠️ **Note**: Ensure dataset files (e.g. `CMOS_VTC_Dataset.csv`) are available in the working directory. Run on Google Colab or local Python environment with the listed dependencies installed.

---

## 📸 Preview(DC Analysis)
![Sequential Model](https://github.com/user-attachments/assets/758079c6-742d-4c93-b32d-07d39081cb7d)
![Input Parameters](https://github.com/user-attachments/assets/8fd979d0-eb1d-4f92-a524-634308cd10b7)
![VTC Plot](https://github.com/user-attachments/assets/8c3410f6-a960-4e52-add0-cebab7fdec2c)
![Critical Voltages](https://github.com/user-attachments/assets/7c8e2c04-63cf-4db2-be56-7f02dbb399ba)


## 📸 Preview(Transient Analysis)
![LSTM Model](https://github.com/user-attachments/assets/5b8ef1b6-cf42-4130-9c13-b4df68a488ec)
![Transient Analysis](https://github.com/user-attachments/assets/d6944af6-5f7a-49fd-9454-922e1f021ace)

---

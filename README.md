# 🚀 Multi-Page Stock Analytics & Forecasting Terminal

An advanced **financial analytics dashboard** built using **Python** and **Streamlit**, designed to simulate real-world stock analysis workflows.
This project combines **data analysis, financial modeling, and time-series forecasting** to help users make informed investment decisions.

---

## 📌 Key Highlights

* 📊 Interactive stock dashboards with real-time data
* 📉 Technical indicators: **RSI & MACD**
* 🔮 Time-series forecasting using **ARIMA**
* ⚖️ Risk & return analysis using **CAPM**
* 📈 Beta calculation via regression (market comparison)
* 🧠 Strong focus on **data-driven decision making**

---

## 🧠 Problem Statement

Investors often rely on fragmented tools for:

* Stock visualization
* Risk analysis
* Forecasting

This project solves that by providing a **unified platform** that integrates:

* Data visualization
* Statistical modeling
* Financial theory

---

## 🏗️ Project Architecture

```
📦 stock-terminal-pro
 ┣ 📜 Trading_App.py           # Main entry point (Navigation UI)
 ┣ 📜 Stock_Analysis.py        # Stock insights & indicators
 ┣ 📜 Stock_Prediction.py      # ARIMA forecasting module
 ┣ 📜 capm_return.py           # Expected return (CAPM)
 ┣ 📜 Calculate_Beta.py        # Beta calculation
 ┣ 📂 utils/
 ┃ ┣ 📜 model_training.py      # ARIMA + ADF logic
 ┃ ┣ 📜 plotly_figure.py       # Visualization engine
 ┃ ┗ 📜 capm_functions.py      # Financial calculations
```

---

## ⚙️ Features Breakdown

### 📊 Stock Analysis

* Live stock data using `yfinance`
* Interactive **Candlestick & Line charts**
* Company fundamentals overview

### 📉 Technical Indicators

* **RSI (Relative Strength Index)**
  Detects overbought & oversold conditions

* **MACD (Moving Average Convergence Divergence)**
  Identifies trend reversals and momentum

---

### 🔮 Stock Price Forecasting

* **ADF Test** for stationarity check
* Data transformation using differencing
* **ARIMA Model (30, d, 30)** for prediction
* Forecasts next **30 days of stock prices**

---

### ⚖️ CAPM Analysis

Implements **Capital Asset Pricing Model**:

[
E(R_i) = R_f + \beta (R_m - R_f)
]

* Calculates **expected return**
* Compares stock performance vs market

---

### 📈 Beta Calculation

* Uses **linear regression**
* Measures volatility relative to market (S&P 500)

| Beta Value | Interpretation    |
| ---------- | ----------------- |
| β = 1      | Moves with market |
| β > 1      | More volatile     |
| β < 1      | Less volatile     |

---

## 🛠️ Tech Stack

| Category      | Tools Used                |
| ------------- | ------------------------- |
| Language      | Python                    |
| Framework     | Streamlit                 |
| Data Source   | yfinance                  |
| Visualization | Plotly, Matplotlib        |
| ML/Stats      | statsmodels, scikit-learn |
| Indicators    | ta library                |

---

## 📦 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/stock-terminal-pro.git
cd stock-terminal-pro
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
streamlit run Trading_App.py
```

---

## 📊 How It Works (Flow)

1. Fetch stock data via API
2. Perform data cleaning & transformation
3. Apply:

   * Technical Indicators
   * CAPM calculations
   * ARIMA forecasting
4. Visualize results using interactive charts

---

## 🎯 Learning Outcomes

* Time-series forecasting using ARIMA
* Financial modeling (CAPM & Beta)
* Data visualization best practices
* Building multi-page Streamlit apps
* Real-world data analysis workflow

---

## 🚀 Future Enhancements

* LSTM / Deep Learning forecasting
* Portfolio optimization module
* News sentiment analysis
* Multi-stock comparison dashboard
* Deployment on cloud (AWS / Render)

---

## 🤝 Contribution

Contributions are welcome!
Feel free to fork the repository and submit a pull request.

---

## 📬 Contact

If you found this project useful or want to collaborate:


* Email: sumranharchirkar58@gmail.com

---

## ⭐ Acknowledgment

If you like this project, consider giving it a ⭐ on GitHub!

---

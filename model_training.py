from datetime import datetime, timedelta
import pandas as pd
import numpy as np
# yfinance and statsmodels are likely imported at the top of the file (not visible)
import yfinance as yf
from statsmodels.tsa.stattools import adfuller #pip install statsmodels
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
def get_data(ticker):
    """Fetches historical stock data and returns only the closing prices."""
    # Download stock data for the given ticker symbol starting from Jan 1st, 2024
    stock_data = yf.download(ticker, start='2024-01-01')
    # Return only the 'Close' column, which is essential for price forecasting
    return stock_data[['Close']]

def stationary_check(close_price):
    """Performs the Augmented Dickey-Fuller test to check if the data is stationary."""
    # Run the ADF test; this checks if the stock price has a constant mean/variance over time
    adf_test = adfuller(close_price)
    # Extract the p-value (index 1 of results) and round it to 3 decimal places
    p_value = round(adf_test[1], 3)
    # Return the p-value: if > 0.05, the data is NOT stationary (has a trend)
    return p_value

def get_rolling_mean(close_price):
    """Calculates a 7-day moving average to smooth out short-term fluctuations."""
    # Create a rolling window of 7 days, calculate the average, and remove empty (NaN) rows
    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price

def get_differencing_order(close_price):
    """Determines how many times the data needs to be differenced to become stationary."""
    # Get the initial p-value to see if the raw data is already stationary
    p_value = stationary_check(close_price)
    # 'd' represents the order of differencing (starting at 0)
    d = 0
    
    # Keep looping until the p-value is 0.05 or less (indicating stationarity)
    while True:
        if p_value > 0.05:
            # Increment the differencing order
            d += 1
            # Subtract the previous value from the current value to remove trends
            close_price = close_price.diff().dropna()
            # Re-check the p-value on the new 'differenced' data
            p_value = stationary_check(close_price)
        else:
            # If p-value <= 0.05, the data is stationary; exit the loop
            break
            
    # Return the total number of times the data was differenced
    return d

def fit_model(data, differencing_order):
    """Initializes and trains the ARIMA model on the provided stock data."""
    # Create the ARIMA model with parameters (p=30, d=differencing_order, q=30)
    # p=30: uses the last 30 days to predict; q=30: uses 30 days of past errors
    model = ARIMA(data, order=(30, differencing_order, 30))
    # Fit the model to find the best mathematical coefficients
    model_fit = model.fit()
    
    # Define how many days into the future we want to predict (30 days)
    forecast_steps = 30
    # Generate the forecast values for the specified number of steps
    forecast = model_fit.get_forecast(steps=forecast_steps)
    
    # Extract the average (mean) predicted values from the forecast object
    predictions = forecast.predicted_mean
    return predictions

def evaluate_model(original_price, differencing_order):
    """Splits data into train/test sets and calculates the error (RMSE)."""
    # Use everything except the last 30 days for training; use the last 30 for testing
    train_data, test_data = original_price[:-30], original_price[-30:]
    # Get predictions by running the training data through our fit_model function
    predictions = fit_model(train_data, differencing_order)
    # Calculate Root Mean Squared Error (RMSE) to see how far off predictions are from reality
    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    # Return the error rounded to 2 decimal places (lower is better)
    return round(rmse, 2)

def scaling(close_price):
    """Standardizes data so it has a mean of 0 and a standard deviation of 1."""
    # Initialize the StandardScaler from sklearn
    scaler = StandardScaler()
    # Reshape data to 2D (required by scaler) and apply the transformation
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    # Return both the scaled data and the scaler object (needed to reverse scaling later)
    return scaled_data, scaler

def get_forecast(original_price, differencing_order):
    """Generates a 30-day forecast and packages it into a labeled DataFrame."""
    # Step 1: Generate the raw predictions using the ARIMA model
    predictions = fit_model(original_price, differencing_order)
    
    # Step 2: Set the timeline. Start from today's date formatted as YYYY-MM-DD
    start_date = datetime.now().strftime('%Y-%m-%d')
    # Step 3: Calculate the end date (29 days ahead for a total 30-day window)
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')
    
    # Step 4: Create a Pandas date range (a list of dates) with Daily frequency ('D')
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Step 5: Put predictions into a DataFrame using the dates as the row index
    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=['Close'])
    
    # Return the clean, dated forecast table
    return forecast_df

def inverse_scaling(scaler, scaled_data):
    """Converts scaled prediction numbers back into original stock price values."""
    # Use the 'scaler' object that was created during the training phase
    # 'inverse_transform' reverses the math (z-score) applied earlier
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1, 1))
    
    # Return the actual price values that humans can understand
    return close_price
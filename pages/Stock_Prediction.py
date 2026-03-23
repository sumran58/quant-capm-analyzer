import streamlit as st
# Import all the helper functions we discussed from the 'model_train' file
from utils.model_training import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model,get_forecast,inverse_scaling
import pandas as pd
# Import visualization functions for tables and charts from 'plotly_figure'
from utils.plotly_figure import plotly_table, Moving_average_forecast

# Configure the browser tab title, icon, and set the app to use the full width of the screen
st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)

# Display a large title at the top of the web page
st.title("Stock Prediction")

# Create three equal-width columns to organize the input fields horizontally
col1, col2, col3 = st.columns(3)

with col1:
    # Create a text input box where the user can type a stock symbol (default is 'AAPL')
    ticker = st.text_input('Stock Ticker', 'AAPL')

# Initialize the Root Mean Squared Error variable at 0
rmse = 0

# Display a sub-heading that updates dynamically based on the ticker entered
st.subheader('Predicting Next 30 days Close Price for: ' + ticker)

# --- Logic Execution Starts Here ---

# 1. Fetch the raw data for the entered ticker
close_price = get_data(ticker)

# 2. Calculate the 7-day moving average to smooth the data for the model
rolling_price = get_rolling_mean(close_price)

# 3. Find the differencing order (d) required to make the rolling data stationary
differencing_order = get_differencing_order(rolling_price)

# 4. Scale the data to a standard range (-3 to 3) and save the scaler for later use
scaled_data, scaler = scaling(rolling_price)

# 5. Calculate the error (RMSE) to show the user how reliable the current prediction is
rmse = evaluate_model(scaled_data, differencing_order)

# Display the Model's error score (RMSE) using bold Markdown text
st.write("**Model RMSE Score:**", rmse)

# 6. Generate the 30-day forecast using the scaled data and the calculated differencing order
forecast = get_forecast(scaled_data, differencing_order)

# 7. Convert the forecast prices from 'scaled' values back to 'actual' dollar values
forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

# Display a header for the data table
st.write('##### Forecast Data (Next 30 days)')

# 8. Create an interactive table using Plotly. 
# We sort the dates in order, round prices to 3 decimals, and set the table height.
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)

# Render the Plotly table in the Streamlit app, making it responsive to the container width
st.plotly_chart(fig_tail, use_container_width=True)

# 9. Combine the historical rolling price data with the new forecast data into one single DataFrame
forecast = pd.concat([rolling_price, forecast])

# 10. Generate and display the final trend chart. 
# .iloc[150:] is used to zoom in on the most recent data (starting from index 150) 
# so the chart isn't too crowded with old history.
st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)

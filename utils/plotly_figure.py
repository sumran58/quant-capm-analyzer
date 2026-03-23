import plotly.graph_objects as go
#import pandas_ta as pta
import datetime,dateutil

def plotly_table(dataframe):
    
    header_color = '#0078ff'
    row_even_color = '#f8fafd'
    row_odd_color = '#e1efff'
    
    fig = go.Figure(data=[go.Table(
        
        header=dict(
            values=["<b>Metric</b>", "<b>Value</b>"],
            fill_color=header_color,
            font=dict(color='white', size=14),
            align='center',
            height=35
        ),
        
        cells=dict(
            values=[
                dataframe.index,          # ✅ index as first column
                dataframe.iloc[:, 0]      # ✅ values column
            ],
            fill_color=[[row_odd_color, row_even_color] * len(dataframe)],
            align='left',
            font=dict(color='black', size=13)
        )
    )])
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def filter_data(dataframe, num_period):
    #dateutil.relativedelta: This library is used because it handles months and years perfectly (it knows which months have 30 vs 31 days).
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1).strftime('%Y-%m-%d')
    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def close_chart(dataframe, num_period=False):
    #num_period=False: This is a default argument. If you don't provide a period (like '1mo'), the chart shows all available data. If you do provide one, it triggers the filtering logic.
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    #When you call fig.add_trace(), you are telling Plotly: "Take this specific data and draw it on top of whatever is already in the frame."
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines', name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines', name='Low', line=dict(width=2, color='red')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff', legend=dict(yanchor="top", xanchor="right"))
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'], open=dataframe['Open'], high=dataframe['High'], low=dataframe['Low'], close=dataframe['Close']))
    fig.update_layout(showlegend=False, height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig

def RSI(dataframe, num_period):
    # Manual RSI Calculation (14 periods)
    delta = dataframe['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    dataframe['RSI'] = 100 - (100 / (1 + rs))
    
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe.RSI, name='RSI', marker_color='orange', line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe), name='Overbought', marker_color='red', line=dict(width=2, color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe), fill='tonexty', name='Oversold', marker_color='#79da84', line=dict(width=2, color='#79da84', dash='dash')))
    fig.update_layout(yaxis_range=[0, 100], height=200, plot_bgcolor='white', paper_bgcolor='#e1efff', margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1))
    return fig

def MACD(dataframe, num_period):
    # Manual MACD Calculation
    exp1 = dataframe['Close'].ewm(span=12, adjust=False).mean()
    exp2 = dataframe['Close'].ewm(span=26, adjust=False).mean()
    dataframe['MACD'] = exp1 - exp2
    dataframe['MACD Signal'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()
    dataframe['MACD Hist'] = dataframe['MACD'] - dataframe['MACD Signal']
    
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD'], name='MACD', marker_color='orange', line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD Signal'], name='Signal', marker_color='red', line=dict(width=2, color='red', dash='dash')))
    c = ['red' if cl < 0 else "green" for cl in dataframe['MACD Hist']]
    fig.add_trace(go.Bar(x=dataframe['Date'], y=dataframe['MACD Hist'], name='Histogram', marker_color=c))
    fig.update_layout(height=200, plot_bgcolor='white', paper_bgcolor='#e1efff', margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1))
    return fig

def Moving_average_forecast(forecast):
    """Creates a Plotly chart showing historical data and future predictions."""
    # 1. Initialize a Plotly Figure object
    fig = go.Figure()

    # 2. Add the 'Historical' line (the last 30 days of known data)
    # We use a black line to represent actual prices that have already happened
    fig.add_trace(go.Scatter(
        x=forecast.index[:-30],           # Dates up until the start of the forecast
        y=forecast['Close'].iloc[:-30],   # Historical prices
        mode='lines',                     # Connect points with a line
        name='Close Price',               # Label for the legend
        line=dict(width=2, color='black') # Line style: thin and black
    ))

    # 3. Add the 'Forecast' line (the predicted next 30 days)
    # We use a red line to visually distinguish the prediction from history
    # Note: index[-31:] is used to create a small overlap so the lines connect
    fig.add_trace(go.Scatter(
        x=forecast.index[-31:],           # The 30 future dates (plus one overlap)
        y=forecast['Close'].iloc[-31:],   # Predicted prices
        mode='lines',                     # Connect points with a line
        name='Future Close Price',        # Label for the legend
        line=dict(width=2, color='red')   # Line style: thin and red
    ))

    # 4. Add a 'Range Slider' at the bottom to allow zooming in/out of time periods
    fig.update_xaxes(rangeslider_visible=True)

    # 5. Customize the look: set height, margins, and background colors
    fig.update_layout(
        height=500, 
        margin=dict(l=0, r=20, t=20, b=0), 
        plot_bgcolor='white',             # White background for the plot area
        paper_bgcolor='#e1efff',          # Light blue background for the page
        legend=dict(
            yanchor="top",                # Position the legend box at the top
            y=1.02, 
            xanchor="right",              # Position the legend box on the right
            x=1
        )
    )

    # Return the completed figure to be displayed in Streamlit
    return fig
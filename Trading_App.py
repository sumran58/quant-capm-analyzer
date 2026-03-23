import streamlit as st
st.set_page_config(
    page_title="Trading App",
    page_icon="📈",
    layout="wide"
)
st.title("Trading guide App")
st.header("We provide the greatest platform for you to collect all information prior to investing in stocks")

st.markdown("### We provide the following services:")

st.markdown("### :one: Stock Information")
st.write("Through this page you will see all the information about the stocks")

st.markdown("### :two: Stock Prediction")
st.write("You can explore the predicted closing prices for the next 30 days based upon the historical stocks data and advanced forecasting model")

st.markdown("### :three: CAPM Return")
st.write("D9iscover how the Capital Asset Pricing Model calculate the expected return of different stock assets based on its risk")

st.markdown("### :four: CAPM Beta")
st.write("Calculate Beta and expected returns for individual Stocks ")

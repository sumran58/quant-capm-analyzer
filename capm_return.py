#importing all the libraraies

import streamlit as st
import pandas as pd
import yfinance as yf 
import datetime 
from datetime import date
from pandas_datareader import data as web
import capm_functions
from capm_functions import interactive_plot
from capm_functions import normalize

st.set_page_config(page_title="CAPM",
                   page_icon="📈",
                   layout='wide')
#set_page _config is the function provided by streamlit to set how the webpage is going to look . we can pass multiple parameters in it 
#layout wide means it is going to make use of entire page 
#capm title will appear at the browser tab and its icon will appear next to it instead of streamlit text and its icon 
st.title("Capital Asset Pricing Model")

#getting input from user
col1,col2=st.columns([1,1]) #ek he row me but different different columns
with col1:
    stocks_list=st.multiselect("Choose 4 stocks:",('TSLA','AMZN','AAPL','NFLX','MSFT','MGM','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
with col2:
    year=st.number_input("Number of years",1,10)

#downlading the data for S&P500
end = datetime.date.today()

start = datetime.date(
    datetime.date.today().year - year,
    datetime.date.today().month,
    datetime.date.today().day
)
SP500=web.DataReader(['sp500'],'fred',start,end) #contains market performance 
print(SP500.head())
stocks_df=pd.DataFrame() #contains individual stock performance 

for stock in stocks_list:
    data=yf.download(stock,period=f'{year}y')
    stocks_df[f'{stock}']=data['Close']
print(stocks_df.head())

#we need to merge the stocks_df and SP500 because we need to compare both 
stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
SP500.columns=['Date','sp500'] #renaming the sp500 column name to date and sp500 
stocks_df['Date']=stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date']=stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df['Date']=pd.to_datetime(stocks_df['Date'])
#its very important that we match both the date column from both the dataset so that merging wont fail 
stocks_df=pd.merge(stocks_df,SP500,on='Date',how='inner')
col1,col2=st.columns([1,1])
with col1:
    st.markdown("### DataFrame head")
    st.dataframe(stocks_df.head(),use_container_width=True)
with col2:
    st.markdown("### DataFrame tail")
    st.dataframe(stocks_df.tail(),use_container_width=True)

col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Price of all the stocks")
    st.plotly_chart(interactive_plot(stocks_df))
with col2:
    st.markdown("### Price of all the Stocks after Normalizing")
    normalized_df = normalize(stocks_df)
    st.plotly_chart(interactive_plot(normalized_df))

stocks_daily_return=capm_functions.daily_returns(stocks_df)
print(stocks_daily_return.head())

alpha={}
beta={}
for i in stocks_daily_return.columns:
    if i!='Date' and i !='sp500':
        b,a=capm_functions.calculate_beta(stocks_daily_return,i)

        beta[i]=b
        alpha[i]=a
print(alpha,beta)

beta_df=pd.DataFrame(columns=['stocks','Beta value'])
beta_df['stocks']=beta.keys()
beta_df['Beta value']=[str(round(i,2)) for i in beta.values()]

with col1:
    st.markdown("### Calculated beta value")
    st.dataframe(beta_df,use_container_width=True)

rf=0
rm=stocks_daily_return['sp500'].mean()*252

return_df=pd.DataFrame()
return_value=[]
for stock,value in beta.items():
    return_value.append(str(round(rf+(value*(rm-rf)),2)))
return_df['Stocks']=stocks_list
return_df['return_value']=return_value

with col2:
    st.markdown("### Calculated Return using CAPM")
    st.dataframe(return_df,use_container_width=True)

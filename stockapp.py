import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import time
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('S&P 500 Stocks Comparasion App')

st.markdown("""
This app retrieves the  basic list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit,  matplotlib
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
* **Author** [Aditya](https://www.linkedin.com/in/aditya-kanodia-755669131/)
""")

st.sidebar.header('Features')
@st.cache
def load_data():
	url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
	html = pd.read_html(url, header = 0)
	df = html[0]
	return df

df = load_data()



# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Please select Interested Sector', sorted_sector_unique)
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]



st.header('Display Companies in Selected Sector')
st.dataframe(df_selected_sector)
def filedownload(df):
	csv = df.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
	href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
	return href
st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

number=st.sidebar.multiselect("Select atleast 2 Companies from"+' '+str(len(df_selected_sector['Symbol'].unique()))+" "+'Companies',df_selected_sector['Symbol'].unique())

if len(number)>=2:
	data = yf.download(
		tickers = list(number),
		period = "ytd",
		interval = "1d",
		group_by = 'ticker',
		auto_adjust = True,
		prepost = True,
		threads = True,
		proxy = None
			)
	#st.write(data)



def plot(symbol):
	df = pd.DataFrame(data[symbol].Close)
	df['Date'] = df.index
	
	
	plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
	plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
	plt.xticks(rotation=90)
	plt.title(symbol, fontweight='bold')
	plt.xlabel('Date', fontweight='bold')
	plt.ylabel('Closing Price', fontweight='bold')
	return st.pyplot()
button=st.button("Show/Hide Plots")
if button :


	with st.spinner('Wait for it Plots are loading...'):
		time.sleep(5)
	st.snow()
if button:
    st.header("Stocks Closing Price of Companies")
    for i in number:
        plot(i)

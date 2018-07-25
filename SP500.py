import bs4 as bs
import datetime as dt 
import matplotlib.pyplot as plt 
from matplotlib import style
import numpy as np
import os 
import pandas as pd 
import pandas_datareader.data as web
import pickle
import requests
import time
import fix_yahoo_finance as yf

style.use('ggplot')

# saves all tickers onto a csv
def save_sp500_tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

	soup = bs.BeautifulSoup(resp.text, "lxml")
	table = soup.find('table', {'class':'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker)

	with open("sp500tickers.pickle", "wb") as f:
		pickle.dump(tickers, f)

	print(tickers)
	return tickers

# gets ticker data for each company from yahoo and saves it to csv
# 2 companies did not pass
def get_data_from_yahoo(reload_sp500=False):
	if reload_sp500:
		tickers = save_sp500_tickers()
	else:
		with open("sp500tickers.pickle", "rb") as f:
			tickers = pickle.load(f)

	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')

	start = dt.datetime(2010, 1, 1)
	end = dt.datetime.now()

	for ticker in tickers:
		print(ticker)
		if not os.path.exists('stock_dfs/{}.cvs'.format(ticker)):
			try:
				yf.pdr_override()
				# data = yf.download(ticker, start, end)
				df = web.get_data_yahoo(ticker, start, end)
				# df.reset_index(inplace=True)
				# df.set_index("Date", inplace=True)
				# df = df.drop("Symbol", axis=1)
				df.to_csv('stock_dfs/{}.csv'.format(ticker))
				time.sleep(0.5)
			except:
				pass


		else:
			print('Already have {}'.format(ticker))

# combines all the ticker data into one single dataframe
def compile_data():
	with open("sp500tickers.pickle", "rb") as f:
		tickers = pickle.load(f)

	main_df = pd.DataFrame()

	for count, ticker in enumerate(tickers):
		try:
			df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
			df.set_index('Date', inplace=True)

			df.rename(columns = {'Adj Close': ticker}, inplace=True)
			df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

			if main_df.empty:
				main_df = df
			else:
				main_df = main_df.join(df, how='outer')

			if count % 10 == 0:
				print(count)
		except:
			pass

	print(main_df.head())
	main_df.to_csv('sp500_joined_closes.csv')
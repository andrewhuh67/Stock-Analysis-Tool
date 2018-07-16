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
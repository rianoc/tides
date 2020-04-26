
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from config import URL
from config import LOCATION

html = requests.get(URL).text
data = BeautifulSoup(html, 'html.parser')

tab = (data.findAll("table", {"class": "vis3"}))[0]
df = (pd.read_html(str(tab)))[0]
df = df.rename(columns=df.iloc[0])
df = df.drop(0)
df = df.sort_values(by=['Hi/Lo'])
times = df['Time'].tolist()
heights = df['Height'].tolist()
heights = list(map(lambda x: x[:-1],heights))
labels = ['H1T','H2T','L1T','L2T','H1H','H2H','L1H','L2H']
info = times + heights
out = pd.DataFrame(list(zip(labels, info)),columns =['label', 'info']) 
out.to_csv(LOCATION+'\\tides.csv', index = False)


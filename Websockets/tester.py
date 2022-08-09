#!/usr/bin/env python
import random
import pandas as pd 
import numpy as np 
import pandas_datareader.data as web 
from datetime import datetime
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mplfinance as mpf

plt.style.use('fivethirtyeight')

fig = plt.figure(figsize=(16,8))
plt.xlabel('Time')
plt.ylabel('BTC Price')

def animate(i):
    df = pd.read_csv('./live-btc-data.csv')
    df.set_index('Minute',inplace=True)
    df.index = pd.to_datetime(df.index)
    plt.cla()
    plt.plot(df['Close'], color='orange')
    # creates new window every time
    # mpf.plot(axes, df, type='candle', style='yahoo')
    # mpf.plot()

# runs every 60 seconds
#ani = FuncAnimation(plt.gcf(), animate, interval=5000)

#esting plots
#df = pd.read_csv('./Archives/04-19-2020-btc.csv')
df = pd.read_csv('./Archives/04-23-2020-btc.csv')
df.set_index('Minute',inplace=True)
df.index = pd.to_datetime(df.index)
patDF = pd.read_csv('./Archives/04-23-2020-pattern-data.csv')
patDF.set_index('Time',inplace=True)
patDF.index = pd.to_datetime(patDF.index)
plt.plot(df['Close'], color='orange', lw=2)
# plot temporary df with indexes set 2 minutes earlier
plt.plot(patDF.set_index(patDF.index - pd.Timedelta(minutes=2))['Price'], color='black', marker='s',ls='None', markersize=6)
plt.plot(patDF.set_index(patDF.index - pd.Timedelta(minutes=2))['Profit'], color='green', marker='^',ls='None', markersize=4)
plt.plot(patDF.set_index(patDF.index - pd.Timedelta(minutes=2))['Loss'], color='red', marker='v',ls='None', markersize=4)
#mpf.plot(df, type='candle', style='yahoo')






#print('First Date for BTC data: {}'.format(df.loc[df.index >= datetime(2020,4,22,1,9)]['Close'].index[0]))
#print('First Date for pattern data: {}'.format(patDF['Price'].index[0]))
print(type(pd.to_datetime(patDF.index)[0]))

# plt.tight_layout()
plt.show()
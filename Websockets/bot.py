#!/usr/bin/env python
import websocket, json
import pandas as pd 
import numpy as np 
import pandas_datareader.data as web 
from datetime import datetime
import dateutil.parser


minutes_processed = {}
minute_candlesticks = []
current_tick = None
previous_tick = None
liveDF = None
patterns_found = []
pattern_added = False

def export_patterns():
    patternDF = pd.DataFrame(patterns_found)
    patternDF.set_index('Time',inplace=True)
    patternDF.index = pd.to_datetime(patternDF.index)

    #print(len(patternDF.index))
    patternDF.to_csv('./pattern-data.csv')

# creates a dataframe from minute_candlesticks dict array and exports to csv
def export_chart_data():
    liveDF = pd.DataFrame(minute_candlesticks)
    liveDF.set_index('Minute',inplace=True)
    liveDF.index = pd.to_datetime(liveDF.index)
    #change all numeric value strings to float
    for col in liveDF.columns:
        liveDF[col] = pd.to_numeric(liveDF[col])
    
    liveDF.to_csv('./live-btc-data.csv')


def on_open(ws):
    print('Opened Connection')

    sub_message = {
        'type': 'subscribe',
        'channels': [
            {
                'name': 'ticker',
                'product_ids': [
                    'BTC-USD'
                ]
            }
        ]
    }

    ws.send(json.dumps(sub_message))

def on_message(ws, message):
    global current_tick, previous_tick

    previous_tick = current_tick
    current_tick = json.loads(message)

    print('=== Recieved Tick ===')
    print('{} @ {}'.format(current_tick['time'], current_tick['price']))

    tick_datetime_object = dateutil.parser.parse(current_tick['time'])
    tick_dt = tick_datetime_object.strftime("%m/%d/%Y %H:%M")
    print(tick_dt)

    # if given minute not in minutes_processed, create new candlestick, plot last, and check for previous pattern
    # executes roughly once per minute
    if not tick_dt in minutes_processed:

        # if more than 3 candles, start checking for pattern
        if len(minute_candlesticks) > 3:
            print('== Checking 3 candlestick pattern ==')
            last_candle = minute_candlesticks[-2]
            middle_candle = minute_candlesticks[-3]
            first_candle = minute_candlesticks[-4]

            if last_candle['Close'] > middle_candle['Close'] and middle_candle['Close'] > first_candle['Close']:
                print('== 3 Consecutive green candles! ==')
                # TypeError exception cannot string - string
                distance = float(last_candle['Close']) - float(first_candle['Open'])
                print('Distance is {}'.format(distance))
                profit_price = float(last_candle['Close']) + (distance * 2)
                print('Taking profit at: {}'.format(profit_price))
                loss_price = float(first_candle['Open'])
                print('Selling for loss at: {}'.format(loss_price))

                # needs to be moved.. this is applied for every tick after pattern is found
                # if(!pattern_added)
                patterns_found.append({
                    'Time': tick_dt,
                    'Price': float(last_candle['Close']),
                    'Distance': distance,
                    'Profit': profit_price,
                    'Loss': loss_price
                })
                export_patterns()

        print('Starting new Candlestick')
        minutes_processed[tick_dt] = True
        print(minutes_processed)

        # add close price to last candlestick only if one exists
        if len(minute_candlesticks) > 0:
            minute_candlesticks[-1]['Close'] = previous_tick['price']
            export_chart_data()
            

        minute_candlesticks.append({
            'Minute': tick_dt,
            'Open': current_tick['price'],
            'High': current_tick['price'],
            'Low': current_tick['price']
        })

    # if candlestick has been created update candlestick values (high, low, etc.)
    if len(minute_candlesticks) > 0:
        current_candlestick = minute_candlesticks[-1]
        if current_tick['price'] > current_candlestick['High']:
            current_candlestick['High'] = current_tick['price']
        if current_tick['price'] < current_candlestick['Low']:
            current_candlestick['Low'] = current_tick['price']
        
    # print each created candlestick from list of minute candlesticks
    print('-- CandleSticks ==')
    for candlestick in minute_candlesticks:
        print(candlestick)


def on_close():
    print('Closing Connection')
    print('All recognized patterns:')
    for pattern in patterns_found:
        print(pattern)

socket = ('wss://ws-feed.pro.coinbase.com')
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()

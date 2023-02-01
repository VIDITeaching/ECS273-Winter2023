import pandas as pd
import numpy as np
import os
from pprint import pprint 

def processLineData():
    cur_path = os.path.dirname(__file__)
    data = pd.read_csv(cur_path + r'\\data\\all_data.csv')
    # convert datetime to hours (default conversion is to nanoseconds)
    data['hour'] = pd.to_datetime(data.datetime).values.astype(np.int64) // 10 ** 9 / 60 / 60
    # we have far too much data, so let's just get one data point per day
    data['filter_hour'] = pd.to_datetime(data.datetime).dt.hour
    data = data[(data.filter_hour== 12)]
    data.drop(columns=['datetime', 'filter_hour'], inplace=True)
    # pivot data so that it's in the structure we want
    piv_data = data.pivot(index='hour', columns='station', values='PM2.5')
    # take rolling average over 3 days
    piv_data = piv_data.rolling(window=3, center=True).mean()
    piv_data = piv_data.iloc[::4] # take out every fourth row
    piv_data.reset_index(inplace=True)
    piv_data.dropna(inplace=True)
    return piv_data.to_dict(orient='records'), list(piv_data.columns)


def processParallelData():
    cur_path = os.path.dirname(__file__)
    data = pd.read_csv(cur_path + r'\\data\\all_data.csv')
    # filter out data just to reduce amount
    data = data[data.station == "Aotizhongxin"]
    data['filter_hour'] = pd.to_datetime(data.datetime).dt.hour
    data = data[(data.filter_hour== 12)]
    data = data.iloc[::8]
    data.dropna(inplace=True)
    # get relevant columns and rename them
    data = data[['PM2.5', 'TEMP', 'PRES', 'WSPM']]
    data.rename(columns={'PM2.5':'PM 2.5', 'TEMP':"Temperature", 'PRES': "Pressure",  
                     'WSPM': "Windspeed"}, inplace=True)
    return data.to_dict(orient="records"), list(data.columns)

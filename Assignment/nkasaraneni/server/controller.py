import pandas as pd
import numpy as np
import os
from pprint import pprint 


def processStackedData():
    cur_path = os.path.dirname(__file__)
    data = pd.read_csv(cur_path + r'\\data\\all_data.csv')
    # convert datetime to hours (default conversion is to nanoseconds)
    data['hour'] = pd.to_datetime(data.datetime).values.astype(np.int64) // 10 ** 9 / 60 / 60
    data['filter_hour'] = pd.to_datetime(data.datetime).dt.hour
    data = data[(data.filter_hour== 12)]
    data.drop(columns=['datetime', 'filter_hour'], inplace=True)
    piv_data = data.pivot(index='hour', columns='station', values='PM2.5')
    piv_data = piv_data.iloc[::4]
    piv_data.reset_index(inplace=True)
    piv_data.dropna(inplace=True)
    return piv_data.to_dict(orient='records'), list(piv_data.columns)

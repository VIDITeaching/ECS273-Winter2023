import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from resources.hd_processing_template import perform_PCA, perform_TSNE
import datetime
#from resources.network_process_template import contsruct_networkx
#from resources.text_processing_template import preprocess
#from resources.time_processing_template import prepare_time_template_data, apply_arima, apply_sarima

def processTerrorismData(fromDate, toDate):
    input_file = "data/globalterrorismdb_0718dist.csv"
    # comma delimited is the default
    df = pd.read_csv(input_file, sep=',', header = 0, encoding='ISO-8859-1', quotechar='"').dropna(subset=['iyear', 'imonth', 'iday'])

    df = df.loc[(df['iyear'] >= 1990)
                        & (df['imonth'] >= 1)
                        & (df['imonth'] <= 12)
                        & (df['iday'] >= 1)
                        & (df['iday'] <= 31)
                        ]

    
    df['date'] = pd.to_datetime(dict(year=df.iyear, month=df.imonth, day=df.iday))

    filtered_df = df.loc[(df['date'] >= fromDate)
                        & (df['date'] < toDate)]
    
    print(str(len(df)) + " filtered to " + str(len(filtered_df)))
    print(filtered_df)
    return filtered_df

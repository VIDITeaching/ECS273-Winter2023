import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from resources.hd_processing_template import perform_PCA, perform_TSNE
#from resources.network_process_template import contsruct_networkx
#from resources.text_processing_template import preprocess
#from resources.time_processing_template import prepare_time_template_data, apply_arima, apply_sarima

def processExample():
    df = pd.read_csv('./data/test.csv', index_col=0)
    df = df.dropna()
    return df.to_dict(orient='records')


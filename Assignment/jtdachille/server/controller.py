import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from resources.hd_processing_template import perform_PCA, perform_TSNE
import requests
import io
#from resources.network_process_template import contsruct_networkx
#from resources.text_processing_template import preprocess
from resources.time_processing_template import prepare_time_template_data, apply_arima, apply_sarima, prepare_rent_data

def processExample(method: str = 'PCA') -> tuple[list[dict], list[int]]:
    data: dict = load_wine()
    X: np.ndarray = data.data
    y: np.ndarray = data.target
    #feat_names: np.ndarray = data.feature_names
    target_names: np.ndarray = data.target_names

    if method == 'PCA':
        Z, _ = perform_PCA(X)
    elif method == 't-SNE':
        Z = perform_TSNE(X, perplexity = 10)
    else:
        raise ValueError('Requested a method that is not supported')
    points = pd.DataFrame(Z, columns=['posX', 'posY'])
    points['cluster'] = y
    # How to JSON serialize pandas dataframes and numpy arrays
    return points.to_dict(orient='records'), list(target_names)

def remove_tabs(x):
    if type(x) == str:
        return x.replace("\t", "")
    else:
        return x
        
def processRent():
    url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-07-05/rent.csv'
    download = requests.get(url).content
    rent = pd.read_csv(io.StringIO(download.decode('utf-8')), parse_dates=["date"], date_parser=lambda x: pd.to_datetime(x, format="%Y%m%d"))
    rent_cropped = rent.head(100)
    return rent.to_dict()

def processTinyRent():
    if False:
        url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-07-05/rent.csv'
        download = requests.get(url).content
        rent = pd.read_csv(io.StringIO(download.decode('utf-8'))).applymap(remove_tabs)
        rent = rent.where(pd.notnull(rent), 0)
        rent_cropped = rent.head(100)
        return rent_cropped.to_dict(orient='records')
    else:
        df = prepare_rent_data().applymap(remove_tabs)
        df = df.where(pd.notnull(df), 0)
        ret = df.to_dict(orient='records')
        return ret
import pandas as pd
import numpy as np
from sklearn.datasets import load_linnerud
from resources.hd_processing_template import perform_PCA, perform_TSNE
import csv
#from resources.network_process_template import contsruct_networkx
#from resources.text_processing_template import preprocess, ShowWordCloud
#from resources.time_processing_template import prepare_time_template_data, apply_arima, apply_sarima

def processExample(method: str = 'PCA') -> tuple[list[dict], list[int]]:
    data: dict = load_linnerud()
    X: np.ndarray = data.data
    y: np.ndarray = data.target
    #feat_names: np.ndarray = data.feature_names
    target_names: np.ndarray = data.target_names

    if method == 'PCA':
        Z, _ = perform_PCA(X)
    elif method == 't-SNE':
        Z = perform_TSNE(X, perplexity = 10)
    else:
        raise ValueError("Requested a method that is not supported")
    points = pd.DataFrame(Z, columns=['posX', 'posY'])
    points['cluster'] = y
    # How to JSON serialize pandas dataframes and numpy arrays
    return points.to_dict(orient='records'), list(target_names)

def read_CSVfile():
    president_test = []
    with open("/Users/ginnyhuang/Documents/ECS273-Winter2023/Assignment/Vue-Flask-Template/server/data/us_election_2020.csv") as csv_read_file:
            csv_read_data = csv.reader(csv_read_file)
            for row in csv_read_data:
                president_test.append(row)
    return president_test



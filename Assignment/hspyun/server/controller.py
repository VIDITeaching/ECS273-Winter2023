import pandas as pd
import numpy as np
from resources.hd_processing_template import perform_PCA, perform_TSNE
#from resources.network_process_template import contsruct_networkx
#from resources.text_processing_template import preprocess
#from resources.time_processing_template import prepare_time_template_data, apply_arima, apply_sarima
#from resources.load_bean import load_bean

def read_bean(csv_path="../server/data/Dry_Bean_Dataset.csv"):
    df = pd.read_csv(csv_path)
    data = df.drop(columns='Class').values
    labels = df['Class']

    X: np.ndarray = data
    y: np.ndarray = labels
    target_names = labels.drop_duplicates()
    return X, y, target_names, df  

def processExample(csv_path = "../server/data/Dry_Bean_Dataset.csv", 
                    method: str = 'PCA') -> tuple[list[dict], list[int]]:
    X, y, target_names, _ = read_bean(csv_path)

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


# For debug
if __name__ == "__main__":
    processExample(csv_path="Assignment/hspyun/server/data/Dry_Bean_Dataset.csv")
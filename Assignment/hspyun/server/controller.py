import pandas as pd
import numpy as np
from resources.hd_processing_template import perform_PCA, perform_TSNE
from resources.my_processing import perform_Histogram, perform_CorrMat
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

def processBeanHist(csv_path = "../server/data/Dry_Bean_Dataset.csv", 
                    feature: str = 'Area') -> tuple[list[dict], list[int]]:
    X, y, target_names, df = read_bean(csv_path)

    # Histogram
    X_feature = df[feature].to_numpy()
    arr, new_y = perform_Histogram(X_feature,y,target_names)
    points = pd.DataFrame(arr.T, columns=['posX','posY'])
    points['cluster'] = new_y

    # How to JSON serialize pandas dataframes and numpy arrays
    return points.to_dict(orient='records'), list(target_names)


def processBeanCorrMat(csv_path = "../server/data/Dry_Bean_Dataset.csv", 
                    feature: str = 'Area') -> tuple[list[dict], list[int]]:
    X, y, target_names, df = read_bean(csv_path)
    
    # Corr mat
    
    X_feature = df.drop(columns='Class').values
    arr, corr = perform_CorrMat(X_feature,y,target_names)
    points = pd.DataFrame(arr.T, columns=['posX','posY'])
    points['corr'] = corr

    # How to JSON serialize pandas dataframes and numpy arrays
    return points.to_dict(orient='records'), list(target_names)



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
    #processExample(csv_path="Assignment/hspyun/server/data/Dry_Bean_Dataset.csv")
    #processBeanHist(csv_path="Assignment/hspyun/server/data/Dry_Bean_Dataset.csv")
    processBeanCorrMat(csv_path="Assignment/hspyun/server/data/Dry_Bean_Dataset.csv")
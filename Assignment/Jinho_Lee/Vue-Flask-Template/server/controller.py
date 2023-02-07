import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from resources.hd_processing_template import perform_PCA, perform_TSNE, perform_UMAP
#from resources.network_process_template import contsruct_networkx
#from resources.text_processing_template import preprocess
#from resources.time_processing_template import prepare_time_template_data, apply_arima, apply_sarima

'''
# ====================== Original Homework Code ======================
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
        raise ValueError("Requested a method that is not supported")
    points = pd.DataFrame(Z, columns=['posX', 'posY'])
    points['cluster'] = y
    # How to JSON serialize pandas dataframes and numpy arrays
    return points.to_dict(orient='records'), list(target_names)
# ====================== Original Homework Code ======================
'''

# ====================== Homework Code for Dry bean ======================
def processExample(method: str = 'scatter'):
#def processExample(method):
    data = []
    # df = pd.read_csv('../server/data/Dry_Bean_Dataset_short.csv')
    df = pd.read_csv('../server/data/Dry_Bean_Dataset.csv')
    df = df.drop_duplicates()

    if method == 'scatter': # scatter
        df = df[["Area", "AspectRation", "Compactness", "ConvexArea", "Class"]]
        # dirpath = '../dashboard'
        # filepath = '/public/dry_bean_short.csv'
        # df.to_csv(dirpath+filepath, index=False)
    elif method == 'parallel':
        df = df[["Eccentricity", "ConvexArea", "EquivDiameter", "Extent", "Class"]]
    else:
        data = df.drop(columns='Class').values

    labels = df['Class']

    X: np.ndarray = data
    y: np.ndarray = labels

    if method == 'PCA':
        Z, _ = perform_PCA(X)
    
    elif method == 't-SNE':
        Z = perform_TSNE(X, perplexity = 50)
    
    elif method == 'UMAP':
        Z = perform_UMAP(X, y)
    
    elif method == 'scatter': #scatter plot matrix
        res_data = pd.DataFrame(data=df)
        # filepath = '/public/dry_bean_short.csv'
        return res_data.to_dict(orient='records'), list(y.drop_duplicates()), df.columns.tolist() #return early
    
    else: # parallel matrix
        res_data = pd.DataFrame(data=df)
        return res_data.to_dict(orient='records'), list(y.drop_duplicates()), df.columns.tolist() #return early

    if method == 'PCA':
        points = pd.DataFrame(Z, columns=['posX', 'posY'])
        points['cluster'] = y
        return points.to_dict(orient='records'), list(y.drop_duplicates()), df.columns.tolist()
    else:
        tsne_data_lab = np.vstack((Z.T, y)).T
        points = pd.DataFrame(data=tsne_data_lab, columns=['posX', 'posY', "cluster"])
        return points.to_dict(orient='records'), list(y.drop_duplicates()),  df.columns.tolist()
# ====================== Homework Code for Dry bean ======================

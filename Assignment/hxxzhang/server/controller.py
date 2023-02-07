import pandas as pd
import numpy as np
from resources.hd_processing_template import perform_PCA, perform_TSNE


def getPie():
    data = pd.read_excel('../server/data/Dry_Bean_Dataset.xlsx')
    ans = []
    for i in data['Class'].unique():
        ans.append({
            'name': i,
            'value': (data['Class'] == i).sum().astype(float)
        })
    return ans


def processExample(method: str = '20'):  # get paramater perplexity
    data = pd.read_excel('../server/data/Dry_Bean_Dataset.xlsx')
    X: np.ndarray = data[[
        'Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength',
        'AspectRation', 'Eccentricity', 'ConvexArea', 'EquivDiameter',
        'Extent', 'Solidity', 'roundness', 'Compactness', 'ShapeFactor1',
        'ShapeFactor2', 'ShapeFactor3', 'ShapeFactor4'
    ]]
    y: np.ndarray = data['Class']
    #feat_names: np.ndarray = data.feature_names
    target_names: np.ndarray = data['Class'].unique()
    if method == 'PCA':
        Z, _ = perform_PCA(X)
    elif method == 't-SNE':
        Z = perform_TSNE(X, perplexity=20)
    else:
        Z = perform_TSNE(X, perplexity=int(method))
        # raise ValueError("Requested a method that is not supported")
    points = pd.DataFrame(Z, columns=['posX', 'posY'])
    points['cluster'] = y
    # How to JSON serialize pandas dataframes and numpy arrays
    return points.to_dict(orient='records'), list(target_names)
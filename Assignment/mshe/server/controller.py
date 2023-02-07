import pandas as pd
import numpy as np
from resources.hd_processing_template import perform_PCA, perform_TSNE

def load_data() :
    df = pd.read_excel('data/DryBeanDataset/Dry_Bean_Dataset.xlsx')
    return df

def generateBarPlotData() -> tuple[list[str], list[float]]:
    df = load_data()
    avg_area_of_beans = df.groupby('Class')['Area'].mean()
    class_names: list[str] = []
    for n in avg_area_of_beans.axes[0].values:
        class_names.append(n)
    avg_areas: list[float] = []
    for a in avg_area_of_beans.values:
        avg_areas.append(a)
    return class_names, avg_areas

def generateScatterPlotData(method: str = 'PCA') -> tuple[list[dict], list[int]]:
    df = load_data()
    data: np.ndarray = df.values
    classes = df.Class.values
    class_names: list = []
    class_dict: dict = {}
    for c in classes:
        if c not in class_names:
            class_names.append(c)
    i = 0
    for c in class_names:
        class_dict[c] = i
        i = i + 1
    for d in data:
        class_name = d[16]
        d[16] = class_dict[class_name]
    if method == 'PCA':
        Z, _ = perform_PCA(data)
    elif method == 't-SNE':
        Z = perform_TSNE(data, perplexity=10)
    else:
        raise ValueError("Requested a method that is not supported")
    points = pd.DataFrame(Z, columns=['posX', 'posY'])
    points['cluster'] = classes
    return points.to_dict(orient='records'), class_names
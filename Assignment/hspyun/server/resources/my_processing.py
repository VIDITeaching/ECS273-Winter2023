from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn import preprocessing
import numpy as np

def perform_Histogram(X: np.ndarray, y:np.ndarray, taget_names:np.ndarray, num_bins=50) -> tuple[np.ndarray, np.ndarray]:
    freq_all = []
    edge_all = []
    cluster_all = []

    # Iterate along targets
    for target in taget_names:
        #print(target)
        data = [x for i, x in enumerate(X) if y[i] == target]
        #print(data)

        freq, edge = np.histogram(data,bins=num_bins)
        edge_middle = np.zeros(len(freq))
        for i in range(len(edge_middle)):
            edge_middle[i] = (edge[i] + edge[i+1])/2
        
        freq_all += list(freq)
        edge_all += list(edge_middle)
        cluster_all += [target for i in range(len(list(edge_middle)))]

    hist_all = np.vstack([edge_all,freq_all])

    return hist_all, cluster_all

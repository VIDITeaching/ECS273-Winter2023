import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from resources.hd_processing_template import perform_PCA, perform_TSNE
import csv
import numpy as np
#from resources.network_process_template import contsruct_networkx
#from resources.text_processing_template import preprocess
#from resources.time_processing_template import prepare_time_template_data, apply_arima, apply_sarima

twitchEdge_filename = "../server/data/large_twitch_edges.csv"
twitchFeat_filename = "../server/data/large_twitch_features.csv"
twitch_globalReadCount = False

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

def processTwitchEdge(set, id):
    node = set
    link = id
    note = "ego info"
    return node, link, note

def processTwitchFeat():
    # return ["nodes"], ["links"], ["links_sets"], ["coor_keys"]
    # if not twitch_globalReadCount:
    # read feature from csv
    twitchFeat = {"views": [], "life_time": [], "numeric_id": [], "language": []}
    line_count = -1
    coor_keys = ["language", "view_count", "account_life"]
    uniq_lang = ['DA', 'HU', 'NO'] # the least 3 language.
    uniq_view = ["#view_high", "#view_medium", "#view_low"]
    uniq_life = ["#life_high", "#life_medium", "#life_low"]
    with open(twitchFeat_filename,'r') as data:
        for line in csv.reader(data):
            if line_count < 0:  
                line_count += 1
                continue
            if str(line[7]) not in uniq_lang:
                continue
            twitchFeat["views"].append(int(line[0]))
            twitchFeat["life_time"].append(int(line[2]))
            twitchFeat["numeric_id"].append(int(line[5]))
            twitchFeat["language"].append(str(line[7]))
    
    # construct graph for parallel set chart
    nodes = []
    links = []
    links_sets = []
    max_view = np.max(twitchFeat["views"])
    min_view = np.min(twitchFeat["views"])
    gap_view = float((max_view-min_view)/3)
    value_view = [max_view, max_view-gap_view, min_view+gap_view, min_view-1]
    max_life = np.max(twitchFeat["life_time"])
    min_life = np.min(twitchFeat["life_time"])
    gap_life = float((max_life-min_life)/3)
    value_life = [max_life, max_life-gap_life, min_life+gap_life, min_life-1]
    # uniq_lang = list(np.unique(np.array(twitchFeat["language"])))
    # count_lan = np.zeros((len(uniq_lang)))

    # create sets for all coordinates
    for i in range(len(uniq_lang)):
        nodes.append({"name": uniq_lang[i]})
    for i in range(len(uniq_view)):
        nodes.append({"name": uniq_view[i]})
    for i in range(len(uniq_life)):
        nodes.append({"name": uniq_life[i]})

    # create all combinations between coordinates
    combination_count = 0
    for i in range(len(uniq_lang)):
        for j in range(len(uniq_view)):
            links.append({"source": i, "target": j+len(uniq_lang), "names": [uniq_lang[i], uniq_view[j]], "value": 0})
            links_sets.append([])
            for m in range(len(twitchFeat["numeric_id"])):
                if twitchFeat["language"][m] == uniq_lang[i] and twitchFeat["views"][m] <= value_view[j] and twitchFeat["views"][m] > value_view[j+1]:
                    links[combination_count]["value"] += 1
                    links_sets[combination_count].append(twitchFeat["numeric_id"][m])
            combination_count += 1

    for j in range(len(uniq_view)):
        for k in range(len(uniq_life)):
            links.append({"source": j+len(uniq_lang), "target": k+len(uniq_lang)+len(uniq_view), "names": [uniq_view[j], uniq_life[k]], "value": 0})
            links_sets.append([])
            for m in range(len(twitchFeat["numeric_id"])):
                if twitchFeat["views"][m] <= value_view[j] and twitchFeat["views"][m] > value_view[j+1] and twitchFeat["life_time"][m] <= value_life[k] and twitchFeat["life_time"][m] > value_life[k+1]:
                    links[combination_count]["value"] += 1
                    links_sets[combination_count].append(twitchFeat["numeric_id"][m])
            combination_count += 1

    return nodes, links, links_sets, coor_keys

# N, L, S = processTwitchFeat()
# print(N, L, S)

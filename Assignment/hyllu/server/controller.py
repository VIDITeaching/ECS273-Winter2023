import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from resources.hd_processing_template import perform_PCA, perform_TSNE
import csv
import numpy as np
from resources.network_process_template import contsruct_networkx, find_most_influential, force_layout
#from resources.text_processing_template import preprocess
#from resources.time_processing_template import prepare_time_template_data, apply_arima, apply_sarima

twitchEdge_filename = "../server/data/small_twitch_edges.csv"
twitchFeat_filename = "../server/data/small_twitch_features.csv"
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
    # node = set
    # link = id
    # note = "ego info"

    # find intersection of ids, if mutual exclusive, no nodes will be shown
    intersection_id = np.zeros((10000))
    if len(set) > 1:
        for i in range(len(set)):
            for j in range(len(set)-i-1):
                # print(i, j+i+1)
                intersection_id_tmp = np.intersect1d(np.array(id[i]), np.array(id[j+1+i]))
                if intersection_id_tmp.shape[0] < intersection_id.shape[0]:
                    intersection_id = intersection_id_tmp
    # print(intersection_id)
    # print(tuple(intersection_id))

    if intersection_id.shape[0] == 0:
        return [], [], [], "No intersection of players in the selected sets."
    if len(set) == 0:
        return [], [], [], "No set selected."
    if len(set) == 1:
        intersection_id = id[0]

    # read edge from csv
    twitchEdge = []
    twitchEdge_tmp = []
    line_count = -1
    intersection_id = list(intersection_id)
    for i in range(len(intersection_id)):
        intersection_id[i] = int(intersection_id[i])
    with open(twitchEdge_filename,'r') as data:
        for line in csv.reader(data):
            if line_count < 0:  
                line_count += 1
                continue
            if (int(line[0]) in intersection_id) and (int(line[1]) in intersection_id):
                twitchEdge.append(tuple([int(line[0]), int(line[1])]))
                twitchEdge_tmp.append([int(np.where(np.array(intersection_id)==int(line[0]))[0][0]), int(np.where(np.array(intersection_id)==int(line[1]))[0][0])])

    netG = contsruct_networkx(nodes=intersection_id, edges=twitchEdge)
    # eigen = find_most_influential(netG)
    posG = force_layout(netG)
    note = "dummy note"

    # return node, link, pos, note
    # return intersection_id, twitchEdge_tmp, posG, note
    # print(intersection_id, twitchEdge_tmp, posG, note)
    return intersection_id, twitchEdge_tmp, posG, note

# processTwitchEdge([0, 1, 2], [[5, 6, 7], [5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6]])

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
    # save_ids = []
    # csvfile = open(feat_save, 'w')
    # csvwriter = csv.writer(csvfile) 
    with open(twitchFeat_filename,'r') as data:
        for line in csv.reader(data):
            # row = []
            # for i in range(len(line)):
            #     row.append(line[i])
            if line_count < 0:  
                line_count += 1
                # csvwriter.writerow(row)
                continue
            if str(line[7]) not in uniq_lang:
                continue
            # csvwriter.writerow(row)
            # save_ids.append(int(line[5]))
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
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from sklearn.decomposition import PCA
from sklearn import preprocessing
import numpy as np
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)
data_location = "../server/data/Dry_Bean_Dataset.xlsx"

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/fetchScatter")
@cross_origin()

def fetchScatter(): # handling GET request
    raw_data = pd.read_excel(data_location)
    X = raw_data.loc[:, raw_data.columns[:-1]].to_numpy()
    targets = list(raw_data.Class)
    target_names = list(set(targets))

    scaler = preprocessing.StandardScaler()
    _X = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    pca.fit(_X)  
    Z = pca.transform(_X) 
    
    P = pd.DataFrame(Z, columns=['posX', 'posY'])
    P['cluster'] = np.array(map(lambda x: target_names.index(x), targets))

    points = P.to_dict(orient='records') 
    resp = jsonify(data=points, clusters=target_names)
    return resp

@app.route("/fetchRaw")
@cross_origin()

def fetchRaw():
    raw_data = pd.read_excel(data_location)
    raw_data = raw_data.sample(1000)
    attrs = list(raw_data.columns)
    d = raw_data.loc[:, attrs[:-1]]
    targets = list(raw_data.Class)
    target_names = list(set(targets))
    d['Class'] = np.array(map(lambda x: target_names.index(x), targets))
    data = d.to_dict(orient='records')

    resp = jsonify(data=data, dimensions=attrs, clusters=target_names)
    return resp

if __name__ == "__main__":
    app.run(port=3100, debug=True)
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processExample, read_bean, processBeanHist, processBeanCorrMat
import sys
import pandas as pd
import numpy as np
app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/fetchExample", methods=["GET", "POST"])
@cross_origin()
def fetchExample():
    if request.method == "GET": # handling GET request
        points, cluster_names = processExample()
        resp = jsonify(data=points, clusters=cluster_names)
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        request_context = request.get_json() # JSON object
        method = request_context['method']
        points, cluster_names = processExample(method)
        resp = jsonify(data=points, clusters=cluster_names)
        return resp

@app.route("/fetchData", methods=["GET", "POST"])
@cross_origin()
def fetchData():
    if request.method == "GET": # handling GET request
        points, cluster_names = processBeanHist()
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        request_context = request.get_json() # JSON object
        method = request_context['method']
        points, cluster_names = processBeanHist(feature=method)

    resp = jsonify(data=points, clusters=cluster_names)
    return resp

@app.route("/fetchCorrMat", methods=["GET", "POST"])
@cross_origin()
def fetchCorrMat():
    if request.method == "GET": # handling GET request
        points, cluster_names = processBeanCorrMat()
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        request_context = request.get_json() # JSON object
        method = request_context['method']
        points, cluster_names = processBeanCorrMat(feature=method)

    resp = jsonify(data=points, clusters=cluster_names)
    return resp

if __name__ == "__main__":
    if 0:
        # Debug
        _, y, target_names, df = read_bean("Assignment/hspyun/server/data/Dry_Bean_Dataset.csv")
        #resp = jsonify(data=points.to_dict(orient='records'))
        indexes = list(range(len(df['Area'])))
        arr = np.array([indexes, list(df['Area'].to_numpy())])


    app.run(port=3100, debug=True)
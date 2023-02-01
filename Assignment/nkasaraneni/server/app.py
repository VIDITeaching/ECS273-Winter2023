from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processLineData, processParallelData
import json 

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Testing</p>"


@app.route("/fetchLineData", methods=["GET", "POST"])
@cross_origin()
def fetchLineData():
    if request.method == "GET": # handling GET request
        data, columns = processLineData()
        resp = jsonify(data=data, columns=columns)
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        pass


@app.route("/fetchParallelData", methods=["GET", "POST"])
@cross_origin()
def fetchParallelData():
    if request.method == "GET": # handling GET request
        data, columns = processParallelData()
        resp = jsonify(data=data, columns=columns)
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        pass


if __name__ == "__main__":
    app.run(port=3100, debug=True)
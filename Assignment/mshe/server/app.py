from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import generateBarPlotData, generateScatterPlotData

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/fetchBarPlotData")
@cross_origin()
def fetchBarPlotData():
    class_names, avg_areas = generateBarPlotData()
    resp = jsonify(avg_areas=avg_areas, class_names=class_names)
    return resp

@app.route("/fetchScatterPlotData", methods=["GET", "POST"])
@cross_origin()
def fetchScatterPlotData():
    if request.method == "GET":  # handling GET request
        points, cluster_names = generateScatterPlotData()
        resp = jsonify(data=points, clusters=cluster_names)
        return resp
    else:  # handling POST request
        request_context = request.get_json()  # JSON object
        method = request_context['method']
        points, cluster_names = generateScatterPlotData(method)
        resp = jsonify(data=points, clusters=cluster_names)
        return resp

if __name__ == "__main__":
    app.run(port=3100, debug=True)
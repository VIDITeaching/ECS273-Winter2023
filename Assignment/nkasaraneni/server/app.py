from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processStackedData
import json 

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Testing</p>"


@app.route("/fetchStackedData", methods=["GET", "POST"])
@cross_origin()
def fetchStackedData():
    if request.method == "GET": # handling GET request
        data, columns = processStackedData()
        resp = jsonify(data=data, columns=columns)
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        pass
    #     request_context = request.get_json() # JSON object
    #     method = request_context['method']
    #     points, cluster_names = processExample(method)
    #     resp = jsonify(data=points, clusters=cluster_names)
    #     return resp


if __name__ == "__main__":
    app.run(port=3100, debug=True)
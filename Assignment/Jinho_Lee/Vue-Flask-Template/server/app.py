from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processExample
import csv

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
        print('GET===========================')
        points, cluster_names, columns = processExample(method='plain')
        print('plain this side')
        resp = jsonify(data=points, clusters=cluster_names, columns=columns)

        return resp

    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        print('POST===========================')
        request_context = request.get_json() # JSON object
        print(request_context)
        method = request_context['method']
        print(method)

        points, cluster_names, columns = processExample(method)
        resp = jsonify(data=points, clusters=cluster_names, columns=columns)
        return resp


if __name__ == "__main__":
    app.run(port=3100, debug=True)
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from controller import processExample
import csv
import os
import io
import json
import pandas as pd

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


@app.route("/fetchRent", methods=["GET", "POST"])
@cross_origin()
def fetchRent():
    data = []
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    csv_url = os.path.join(SITE_ROOT, "data/SF-Rentals/rent_subset_full.csv")
    
    with open(csv_url) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Iterate through the items in the row and cast them to float if they're numeric
            for key, value in row.items():
                try:
                    row[key] = float(value)
                except ValueError:
                    pass
            data.append(row)
    return jsonify(data)

@app.route("/fetchOther", methods=["GET", "POST"])
@cross_origin()
def fetchOther():
    data = []
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data/data.json")
    with open(json_url) as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route("/fetchHousing", methods=["GET", "POST"])
@cross_origin()
def fetchRents():
    data = []
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    csv_url = os.path.join(SITE_ROOT, "data/rents.csv")
    with open(csv_url) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # # Iterate through the items in the row and cast them to float if they're numeric
            # for key, value in row.items():
            #     try:
            #         row[key] = float(value)
            #     except ValueError:
            #         pass
            data.append(row)
    si = io.StringIO()
    cw = csv.DictWriter(si, fieldnames=data[0].keys())
    cw.writeheader()
    cw.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-type"] = "text/plain"
    return output

@app.route("/fetchCitiesWithCoords", methods=["GET", "POST"])
@cross_origin()
def fetchCitiesWithCoords():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data/citiesWithCoords2.json")
    with open(json_url) as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route("/fetchMap", methods=["GET", "POST"])
@cross_origin()
def fetchMap():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data/map/states-albers-10m.json")
    with open(json_url) as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route("/fun", methods=["GET", "POST"])
@cross_origin()
def go():
    return "<p>Hello, World!</p>"




if __name__ == "__main__":
    app.run(port=3100, debug=True)
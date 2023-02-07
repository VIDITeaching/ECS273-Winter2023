from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processExample
import csv
from collections import defaultdict

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/fetchExample", methods=["GET", "POST"])
@cross_origin()
def fetchExample():
    labels, monthCount, countryName, countryCount, countryCountSuccess = getData()
    if request.method == "GET": # handling GET request
        resp = jsonify(labels = labels, monthCount = monthCount, countryName = countryName, countryCount = countryCount, countryCountSuccess = countryCountSuccess)
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        request_context = request.get_json() # JSON object
        method = request_context['method']
        resp = jsonify(labels = labels, monthCount = monthCount, countryName = countryName, countryCount = countryCount, countryCountSuccess = countryCountSuccess)
        return resp

def getData():
    with open("../server/data/globalterrorismdb_0718dist.csv", encoding = "ISO-8859-1") as csvfile:
        reader = csv.DictReader(csvfile)
        
        # For Line Chart
        year = []
        monthDict = defaultdict(int)
        monthCountDict = defaultdict(int)
        monthCount = []

        # For Radar Chart
        country = defaultdict(int)
        countryName = []
        countryCount = []
        countrySuccess = defaultdict(int)
        countryCountSuccess = []
        
        for row in reader:
            monthDict[row['iyear']] += int(row['imonth'])
            monthCountDict[row['iyear']] += 1
            country[row['region_txt']] += 1
            if row['success'] == "1":
                countrySuccess[row['region_txt']] += 1
            else:
                countrySuccess[row['region_txt']] += 0

        for y in monthDict:
            monthDict[y] = monthDict[y] / monthCountDict[y]
            year.append(y)
            monthCount.append(monthDict[y])

        for c in country:
            countryName.append(c)
            countryCount.append(country[c])
            countryCountSuccess.append(countrySuccess[c])

        return year, monthCount, countryName, countryCount, countryCountSuccess


if __name__ == "__main__":
    app.run(port=3100, debug=True)
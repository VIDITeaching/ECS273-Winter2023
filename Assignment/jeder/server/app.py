from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processTerrorismData
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/fetchTerrorismData", methods=["GET", "POST"])
@cross_origin()
def fetchTerrorismData():
    fromDate = request.json.get('fromDate')
    fromDate = datetime.strptime(fromDate, '%Y-%m-%dT%H:%M:%S.%fZ')

    toDate = request.json.get('toDate')
    toDate = datetime.strptime(toDate, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    print("from " + str(fromDate) + " to " + str(toDate))
    
    if request.method == "GET": # handling GET request
        terrorism_data = processTerrorismData(fromDate, toDate)
        resp = terrorism_data.to_json(orient='records') #pandas DataFrame to JSON
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        terrorism_data = processTerrorismData(fromDate, toDate)
        resp = terrorism_data.to_json(orient='records') #pandas DataFrame to JSON
        return resp


if __name__ == "__main__":
    app.run(port=3100, debug=True)
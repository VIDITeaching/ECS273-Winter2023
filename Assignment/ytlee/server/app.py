from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import DataManager

app = Flask(__name__)
CORS(app)
dataManager = DataManager()

@app.route("/fetchData")
def fetchData():
    attacks_groupby_region, metadata = dataManager.get_processed_data()
    resp = jsonify(data=attacks_groupby_region, metadata=metadata)
    return resp


if __name__ == "__main__":
    app.run(port=5001, debug=True)
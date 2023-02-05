from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import process
import json
from pathlib import Path
import zipfile
import sys
import urllib.request

app = Flask(__name__)
CORS(app)


@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello World</p>"


@app.route("/fetchExample", methods=["GET", "POST"])
@cross_origin()
def fetchExample():
    titlesFile = open(titlesPath, "r")
    publishTimeFile = open(publishTimePath, "r")

    titlesJson = json.load(titlesFile)
    publishTimeJson = json.load(publishTimeFile)

    resp = jsonify(titles=titlesJson, publishTime=publishTimeJson)

    return resp


if __name__ == "__main__":
    zippedDatasetPath = Path("../server/data/COVID-19.csv.zip")
    datasetPath = Path("../server/data/COVID-19.csv")

    if not zippedDatasetPath.is_file():
        # Download COVID-19 dataset manually as it is too large (1.65 GB) for GitHub
        print('Download COVID-19 dataset manually as it is too large (1.65 GB) for GitHub', file=sys.stderr)
        print('File downloading', file=sys.stderr)
        urllib.request.urlretrieve(
            "https://github.com/tobyyu007/ECS273-Assignment-1/raw/main/server/data/COVID-19.csv.zip",
            "../server/data/COVID-19.csv.zip")

    if not datasetPath.is_file():
        print('Dataset unzipping', file=sys.stderr)
        with zipfile.ZipFile("../server/data/COVID-19.csv.zip", "r") as zip_ref:
            zip_ref.extractall("../server/data")

    titlesPath = Path("../server/data/titles.json")
    publishTimePath = Path("../server/data/publishTime.json")

    if not titlesPath.is_file() or not publishTimePath.is_file():
        print('data not found, start processing data', file=sys.stderr)
        process(str(titlesPath), str(publishTimePath))

    app.run(port=3100)

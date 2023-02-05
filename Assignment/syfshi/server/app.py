from flask import Flask, jsonify, request,json
from flask_cors import CORS, cross_origin
from controller import processExample
from resources.image_fashionMnist import clustering_fashion_mnist, process_mnist

app = Flask(__name__)
CORS(app)


@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/fetchExample", methods=["GET", "POST"])
@cross_origin()
def fetchExample():
    if request.method == "GET":  # handling GET request
        # points, cluster_names = processExample()
        points, cluster_names = clustering_fashion_mnist()
        resp = jsonify(data=points, clusters=cluster_names)
        return resp


@app.route("/svmGamma/<gamma>", methods=["GET", "POST"])
@cross_origin()
def svm_gamma(gamma):
    # request_context = request.get_json()  # JSON object
    # method = request_context['gamma']
    data_dict, labels = process_mnist(float(gamma))

    resp = jsonify(data=data_dict, clusters=labels)
    return resp


if __name__ == "__main__":
    app.run(port=3100, debug=True)

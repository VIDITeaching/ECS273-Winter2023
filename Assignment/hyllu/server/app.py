from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processExample, processTwitchFeat, processTwitchEdge

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

@app.route("/fetchTwitch", methods=["GET", "POST"])
@cross_origin()
def fetchTwitch():
    if request.method == "GET": # handling GET request
        nodes, links, link_set, coors = processTwitchFeat()
        resp = jsonify(nodes=nodes, links=links, link_set=link_set, coors=coors)
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        request_context = request.get_json() # JSON object
        set = request_context['set']
        id = request_context['id']
        nodes, links, positions, notes = processTwitchEdge(set, id)
        resp = jsonify(nodes=nodes, links=links, positions=positions, notes=notes)
        return resp


if __name__ == "__main__":
    app.run(port=3100, debug=True)
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processExample, processRent, processTinyRent

app = Flask(__name__)
CORS(app)

@app.route('/')
@cross_origin()
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/fetchExample', methods=['GET', 'POST'])
@cross_origin()
def fetchExample():
    if request.method == 'GET': # handling GET request
        points, cluster_names = processExample()
        resp = jsonify(data=points, clusters=cluster_names)
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        request_context = request.get_json() # JSON object
        method = request_context['method']
        points, cluster_names = processExample(method)
        resp = jsonify(data=points, clusters=cluster_names)
        return resp

@app.route('/fetchRent', methods=['GET'])
@cross_origin()
def fetchRent():
    if request.method == 'GET': # handling GET request
        rent = processRent()
        resp = jsonify(data=rent)
        # resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp

@app.route('/fetchTinyRent', methods=['POST'])
@cross_origin()
def fetchTinyRent():
    rent = processTinyRent()
    resp = jsonify(data=rent)
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

@app.route('/fetchTinyRent2', methods=['POST'])
@cross_origin()
def fetchTinyRent2():
    rent = processTinyRent()
    resp = jsonify(data=rent)
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

if __name__ == '__main__':
    app.run(port=3100, debug=True)
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import process, process_word_cloud

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
        df = process('Overall')
        resp = jsonify(data=df['data'],
                       emotion=df['index'],
                       people=df['columns'])
        return resp
    else:  # handling POST request
        request_context = request.get_json()  # JSON object
        method = request_context['method']
        df = process(method)
        resp = jsonify(data=df['data'],
                       emotion=df['index'],
                       people=df['columns'])
        return resp


@app.route("/fetchWordCloud", methods=["GET", "POST"])
@cross_origin()
def fetchWordCloud():
    if request.method == "GET":  # handling GET request
        df = process_word_cloud('Moderator')
        data = df['data']
        flat_value = []

        for item in data:
            flat_value += item

        resp = jsonify(data=df['columns'],
                       freq=flat_value)
        return resp

    else:  # handling POST request
        request_context = request.get_json()  # JSON object
        person = request_context['person']

        df = process_word_cloud(person)
        data = df['data']
        flat_value = []

        for item in data:
            flat_value += item

        resp = jsonify(data=df['columns'],
                       freq=flat_value)
        return resp


if __name__ == "__main__":
    app.run(port=3100, debug=True)

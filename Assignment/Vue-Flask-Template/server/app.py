from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processExample
import csv
import re

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

@app.route('/presidentName')
def get_barchart_data():
    president = []
    with open("/Users/ginnyhuang/Documents/ECS273-Winter2023/Assignment/Vue-Flask-Template/server/data/us_election_2020.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            president.append(row)
    
    # Create a dictionary to store the count of each president's name
    president_count = {}
    for name in president:
        name_only_text = re.sub("[^a-zA-Z]", " ", name[0]).strip()
        if(name_only_text == "Vice President Joe Biden"):
            name_only_text = "Joe Biden"
        elif(name_only_text == "President Donald J  Trump"):
            name_only_text = "Donald J. Trump"

        if(name_only_text != "speaker"):
            if name_only_text not in president_count:
                president_count[name_only_text] = 1
            else:
                president_count[name_only_text] += 1
    
    # Convert the dictionary to a list
    president_list = []
    for key, value in president_count.items():
        president_list.append({'name': key, 'count': value})
    
    return jsonify(president_list)

if __name__ == "__main__":
    app.run(port=3100, debug=True)



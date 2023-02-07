from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import processExample
# from controller import processExample_text
import csv

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!!!</p>"

@app.route("/fetchExample", methods=["GET", "POST"])
@cross_origin()
def fetchExample():
    if request.method == "GET": # handling GET request
        points, cluster_names = processExample()
        resp = jsonify(data=points, clusters=cluster_names)
        # print(resp)
        return resp
    else: # handling POST request, which is only effective when ExampleWithInteractions.vue is loaded
        request_context = request.get_json() # JSON object
        method = request_context['method']
        points, cluster_names = processExample(method)
        resp = jsonify(data=points, clusters=cluster_names)
        # print(resp)
        return resp


#在這裡寫一個api去讀csv檔案
# @app.route("/read_csv", methods=["GET"])
# def read_csv():
#     with open("/Users/chenpohsuan/ECS273-Winter2023/Assignment/Vue-Flask-Template/server/data/rental.csv") as file:
#         csv_reader = csv.reader(file)
#         header = next(csv_reader)
#         data = [dict(zip(header, row)) for row in csv_reader]
#     return jsonify(data)


@app.route("/rent_data", methods=["GET"])
def rent_data():
    with open("/Users/chenpohsuan/ECS273-Winter2023/Assignment/phschen/server/data/rental.csv") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = [dict(zip(header, row)) for row in csv_reader]

    data_dict = {}

    for i in data:
        # print(i)
        if i['county'] in data_dict:
            data_dict[i['county']] = int(data_dict[i['county']]) + int(i['totalproduction'])
        else:
            data_dict[i['county']] = int(i['totalproduction'])

    print(data_dict)

    county = []
    totalProduction = []
    for i in data_dict:
        county.append(i)
        totalProduction.append(int(data_dict[i]))

    # print(county)
    # print(totalProduction)

    resp = jsonify(county_=county, totalProduction_=totalProduction)
    return resp


if __name__ == "__main__":
    app.run(port=3100, debug=True)

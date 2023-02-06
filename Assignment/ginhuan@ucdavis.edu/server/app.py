from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import read_CSVfile
import csv
import re

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/presidentName')
def get_barchart_data():
    president = read_CSVfile()
    
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

@app.route('/presidentNameBarChart')
def get_vuebarchart_data():
    president = read_CSVfile()
    
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
    president_list_labels = []
    president_list_count = []
    for key, value in president_count.items():
        president_list_labels.append(key)
        president_list_count.append(value)
    return jsonify(name = president_list_labels, count = president_list_count)


@app.route('/speechTrump')
def get_trump_speech():
    president_test = read_CSVfile()
    trump = []

    for speech in president_test:
        speech_only_text = re.sub('[^a-zA-Z \’]', ' ', speech[2]).strip()
        speech_only_text.replace("crosstalk", "")
        if(speech[0] == "President Donald J. Trump"):
                trump.append(speech_only_text)

    trump_words = {}
    for sentence in trump:
        for words in sentence.split():
                if(words not in trump_words):
                    trump_words[words] = 1
                else:
                    trump_words[words] += 1

    new_dict = {key: val for key,val in trump_words.items() if val > 60}

    # Convert the dictionary to a list
    trump_speech_list = []
    for key, value in new_dict.items():
        trump_speech_list.append({'words': key, 'count': value})
        
    return jsonify(trump_speech_list)

@app.route('/speechBiden')
def get_biden_speech():
    president_test = read_CSVfile()
    biden = []

    for speech in president_test:
        speech_only_text = re.sub('[^a-zA-Z \’]', ' ', speech[2]).strip()
        speech_only_text.replace("crosstalk", "")
        if(speech[0] == "Vice President Joe Biden"):
                biden.append(speech_only_text)

    biden_words = {}
    for sentence in biden:
        for words in sentence.split():
                if(words not in biden_words):
                    biden_words[words] = 1
                else:
                    biden_words[words] += 1

    new_dict = {key: val for key,val in biden_words.items() if val > 70}

    # Convert the dictionary to a list
    biden_speech_list = []
    for key, value in new_dict.items():
        biden_speech_list.append({'words': key, 'count': value})
        
    return jsonify(biden_speech_list)


if __name__ == "__main__":
    app.run(port=3100, debug=True)



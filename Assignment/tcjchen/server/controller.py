import os
import pandas as pd
import numpy as np
from text_processing_template import preprocess, ShowWordCloud
from textblob import TextBlob
import text2emotion as te
import operator

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('words')


def get_data():
    # use below to read when testing the whole web
    data = pd.read_csv(
        "../server/data/us_election_2020_1st_presidential_debate.csv")

    # use below to read when testing controller.py
    # data = pd.read_csv(
    #     "./data/us_election_2020_1st_presidential_debate.csv")
    # remove rules and greetings
    data = data.drop(data.index[range(5)])
    return data


def get_avg_df(df):
    happy, angry, surprise, sad, fear = 0, 0, 0, 0, 0
    for i in range(len(df)):
        happy += df["Happy"].iloc[i]
        angry += df["Angry"].iloc[i]
        surprise += df["Surprise"].iloc[i]
        sad += df["Sad"].iloc[i]
        fear += df["Fear"].iloc[i]

    res = [happy, angry, surprise, sad, fear]
    return [x/len(df) if x/len(df) != 0.0 else 0.000000001 for x in res]


############################Start WordCloud############################
def process_emotion(start: int, end: int, topic: str):
    # Function usage:
    # pass in interested start row's index and row's end index
    # return a dataframe with speaker's name and emotion on that segment.
    df = pd.DataFrame({"Speaker": [],
                       "Word": [],
                       "Happy": [],
                       "Angry": [],
                       "Surprise": [],
                       "Sad": [],
                       "Fear": []})

    # get segment of topic's sentences
    data = get_data()
    selected_data = data.iloc[start:end]
    selected_data = selected_data.drop(columns="minute")

    # assign emotion to each sentence
    for i in range(len(selected_data)):
        emotions = te.get_emotion(selected_data["text"].iloc[i])
        df.loc[len(df.index)] = [selected_data["speaker"].iloc[i],
                                 selected_data["text"].iloc[i],
                                 emotions["Happy"],
                                 emotions["Angry"],
                                 emotions["Surprise"],
                                 emotions["Sad"],
                                 emotions["Fear"]]

    # select row by column's value (i.e. "Chris Wallace")
    chris_df = df.loc[df['Speaker']
                      == "Chris Wallace"]
    trump_df = df.loc[df['Speaker']
                      == "President Donald J. Trump"]
    biden_df = df.loc[df['Speaker']
                      == "Vice President Joe Biden"]

    chris, trump, biden = get_avg_df(chris_df), get_avg_df(
        trump_df), get_avg_df(biden_df)

    # serialize dataframe
    arr = np.array([chris, trump, biden])
    serialize_df = pd.DataFrame(arr.transpose(),
                                columns=["Moderator", "Trump", "Joe Biden"],
                                index=['Happy', 'Angry', 'Surprise', 'Sad', 'Fear'])

    # write csv to the data folder in the server for faster read
    pd.DataFrame(columns=serialize_df.columns).to_csv("./data/" + topic +
                                                      "_with_emotion.csv", index=False)
    serialize_df.to_csv("./data/" + topic +
                        "_with_emotion.csv", header=None, mode='a')

    serialize_df = serialize_df.to_dict(orient="split")
    return serialize_df


def process_supreme_court_topic():
    start = 0
    end = 150
    topic = "supreme_court"
    path = "../server/data/" + topic + "_with_emotion.csv"

    if os.path.isfile(path):
        df = pd.read_csv(path)
        return df.to_dict('split')
    else:
        df = process_emotion(start, end, topic)
        return df


def process_covid19_topic():
    # covid-19
    # c19_data = data.iloc[150:273]
    # # print(c19_data.head(1))
    # # print(c19_data.tail(1))

    start = 150
    end = 273
    topic = "covid"
    path = "../server/data/" + topic + "_with_emotion.csv"

    if os.path.isfile(path):
        df = pd.read_csv(path)
        return df.to_dict('split')
    else:
        df = process_emotion(start, end, topic)
        return df


def process_economy_topic():
    # economy_data = data.iloc[273:473]
    # # print(economy_data.head(1))
    # # print(economy_data.tail(1))

    start = 273
    end = 473
    topic = "economy"
    path = "../server/data/" + topic + "_with_emotion.csv"

    if os.path.isfile(path):
        df = pd.read_csv(path)
        return df.to_dict('split')
    else:
        df = process_emotion(start, end, topic)
        return df


def process_violence_topic():
    # # race and violence in cities
    # vio_data = data.iloc[473:601]
    # # print(vio_data.head(1))
    # # print(vio_data.tail(1))

    start = 473
    end = 601
    topic = "violence"
    path = "../server/data/" + topic + "_with_emotion.csv"

    if os.path.isfile(path):
        df = pd.read_csv(path)
        return df.to_dict('split')
    else:
        df = process_emotion(start, end, topic)
        return df


def process_records_topic():
    # # records
    # record_data = data.iloc[601:718]
    # # print(record_data.head(1))
    # # print(record_data.tail(1))

    start = 601
    end = 718
    topic = "records"
    path = "../server/data/" + topic + "_with_emotion.csv"

    if os.path.isfile(path):
        df = pd.read_csv(path)
        return df.to_dict('split')
    else:
        df = process_emotion(start, end, topic)
        return df


def process_integrity_topic():
    # # integrity of the election
    # int_data = data.iloc[718:]
    # # print(int_data.head(1))
    # # print(int_data.tail(1))

    start = 718
    end = 784
    topic = "integrity"
    path = "../server/data/" + topic + "_with_emotion.csv"

    if os.path.isfile(path):
        df = pd.read_csv(path)
        return df.to_dict('split')
    else:
        df = process_emotion(start, end, topic)
        return df


def process_overall():

    start = 0
    end = 784
    topic = "overall"
    path = "../server/data/" + topic + "_with_emotion.csv"

    if os.path.isfile(path):
        df = pd.read_csv(path)
        return df.to_dict('split')
    else:
        df = process_emotion(start, end, topic)
        return df


def process(topic='Supreme Court'):
    if topic == "Supreme Court":
        return process_supreme_court_topic()
    elif topic == "Covid-19":
        return process_covid19_topic()
    elif topic == "Economy":
        return process_economy_topic()
    elif topic == "Race and Violence":
        return process_violence_topic()
    elif topic == "Records":
        return process_records_topic()
    elif topic == "Integrity":
        return process_integrity_topic()
    elif topic == "Overall":
        return process_overall()

############################BarChart END############################


############################Start WordCloud############################

def process_word_cloud(person: str):
    data = get_data()
    data = data.drop(columns="minute")

    chris = ""
    trump = ""
    biden = ""

    for i in range(len(data)):
        if data.iloc[i]['speaker'] == "Chris Wallace":
            chris += data.iloc[i]['text']
        elif data.iloc[i]['speaker'] == "President Donald J. Trump":
            trump += data.iloc[i]['text']
        elif data.iloc[i]['speaker'] == "Vice President Joe Biden":
            biden += data.iloc[i]['text']

    if person == "Moderator":
        processed_words = preprocess(chris).split()
    elif person == "Trump":
        processed_words = preprocess(trump).split()
    elif person == "Biden":
        processed_words = preprocess(biden).split()

    # check if the words exist
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    clean_processed_words = []
    for word in processed_words:
        if word in english_vocab:
            clean_processed_words.append(word)

    # Count the word frequency happen in the debate
    frequency = {}
    for item in clean_processed_words:
        if item in frequency:
            frequency[item][0] += 1
        else:
            polarity = TextBlob(item).sentiment.polarity
            subjectivity = TextBlob(item).sentiment.subjectivity
            frequency[item] = [1, polarity, subjectivity]

    # cnt = 0
    # cnt_sub = 0
    # for i, v in enumerate(frequency):
    #     if frequency[v][1] != 0:
    #         cnt += 1
    #     if frequency[v][2] != 0:
    #         cnt_sub += 1

    # print("Length of Frequency: ", len(frequency))
    # print("Word with Polarity value not equal to 0: ", cnt)
    # print("Word with Subjectivity value not equal to 0: ", cnt_sub)

    # Sort the frequency dict by freq in descending order
    sorted_freq = dict(
        sorted(frequency.items(), key=operator.itemgetter(1), reverse=True))

    # Convert to list
    words = list(sorted_freq.keys())
    values = list(sorted_freq.values())

    df = pd.DataFrame(columns=words)
    df.loc[0, words] = values

    return df.to_dict('split')


############################WordCloud END############################

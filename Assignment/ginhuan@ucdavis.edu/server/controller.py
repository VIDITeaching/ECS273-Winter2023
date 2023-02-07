import pandas as pd
import numpy as np
import csv

def read_CSVfile():
    president_test = []
    with open("/Users/ginnyhuang/Documents/ECS273-Winter2023/Assignment/Vue-Flask-Template/server/data/us_election_2020.csv") as csv_read_file:
            csv_read_data = csv.reader(csv_read_file)
            for row in csv_read_data:
                president_test.append(row)
    return president_test



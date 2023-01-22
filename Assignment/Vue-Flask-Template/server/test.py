import pandas as pd
import numpy as np

import os

def processRent():
    path = '/data/SF-Rentals/rent.csv'

    print('Get current working directory : ', os.getcwd())
    rent = pd.read_csv(os.getcwd() + path)

processRent()
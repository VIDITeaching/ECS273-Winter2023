from calendar import c
import numpy as np
import csv
from collections import defaultdict
import math


class DataManager():
    def __init__(self):
        self.raw_data = csv.DictReader(open(r'data/raw_data.csv', encoding='ISO-8859-1'))
        self.processed_data = self.process_data(self.raw_data)

    def process_data(self, raw_csv):
        attacks_groupby_region = defaultdict(list)
        max_casualty = -1
        min_casualty = math.inf
        for row in raw_csv:
            year = row['iyear']
            month = row['imonth']
            day = row['iday']
            country = row['country_txt']
            kill = int(float(row['nkill'] or 0))
            wound = int(float(row['nwound'] or 0))
            casualty = kill+wound
            if max_casualty < casualty: max_casualty = casualty
            if min_casualty > casualty: min_casualty = casualty
            point = {
                'date': '{}-{}-{}'.format(year, month, day), 
                'casualty': casualty,
                'kill': kill,
                'wound': wound,
                'country': row['country_txt'],
                'summary': row['summary'] or "No summary",
                'notes': row['addnotes'] or "No notes",
                'attack_type': row['attacktype1_txt'],
                'target': row['target1'],
                'motive': row['motive'],
            }
            attacks_groupby_region[country].append(point)
        # filter out countries by attack number
        removed_countries = [country for country, attacks in attacks_groupby_region.items() if len(attacks) < 10000]
        for country in removed_countries: del attacks_groupby_region[country]
        metadata = {
            "max_casualty": max_casualty,
            "min_casualty": min_casualty,
        }
        return attacks_groupby_region, metadata

    def get_processed_data(self):
        return self.processed_data

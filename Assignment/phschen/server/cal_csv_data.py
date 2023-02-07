import csv

def cal_csv_data():
    with open("/Users/chenpohsuan/ECS273-Winter2023/Assignment/Vue-Flask-Template/server/data/rental.csv") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = [dict(zip(header, row)) for row in csv_reader]

    year_dict = {}

    for i in data:
        # print(i)
        if i['year'] in year_dict:
            year_dict[i['year']] += 1
        else:
            year_dict[i['year']] = 1

    print(year_dict)
    

    data_list = []

    for i in year_dict:
        data_list.append({i:year_dict[i]})
    
    print(data_list)
    return year_dict
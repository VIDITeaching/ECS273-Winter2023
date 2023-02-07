import numpy as np
import pandas as pd
dataset = pd.read_csv('rent.csv')
price=dataset.iloc[:,6].values
county=dataset.iloc[:,5].values
total_rent_county=dict()
total_home_per_county=dict()
for i in county:
    if(i):
        if i in total_home_per_county:
            total_home_per_county[i]+=1
        else:
            total_home_per_county[i]=1
for i in range(len(county)):
    if(i):
        if county[i] in total_rent_county:
            total_rent_county[county[i]]+=price[i]
        else:
            total_rent_county[county[i]]=price[i]
distinct_county=set(county)
avg_rent_county=[]
county_soul_list=[]
county_details=[]
for i in distinct_county:
    if int(total_rent_county[i]/total_home_per_county[i]) == 2100:
        continue
    avg_rent_county.append(int(total_rent_county[i]/total_home_per_county[i]))
    county_soul_list.append(i)
for i in range(len(county_soul_list)):
    temp={}
    temp['Place'] = county_soul_list[i]
    temp['Price'] = avg_rent_county[i]
    county_details.append(temp)
print(county_details)
Price_Home=dataset.iloc[:,6].values
Bedroom=dataset.iloc[:,7].values
Sqft=dataset.iloc[:,9].values
k=0
interactive=[]
for i in range(len(Price_Home)):
  if Price_Home[i]>0 and Bedroom[i]> -1 and Sqft[i]>0 and k<500:
    temp={}
    temp['county']="alameda"
    temp['price']=int(Price_Home[i])
    temp['beds']=int(Bedroom[i])
    temp['sqft']=int(Sqft[i])
    k+=1
    interactive.append(temp)
print(interactive)


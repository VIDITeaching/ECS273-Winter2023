import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

res_dict={'data': []}
column_dict = {'columns': []}

df = pd.read_csv('../server/data/Dry_Bean_Dataset_short.csv')
#df = pd.read_csv('../server/data/Dry_Bean_Dataset.csv')
df = df.drop_duplicates()

# "Area", "AspectRation", "Compactness", "ConvexArea", "Class"

df = df[["Area", "AspectRation", "Compactness", "ConvexArea", "Class"]]
data = df.values

labels = df['Class']

X: np.ndarray = data
y: np.ndarray = labels

res_data = pd.DataFrame(data=df)
column_dict['columns'] = df.columns.tolist()

res_dict['data'] = res_data.to_dict(orient='records')
print(res_dict)
print(res_dict['data'])
res_dict['data'].append(column_dict)
print(res_dict)
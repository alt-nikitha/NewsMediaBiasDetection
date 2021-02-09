import pandas as pd 
import re
import numpy as np


# this is full dataset
df1= pd.read_csv('articleswithlabels.csv').reset_index(drop=True)

# replace empty brackets with np.nan
df1.loc[(df1[' authors']=="[]")," authors"]=np.nan

# get the required columns, add the one for news_source url 
newdf= df1[['title',' authors',' date',' url','Name','Bias']]

# remove rows with null values
index_with_nan = df1.index[df1.isnull().any(axis=1)]
df=df1.drop(index_with_nan,0).reset_index(drop=True)
print(df.columns)
authorsmixed=pd.unique(df[' authors'])
    # print(authorsmixed[-100:])

    

for ele in authorsmixed:
    
    if(not(isinstance(ele,str))):
        print("haha")
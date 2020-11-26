import pandas as pd 

df=pd.read_csv('all_articles.csv')
df.rename(columns = {" publication": "URL"},  
          inplace = True) 
df1=pd.read_csv('final.csv')
df['URL']=df['URL'].astype(str)
df1['URL']=df1['URL'].astype(str)
for i in range(len(df)):
    val=df['URL'].iloc[i]
    if(val[-1]!='/'):
        df['URL'].iloc[i]=val+'/'

for i in range(len(df1)):
    val=df1['URL'].iloc[i]
    if(val[-1]!='/'):
        df1['URL'].iloc[i]=val+'/'



# print(df.columns, df1.columns)

joined=df.merge(df1, on="URL", how="left", sort=False)

joined.to_csv("articleswithlabels.csv")
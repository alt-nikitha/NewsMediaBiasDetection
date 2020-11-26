import pandas as pd 

# read the csv file with all articles
df=pd.read_csv('all_articles.csv')

# rename the news source column from publication to URL so that it can 
# be joined with the news source csv file to get bias
df.rename(columns = {" publication": "URL"},  
          inplace = True) 

# read the news source with bias csv file
df1=pd.read_csv('final.csv')

#make sure data types are same for merge
df['URL']=df['URL'].astype(str)
df1['URL']=df1['URL'].astype(str)

#some URLs do not have / at the end in both files, so append at the end
for i in range(len(df)):
    val=df['URL'].iloc[i]
    if(val[-1]!='/'):
        df['URL'].iloc[i]=val+'/'

for i in range(len(df1)):
    val=df1['URL'].iloc[i]
    if(val[-1]!='/'):
        df1['URL'].iloc[i]=val+'/'



# join both dataframes based on URL
joined=df.merge(df1, on="URL", how="left", sort=False)

#store final dataset of articles with bias labels
joined.to_csv("articleswithlabels.csv")
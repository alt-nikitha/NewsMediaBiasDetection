import pandas as pd

folder='data_raw/google_news/'

for f in os.listdir(folder):
    # for each csv file in the google news folder
    if(f[-3:]=='csv'):
        #open as a dataframe
        df=pd.read_csv(folder+f)
        #get column names of csv file and create a new empty dataframe with same column names
        all_articles = pd.DataFrame(columns=df.columns)
        # break because all csv files have same column names
        break

# concatenate each csv file in google news folder to the new empty dataframe 
# created earlier and store as all_articles.csv
for f in os.listdir(folder):
    if(f[-3:]=='csv'):
        df=pd.read_csv(folder+f)
        frames=[all_articles,df]
        all_articles=pd.concat(frames,sort=False)
all_articles.to_csv('all_articles.csv')


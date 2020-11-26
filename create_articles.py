import pandas as pd

folder='data_raw/google_news/'
for f in os.listdir(folder):
    if(f[-3:]=='csv'):
        df=pd.read_csv(folder+f)
        all_articles = pd.DataFrame(columns=df.columns)
        # print(pd.unique(df[' publication']))
        break
for f in os.listdir(folder):
    if(f[-3:]=='csv'):
        df=pd.read_csv(folder+f)
        frames=[all_articles,df]
        all_articles=pd.concat(frames,sort=False)
all_articles.to_csv('all_articles.csv')
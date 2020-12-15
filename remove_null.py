import pandas as pd
import numpy as np

ns=pd.read_csv("final.csv")
authors=pd.read_csv("authors.csv")
articles=pd.read_csv("articles.csv")
writes=pd.read_csv('writes.csv')
wf=pd.read_csv("writes_for.csv")
contains=pd.read_csv("contains.csv")

def remove(df,fname):
    df=df.drop(['Unnamed: 0'],axis=1)
    index_with_nan = df.index[df.isnull().any(axis=1)]
    # index_with_nan.shape
    newdf=df.drop(index_with_nan,0).reset_index(drop=True)
    print(newdf)
    newdf.to_csv(fname+".csv")
remove(ns,"newsource")
# remove(authors,"authors")
# remove(articles,"articles")
# remove(writes,"writes")
# remove(wf,"writes_for")
# remove(contains,"contains")
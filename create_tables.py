import pandas as pd 
import re
import numpy as np
df1= pd.read_csv('articleswithlabels.csv').reset_index(drop=True)
df1.loc[(df1[' authors']=="[]")," authors"]=np.nan
newdf= df1[['title',' authors',' date',' url','Name','Bias']]
index_with_nan = df1.index[df1.isnull().any(axis=1)]
df=df1.drop(index_with_nan,0).reset_index(drop=True)
print(df.columns)

def create_authors():
    # print(df[' authors'])
    authorsmixed=pd.unique(df[' authors'])
    # print(authorsmixed[-100:])
    authorslist=[]
    for ele in authorsmixed:
        if(isinstance(ele,str)):
            newele=re.match(r"\[([^\]]+)\]",ele)
        # if(newele):
        #     print(newele[1])
        try:
            authorshere=newele[1].split(",")
            for author in authorshere:
                authorslist.append(author)

        except:
            authorslist.append(author)

    # print(authorslist)
    authors=sorted(set([x.lower() for x in authorslist]))
    newdf=pd.DataFrame(authors,columns=['Name'])
    newdff=newdf.drop_duplicates(subset='Name')
    print(len(newdff))
    newdff.to_csv("authors.csv")
    
def create_articles():
    
    articles=df[['title',' date',' url','Bias']]
    
    newfinal=articles.drop_duplicates(subset=[' url'], keep='last')
    print(len(newfinal))
    newfinal.to_csv('articles.csv')

def create_works_for():
    works_for=pd.DataFrame(columns=['Author','News Source'])
    k=0
    for i in range(len(df)):
        
        author=df.loc[i][' authors']
        if(isinstance(author,str)):
            newele=re.match(r"\[([^\]]+)\]",author)
            try:
                authorshere=newele[1].split(",")
                for ele in authorshere:
                    row=pd.Series({"Author":ele.lower(),"News Source":df.loc[i]['Name']})
                    works_for.loc[k]=row
                    k+=1
            except:
                print(author)
                row=pd.Series({"Author":newele.lower(),"News Source":df.loc[i]['Name']})
                works_for.loc[k]=row
                k+=1
    newdf=works_for.drop_duplicates()
    print(len(newdf))
    newdf.to_csv("writes_for.csv")





def create_writes():
    writes=pd.DataFrame(columns=['Author','ArticleURL'])
    k=0
    for i in range(len(df)):
        
        author=df.loc[i][' authors']
        if(isinstance(author,str)):
            newele=re.match(r"\[([^\]]+)\]",author)
            try:
                authorshere=newele[1].split(",")
                for ele in authorshere:
                    row=pd.Series({"Author":ele.lower(),"ArticleURL":df.loc[i][' url']})
                    writes.loc[k]=row
                    k+=1
            except:
                row=pd.Series({"Author":newele.lower(),"ArticleURL":df.loc[i][' url']})
                writes.loc[k]=row
                k+=1
    neww=writes.drop_duplicates()
    print(len(neww))
    neww.to_csv("writes.csv")

def contains():
    contains=df[['Name',' url']]
    newc=contains.drop_duplicates()
    # print(newc)
    newc.to_csv('contains.csv')
    
    pass


create_authors()
create_articles()
create_works_for()
create_writes()
contains()
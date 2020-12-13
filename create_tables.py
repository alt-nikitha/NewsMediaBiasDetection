import pandas as pd 
import re
import numpy as np
df= pd.read_csv('articleswithlabels.csv').reset_index(drop=True)
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
    pd.DataFrame(authors,columns=['Name']).to_csv("authors.csv")
def create_articles():
    
    articles=df[['title',' date',' url','Bias']]
    
    final=articles[pd.notnull(articles)]
    print(final)
    final.to_csv('articles.csv')

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
                    row=pd.Series({"Author":ele,"News Source":df.loc[i]['Name']})
                    works_for.loc[k]=row
                    k+=1
            except:
                row=pd.Series({"Author":newele,"News Source":df.loc[i]['Name']})
                works_for.loc[k]=row
                k+=1
    works_for.to_csv("writes_for.csv")





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
                    row=pd.Series({"Author":ele,"ArticleURL":df.loc[i][' url']})
                    writes.loc[k]=row
                    k+=1
            except:
                row=pd.Series({"Author":newele,"ArticleURL":df.loc[i][' url']})
                writes.loc[k]=row
                k+=1
    writes.to_csv("writes.csv")

def contains():
    contains=df[['Name',' url']]
    contains.to_csv('contains.csv')
    
    pass


create_authors()
create_articles()
create_works_for()
create_writes()
contains()
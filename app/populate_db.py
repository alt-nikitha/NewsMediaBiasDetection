from flask_sqlalchemy import SQLAlchemy 
from app.models import db
import pandas as pd
from app.models import NewsSourceDropDown,NewsSource,Authors,Articles,Writes,Writes_For,Contains

def add_to_db():
    
    newsourcesdd=pd.read_csv('app/newsourcedd.csv')
    newsources=pd.read_csv('app/newsource.csv')
    authors=pd.read_csv("app/authors.csv")
    articles=pd.read_csv("app/articles.csv")
    writes=pd.read_csv('app/writes.csv')
    wf=pd.read_csv("app/writes_for.csv")
    contains=pd.read_csv("app/contains.csv")

    for i in range(len(newsourcesdd)):
        name=newsourcesdd['Name'].iloc[i]
        url=newsourcesdd['URL'].iloc[i]
        bias=newsourcesdd['Bias'].iloc[i]
        newdd = NewsSourceDropDown(name=name, URL=url,bias=bias)
        db.session.add(newdd)
        db.session.commit()

    for i in range(len(newsources)):
        name=newsources['Name'].iloc[i]
        url=newsources['News_Source'].iloc[i]
        bias=newsources['Bias'].iloc[i]
        new = NewsSource(name=name, URL=url,bias=bias)
        db.session.add(new)
        db.session.commit()

    for i in range(len(authors)):
        name1=authors['Name'].iloc[i] 
        name=(name1[:100]) if len(name1)>100 else name1
        author=Authors(name=name)
        db.session.add(author)
        db.session.commit()

    
    for i in range(len(articles)):
        title1=articles['title'].iloc[i]
        title=(title1[:150]) if len(title1)>150 else title1
        date=articles[' date'].iloc[i]
        url=articles[' url'].iloc[i]
        bias=articles['Bias'].iloc[i]
        article=Articles(title=title,date=date,url=url,bias=bias)
        db.session.add(article)
        db.session.commit()

    for i in range(len(writes)):
        url=writes['ArticleURL'].iloc[i]
        name1=writes['Author'].iloc[i]
        name=(name1[:100]) if len(name1)>100 else name1
        w=Writes(author=name,article=url)
        db.session.add(w)
        db.session.commit()


    for i in range(len(wf)):
        name1=wf['Author'].iloc[i]
        aname=(name1[:100]) if len(name1)>100 else name1
        ns=wf['News Source'].iloc[i]
        w=Writes_For(author=aname,newssource=ns)
        db.session.add(w)
        db.session.commit()



    for i in range(len(contains)):
        name=contains['Name'].iloc[i]
        url=contains[' url'].iloc[i]
        c=Contains(article=url,newssource=name)
        db.session.add(c)
        db.session.commit()


def add_to_mongo(collection,date,summary,title,authors,source_url,text):
    if(len(authors)):
        for authorname in authors:
            post= {"author": authorname, "source":source_url, "content":text,"date":date,"summary":summary,"title":title}
            collection.insert_one(post)
            
    else:
        post= {"author": authors, "source":source_url, "content":text,"date":date,"summary":summary,"title":title}
        collection.insert_one(post)
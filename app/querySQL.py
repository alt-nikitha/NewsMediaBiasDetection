from flask_sqlalchemy import SQLAlchemy 
from urllib.parse import urlparse
from app.models import db
import newspaper 
from app.models import NewsSourceDropDown,NewsSource,Authors,Articles,Writes,Writes_For,Contains

def get_drop_down():
    all_news_sources=NewsSourceDropDown.query.order_by(NewsSourceDropDown.name).all()
    news_sources=[]
    for ele in all_news_sources:
        news_sources.append(ele.name)
    return news_sources

def query_or_add(url,title,date,bias,authors, source_url):
    # otherartsinns=[]
    # otherartsbyauthor=[]

    articleurlexists=Articles.query.filter_by(url=url).first()
    articletitleexists=Articles.query.filter_by(title=title).first()
    # print(articleurlexists, articletitleexists)
    # try :
    if((not articleurlexists) and (not articletitleexists)):
        print("haha2")

        article1=Articles(title=title,date=date,url=url,bias=bias)
        db.session.add(article1)
        db.session.commit()
        
    
        for author in authors:
            print(author)
            print("haha3")

            authorexists=Authors.query.filter_by(name=author.lower()).first()
            if not authorexists:
                authorobj=Authors(name=author.lower())
                db.session.add(authorobj)
                db.session.commit()
                print("haha4")


            authorwrites=Writes(author=author.lower(),article=url)
            print("haha1")
            db.session.add(authorwrites)
            db.session.commit()

            # otherobj=Writes.query.filter_by(author=author.lower())
            # # print(otherobj.article)
            # if(otherobj):
            #     for art in otherobj:
            #         print("haha5") 
            #         otherartsbyauthor.append(art.article)
            # else:
            #     otherartsbyauthor.append(url)
            
            # parsed_uri = urlparse(url)
            # result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            
            newssourcequery=NewsSource.query.filter_by(URL=source_url).first()
            if(not(newssourcequery)):
                # nsname=newssourcequery.name
                # print("haha6") 
            
                print(source_url)
                nobj=newspaper.build(source_url)
                print(nobj)
                nsname=nobj.brand
                print("haha6") 
                newsourceobj=NewsSource(name=nsname,URL=source_url)
                print("haha7") 
                db.session.add(newsourceobj)
                db.session.commit()
            else:
                nsname=newssourcequery.name
            
                

            authorwritesforexists=Writes_For.query.filter_by(author=author.lower(),newssource=nsname).first()
            print("haha8") 
            if not authorwritesforexists:
                authorwfobj=Writes_For(author=author.lower(),newssource=nsname)
                print("haha9") 
                db.session.add(authorwfobj)
                db.session.commit()

        containsart=Contains.query.filter_by(article=url,newssource=nsname).first()
        print("haha10") 
        if not containsart:
            containsartobj=Contains(article=url,newssource=nsname)
            print("haha11") 
            db.session.add(containsartobj)
            db.session.commit()
        
        # otherartsinnsobj=Contains.query.filter_by(newssource=nsname)
        # print("haha12") 
        # for art in otherartsinnsobj:
        #     otherartsinns.append(art.article)
        # print("haha")
        # db.session.commit()
    # except :
    #     pass
        
            
        

        # for author in authors:

        #     otherobj=Writes.query.filter_by(author=author.lower())
        #     for art in otherobj:
        #         otherartsbyauthor.append(art.article)

        # # parsed_uri = urlparse(url)
        # # result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        # # print(result)
        # newssourcequery=NewsSource.query.filter_by(URL=source_url).first()
        # nsname=newssourcequery.name
        # otherartsinnsobj=Contains.query.filter_by(newssource=nsname)
        # for art in otherartsinnsobj:
        #     otherartsinns.append(art.article)

def find_same_bias_authors(label):
    artobj=Articles.query.filter_by(bias=label)
    otherauthorsbias=[]
    if(artobj):
        for obj in artobj:
            newobj=Writes.query.filter_by(article=obj.url)
            for subobj in newobj:
                otherauthorsbias.append(subobj.author)
    return otherauthorsbias

def find_same_bias_articles(label):
    obj=Articles.query.filter_by(bias=label)
    otherartsbias=[]
    if(obj):
        for art in obj:
            odic={}
            odic['url']=art.url
            odic['title']=art.title
            otherartsbias.append(odic)
    return otherartsbias

def find_same_bias_news(label=None,name=None):
    otherbias=[]
    # if(name and not(dd) ):
    #     nobj=NewsSource.query.filter_by(name=name).first_or_404()
    #     # obj=NewsSourceDropDown.query.filter_by(URL=nobj.URL).first_or_404()
    #     # print(obj.name, obj.URL)
    #     otherbiasobj=NewsSourceDropDown.query.filter_by(bias=nobj.bias)
        
    #     # find other news sources with same bias
    #     if(otherbiasobj):
    #         for news in otherbiasobj:
    #             otherdic={}
    #             otherdic['name']=news.name
    #             otherdic['url']=news.URL
    #             otherbias.append(otherdic)
    #         return otherbias
    if(name):
        # nobj=NewsSource.query.filter_by(name=name).first_or_404()
        obj=NewsSourceDropDown.query.filter_by(name=name).first_or_404()
        # print(obj.name, obj.URL)
        otherbiasobj=NewsSourceDropDown.query.filter_by(bias=obj.bias)
        
        # find other news sources with same bias
        if(otherbiasobj):
            for news in otherbiasobj:
                otherdic={}
                otherdic['name']=news.name
                otherdic['url']=news.URL
                otherbias.append(otherdic)
            return otherbias,obj.bias,obj.URL
    if(label):
        obj=NewsSourceDropDown.query.filter_by(bias=label)
        for news in obj:
            otherdic={}
            otherdic['name']=news.name
            otherdic['url']=news.URL
            otherbias.append(otherdic)
        return otherbias

    



def find_same_news_source_author(req):
    otherauthsinns=[]
    # nsobj=NewsSource.query.filter_by(URL=req).first_or_404()
    otherauthsinnsobj=Writes_For.query.filter_by(newssource=req)
    if(otherauthsinnsobj):
        for obj in otherauthsinnsobj:
            otherauthsinns.append(obj.author)
    return otherauthsinns
    
def find_same_news_source_articles(req):
    otherartsinns=[]
    # obj=NewsSource.query.filter_by(URL=req).first_or_404()
    # print(obj.name)
    otherartsinnsobj=Contains.query.filter_by(newssource=req)
    if(otherartsinnsobj):
        for art in otherartsinnsobj:
            odic={}
            odic['url']=art.article
            artob=Articles.query.filter_by(url=art.article).first_or_404()
            odic['title']=artob.title
            otherartsinns.append(odic)
    
    return otherartsinns
    

def find_same_author_articles(author):

    otherartsbyauthor=[]
    
    otherobj=Writes.query.filter_by(author=author.lower())
        
    if(otherobj): 
        
        for art in otherobj:
            odic={}
            artobj=Articles.query.filter_by(url=art.article).first_or_404()
            # print(artobj.title) 
            odic['url']=art.article
            odic['title']=artobj.title
            
            otherartsbyauthor.append(odic)
        
    return otherartsbyauthor



from flask import Flask, render_template, request
import pandas as pd
from flask_sqlalchemy import SQLAlchemy 
import pymongo
from pymongo import MongoClient 
import newspaper 
from newspaper import Article

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/nmbd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
newsources=pd.read_csv("final.csv")

class NewsSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    URL = db.Column(db.String(75))
    bias=db.Column(db.String(15))


# def add_to_db():
#     newsources=pd.read_csv('final.csv')
#     for i in range(len(newsources)):
#         name=newsources['Name'].iloc[i]
#         url=newsources['URL'].iloc[i]
#         bias=newsources['Bias'].iloc[i]
#         new = NewsSource(name=name, URL=url,bias=bias)
#         db.session.add(new)
#         db.session.commit()


##Mongo Part
## This is my cluster , which is linked to my specific IP address
cluster=MongoClient("mongodb+srv://neelb:NewsBiasDetect246@newsbiasdetection.bxxdo.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=cluster["test"] ##database name
collection =db["test1"] ##collection
#collection.insert_one(post)
#results = collection.delete_one({"_id":1})

@app.route('/')
def index():
    all_news_sources=NewsSource.query.order_by(NewsSource.name).all()
    news_sources=[]
    for ele in all_news_sources:
        news_sources.append(ele.name)
    # news_sources=newsources['Name'].to_list()
    return render_template('index.html',ns=news_sources)

@app.route('/detect',methods=['GET','POST'])
def detect():
    url=request.form.get('name')
    article = Article(url)
    article.download()
    article.parse()
    author =article.authors
    date=article.publish_date
    text= article.text

    ##Post is the data you want to enter into the database. Not specifying an ID generates a random one 
    post= {"author": author[0], "source":article.source_url, "content":text,"date":date}

    collection.insert_one(post)
    context=dict(
        ns="haha",
        bias="left",
        URL=url,
        author=author,
        date=date,
        text=text,
        flag=1
    )
    return render_template('results.html', **context)

@app.route('/select',methods=['GET','POST'])
def select():
    if request.method == "POST":

        req = request.form['menu']
        obj=NewsSource.query.filter_by(name=req).first_or_404()
        print(obj)

        return render_template('results.html',ns=req, bias=obj.bias,URL=obj.URL, flag=0)
    return render_template('index.html',ns=news_sources)

if __name__=='__main__':
    # add_to_db()
    app.run(debug=True)


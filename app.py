from flask import Flask, render_template, request
import pandas as pd
from flask_sqlalchemy import SQLAlchemy 
import pymongo
from pymongo import MongoClient 
import newspaper 
from newspaper import Article
import torch
import numpy as np
from transformers import BertTokenizer
from transformers import BertForSequenceClassification
from decouple import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('PostgreSQLURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
# newsources=pd.read_csv("final.csv")

class NewsSource(db.Model):
    name = db.Column(db.String(75),primary_key=True)
    URL = db.Column(db.String(75))
    bias=db.Column(db.String(15))

class Authors(db.Model):
    name=db.Column(db.String(100),primary_key=True)

class Articles(db.Model):
    title=db.Column(db.String(150))
    date=db.Column(db.DateTime())
    url=db.Column(db.String(300),primary_key=True)
    bias=db.Column(db.String(15))

class Writes(db.Model):
    author=db.Column(db.String(100),db.ForeignKey(Authors.name))
    article=db.Column(db.String(300),db.ForeignKey(Articles.url))
    __table_args__ = (
        db.PrimaryKeyConstraint('author', 'article'),
        {},
    )
class Writes_For(db.Model):
    author=db.Column(db.String(100),db.ForeignKey(Authors.name))
    newssource=db.Column(db.String(75),db.ForeignKey(NewsSource.name))
    __table_args__ = (
        db.PrimaryKeyConstraint('author', 'newssource'),
        {},
    )

class Contains(db.Model):
    article=db.Column(db.String(300),db.ForeignKey(Articles.url))
    newssource=db.Column(db.String(75),db.ForeignKey(NewsSource.name))
    __table_args__ = (
        db.PrimaryKeyConstraint('article', 'newssource'),
        {},
    )

# def add_to_db():
#     newsources=pd.read_csv('newsource.csv').reset_index(drop=True)
#     authors=pd.read_csv("authors.csv")
#     articles=pd.read_csv("articles.csv")
#     writes=pd.read_csv('writes.csv')
#     wf=pd.read_csv("writes_for.csv")
#     contains=pd.read_csv("contains.csv")

#     for i in range(len(newsources)):
#         name=newsources['Name'].iloc[i]
#         url=newsources['URL'].iloc[i]
#         bias=newsources['Bias'].iloc[i]
#         new = NewsSource(name=name, URL=url,bias=bias)
#         db.session.add(new)
#         db.session.commit()

#     for i in range(len(authors)):
#         name1=authors['Name'].iloc[i] 
#         name=(name1[:100]) if len(name1)>100 else name1
#         author=Authors(name=name)
#         db.session.add(author)
#         db.session.commit()

    
#     for i in range(len(articles)):
#         title1=articles['title'].iloc[i]
#         title=(title1[:150]) if len(title1)>150 else title1
#         date=articles[' date'].iloc[i]
#         url=articles[' url'].iloc[i]
#         bias=articles['Bias'].iloc[i]
#         article=Articles(title=title,date=date,url=url,bias=bias)
#         db.session.add(article)
#         db.session.commit()

#     for i in range(len(writes)):
#         url=writes['ArticleURL'].iloc[i]
#         name1=writes['Author'].iloc[i]
#         name=(name1[:100]) if len(name1)>100 else name1
#         w=Writes(author=name,article=url)
#         db.session.add(w)
#         db.session.commit()


#     for i in range(len(wf)):
#         name1=wf['Author'].iloc[i]
#         aname=(name1[:100]) if len(name1)>100 else name1
#         ns=wf['News Source'].iloc[i]
#         w=Writes_For(author=aname,newssource=ns)
#         db.session.add(w)
#         db.session.commit()



#     for i in range(len(contains)):
#         name=contains['Name'].iloc[i]
#         url=contains[' url'].iloc[i]
#         c=Contains(article=url,newssource=name)
#         db.session.add(c)
#         db.session.commit()


##Mongo Part
## This is my cluster , which is linked to my specific IP address
cluster=MongoClient(config('MongoDBURL'))
db1=cluster["test"] ##database name
collection =db1["test1"] ##collection

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', 
                                          do_lower_case=True)
                                          
label_dict={'center': 5,
 'left': 2,
 'leftcenter': 1,
 'nan': 4,
 'right': 0,
 'right-center': 3}

inverse_dic={
 5:'center',
 2:'left',
 1:'leftcenter',
 4:'nan',
 0:'right',
 3:'right-center'
}

model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                      num_labels=len(label_dict),
                                                      output_attentions=False,
                                                      output_hidden_states=False)
device=torch.device('cpu')
model.to(device)
model.load_state_dict(torch.load('finetuned_BERT_epoch_5.model',map_location=torch.device('cpu')))

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
    article.nlp()
    summary= article.summary
    title= article.title
    
    inputs = tokenizer(text, padding='max_length', return_tensors='pt',truncation=True)
    # print(len(inputs))
    model.eval()

    with torch.no_grad():
        outputs = model(**inputs)
    pred_labels = np.argmax(outputs[0].cpu().detach().numpy(), axis=1).tolist()

    ##Post is the data you want to enter into the database. Not specifying an ID generates a random one 
    post= {"author": author[0], "source":article.source_url, "content":text,"date":date,"summary":summary,"title":title}
    collection.insert_one(post)

    
    
    context=dict(
        ns=article.source_url,
        bias=inverse_dic[pred_labels[0]],
        URL=url,
        author=author,
        date=date,
        title=title,
        summary=summary,
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


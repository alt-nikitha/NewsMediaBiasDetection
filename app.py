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


    # textsplit=text.split(' ')
    # print(len(textsplit))
    # if(len(textsplit)>512):
    #     limittext=textsplit[:512]
    #     print(len(limittext))
    #     newtext=' '.join(limittext)
    # else:
    #     newtext=text
    
    inputs = tokenizer(text, padding='max_length', return_tensors='pt',truncation=True)
    # print(len(inputs))
    model.eval()

    with torch.no_grad():
        outputs = model(**inputs)
    pred_labels = np.argmax(outputs[0].cpu().detach().numpy(), axis=1).tolist()

    ##Post is the data you want to enter into the database. Not specifying an ID generates a random one 
    post= {"author": author[0], "source":article.source_url, "content":text,"date":date}
    collection.insert_one(post)

    # textsplit=text.split('.')
    # print(len(textsplit))
    # if(len(textsplit)>20):
    #     limittext=textsplit[:20]
    #     # print(len(limittext))
    #     newtext='.'.join(limittext)
    # else:
    #     newtext=text
    
    context=dict(
        ns="haha",
        bias=inverse_dic[pred_labels[0]],
        URL=url,
        author=author,
        date=date,
        # text=newtext,
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


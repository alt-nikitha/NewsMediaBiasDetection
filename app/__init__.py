
from decouple import config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, Blueprint
from app.models import db
from app.models import NewsSourceDropDown,NewsSource,Authors,Articles,Writes,Writes_For,Contains
import app.querySQL as q
import app.populate_db as pdb
import app.nlp as nlp
import pymongo
import newspaper 
from pymongo import MongoClient 


model,tokenizer=nlp.load_model_tokeniser() 

app = Flask(__name__ , static_url_path='', static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = config('PostgreSQLURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
def init_db():
    db.init_app(app)
# with app.app_context():
#     db.create_all()
#     pdb.add_to_db()

# Mongo Part
# This is my cluster , which is linked to my specific IP address
cluster=MongoClient(config('MongoDBURL'))
db1=cluster["test"] ##database name
collection =db1["test1"] ##collection
@app.route('/')
def index():
    
    return render_template('newindex.html')

@app.route('/detect',methods=['POST'])
def detect():
    url=request.form.get('name')
   
    
    date,summary,title,authors,bias,polarity,subjectivity,source_url,text=nlp.newspaper_extract(model,tokenizer,url)
    print(source_url)
    # nobj=newspaper.build(source_url)
    # nsname=nobj.brand
    nobj=NewsSource.query.filter_by(URL=source_url).first_or_404()
    nsname=nobj.name
    if(bias=='nan' or bias == None):
        bias='center'
    if(text):
        pdb.add_to_mongo(collection,date,summary,title,authors,source_url,text)
        if (len(authors) and source_url and bias):
            q.query_or_add(url,title,date,bias,authors, source_url)

            context=dict(
                ns=source_url,
                bias=bias,
                URL=url,
                authors=authors,
                date=date,
                title=title,
                summary=summary,
                nsname=nsname,
                
                polarity=polarity,
                subjectivity=subjectivity
                
            )
            
            return render_template('cards1.html', **context)
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')
    
    

@app.route('/select',methods=['POST'])
def select():

    req = request.form['menu']
    otherbias,bias,URL=q.find_same_bias_news(name=req)
    return render_template('results.html',ns=req, bias=bias,URL=URL,otherbias=otherbias)

@app.route('/temp',methods=['POST','GET'])
def temp():
    return render_template('temp.html',ns=q.get_drop_down())



@app.route('/author/<author>')
def author(author):
    
    otherartsbyauthor=q.find_same_author_articles(author)
    context=dict(
        author=author,
        otherartsbyauthor=otherartsbyauthor
    )
    return render_template('authors.html', **context)

@app.route('/bias/<label>')
def bias(label):
    
    otherartsbias=q.find_same_bias_articles(label)
    otherbiasns=q.find_same_bias_news(label=label)
    otherauthorsbias=q.find_same_bias_authors(label)
    context=dict(
        bias=label, 
        otherartsbias=otherartsbias,
        otherbiasns=otherbiasns,
        otherauthorsbias=otherauthorsbias
    )
    # return 'bias is' + label


    return render_template('bias.html',**context)

@app.route('/ns/<name>/<bias>')
def ns(name,bias):
    # name=request.args.get('name',None)
    otherartsinns=q.find_same_news_source_articles(name)
    otherauthsinns=q.find_same_news_source_author(name)
    otherbiasns=q.find_same_bias_news(label=bias)
    context=dict( 
        otherbiasns=otherbiasns,
        bias=bias,
        otherartsinns=otherartsinns,
        otherauthsinns=otherauthsinns,
        name=name
        )
    # return 'hi'+name
    return render_template('ns.html',**context)

if __name__ == "__main__":
    app.run(debug=True)
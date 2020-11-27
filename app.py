from flask import Flask, render_template, request
import pandas as pd
from flask_sqlalchemy import SQLAlchemy 

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

@app.route('/',methods=['GET','POST'])
def index():
    all_news_sources=NewsSource.query.order_by(NewsSource.name).all()
    news_sources=[]
    for ele in all_news_sources:
        news_sources.append(ele.name)
    # news_sources=newsources['Name'].to_list()
    if request.method == "POST":

        req = request.form['menu']
        obj=NewsSource.query.filter_by(name=req).first_or_404()
        print(obj)

        return render_template('results.html',ns=req, bias=obj.bias,URL=obj.URL)
    return render_template('index.html',ns=news_sources)

if __name__=='__main__':
    # add_to_db()
    app.run(debug=True)


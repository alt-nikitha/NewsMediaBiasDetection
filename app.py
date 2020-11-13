from flask import Flask, render_template
import pandas as pd
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])

def index():
    dataset=pd.read_csv("final.csv")
    news_sources=dataset['Name'].to_list()
    
    return render_template('index.html',ns=news_sources)


if __name__=='__main__':
    app.run(debug=True)


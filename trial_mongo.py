import pymongo
from pymongo import MongoClient 
import newspaper 
from newspaper import Article
## This is my cluster , which is linked to my specific IP address
cluster=MongoClient("mongodb+srv://neelb:NewsBiasDetect246@newsbiasdetection.bxxdo.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=cluster["test"] ##database name
collection =db["test1"] ##collection
#collection.insert_one(post)
#results = collection.delete_one({"_id":1})


#scraping section
url='https://www.nytimes.com/2020/11/27/opinion/2020-us-election-world-relations.html?action=click&module=Opinion&pgtype=Homepage'
article = Article(url)
article.download()
article.parse()
author =article.authors
date=article.publish_date
text= article.text

##Post is the data you want to enter into the database. Not specifying an ID generates a random one 
post= {"_id":2,"author": author[0], "source":article.source_url, "content":text,"date":date}

collection.insert_one(post)
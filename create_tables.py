import pandas as pd 
import re
import numpy as np
from urllib.parse import urlparse


# this is full dataset
df1= pd.read_csv('/content/drive/MyDrive/articleswithlabels.csv').reset_index(drop=True)

# replace empty brackets with np.nan
df1.loc[(df1[' authors']=="[]")," authors"]=np.nan

# get the required columns, NEEEL add the column for news_source url also here
newdf= df1[['title',' authors',' date',' url','Name','Bias']]

# remove rows with null values
index_with_nan = df1.index[df1.isnull().any(axis=1)]
df=df1.drop(index_with_nan,0).reset_index(drop=True)
print(df.columns)

def cleaner(name):
  s= name
  pattern= "\'(.*?)\'"
  substring = re.search(pattern, s)
  if(substring==None):
    pattern1= "\"(.*?)\""
    substring1 = re.search(pattern1, s).group(1)
  if(substring!=None):
    substring=substring.group(1)
    f=' '.join(substring.split()[:2])
  else:
    f=' '.join(substring1.split()[:2])
  return f;


# to create news_source.csv
def newsource():
  sliced=df[['Name','Bias',' url']]
  new=pd.DataFrame(columns=['Name','Bias','News_Source'])
  print(len(sliced))
  for i in range(len(sliced)):
    url=sliced[' url'][i]
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    row=pd.Series({"Name":sliced['Name'][i],"Bias":sliced['Bias'][i],"News Source":str(result)})
    new.loc[i]=row
    i=i+1
  new.to_csv('newsource.csv')

    # NEEEL use the name, bias, news_source url from df 

# to create authors.csv
def create_authors():
    # print(df[' authors'])
    authorsmixed=pd.unique(df[' authors'])
    # print(authorsmixed[-100:])

    
    authorslist=[] # create list of individual authors in the dataset
    for ele in authorsmixed:
        # this if condition isnt needed since i removed null values
        if(isinstance(ele,str)):

            # this removes the brackets surrounding the list of authors
            newele=re.match(r"\[([^\]]+)\]",ele)
        # if(newele):
        #     print(newele[1])
        try:

            # check if there are multiple authors separated by commas
            authorshere=newele[1].split(",")

            for author in authorshere:
                # NEEEEL here clean quotes and append that to authorslist instead 
                author = cleaner(author)
                authorslist.append(author)
        
        # if there is only one author
        except:
            # NEEEEL here clean quotes, same function as you use above to clean quotes, and append that to authorslist instead 
            author = cleaner(author)
            authorslist.append(author)

    # print(authorslist)

    # get unique authors, and also convert to lower case, because same author appears twice, once in title case, once in upper and all
    authors=sorted(set([x.lower() for x in authorslist]))

    #create new df for the authors.csv 
    newdf=pd.DataFrame(authors,columns=['Name'])
    newdff=newdf.drop_duplicates(subset='Name')
    for author 
    newdff.to_csv("authors.csv")

# to create articles.csv   
def create_articles():
    
    articles=df[['title',' date',' url','Bias']]
    
    # check if there are multiple rows with same article url
    newfinal=articles.drop_duplicates(subset=[' url'], keep='last')
    print(len(newfinal))
    newfinal.to_csv('articles.csv')

# to create works_for.csv
def create_works_for():
    works_for=pd.DataFrame(columns=['Author','News Source'])
    k=0
    for i in range(len(df)):
        
        author=df.loc[i][' authors']

        # again if condition not needed, same as what we did for create_authors 
        if(isinstance(author,str)):
            newele=re.match(r"\[([^\]]+)\]",author)
            try:
                authorshere=newele[1].split(",")

                for ele in authorshere:
                    # NEEEL here remove quotes from ele and then use that ele below
                    ele=cleaner(ele)
                    row=pd.Series({"Author":ele.lower(),"News Source":df.loc[i]['Name']})
                    works_for.loc[k]=row
                    k+=1
            except:
                print(author)
                # NEEEEL here remove quotes from newele and use the result below
                newele=cleaner(newele)
                row=pd.Series({"Author":newele.lower(),"News Source":df.loc[i]['Name']})
                works_for.loc[k]=row
                k+=1

    # drop duplicates if any
    newdf=works_for.drop_duplicates()
    print(len(newdf))
    newdf.to_csv("writes_for.csv")




# to create writes.csv
def create_writes():
    writes=pd.DataFrame(columns=['Author','ArticleURL'])
    k=0

    # same procedure as above
    for i in range(len(df)):
        
        author=df.loc[i][' authors']
        if(isinstance(author,str)):
            newele=re.match(r"\[([^\]]+)\]",author)
            try:
                authorshere=newele[1].split(",")
                for ele in authorshere:
                    # NEEEL here remove quotes from ele and then use that ele below
                    ele=cleaner(ele)
                    row=pd.Series({"Author":ele.lower(),"ArticleURL":df.loc[i][' url']})
                    writes.loc[k]=row
                    k+=1
            except:
                # NEEEEL here remove quotes from newele and use the result below
                newele=cleaner(newele)
                row=pd.Series({"Author":newele.lower(),"ArticleURL":df.loc[i][' url']})
                writes.loc[k]=row
                k+=1
    neww=writes.drop_duplicates()
    print(len(neww))
    neww.to_csv("writes.csv")


# to create contains.csv
def contains():
    contains=df[['Name',' url']]
    newc=contains.drop_duplicates()
    # print(newc)
    newc.to_csv('contains.csv')
    
    pass


# call all above functions, this will take a few minutes because drop duplicates takes time to search
# create_newssource()
create_authors()
create_articles()
create_works_for()
create_writes()
contains()
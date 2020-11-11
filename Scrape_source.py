import requests 
from bs4 import BeautifulSoup 
import pandas as pd


def make_soup(URL):
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup
     # If this line causes an error, run 'pip install html5lib' or install html5lib 




biases=['left','leftcenter','right-center','right','center']
# print(soup.prettify()) 

def make_csv(bias):
    URL = "https://mediabiasfactcheck.com/"
    abs_url=URL+bias+'/'
    soup=make_soup(abs_url)
    names=[]
    urls=[]
    for row in soup.select('tbody tr td'):
        try:
            soup1=make_soup(row.a['href'])
            table = soup1.select('div div div div article div p a')
            
            urls.append(table[-1]['href'])
            ind=row.a['href'][:-1].rfind('/')
            # print(row.a['href'])
            # data[table[-1]['href']]=row.a['href'][ind+1:-1]
            names.append(row.a['href'][ind+1:-1])
            # print(row.a['href'][ind+1:-1],"______",table[-1]['href'])
            
        except:
            continue
    data={'URL':urls,
            'Name':names}
    df=pd.DataFrame(data) 
    df.to_csv(bias+'.csv')  

for bias in biases:
    make_csv(bias)

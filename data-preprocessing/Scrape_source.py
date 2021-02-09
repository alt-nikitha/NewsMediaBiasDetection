import requests 
from bs4 import BeautifulSoup 
import pandas as pd

# create a beutiful soup representation of the content in given URL
def make_soup(URL):
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup
     # If this line causes an error, run 'pip install html5lib' or install html5lib 




biases=['left','leftcenter','right-center','right','center']
# print(soup.prettify()) 


def make_csv(bias):
    URL = "https://mediabiasfactcheck.com/"

    # get URL for given bias category
    abs_url=URL+bias+'/'

    # get soup for the page
    soup=make_soup(abs_url)

    names=[]
    urls=[]

    # for each row in the table in the page
    for row in soup.select('tbody tr td'):
        try:
            #make soup for the page whose URL is in the table row
            soup1=make_soup(row.a['href'])

            #obtain the relevant section that contains news source website URL and name
            table = soup1.select('div div div div article div p a')
            
            #append URL to urls
            urls.append(table[-1]['href'])

            ind=row.a['href'][:-1].rfind('/')
            # append name to names
            names.append(row.a['href'][ind+1:-1])
            
        except:
            continue
    
    # create a dictionary of URLs and names
    data={'URL':urls,
            'Name':names}
    # store dictionary as a dataframe
    df=pd.DataFrame(data) 

    # create csv file for the bias category
    df.to_csv(bias+'.csv')  

# to obtain csv files for each bias category
for bias in biases:
    make_csv(bias)

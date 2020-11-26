# News Media Bias Detection System

To develop this project from scratch, first create a virtual environment: <br>
` python3 -m venv env ` <br>

Activate the virtual environment <br>
` source env/bin/activate ` <br>

Install all the requirements for the project <br>
` pip install -r requirements.txt `<br>


## Data Collection 
We create 5 different files containing news source names and URLs for the 5 bias categories - ` left.csv, right.csv, leftcenter.csv, right-center.csv, right.csv, center.csv ` <br>

To create these 5 files run : <br>

` python Scrape_source.py ` <br>
 
Next, create a combined file ` final.csv ` that has news source names, their URLs and their bias categories, run: <br>

` python create_one_dataset.py `

## Data Preprocessing

We have used a readymade dataset from google news that contain multiple csv files.

To combine all of them into one ` all_articles.csv `, run : <br>
` python create_articles.py `

Next to join the news source bias labels with the above file to create the final dataset `articleswithlabels.csv`, run: <br>
` python article_labels.py `



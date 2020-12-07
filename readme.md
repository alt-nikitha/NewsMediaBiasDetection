# News Media Bias Detection System


With the rise of the digital age, the access that individuals have to the news has increased exponentially. This is undoubtedly great for the democratic process. However, what seems to be a huge flaw in the implementation of this has been the bias which exists within the media houses themselves. Individuals, unbeknownst to the bias in the news they read, are pigeonholed into a situation where truth to them is simply what media houses find will flare up their readership. In the process, we see massive misinformation campaigns , which crumble the democratic process by creating divisive, sensationalised news.
Motivated by this problem, we have created a tool which promises to provide the reader with the necessary context that they need before reading an article i.e its political bias.

## Working of the UI
As the User, you simply need to enter the URL linked to the article you want to analyse, and our tool will output the necessary information you need to get a clearer understanding of the news you read.
If you are interested in just learning about the general bias of news media houses instead of a specific article, we have you covered there too! We have a database of popular media houses and their biases stored, which you can choose from to better your understanding of the news you read.

## Methodology:
When the user enters a url linked to the article they would like to analyse ,this tool will first scrape the article, and store the necessary information in a MongoDB database. Following this, this information will be queried by our Fine-Tuned pre-trained BERT Model, which will classify the article as having a certain bias on the political spectrum. This data will be sent to a  PostgreSQL database, where it will be queried from based on the user’s choice selection in our UI.

The accuracy of the data we provide to you is backed by Media Bias Fact Check, a reputed organisation that provides bias information on news media houses. We have used the same bias labels we acquired from MBFC  in our training dataset as well.

<hr>

# Developing and Deploying this project 

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



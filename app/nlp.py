import pandas as pd
import newspaper 
from newspaper import Article
import torch
import numpy as np
from transformers import BertTokenizer
from transformers import BertForSequenceClassification
import pandas as pd
from textblob import TextBlob
from urllib.parse import urlparse



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

def load_model_tokeniser():

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', 
                                            do_lower_case=True)

    model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                        num_labels=len(label_dict),
                                                        output_attentions=False,
                                                        output_hidden_states=False)
    device=torch.device('cpu')
    model.to(device)
    model.load_state_dict(torch.load('app/finetuned_BERT_epoch_5.model',map_location=torch.device('cpu')))
    return model,tokenizer

def newspaper_extract(model,tokenizer,url):
    
    article = Article(url)
    article.download()
    article.parse()
    authors =article.authors
    date=article.publish_date
    text= article.text
    article.nlp()
    summary= article.summary
    title= article.title
    parsed_uri = urlparse(url)
    source_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    if(text and summary):
        inputs = tokenizer(text, padding='max_length', return_tensors='pt',truncation=True)
        # print(len(inputs))
        model.eval()

        with torch.no_grad():
            outputs = model(**inputs)
        pred_labels = np.argmax(outputs[0].cpu().detach().numpy(), axis=1).tolist()
        bias=inverse_dic[pred_labels[0]]
        ##Post is the data you want to enter into the database. Not specifying an ID generates a random one 
        
        sentiment=TextBlob(summary).sentiment


        return date,summary,title,authors,bias,sentiment.polarity,sentiment.subjectivity,source_url,text
    return None, None, None,None,None,None,None,None,None
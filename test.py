# import pandas as pd 

# all=pd.read_csv('articleswithlabels.csv')

# print(all.columns)

# print(all[['URL','Bias']])

# all[['URL','Bias']].to_csv("test.csv")
import torch
import numpy as np
from transformers import BertTokenizer
from transformers import BertForSequenceClassification
texts = "Across the country, suburban voters’ disgust with Mr. Trump — the key to Mr. Biden’s election — did not translate into a wide rebuke of other Republicans, as Democrats had expected after the party made significant gains in suburban areas in the 2018 midterm elections. From the top of the party down to the state level, Democratic officials are awakening to the reality that voters may have delivered a one-time verdict on Mr. Trump that does not equal ongoing support for center-left policies. “There’s a significant difference between a referendum on a clown show, which is what we had at the top of the ticket, and embracing the values of the Democratic ticket,” said Nichole Remmert, Ms. Skopov’s campaign manager. “People bought into Joe Biden to stop the insanity in the White House. They did not suddenly become Democrats.” That dawning truth is evident in the narrower majority that House Democrats will hold in Congress next year, and especially in the blood bath that the party suffered in legislative races in key states around the country, despite directing hundreds of millions of dollars and deploying top party figures like former President Barack Obama to obscure down-ballot elections. This year, Democrats targeted a dozen state legislative chambers where Republicans held tenuous majorities, including in Pennsylvania, Texas, Arizona, North Carolina and Minnesota. Their goal was to check the power of Republicans to redraw congressional and legislative districts in 2021, and to curb the rightward drift of policies from abortion to gun safety to voting rights. But in all cases, Democrats came up short. None of their targeted legislative chambers flipped, even though Mr. Biden carried many of the districts that down-ballot Democrats did not. It could make it harder for Democrats to retain a House majority in 2022."

# texts = sample['Title'].to_list()
# true_labels = sample['label'].to_list()
# Tokenise the texts and run the model:
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', 
                                          do_lower_case=True)
                                          
label_dict={'center': 5,
 'left': 2,
 'leftcenter': 1,
 'nan': 4,
 'right': 0,
 'right-center': 3}

inputs = tokenizer(texts, padding='max_length', return_tensors='pt')
model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                      num_labels=len(label_dict),
                                                      output_attentions=False,
                                                      output_hidden_states=False)
device=torch.device('cpu')
model.to(device)
model.load_state_dict(torch.load('finetuned_BERT_epoch_5.model',map_location=torch.device('cpu')))
model.eval()
with torch.no_grad():
    outputs = model(**inputs)
# Get the predicted labels
pred_labels = np.argmax(outputs[0].cpu().detach().numpy(), axis=1).tolist()
# print(f"text = {text}")
# print(f"true_labels = {true_labels}")
print(f"pred_labels = {pred_labels}")
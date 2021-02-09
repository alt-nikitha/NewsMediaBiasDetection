import pandas as pd

biases=['left','leftcenter','right-center','right','center']

# empty dataframe to store all news sources and their biases
final=pd.DataFrame(columns=['URL','Name','Bias'])

# read files for all biases and append their bias labels in bias column
for bias in biases:
    current=pd.read_csv(bias+".csv")
    removed=current.drop(['Unnamed: 0'],axis=1)
    removed['Bias']=bias
    frames = [final, removed]
    final = pd.concat(frames, sort=False)
    final.reset_index(drop=True)
    
    


# print(final)

#csv file with all news sources and bias labels
final.to_csv("final.csv")
import pandas as pd

biases=['left','leftcenter','right-center','right','center']
final=pd.DataFrame(columns=['URL','Name','Bias'])
for bias in biases:
    current=pd.read_csv(bias+".csv")
    # print(current.head())
    removed=current.drop(['Unnamed: 0'],axis=1)
    removed['Bias']=bias
    frames = [final, removed]
    final = pd.concat(frames, sort=False)
    final.reset_index(drop=True)
    
    


print(final)

final.to_csv("final.csv")
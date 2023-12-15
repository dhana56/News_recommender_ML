import numpy as np
import warnings
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings("ignore")

news = pd.read_csv("MegaZord.csv")

#randomly generating ratings
trial_user_rating_df = pd.DataFrame([[np.random.randint(0, 6) for i in range(len(news))] for user in range(50)], columns = news.index)

#random user chosen
user_id = np.random.randint(0,50)
#print(user_id)
#dummy variable recommend to compare ratings
recommend = pd.DataFrame(trial_user_rating_df)

#finding 5 closest neighbours of chosen user
cos_sim = pd.DataFrame(cosine_similarity(recommend))
neighbours = pd.DataFrame(cos_sim[user_id].sort_values(ascending=False)[1:6])

#changing the rating of viewed articles to 0 and unviewed articles according to weightage of and rating given by neighbours 
def new_func(trial_user_rating_df, user_id, neighbours, article, article_score, rating):
    article_score += neighbours[user_id][rating]*trial_user_rating_df[article][rating]

for article in recommend.columns:
    if recommend[article][user_id] == 0:
        article_score = 0
        for rating in neighbours.index:
            new_func(trial_user_rating_df, user_id, neighbours, article, article_score, rating)
        recommend.loc[user_id,article] = article_score
    else:
        recommend.loc[user_id,article] = 0
        
#sorting recommend row of user according to ratings 
recco = []
for i in recommend.columns:
    recco.append(recommend[i][user_id])   
recco = pd.DataFrame(recco)
recco = recco.sort_values(by = [0], ascending = False)[:10]

#appending news headline and link to empty dataframe output
output = pd.DataFrame(columns = ['Headline','News_Link'])
for i in recco.index:
    headline = news.iloc[i]['Headline']
    link = news.iloc[i]['News_Link']#[user_id]
    output = output.append({'Headline' : headline, 'News_Link' : link},ignore_index = True)
output.index+=1
print(output)
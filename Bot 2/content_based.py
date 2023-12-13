'''importing the required libraries '''
    
import pandas as pd
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import BOT1

# making the dataframe using the numpy module 
Dataframe = pd.read_csv("MegaZord.csv")

# printing the first 5 entries 
#print(Dataframe.head())
# making the dataframe using the numpy module 
#Dataframe = pd.read_csv("C:\\Users\\dhana\\OneDrive\\Desktop\\Conjoined.csv")
Dataframe.drop_duplicates(subset ="News_Link",
                    keep = False, inplace = True, ignore_index= True)



''' Using the Tf-idf vectorizer to conver the text file into the vector file '''


TFIDF= TfidfVectorizer(stop_words='english')

#converting the the texts into corresponding unicode values 
corpus = Dataframe[' cleaned_news'].values.astype('U')   

#converted unicodes are passing into the the tf-idf vectorizer 
X = TFIDF.fit_transform(corpus)
X


''' next  we are implementing the cosine similarity matrix based on the X vexctor by using the linear_kernel '''
cosinesimilarity = linear_kernel(X, X)

# printing the indices of the cleaned news entries
indices = pd.Series(Dataframe.index, index= Dataframe['Headline']).drop_duplicates()
##indices

#checking the indice variable gives the correct values for the news headings that we are providing  
#indices ['"Just Priceless": Shamita Shetty Shares Adorable Video With Shilpa Shetty And Their Mother']



# buliding the recommendation system function which  news that are based on the cosine similarity values 
def get_recommendation(titile, cosinesimilarity = cosinesimilarity):

    idx = indices[titile]
    cos_scores = enumerate(cosinesimilarity[idx])
    cos_scores =sorted(cos_scores, key = lambda x: x[1], reverse= True)
    cos_scores =cos_scores[1:11]
    
    for i in cos_scores:
    # print (i)
        cos_index = [i[0] for i in cos_scores]
            #  print(cos_index)
    print(Dataframe[['Headline','News_Link']].iloc[cos_index])
    #print(Dataframe[['News_Link']].iloc[cos_index])
#print(number_gen)
# entering the news and giving the recommendation based on the news headline that we are provided 

number_gen = np.random.randint(0, 10)
k = BOT1.bot1['Headline'][ number_gen]
get_recommendation(k)


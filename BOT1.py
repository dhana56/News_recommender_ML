'''importing the required libraries '''
import warnings
import sys
import subprocess
import pkg_resources


warnings.filterwarnings("ignore")

required = {'pandas', 'numpy', 'sklearn', 'pymongo'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import pymongo
import pandas as pd    
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans



client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')

#Creating a dataframe of the news articles
rom = pd.read_csv('MegaZord.csv')
bom =pd.DataFrame(rom)
bom.drop_duplicates(subset ="News_Link",
                     keep = False, inplace = True, ignore_index= True)
#print(bom)                     



#Array for vectorized news articles
total_corpus =[]
#print(len(bom[' cleaned_news']))
corpus = bom[' cleaned_news'].values.astype('U')

#running the for loops and getting the each values from the cleaned news entry
for i in range(len(bom[' cleaned_news'])):
    
    #corpus = [bom[' cleaned_news'].values.astype('U')[i]]    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([corpus[i]])
    #keyphrase =vectorizer.get_feature_names_out()    
    total_corpus.append(X.toarray())


''' we are taking the particular valuses from the data frames converting them in to the unicode values  '''

documents =bom[' cleaned_news'].values.astype('U')
documents1 =bom['Headline'].values.astype('U')


#do fitting ,transorm the documents, documents 1 data 
features = vectorizer.fit_transform(documents,documents1)


#applyinh the KMean clustering to find out the nearest neighbours 
k = 10
models =KMeans(n_clusters= k, init= 'k-means++', max_iter=100, n_init= 1)
models.fit_predict(features)


'''creating the newcolumn in the datframe and putting the clusterlabels of 
each news'''

bom['cluster_labels'] = models.labels_


#Printing cluster centroids
#print("Cluster centeroids : \n")
order_centeroids = models.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()
'''for i in range(k):
   # print("Cluster % d:" %i)
    for j in order_centeroids[i, : 10]:
        #print('%s' % terms[j])
    #print(' ---------------') '''   

    

#Creating Bot for new user

bot1= pd.DataFrame(columns=['Headline','Link'])
number_gen = np.random.randint(0, 20)
for g in range(10):
    df2=bom[bom['cluster_labels']== g] ['News_Link'].values[number_gen]
    df3=bom[bom['News_Link']==df2]['Headline'].values[0]
    bot1 = bot1.append([{'Link':df2, 'Headline':df3}],ignore_index = True)


#this is the output for new user 
print(bot1)
   
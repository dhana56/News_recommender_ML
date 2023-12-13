#importing required libraries
import warnings
warnings.filterwarnings("ignore")
import nltk
import string
from nltk.tokenize import word_tokenize  
from nltk.tokenize import sent_tokenize
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import csv

class TEXT_PROCESSING:
    def __init__(self,raw_text) :
        self.raw_text = raw_text
        
    def cleaninised_fun(self):

        raw_text_lowered = [ doc.lower() for doc in self.raw_text ]
        #print( raw_text_lowered )
        #word tokenization
        tokenise_text = [ word_tokenize(docs) for docs in raw_text_lowered ]
        #print(tokenise_text)
        # sentence tokenization
        #sent_token = [sent_tokenize(docs) for docs in raw_text]
        #print(sent_token)

        regex = re.compile('[%s]' %  re.escape(string.punctuation))  #removing punctuation
        #print( regex)
        tokenized_doc_no_punctuation = []
        for review in tokenise_text:            
            new_review = []
            for token in review:
                new_token = regex.sub(u'', token)
                if not new_token == u'' :
                    new_review.append(new_token)
            tokenized_doc_no_punctuation.append(new_review)
        #print( tokenized_doc_no_punctuation)
        #print(len( tokenized_doc_no_punctuation))
        tokenized_no_stopwords = []
        for doc in  tokenized_doc_no_punctuation:
            new_term_vector = []
            for word in doc:
                if not word in stopwords.words("english"): #removing stop words
                    new_term_vector.append(word)
            tokenized_no_stopwords.append(new_term_vector)
        #print(tokenized_no_stopwords)
        #print(len(tokenized_no_stopwords))
        preprocesed_doc = []
        porter =PorterStemmer()
        wordnet = WordNetLemmatizer()
        for doc in tokenized_no_stopwords:
            final_doc = []
            for word in doc :
                #final_doc.append(porter.stem(word))
                
                final_doc.append(wordnet.lemmatize(word)) # ---> lemmatization
                    #print(preprocesed_doc)
            #print(final_doc)        
            
                self.doc = (" ".join(final_doc))

            preprocesed_doc.append([self.doc])          
        print(preprocesed_doc)
        print(len(preprocesed_doc))
# csv file making section        

        file = open('g4g4.csv', 'w+', newline ='',encoding="utf-8")
  
# writing the data into the file
        with file:    
            write = csv.writer(file)
            write.writerows(preprocesed_doc)

            # code for the text file, if necessary
        '''for sent in preprocesed_doc:
            self.doc = ("".join(sent))
           # print([self.doc])
            print(len(self.doc))
            with open("cleaned.txt", "a+", encoding= 'utf-8') as f:
                f.writelines(self.doc)
            f.close()    '''
                      



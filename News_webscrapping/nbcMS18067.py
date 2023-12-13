# importing the required modules
from bs4 import BeautifulSoup as soup
import requests
import time

news_headlines = list()
news_links = list()
news_author= list()
news_time_date = list()
news_text = list()


keywords = ["", "/investigations","/politics", '/health', '/science''/?cid=eref:nbcnews:text','/culture-matters',
'/tech-media','/asian-america','/news/weather','/business','/nbcblk','/latino','/think','/health/coronavirus','/us-news','/health/coronavirus','/science/weird-science',
'/datagraphics''/nfl'
] 

for key_words in keywords:
    url = "https://www.nbcnews.com"+str(key_words)
    print(url)
    try:
            httml = requests.get(url)
            httml_content = soup(httml.content, 'lxml')
        #print(httml_content)


        #here we are making the lists that are contains the specific html tags for each websites
        #passing them into the corresponding values in the dictionaries ----line: 25, 29
            links = []
            path_tags_headlines = ["alacarte__text-wrapper","tease-card__info","wide-tease-item__info-wrapper flex-grow-1-m"]
            path_tags_links = ["alacarte__text-wrapper","tease-card__info","wide-tease-item__info-wrapper flex-grow-1-m","wide-tease-item__info-wrapper flex-grow-1-m"]

            for class_tags in path_tags_headlines:
                
                for link in httml_content.find_all("div" ,attrs={'class':class_tags}):
                    link.text
                    #print("Headline: {}".format(link.text))#head line of main page 

            for path_tag in path_tags_links:

                for news_link in httml_content.find_all("div", attrs={"class" : path_tag}):
                    #print( "newslinks:{}".format(news_link.find('a')['href']))

                    # # finding news links in the main page 
                    links.append(news_link.find('a')['href'])
                #print(links)
            print("NUMBER_of links: " + str(len(links)))
                
            #from here onwards it will start scrapping the  the rquired information with in each articles 
            for i in links:
                try :
                    
                    page = requests.get(i)
                    bsobl =soup(page.content,"lxml" )
                    

                    for news in bsobl.find_all('article',attrs={ "class" : "article-body"} ):
                        news.text.strip()
                        #print("NEWS ARTICLES HERE: {}".format(news.text.strip()))

                        #  html pages had different heading tags  
                        for news_name in bsobl.find_all("h1" or "h2"):
                            news_name.text   
                            print("news_name: {}".format(news_name.text))

                        for time in bsobl.find_all("time",attrs={'class': "relative z-1"}):
                            print("time: {}".format(time.text))

                        for author in  bsobl.find_all("div",attrs={'class': "article-inline-byline"}):   
                            print("author: {}".format(author.text)) 
                        print(i)
                        news_headlines.append(news_name.text)
                        news_links.append(i)
                        news_author.append(author.text)
                        news_time_date.append(time.text)
                        news_text.append(news.text.strip())
                            
                except:

                    pass
                             
            
    except:
        
        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        time.sleep(5)
        print("Was a nice sleep, now let me continue...")


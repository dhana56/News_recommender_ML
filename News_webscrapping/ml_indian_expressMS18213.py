'''importing the required modules '''
from bs4 import BeautifulSoup as soup
import requests
import time
keywords = ["", "/section/india","/section/sports/ipl",'/section/sports/cricket/','/olympics/','/section/entertainment/',
'/section/sports/']  # making keyworrds that will be use for the url
                                             #url generation 
for key_words in keywords:
    url = "https://www.indianexpress.com"+str(key_words)
    print(url)
    try:
            httml = requests.get(url)
            httml_content = soup(httml.content, 'lxml')

        #print(httml_content)
        #here we are making the lists that are contains the specific html tags for each websites

            links = []
            path_tags_headlines = ["top-news","ie-first-story m-premium","other-article first ","other-article ","snaps", "north-east-grid explained-section-grid"]
            path_tags_links = ["top-news","ie-first-story m-premium","other-article first ","other-article ","snaps","north-east-grid explained-section-grid"]

            for class_tags in path_tags_headlines:
                
                for link in httml_content.find_all("div",attrs={'class':class_tags}):
                    link.text
                    #print("Headline: {}".format(link.text))#head line of main page 
            for path_tag in path_tags_links:
                for news_link in httml_content.find_all("div", attrs={"class" : path_tag}):
                    #print( "newslinks:{}".format(news_link.find('a')['href']))# finding news links in the main page 
                    links.append(news_link.find('a')['href'])
                #print(links)
            print("NUMBER_of links: " + str(len(links)))

                #from here onwards it will start scrapping the  the rquired information with in each articles 

            for i in links:
                try :
                    page = requests.get(i)
                    bsobl =soup(page.content,"lxml" )
                    for news in bsobl.find_all('div',attrs={ "class" : "full-details"} ):
                        news.text.strip()
                        #print("NEWS ARTICLES HERE: {}".format(news.text.strip()))
                        #"""
                        for news_name in bsobl.find_all("h1" or "h2" or "h3"):  #  html pages had different heading tags  
                            print("news_name: {}".format(news_name.text))
                        for time in bsobl.find_all("span",attrs={'itemprop': "dateModified"}):
                            print("time: {}".format(time.text))
                        for author in  bsobl.find_all("a",attrs={'class': "bulletProj"}):   
                            print("author: {}".format(author.text))
                        #"""
                        print(i)
                except:
                    pass             

    except:
        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        time.sleep(5)
        print("Was a nice sleep, now let me continue...")

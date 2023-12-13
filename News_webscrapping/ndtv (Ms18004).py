# -*- coding: utf-8 -*-
"""NDTV.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aOIyR3nECVxjRKRcTseM0i8_YhWEKG0R
"""

import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

news_count_threshold = 1000
page_count = 0
news_count = 0
news_info = []

categories = {'business':['your-money', 'corporates','industries', 'cryptocurrency' , 'economy', 'earnings', 'latest'],
              'entertainment':['bollywood','hollywood','television']}
#'education':['latest-news' , 'exams-news' , 'school-news' , 'campus-news']

for category in categories:
        for subcategory in categories[category]:
            news_count = 1
            for page_ in range(1,15):
                if news_count <= news_count_threshold: 
                    news_url = "https://www.ndtv.com/{}/{}/page-{}".format(category, subcategory, page_)
                    #print(news_url)

                    try:
                      page = requests.get(news_url)

                      if page.status_code != 200:
                        print(page.status_code)
                        continue
                      
                      soup = BeautifulSoup(page.content , "html.parser")
                      #print(soup)

                      news_heading_tags = soup.find_all("h2", class_ = "newsHdng")
                      #print(news_heading_tags)

                      news_links_list = []
                      for news_heading_tag in news_heading_tags:
                        news_links_list.append(news_heading_tag.find_all("a")[0].get("href"))
                      #print(news_links_list)

                      for link in news_links_list:
                        time.sleep(2)

                        try:
                          page_in = requests.get(link)
                          time.sleep(2)
                          if page_in.status_code != 200:
                            print(page_in.status_code)
                            continue
                          
                          soup_in = BeautifulSoup(page_in.content , "html.parser")
                          #print(soup_in)

                          #Fetching Time

                          news_datetime_in = soup_in.find_all("span", itemprop = "dateModified")[0].get_text().strip()
                          news_datetime_in_list = news_datetime_in.split()[1:]
                          news_date_in = " ".join(news_datetime_in_list[:3])
                          news_time_in = " ".join(news_datetime_in_list[3:])
                          temp_news_info = [news_date_in, news_time_in, category, subcategory]
                          #print(news_time_in)

                          #Fetching Heading

                          news_heading_in = soup_in.find_all("h1", itemprop = "headline")
                          news_heading_in = news_heading_in[0].get_text().strip()
                          temp_news_info.append(news_heading_in)
                          #print(news_heading_in)

                          #Fetching Summary

                          news_summary_in = soup_in.find_all("h2", class_ = "sp-descp")
                          news_summary_in = news_summary_in[0].get_text().strip()
                          temp_news_info.append(news_summary_in)
                          #print(news_summary_in)

                          #Fetching Entire News

                          news_content_in = soup_in.find_all('p', class_ = None)
                          news_content_in = " ".join([news_content_in_para.get_text().strip() for news_content_in_para in news_content_in])
                          news_content_in = re.sub("Follow Us: \.+ Advertisement \.+", "", news_content_in)
                          temp_news_info.append(news_content_in)
                          #print(news_content_in)

                          #Fetching Author

                          news_author_in = soup_in.find_all("span", itemprop = "author")
                          news_author_in = news_author_in[0].get_text().strip()
                          temp_news_info.append(news_author_in)
                          #print(news_author_in)

                          #Fetching News Link

                          temp_news_info.append(link)

                          #Making Final list

                          news_info.append(temp_news_info)

                          if news_count == news_count_threshold:
                            news_count = news_count + 1
                            break
                          elif news_count < news_count_threshold:
                            news_count = news_count + 1



                        except Exception as e:
                                error_type, error_obj, error_info = sys.exc_info()
                                #print("Link:", link)
                                #print(error_type, "Line:", error_info.tb_lineno)
                                continue





                    except Exception as e:
                        error_type, error_obj, error_info = sys.exc_info()
                        #print("Link:", news_url)
                        #print(error_type, "Line:", error_info.tb_lineno)
                        continue

news_dataframe = pd.DataFrame(news_info, columns = ["Date", "Time", "Category", "Subcategory", "Heading", "Summary",
                                                 "Entire_News", "Author", 
                                                   "News_Link"])
news_dataframe.to_csv(r'NDTV.csv' , index = False)
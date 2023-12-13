import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

news_count_threshold = 1000
page_count = 1
news_count = 1
news_info = list()

news_count = 1

#categories = {'business':['your-money', 'corporates','industries', 'economy', 'earnings', 'latest'],
#             'entertainment':['bollywood','hollywood','television'], 'sports':[]}

categories = {'sports':['cricket', 'football', 'kabaddi', 'tennis']}

for category in categories:
        for subcategory in categories[category]:
            for page_ in range(1,10):
                if news_count <= news_count_threshold: 
                    news_url = "https://www.ndtv.com/{}/{}/page-{}".format(category, subcategory, page_) 
                
                    try:
                        page = requests.get(news_url)
                    
                        
                        if page.status_code != 200: 
                            print(page.status_code)
                            continue   

                        soup = BeautifulSoup(page.content, "html.parser")

                        news_heading_tags = soup.find_all("h2", class_ = "newsHdng")

                        news_links_list = list()
                        for news_heading_tag in news_heading_tags:
                            news_links_list.append(news_heading_tag.find_all("a")[0].get("href"))

                        for link in news_links_list:
                            # Delaying the Get Request by 2 Seconds 
                            time.sleep(2)

                            try:
                                page_in = requests.get(link)
                                
                                if page_in.status_code != 200:
                                    print(page.status_code)
                                    continue

                                soup_in = BeautifulSoup(page_in.content, "html.parser")

                                
                                # Fetching Date and Time 
                                news_datetime_in = soup_in.find_all("span", itemprop = "dateModified")[0].get_text().strip()
#                                print(news_datetime_in)
                                news_datetime_in_list = news_datetime_in.split()[1:]
                                news_date_in = " ".join(news_datetime_in_list[:3])
                                news_time_in = " ".join(news_datetime_in_list[3:])
                                temp_news_info = [news_date_in, news_time_in, category, subcategory]

                                # Fetching News Heading 
                                news_heading_in = soup_in.find_all("h1", itemprop = "headline")
#                                print(news_heading_in)
#                                print(len(news_heading_in))
#                                print("-"*120)
                                news_heading_in = news_heading_in[0].get_text().strip()
                                temp_news_info.append(news_heading_in)
                                
                                # Fetching News Summary 
                                news_summary_in = soup_in.find_all("h2", class_ = "sp-descp")
                                news_summary_in = news_summary_in[0].get_text().strip()
                                temp_news_info.append(news_summary_in)                                


                                # Fetching News Content 
                                news_content_in = soup_in.find_all('p', class_ = None)
#                                print(news_content_in)
#                                print(len(news_content_in))
                                news_content_in = " ".join([news_content_in_para.get_text().strip() for news_content_in_para in news_content_in])
                                news_content_in = re.sub("Follow Us: \.+ Advertisement \.+", "", news_content_in)
#                                print(news_content_in)
#                                print("*"*120)
                                temp_news_info.append(news_content_in)
                                
                                # Fetching News Author 
                                news_author_in = soup_in.find_all("span", itemprop = "author")
                                news_author_in = news_author_in[0].get_text().strip()
                                temp_news_info.append(news_author_in)                                


                                 # Adding URL to the temp_news_info List 
                                temp_news_info.append(link)

                                # Appending the temp_news_info List Into news_info List 
                                news_info.append(temp_news_info)

                                # Increasing the News Count by 1 Since the News Web Page has Successfully been Scraped 
                                if news_count == news_count_threshold: # round(news_count_threshold - (news_count_threshold/2)):
                                    news_count += 1
                                    break
                                elif news_count < news_count_threshold: # round(news_count_threshold - (news_count_threshold/2)):
                                    news_count += 1
                            
                            except Exception as e:
                                error_type, error_obj, error_info = sys.exc_info()
                                print("Link:", link)
                                print(error_type, "Line:", error_info.tb_lineno)
                                continue
                        
                    except Exception as e:
                        error_type, error_obj, error_info = sys.exc_info()
                        print("Link:", news_url)
                        print(error_type, "Line:", error_info.tb_lineno)
                        continue



news_dataframe = pd.DataFrame(news_info, columns = ["Date", "Time", "Category", "Subcategory", "Heading", "Summary",
                                                    "Entire_News", "Author", 
                                                    "News_Link"])


news_dataframe.to_csv('MS18158_SohamMKor_06_04_2022.csv', index=False)#Writing to csv file
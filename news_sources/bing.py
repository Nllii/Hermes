
import requests
from bs4 import BeautifulSoup
import re
import pprint


def bing_search(search_term):
    """
    This function takes a search term and returns a list of news sources
    """
    bing_search = []
    for news_search in search_term:
        url = f"https://www.bing.com/news/search?q={news_search}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for news_card in soup.find_all('div', class_="news-card-body"):
            title = news_card.find('a', class_="title").text
            article_link = news_card.find('a', class_="title").get('href')
            try:
                time = news_card.find(
                    'span',
                    attrs={'aria-label': re.compile(".*ago$")}
                ).text
                bing_search.append({
                    'title': title,
                    'article_link': article_link,
                    'time': time
                })
            except Exception as e:
                bing_search.append({
                    'title': title,
                    'article_link': article_link,
                    'time': None
                })
                print("ERROR, getting time " + str(e))
                continue
    print("bing_search: ",bing_search)
    return bing_search

            # except  Exception as e:
            #     continue
    # pprint.pprint(bing_search)
    return bing_search



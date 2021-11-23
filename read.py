import requests
from news_sources.bing import bing_search
from news_sources.bloomberg import bloomberg_current_news



class read_articles:
    def __init__(self, search_term,url = None):
        self.search_term = search_term
        articles = self.get_articles()
     

    def get_articles(self):
        for x_articles in self.search_term:
            print("finding and reading articles: %s " % x_articles)
            bing_search(x_articles)
            bloomberg_current_news(x_articles)

            



        

read_articles(search_term = ["hello", "world"])
import requests
import pprint
import datetime



def bloomberg_current_news(ticker,country = None):
    """
    ticker = list[]
    country: default to US if not specified:
    :sometimes this shit isn't updated from bloomberg: FUCK bloomberg!
    """
    if country is None:
        country = "US"
    for ticker_symbol in ticker:
        print(ticker_symbol)
        cookies = {
        }

        headers = {
            'If-None-Match': '"*"',
        }
        
        params = (
            ('template', 'STOCK'),
            ('id', f'{ticker_symbol}:{country}'),
        )
        params_updated = (
            ('contentCliff', 'false'),
        )
        response = requests.get('https://cdn-mobapi.bloomberg.com/wssmobile/v1/security/stories', headers=headers, params=params, cookies=cookies)
        bloomberg_articles = response.json()
        print(f"searching for: {ticker_symbol}")
        for article in bloomberg_articles['stories']:
            card = article['card']
            published_date = article['published']
            article_day = datetime.datetime.fromtimestamp( int(published_date))
            article_day_published = article_day.strftime("%Y-%m-%d")
            stories_title = article['title']
            stories_link = article['links']['self']['href']
            if card == "article":
                text_append = []
                internal_id = article['internalID']
                article_updated = requests.get(f'https://cdn-mobapi.bloomberg.com/{stories_link}', headers=headers, params=params_updated, cookies=cookies)
                article_updated_json = article_updated.json()
                for items_text in article_updated_json['components']:
                    for keys,value in items_text.items():
                        if keys == 'parts':
                            for parts_text in value:
                                for fucking_text, pwned_fucking_text in parts_text.items():
                                    if fucking_text == 'text':
                                        if pwned_fucking_text is not None:
                                            # join \n together to make it easier to read
                                            text_append.append(pwned_fucking_text.replace("\n", " "))
                                        else:
                                            text_append.append("")
                text_append = " ".join(text_append)
                return text_append, internal_id, stories_title, stories_link, article_day_published
                # if len(text_append) > 0:
                #     print(f"found articles text for: {ticker_symbol}")
                #     sentiments, neg, pos, neu,label = text_processing_api(text_append)
                #     polarity, sentiment_sub, sentiment = local_sentiment(text = text_append)
                #     if sentiments is not None:
                #         # print(f"text_processing_api: {text_append}")
                #         bloomberg_cdn_data = {
                #             "source":"bloomberg",
                #             "text": text_append,
                #             "internal_id": internal_id,
                #             "ticker": ticker_symbol,
                #             "country": country,
                #             "title": stories_title,
                #             "date": article_day_published,
                #             "link": stories_link,
                #             "sentiment_analysis_api":{
                #                 "sentiment": sentiments,
                #                 "neg": neg,
                #                 "pos": pos,
                #                 "neu": neu,
                #                 "label": label,

                #             },
                #             "sentiment_analysis_local":{
                #                 "polarity": polarity,
                #                 "sentiment_sub": sentiment_sub,
                #                 "sentiment": sentiment,
                #             }
                #         }
                #         pprint.pprint(bloomberg_cdn_data)
                #         print(f"saved to database: {ticker_symbol}")
                #     else:
                #         print(f"didn't find  articles text for :{ticker_symbol}")





# def text_processing_api(text):
#     """
#     This function takes a text and returns a dictionary with the polarity and subjectivity of the text:
#     I think there is a 1000 per day ip limit on the text processing api.
#     """


#     sentimentURL = "http://text-processing.com/api/sentiment/"
#     payload = {'text': text}
#     try:
#         post = requests.post(sentimentURL, data=payload) 
#     except requests.exceptions.RequestException as re:
#         print("Exception: requests exception getting sentiment from url caused by %s" % re)
#         raise
#     if post.status_code != 200:
#         print("Can't get sentiment from url caused by %s %s" % (post.status_code, post.text))
#         return None

#     response = post.json()
#     neg = response['probability']['neg']
#     pos = response['probability']['pos']
#     neu = response['probability']['neutral']
#     label = response['label']

#     if label == "neg":
#         sentiments = "negative"
#     elif label == "neutral":
#         sentiments = "neutral"
#     else:
#         sentiments = "positive"
#     # print("online_api_sentiment: " + sentiments)
#     print("neg: %s, pos: %s, neu: %s, label: %s" % (neg, pos, neu, sentiments))
#     return sentiments, neg, pos, neu,label


# def local_sentiment(text):
#     """
#     This function takes a text and returns a dictionary with the polarity and subjectivity of the text:
#     """
#     sentiment_url = None
#     text_tb = TextBlob(text)
#     analyzer = SentimentIntensityAnalyzer()
#     text_vs = analyzer.polarity_scores(text)

#     # determine sentiment from our sources
#     if sentiment_url is None:
#         if text_tb.sentiment.polarity < 0 and text_vs['compound'] <= -0.05:
#             sentiment = "negative"
#         elif text_tb.sentiment.polarity > 0 and text_vs['compound'] >= 0.05:
#             sentiment = "positive"
#         else:
#             sentiment = "neutral"
#     else:
#         if text_tb.sentiment.polarity < 0 and text_vs['compound'] <= -0.05 and sentiment_url == "negative":
#             sentiment = "negative"
#         elif text_tb.sentiment.polarity > 0 and text_vs['compound'] >= 0.05 and sentiment_url == "positive":
#             sentiment = "positive"
#         else:
#             sentiment = "neutral"

#     # calculate average polarity from TextBlob and VADER
#     polarity = (text_tb.sentiment.polarity + text_vs['compound']) / 2

#     # output sentiment polarity
#     # print("_____________________________________________________________")
#     print("on_device Sentiment: Sentiment (algorithm): " + str(sentiment))
#     # print("Sentiment Polarity: " + str(round(polarity, 3)))

#     # output sentiment subjectivity (TextBlob)
#     # print("Sentiment Subjectivity: " + str(round(text_tb.sentiment.subjectivity, 3)))

#     # output sentiment
#     # print("Sentiment (url): " + str(sentiment_url))
#     # print("Overall sentiment (textblob): ", text_tb.sentiment) 
#     # print("Overall sentiment (vader): ", text_vs) 
#     # print("sentence was rated as ", round(text_vs['neg']*100, 3), "% Negative") 
#     # print("sentence was rated as ", round(text_vs['neu']*100, 3), "% Neutral") 
#     # print("sentence was rated as ", round(text_vs['pos']*100, 3), "% Positive") 
#     # print("************")

#     return polarity, text_tb.sentiment.subjectivity, sentiment

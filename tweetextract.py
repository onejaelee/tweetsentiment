# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:12:25 2022

@author: One
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax


import tweepy

#Loading roberta model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', "Positive"]

def preprocessTw(tweet):
    proctweet = []
    for word in tweet.split(' '):
        if len(word) > 0:
            if word[0] == '@' and len(word) > 1:
                word = "@user"
            elif word.startswith('http'):
                word = "http"
        proctweet.append(word)
    tweetproc = " ".join(proctweet)
    return tweetproc


#Initialize keys from your Twitter Dev Account
APIKey = "consumerkey"
APISecret = "consumersecret"
accessToken = "accesstoken"
accessTokenSecret = "accesstokensecret"



auth = tweepy.OAuthHandler(APIKey, APISecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#Keyword or hashtag to search
keyword = "mango"
#quantity of tweets to input
countTweet = 2
#YYYY- MM-DD
dateuntil = "2022-12-02"
#Fetch tweets, you need elevated access for this
#Filtering retweets, searching by keywords, only English tw
tweets = tweepy.Cursor(api.search_tweets, q= keyword + " -filter:retweets", lang = "en",until=dateuntil, tweet_mode = 'extended').items(countTweet)

#iterate through tweets and print
count = 0

for tweet in tweets:
    print(tweet.full_text)
    encodedtw = tokenizer(preprocessTw(tweet.full_text), return_tensors = "pt")
    output = model(**encodedtw)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    print(scores)
    print(tweet.full_text)
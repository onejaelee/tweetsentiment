# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:12:25 2022

@author: One
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax


import tweepy


def preprocessTw(tweet):
    for word in tweet.split(' '):
        if word[0] == '@' and len(word) > 1:
            word = "@user"
        elif word.startswith('http'):
            word = "http"
        tweet.append(word)
    tweetproc = " ".join(tweet)
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

#Fetch tweets, you need elevated access for this
tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang = "en").items(countTweet)

#iterate through tweets and print
for tweet in tweets:
    print(tweet)
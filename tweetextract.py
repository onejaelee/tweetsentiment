# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:12:25 2022

@author: One
"""




import tweepy

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
countTweet = 5

#Fetch tweets, you need elevated access for this
tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(countTweet)

#iterate through tweets and print
for tweet in tweets:
    print(tweet)
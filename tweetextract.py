# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:12:25 2022

@author: One
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pandas as pd
from os.path import exists
import tweepy

from datetime import date
from datetime import timedelta
import time



#Loading roberta model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', "Positive"]

#Initialize keys from your Twitter Dev Account
APIKey = "consumerkey"
APISecret = "consumersecret"
accessToken = "accesstoken"
accessTokenSecret = "accesstokensecret"

auth = tweepy.OAuthHandler(APIKey, APISecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

today = date.today()

#YYYY- MM-DD - use current date to extract tweet
dateuntil = today.strftime("%Y-%m-%d")
#Keyword or hashtag to search
keyword = "#chainsawman"


#quantity of tweets to input PER DAY, must be broken down into chunks <=100
tweetsPerQ= 5
totalTweets = 10

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

def processTweet(tweets):
    data = {"Negative":[], "Neutral":[],"Positive":[],"id":[],"created_at":[], "text":[]}
    for tweet in tweets:
        #print(tweet.full_text)
        encodedtw = tokenizer(preprocessTw(tweet.full_text), return_tensors = "pt")
        output = model(**encodedtw)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        print(scores,tweet.created_at)
        #Add probability scores to corresponding column
        data["Negative"].append(scores[0])
        data["Neutral"].append(scores[1])
        data["Positive"].append(scores[2])
        
        data["id"].append(tweet.id)
        data["text"].append(tweet.full_text)
        data["created_at"].append(tweet.created_at)
        last_id = tweet.id
        
    return data, last_id



#Fetch tweets, you need elevated access for this
#Filtering retweets, searching by keywords, only English tw

if exists(keyword + "sentiment.pkl"):
    df = pd.read_pickle(keyword + "sentiment.pkl")
    last_id = max(df.index)
    prev_last_date = max(df.created_at.dt.date)
    
    curr_date = prev_last_date
    #last_time = max(df.created_at)
    
    while (curr_date <= today):
        dateuntil = curr_date.strftime("%Y-%m-%d")
        tweetsDone = 0
        
        while(totalTweets>tweetsDone):
            tweets = api.search_tweets(q= keyword + " -filter:retweets",count=tweetsPerQ, lang = "en",until = dateuntil,since_id = last_id, tweet_mode = 'extended')
            data,last_id = processTweet(tweets)
            df_today = pd.DataFrame(data)
            df_today = df_today.set_index("id")
            df = df.append(df_today)
            tweetsDone += tweetsPerQ
            time.sleep(2)
        
        curr_date = curr_date + timedelta(days=1)
        
        time.sleep(60*16)
    df.to_pickle(keyword + "sentiment.pkl")
    print(df)
    
else:
    curr_date = today - timedelta(days=6)
    dateuntil = curr_date.strftime("%Y-%m-%d")
    
    tweetsDone = 0
    
    tweets = api.search_tweets(q= keyword + " -filter:retweets", lang = "en",count=tweetsPerQ,until = dateuntil, tweet_mode = 'extended')
    data,last_id = processTweet(tweets)
    df = pd.DataFrame(data)
    df = df.set_index("id")
    tweetsDone += tweetsPerQ
    print("hey")
    while(totalTweets>tweetsDone):
        tweets = api.search_tweets(q= keyword + " -filter:retweets",count=tweetsPerQ, lang = "en",until = dateuntil,since_id = last_id, tweet_mode = 'extended')
        data,last_id = processTweet(tweets)
        df_today = pd.DataFrame(data)
        df_today = df_today.set_index("id")
        df = df.append(df_today)
        tweetsDone += tweetsPerQ
        time.sleep(2)
        print("hello")

    print("what")
    curr_date = curr_date + timedelta(days=1)
    #time.sleep(60*16)
    time.sleep(30)
    print("the")
    while (curr_date <= today):
        dateuntil = curr_date.strftime("%Y-%m-%d")
        tweetsDone = 0
        while(totalTweets>tweetsDone):
            tweets = api.search_tweets( q= keyword + " -filter:retweets",count=tweetsPerQ, lang = "en",until = dateuntil,since_id = last_id, tweet_mode = 'extended')
            data,last_id = processTweet(tweets)
            df_today = pd.DataFrame(data)
            df_today = df_today.set_index("id")
            df = df.append(df_today)
            tweetsDone += tweetsPerQ
            time.sleep(2)
        
        curr_date = curr_date + timedelta(days=1)
        time.sleep(30)
        #time.sleep(60*16)
        
    df.to_pickle(keyword + "sentiment.pkl")
    print(df)
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:12:25 2022

@author: One
"""


import tweepy

#Initialize keys from your Twitter Dev Account
consumerKey = "consumerkey"
consumerSecret = "consumersecret"
accessToken = "accesstoken"
accessTokenSecret = "accesstokenseceret"


auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)
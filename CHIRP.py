#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 12:15:13 2020

@author: thunderspark
"""
#############################################################################
#IMPORT TIME
import tweepy as tp
import pandas as pd
import sys
#############################################################################

class Tweet:    
    
    '''
    Objective: This class is for capsuling all API related methods.
    
    Authorization used: OAuth 1.0
    
    Params : 
    ------    
    twitter_keys : dict type object- API consumer and Access Keys

    methods defined : 
            
            __int__(self,twitter_keys)
                API Instance Constructor
            
            OAuth_API_create(self)
            woeid_find(self,name)
            trends_extract(self,id_place,api)
            tweet_pull(self,keywords,api)
            scour()
                

    '''
    
    def __init__(self,twitter_keys):
        
        '''
        Parameters
        ----------
        twitter_keys : Dictionary with API consumer key,consumer key secret, 
                       access token and access token secret. Use latest tokens. 

        Returns
        -------
        None

        '''


        self.consumer_key=twitter_keys['consumer_key']
        self.consumer_secret=twitter_keys['consumer_secret']
        self.access_token=twitter_keys['access_token_key']
        self.access_secret=twitter_keys['access_token_secret']


        
    def OAuth_API_create(self):
        
        '''
        Returns
        -------
        api : an object of tweepy.API

        '''
        
        auth=tp.OAuthHandler(consumer_key=self.consumer_key ,consumer_secret=self.consumer_secret)
        auth.set_access_token(key=self.access_token,secret=self.access_secret)
        api=tp.API(auth)
        return api
    
    def woeid_find(self,name):
        
        '''
        Parameters
        ----------
        name : str type- Name of a place

        Returns
        -------
        WOE ID or Where On Earth Id of given name

        '''
        
        woeid=pd.read_csv('/Users/satyadev/ML Projects/woeid.csv')
        flag=False
        for i in range(len(woeid)):
            if name == woeid['name'][i]:
                flag=True
                return (woeid['woeid'][i])
        if flag==False:
            print('Type Y to re enter country:')
            choice=input().lower()
            if choice=='y':
                self.trends_extract()
            else:
                sys.exit()
            
    def user_pull(self):
        '''
        

        Parameters
        ----------
        name : str type- screen name or handle name of the user.
        api : tweepy.API type object-Object that has the OAuth authorization loaded.

        Returns
        -------
        tweets : list type- Tweets by the handle that was passed as argument

        '''

        print('Enter screen name of the twitter handle: ')
        name=input()
        api=self.OAuth_API_create()
        user_tweets=api.user_timeline(screen_name=name,tweet_mode='extended')
        tweets=[]
        try: 
            for i in range(len(user_tweets)):
                tweets.append(user_tweets[i].full_text)
        except tp.TweepError:
            print('Could not authenticate your request. Verify your consumer key and your consumer key secret.')
            print('Type Y to retry:')
            choice=input().lower()
            if choice=='y':
                self.user_pull(name)    
            else:
                sys.exit()
            
        return tweets
        
                                

    def trends_extract(self):
        
        '''
        Parameters
        ----------
        id_place : int type-WOE Id of a place
        api : Tweepy.API type object- Object that has OAuth Authorization tokens loaded.

        Returns
        -------
        trend : list of str objects- Trends on Twitter based on Geographical location.

        '''
        api=self.OAuth_API_create()    
        print('Enter country name: ')
        name=input().lower()
        woe_id=self.woeid_find(name)
        try:
            trends_id=api.trends_place(id=woe_id)
            trend=[]
            trends_id=dict(trends_id[0])
            trends_id=trends_id['trends']
            for i in range(len(trends_id)):
                trend.append(trends_id[i]['name'])
            
        except tp.TweepError:
            print('Could not authenticate your request. Verify your consumer key and your consumer key secret.')
            print('Type Y to retry:')
            choice=input().lower()
            if choice=='y':
                self.trends_extract(woe_id)    
            else:
                sys.exit()
        return trend
        
        
        
    def tweet_pull(self):
        
        '''
        Parameters
        ----------
        keywords : list or str obj- Words that you want to look for in tweets.
            
        api : Tweepy.API type object- Object that has OAuth Authorization tokens loaded.

        Returns
        -------
        tweets : Someweird jackshit I still haven't figured out

        '''
        print('Enter search word: ')
        name=input().lower()
        api=self.OAuth_API_create()        
        tweets=[]
        try:
            tweets.append(api.search(q=name))
        except tp.TweepError:
            print('Could not authenticate your request. Verify your consumer key and your consumer key secret.')
            print('Type Y to retry:')
            choice=input().lower()
            if choice=='y':
                self.tweet_pull(name)    
            else:
                sys.exit()
            
        return tweets

        

            
        
        
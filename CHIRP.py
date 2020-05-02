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
    Authorization Keys and Tokens: 
    twitter_keys = {
        'consumer_key':        'U4W8eBUcHUs8mYSfVreqbbMN7',
        'consumer_secret':     'SzNG09CQ4kH2BTskYkXhxZa2XlcBM2qCdql4tBFgdFRn3h53VE',
        'access_token_key':    '1255208873591357440-rIB7vF1eeFeWZpEvNZb37lN0o4Y06B',
        'access_token_secret': 'gVoK9ORmYvUjVv0efZv8ZAv6zy6Vo6yK6t4njUkkN3HZy'
    }
    
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
                self.scour()
            else:
                sys.exit()
                                

    def trends_extract(self,id_place,api):
        
        '''
        Parameters
        ----------
        id_place : int type-WOE Id of a place
        api : Tweepy.API type object- Object that has OAuth Authorization tokens loaded.

        Returns
        -------
        trend : list of str objects- Trends on Twitter based on Geographical location.

        '''
        
        try:
            trends_id=api.trends_place(id=id_place)
            trend=[]
            trends_id=dict(trends_id[0])
            trends_id=trends_id['trends']
            for i in range(len(trends_id)):
                trend.append(trends_id[i]['name'])
            return trend
        except tp.TweepError:
            print('Could not authenticate your request. Verify your consumer key and your consumer key secret.')
            print('Type Y to retry:')
            choice=input().lower()
            if choice=='y':
                self.trends_extract(id_place)    
            else:
                sys.exit()
        
        
    def tweet_pull(self,keywords,api):
        
        '''
        Parameters
        ----------
        keywords : list or str obj- Words that you want to look for in tweets.
            
        api : Tweepy.API type object- Object that has OAuth Authorization tokens loaded.

        Returns
        -------
        results : Someweird jackshit I still haven't figured out

        '''
        
        results=[]
        for i in range(len(keywords)):
            results.append(api.search(q=keywords[i],count=1))
        return results

        
    def scour(self):
        '''
        
        Returns
        -------
        tweets : Someweird jackshit I still haven't figured out
        '''
        
        
        
        print('Enter country name: ')
        name=input().lower()
        woe_id=self.woeid_find(name)
        api=self.OAuth_API_create()
        trends=self.trends_extract(woe_id,api)
        tweets=self.tweet_pull(trends,api)         
        return tweets
        
                    


            
        
        
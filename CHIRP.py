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
#CLASS DECLARATION
#############################################################################
class Tweet:    
    '''
    Class Tweet to '''
    
    def __init__(self,twitter_keys):

        self.consumer_key=twitter_keys['consumer_key']
        self.consumer_secret=twitter_keys['consumer_secret']
        self.access_token=twitter_keys['access_token_key']
        self.access_secret=twitter_keys['access_token_secret']
        
        
    def OAuth_API_create(self):
        
        auth=tp.OAuthHandler(consumer_key=self.consumer_key ,consumer_secret=self.consumer_secret)
        auth.set_access_token(key=self.access_token,secret=self.access_secret)
        api=tp.API(auth)
        return api
    
    def woeid_find(self,name):
        
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
        
        results=[]
        for i in range(len(keywords)):
            results.append(api.search(q=keywords[i],count=1))
        return results

        
    def scour(self):
        
        print('Enter country name: ')
        name=input().lower()
        woe_id=self.woeid_find(name)
        api=self.OAuth_API_create()
        trends=self.trends_extract(woe_id,api)
        tweets=self.tweet_pull(trends,api)         
        return tweets
        
                    


            
        
        
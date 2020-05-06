#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 23:53:42 2020

@author: satyadev
"""

import CHIRP
from keras.models import model_from_json
import time
import pre_model

class Integrator:
    def __init__(self):
        json_file=open('model_json.json','r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights("model-2.h5")
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        
        
    def twitter_dev(self):
        print('Please enter your developer crendentials(OAuth1): ')
        consumer_key=input('Consumer_Key: ')
        consumer_key_secret=input('Consumer Key Secret: ')
        access_key=input('Access Key: ')
        access_key_secret=input('Access Key Secret:')
        print('Let us now pray these are correct. Thank you.')
        twitter_keys={'consumer_key':consumer_key,'consumer_secret':consumer_key_secret,
                           'access_token_key':access_key,'access_token_secret':access_key_secret}
        time.sleep(3)
        return twitter_keys


    def tweet_analyser(self):
        twitter_keys=self.twitter_dev()
        tweep=CHIRP.Tweet(twitter_keys)
        tweets=tweep.user_pull()
        tester=pre_model.Pre_Model('whateverman')
        model_inp=tester.data_tokenize_test(tweets)
        y=[o for o in self.model.predict(model_inp)]
        return y
        
        
        

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 23:33:21 2020

@author: thunderspark
"""
#############################################################################
import pandas as pd
import re
import string
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.tokenize import word_tokenize
#############################################################################
class Model:
    """Class to """
    
    def __init__(self,path):
        self.path=path
        self.true=pd.read_csv(self.path+'true.csv')
        self.fake=pd.read_csv(self.path+'fake.csv')
        
    def conc(self):
        data=pd.concat(objs=[self.true,self.fake],axis=0)
        data=data.drop(labels=['subject','date'],axis=1)
        return data
###    
    def rem_links(self,text):
        text=re.sub(r"http\S+","",text)
        return text
    
    def lower_text(self,text):
        text=text.lower()
        return text
    
    def rem_punct(self,text):
        text=text.translate(str.maketrans(dict(string.punctuation)))
        return text
    
    def rem_white(self,text):
        text=text.strip()
        return text
    
    def rem_line(self,text):
        text=text.replace('\n','')
        return text
    
    def number(self,text):
        text=re.sub(r"\d",'',text)
        return text
    
    def pipe_text(self,text):
        cleaner=[self.rem_line,self.rem_links,self.rem_punct,self.rem_white,self.lower_text,self.number]
        for func in cleaner:
            text=func(text)
        return text
####     
    def token_it(self,text):
        tokens=word_tokenize(text)
        return tokens
    
    def dont_stop_me_now(self,text):
        unstopped_words=[word for word in text if word not in ENGLISH_STOP_WORDS]
        return unstopped_words
    
    def lemmatize(self,text):
        lem=WordNetLemmatizer()
        lemmed=[lem.lemmatize(word) for word in text]
        return lemmed
    def pipe_token(self,text):
        pre_process=[self.token,self.dont_stop_me_now,self.lemmatize]
        for func in pre_process:
            text=func(text)
        
#####
    def preprocess(self):
        data=self.conc()
        data['text']=self.pipe_text(data['text'])
        data['text']=self.pipe_token(data['text'])
        data['title']=self.pipe_text(data['title'])
        data['title']=self.pipe_token(data['title'])
        for i in range(len(data)):
            data['text'][i]=data['text'][i]+data['title'][i]
        data=data.drop(labels=['title'],axis=1)
        return data
        

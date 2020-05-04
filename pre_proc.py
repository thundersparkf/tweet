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
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.tokenize import word_tokenize
import numpy as np

#############################################################################
class Pre_Proc:
    '''
    Objective: This class is for cleaning the data set.
    '''
    
    
    
    
    
    def __init__(self,path):
        self.path=path
        true=self.path+'/True.csv'
        fake=self.path+'/Fake.csv'
        mixed=self.path+'/train.csv'
        self.true=pd.read_csv(true)
        self.false=pd.read_csv(fake)
        self.mixed=pd.read_csv(mixed)
        self.true['veri']=1
        self.false['veri']=0
        self.mixed=self.mixed.rename({'label':'veri'})
        print('MIXXED COLS: ',self.mixed.columns)
        print('MIXED UNIQUE: ',np.unique(self.mixed['veri']))
        
        
        
    def conc(self):
        data=pd.concat(objs=[self.true,self.false],axis=0)
        print('CONCAT ONE: 'np.unique(data['veri']))
        named=['title','text','veri']
        col_names=[]
        col_names1=[]
        for name in data.columns:
            if name not in named:
                col_names.append(name) 
        for name in self.mixed.columns:
            if name not in named:
                col_names1.append(name) 
        data=data.drop(labels=col_names,axis=1)
        print('CONCAT TWO: ',np.unique(data['veri']))
        print(self
        self.mixed=self.mixed.drop(labels=col_names1,axis=1)
        print('MIXED DROP KE BAAD: ',np.unique(self.mixed['veri']))
        data=pd.concat(objs=[self.mixed,data],axis=0)
        data.index=[x for x in range(len(data))]
        print(data.tail(100))
        print(np.unique(data['veri']))
        return data
###    
    def rem_links(self,text):
        text=re.sub(pattern=r"http\S+",repl="",string=str(text))
        return text
    
    def lower_text(self,text):
        text=text.lower()
        return text
    
    def rem_punct(self,text):
        text=text.translate(str.maketrans(dict.fromkeys(string.punctuation)))
        return text
    
    def rem_white(self,text):
        text=text.strip()
        return text
    
    def rem_line(self,text):
        text=text.replace('\n',' ')
        return text
    
    def number(self,text):
        text=re.sub(pattern=r"1234567890",repl="",string=str(text))
        return text
    
    def pipe_text(self,text):
        cleaner=[self.rem_links,self.rem_punct,self.rem_white,self.lower_text,self.rem_line,self.number]
        for func in cleaner:
            text=func(text)

        return text
####     
    def token_it(self,data,name):
        data[name]=data[name].apply(lambda x: word_tokenize(str(x)))
        return data
    
    #def Stemmer(self,data,name):
     #   stem=PorterStemmer()
      #  data[name]=data[name].apply(lambda x: [stem.stem(word) for word in x])
       # return data
    
    def dont_stop_me_now(self,data,name):
        data[name]=data[name].apply(lambda x: [word for word in x if word not in ENGLISH_STOP_WORDS])
        return data
    
    def lemmatize(self,data,name):
        lem=WordNetLemmatizer()
        data[name]=data[name].apply(lambda x: [lem.lemmatize(word) for word in x])
        return data
    
    def pipe_token(self,data,name):
        pre_process=[self.token_it, self.dont_stop_me_now, self.lemmatize]
        for func in pre_process:
            data=func(data,name)
        return data
        
#####
    def preprocess(self):
        data=self.conc()
        data['text']=data['text'].apply(lambda x: self.pipe_text(x))
        data['title']=data['title'].apply(lambda x: self.pipe_text(x))
        data=self.pipe_token(data,'text')
        data=self.pipe_token(data,'title')

        #print(type(data))
        for i in range(len(data)):
            data['text'].iloc[i]=str(data['text'].iloc[i])+str(data['title'].iloc[i])
 
        data=data.drop(labels=['title'],axis=1)
        
        return data
    
#################

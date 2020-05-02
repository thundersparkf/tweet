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
from sklearn.feature_extraction.text import CountVectorizer


#############################################################################
class Pre_Proc:
    """Class to """
    
    def __init__(self,path):
        self.path=path
        true=self.path+'True.csv'
        #fake=self.path+'Fake.csv'
        self.data=pd.read_csv(true,nrows=5)
        #self.false=pd.read_csv(fake,nrows=5)
        self.data['veri']=1
        #self.false['veri']=0
        
        
    def conc(self):
        #data=pd.concat(objs=[self.true,self.false],axis=0)
        data=self.data
        data.index=[x for x in range(len(data))]
        data=data.drop(labels=['subject','date'],axis=1)
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
        text=re.sub(r"\d",'',text)
        return text
    
    def pipe_text(self,text):
        cleaner=[self.rem_line,self.rem_links,self.rem_punct,self.rem_white,self.lower_text,self.number]
        for func in cleaner:
            text=func(text)
        return text
####     
    def token_it(self,data):
        data['text'] = df.apply(lambda x: nltk.word_tokenize(data['text'][x]))
        
        #counts.append()
        return counts
    
    def dont_stop_me_now(self,text):
        unstopped_words=[word for word in text if word not in ENGLISH_STOP_WORDS]
        return unstopped_words
    
    def lemmatize(self,text):
        lem=WordNetLemmatizer()
        lemmed=[lem.lemmatize(word) for word in text]
        return lemmed
    def pipe_token(self,text):
        pre_process=[self.dont_stop_me_now,self.lemmatize]
        return text
        
#####
    def preprocess(self):
        data=self.conc()
        data['text']=self.pipe_text(data['text'])
        data['title']=self.pipe_text(data['title'])
        data['text']=self.pipe_token(data)
        data['title']=self.pipe_token(data)

        #print(type(data))
        for i in range(len(data)):
            data['text'].iloc[i,]=str(data['text'].iloc[i,])+str(data['title'].iloc[i,])
 
        data=data.drop(labels=['title'],axis=1)
        print(data.head())
        
        return data
    
#################
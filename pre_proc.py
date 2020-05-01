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
class Pre_Proc:
    """Class to """
    
    def __init__(self,path):
        self.path=path
        true=self.path+'True.csv'
        fake=self.path+'Fake.csv'
        self.true=pd.read_csv(true,nrows=5)
        self.false=pd.read_csv(fake,nrows=5)
        self.true['veri']=1
        self.false['veri']=0
        
        
    def conc(self):
        data=pd.concat(objs=[self.true,self.false],axis=0)
        
        data.reset_index
        data=data.drop(labels=['subject','date'],axis=1)
        print("SELFCONC",data.head())
        return data
###    
    def rem_links(self,text):
        text=re.sub(pattern=r"http\S+",repl="",string=str(text))
        print('\nOP without links',text)
        return text
    
    def lower_text(self,text):
        text=text.lower()
        print('\nOP in lowercase',text)
        return text
    
    def rem_punct(self,text):
        text=text.translate(str.maketrans(dict.fromkeys(string.punctuation)))
        print('\nOP without Punctuation',text)
        return text
    
    def rem_white(self,text):
        text=text.strip()
        print("\nOP without Whitespaces")
        return text
    
    def rem_line(self,text):
        text=text.replace('\n',' ')
        print("OP without lines")
        return text
    
    def number(self,text):
        text=re.sub(r"\d",'',text)
        print('OP wihtout Numbers',text)
        return text
    
    def pipe_text(self,text):
        cleaner=[self.rem_line,self.rem_links,self.rem_punct,self.rem_white,self.lower_text,self.number]
        for func in cleaner:
            text=func(text)
        print('PIPE TEXT',text)
        return text
####     
    def token_it(self,text):
        text=str(text)
        tokens=word_tokenize(text)
        print('\nOP tokened',tokens)
        return tokens
    
    def dont_stop_me_now(self,text):
        unstopped_words=[word for word in text if word not in ENGLISH_STOP_WORDS]
        print('\nOP stop words gone',unstopped_words)
        return unstopped_words
    
    def lemmatize(self,text):
        lem=WordNetLemmatizer()
        lemmed=[lem.lemmatize(word) for word in text]
        print('\nOP lemmed',lemmed)
        return lemmed
    def pipe_token(self,text):
        pre_process=[self.token_it,self.dont_stop_me_now,self.lemmatize]
        for func in pre_process:
            text=func(text)
        print('\n\n\nPIPETOKEN',text)
        print('AFTER',len(text))
        return text
        
#####
    def preprocess(self):
        data=self.conc()
        print(data.head())
        data['text']=self.pipe_text(data['text'])
        data['title']=self.pipe_text(data['title'])
        data['text']=self.pipe_token(data['text'])
        data['title']=self.pipe_text(data['title'])
        print('BEFORE',len(data['title']))
        data['title']=self.pipe_token(data['title'])

        #print(type(data))
        print("CLEAN OVER",data.head())
        for i in range(len(data)):
            print("NONE Test",data['text'].iloc[i,])
            data['text'].iloc[i,]=str(data['text'].iloc[i,])+str(data['title'].iloc[i,])
            data['veri'].iloc[i,]=data['veri'].iloc[i,]
 
        data=data.drop(labels=['title'],axis=1)
        
        return data
    
#################
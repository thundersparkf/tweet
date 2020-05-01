#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 12:00:24 2020

@author: thunderspark
"""
maxlen = 2000
max_features = 50000
embed_file= '/Users/satyadev/Downloads/glove/glove.6B.300d.txt'
###################
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

import pre_proc

###########################
class Pre_Model:
    def __init__(self):
        self.df=pre_proc.Pre_Proc.preprocess()
        
    def train_test(self,data):
        x_train,x_test,y_train,y_test=train_test_split(x=data['text'],y=data['veri'],test_size=0.2,random_state=666)
        return x_train,x_test,y_train,y_test
    
    def keras_token(self,x_train,x_test):
        tokenize=Tokenizer(num_words=max_features)
        tokenize.fit_on_texts(x_train)
        return tokenize
    
    def data_tokenize(self,x_train,x_test):
        tokenize=self.keras_token(x_train,x_test)
        x_train_features=np.array(tokenize.texts_to_sequences(x_train))
        x_test_features=np.array(tokenize.texts_to_sequences(x_test))
        x_train_features=pad_sequences(x_train_features,maxlen=maxlen)
        x_test_features=pad_sequences(x_test_features,maxlen=maxlen)
        return x_train_features,x_test_features,tokenize
    
    def get_coef(self,word,*arr):
        return word,np.asarray(*arr,dtype='float32')
    
    def embedding(self,x_train,x_test,tokenize):
        emb_index=dict(self.get_coef(*o.split(' '))for o in open(embed_file))
        all_emb=np.stack(emb_index.values())
        emb_mean,emb_std=all_emb.mean(),all_emb.std()
        emb_size=all_emb.shape(1)
        
        word_index=tokenize.word_index
        nb_words=min(max_features,len(word_index))
        emb_mat=np.random.normal(emb_mean,emb_std,(nb_words,emb_size))
        
        for word,i in word_index.items():
            if i>=max_features: continue
            emb_vect=emb_index.get(word)
            if emb_vect is not None:
                emb_mat[i]=emb_vect
        return emb_size,emb_mat
    
    def pre_mod(self):
        x_train,x_test,y_train,y_test=self.train_test(self.df)
        x_train,x_test,tokenize=self.data_tokenize(x_train, x_test)
        emb_size,emb_mat=self.embedding(x_train, x_test, tokenize)
        return x_train,x_test,y_train,y_test,emb_size,emb_mat
        
        
    
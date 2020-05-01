#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:05:47 2020

@author: thunderspark
"""



############################

from keras.layers import Dense, Input, LSTM, Embedding, CuDNNGRU, Dropout
from keras.layers import Bidirectional,GlobalMaxPool1D
from keras.models import Model

import pre_model

########################
class Model:
    def __init__(self):
        obj=pre_model.Pre_Model()
        self.x_train,self.x_test,self.y_train,self.y_test,self.emb_size,self.emb_mat=obj.pre_mod()
    
    def Model_train(self):
        inp=Input(shape=(pre_model.maxlen,))
        x=Embedding(pre_model.max_features,self.emb_size,weights=[self.emb_mat])(inp)
        x=Bidirectional(CuDNNGRU(64, return_sequences=True))(x)
        x=GlobalMaxPool1D()(x)
        x=Dense(16,activation='relu')(x)
        x=Dropout(0.1)(x)
        x=Dense(1,activation='sigmoid')
        model=Model(inputs=inp,outputs=x)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        print(model.summary())
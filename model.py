#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:05:47 2020

@author: thunderspark
"""



############################

from keras.layers import Dense, Input, LSTM, Embedding, Dropout
from keras.layers import Bidirectional,GlobalMaxPool1D
from keras.models import Model
import matplotlib.pyplot as plt 
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score, confusion_matrix
from sklearn.utils import class_weight
import numpy as np
import pre_model

########################
class Model_class:
    def __init__(self,data_path):
        obj=pre_model.Pre_Model(data_path)
        self.x_train,self.x_test,self.y_train,self.y_test,self.emb_size,self.emb_mat=obj.pre_mod()
    
    def Model_create(self):
        inp=Input(shape=(pre_model.maxlen,))
        x=Embedding(pre_model.max_features, self.emb_size)(inp)
        x=Bidirectional(LSTM(64, return_sequences=True))(x)
        x=GlobalMaxPool1D()(x)
        x=Dense(16,activation='relu')(x)
        x=Dropout(0.2)(x)
        x=Dense(1,activation='sigmoid')(x)
        model=Model(inputs=inp,outputs=x)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        print(model.summary())
        return model
    def Model_train(self):
        model=self.Model_create()
        model.layers[1].trainable = False
        class_weights=class_weight.compute_class_weight('balanced',np.unique(self.y_train),self.y_train)
        history = model.fit(self.x_train, self.y_train, batch_size=2048, epochs=5, validation_data=(self.x_test, self.y_test),shuffle=True,class_weight=class_weights)
        self.graph(history)
        self.predic(model)
        return history,model
    def graph(self, history):
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        
    def predic(self,model):
        y_pred_train=[1 if o>0.5 else 0 for o in model.predict(self.x_train)]
        y_pred_test=[1 if o>0.5 else 0 for o in model.predict(self.x_test)]
        acc_tra,f1_tra,pre_tra,rec_tra=accuracy_score(self.y_train,y_pred_train),f1_score(self.y_train,y_pred_train),precision_score(self.y_train,y_pred_train),recall_score(self.y_train,y_pred_train)
        acc_test,f1_test,pre_test,rec_test=accuracy_score(self.y_test,y_pred_test),f1_score(self.y_test,y_pred_test),precision_score(self.y_test,y_pred_test),recall_score(self.y_test,y_pred_test)
        conf_train=confusion_matrix(self.y_train,y_pred_train)
        conf_test=confusion_matrix(self.y_test,y_pred_test)
        
        print('\n\n\nSTATSSSSSS BABYYYYY:\n\n')
        print('TRAINING DATA:\n\n\n')
        print('CONFUCIAN MATRIX: \n',conf_train)
        print('Accuracy: ',acc_tra)
        print('F1_Score: ',f1_tra)
        print('Preision: ',pre_tra)
        print('Recall: ',rec_tra)
        
        print('\n\n\nTESTING DATA:\n\n\n')
        print('CONFUCIAN MATRIX: \n',conf_test)
        print('Accuracy: ',acc_test)
        print('F1_Score: ',f1_test)
        print('Preision: ',pre_test)
        print('Recall: ',rec_test)

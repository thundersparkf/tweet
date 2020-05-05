#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:05:47 2020

@author: thunderspark
"""
import model
import pre_model
import integrator

def  load_model():

    data_path = input('Enter Path for Dataset: ')
    pre_model.embed_file = input('\n\nEnter path for GloVe file: ')
    model_obj=model.Model_class(data_path)
    history, trained=model_obj.Model_train()
    trained_json=trained.to_json()
    with open('model_json.json','w') as json_file:
        json_file.write(trained_json)
    trained.save_weights('model.h5')
        
def test():
    tweep=integrator.Integrator()
    pred=tweep.tweet_analyser()
    print('Here goes my hard work:')
    for y in pred:
        print(y)
            
def main():
    print('Type 1 for training model.\nType 2 for testing model. ')
    choice=int(input())
    if choice==1:
        load_model()
    else:
        test()
        
        
    
if __name__=='__main__':
    main()
    
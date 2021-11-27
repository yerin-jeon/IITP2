# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 17:31:06 2021

@author: tkdgu
"""

from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def CPC_embedding(model, CPC_definition, CPC_dict):
    
    subclass_list = CPC_dict['subclass_list']
    
    encoded_CPC = {}
    
    for i in subclass_list :
        encoded_CPC[i] = model.encode(CPC_definition[i].lower())
    
    encoded_CPC_ = []
    
    for temp in encoded_CPC.values() :   
        encoded_CPC_.append(temp)
        # encoded_CPC = np.append([encoded_CPC, temp])
    encoded_CPC_ = np.array(encoded_CPC)
        
    return(encoded_CPC)

def keyword_embedding(model, keyword_list) :
    
    text_list = keyword_list
    
    encoded_text = {}   
        
    for text in keyword_list :
        
        if text in encoded_text.keys() :
            text_embedding = encoded_text[text]
        else :
            text_embedding = model.encode(text)
            encoded_text[text] = text_embedding

    return(encoded_text)

def docs_embedding(model, docs) :
    
    embedding_result = model.encode(docs)
    
    return(embedding_result)
    
    
def get_sim_dist(encoded_cpc_array, encoded_keyword) :
    sim_list = []    
    
    for k,v in encoded_keyword.items() :
        
        cpc_embedding = encoded_cpc_array
        sim = cosine(v, cpc_embedding)
        sim_list.append(sim)
    
    return(sim_list)

def get_sim_matrix(cpc_list, encoded_CPC, encoded_keyword) :
        
    sim_df = pd.DataFrame(columns = cpc_list, index = encoded_keyword.keys())
    
    for k,v in encoded_keyword.items() :
            
        for cpc in cpc_list :
            cpc_embedding = encoded_CPC[cpc]
            sim = cosine(v, cpc_embedding)
            sim_df[cpc][k] = sim
            
    return(sim_df)

def classify_keyword(sim_matirix) :
    
    DICT = {}
    for idx, row in sim_matirix.iterrows() :
        if all(word == 0 for word in row)  :
            DICT[idx] = 'Unknown'
        else :
            DICT[idx] = 'Known'
            
    return(DICT)



        # for col in sim_matirix.columns : 
            
        
    
    
# def get_standard(sim_matrix):
    
    # standard = {}
    
                # mean = np.mean(sim_list)
                # var = np.var(sim_list)
                # total_df = total_df.append([[mean,var]], ignore_index=1)
            
        # total_df.columns = ['MEAN' , 'VAR']
            
        # MEAN = np.mean(total_df['MEAN'])
        # VAR = np.mean(total_df['VAR'])
        
        # standard[level] = (MEAN, VAR)
            
        # level +=1
            
    # return(total_df)
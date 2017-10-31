# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 19:28:54 2017

@author: Jadon
"""

import numpy as np
import itertools


def single_ts(players):
    #first shuffle the list
    shuffle = np.random.permutation(players).tolist()
    gen_ts = list()
    
    for i in np.arange(0,len(shuffle), 2):
        gen_ts.append([shuffle[i], shuffle[i+1]])
        print(i)
    return gen_ts    

l = ["a","b","c","d","e","f","g","h"]

s = single_ts(l)

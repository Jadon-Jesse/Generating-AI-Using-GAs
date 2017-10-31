# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 18:13:05 2017

@author: Jadon
"""
import sys

print("Hello"+ sys.argv[1])

file = open("ou.txt","w")
file.write(str(sys.argv[1]))
file.close()
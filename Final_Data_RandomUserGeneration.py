# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:28:43 2020

@author: Nathan
"""

import random as rnd
import json

users = list(range(1,50))
user = 0
user_data = {}

for i in users:
    Ratings = []
    Books = []
    
    num_books = rnd.randint(1,50)
    
    for i in range(0,num_books):
        Ratings.append(rnd.randint(1,5))
        Books.append(rnd.randint(1,))
    user+=1
    #user_data['User ' + str(user)] = 
print(Ratings)
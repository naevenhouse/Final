# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 19:35:50 2020

@author: Nathan
"""

class rating():
    book_ID = 0
    rating = 0

class user_info:
    ratings = []
    
    def AddRating(self, rating):
        self.ratings.append(rating)
        
    def Distance(self, user):
        for item in self.ratings:
            
        
    def GetRating(self):
        return self.ratings
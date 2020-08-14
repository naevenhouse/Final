# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 15:37:01 2020

@author: Nathan
"""

import time
import pandas as pd
import seaborn as sns

t_0 = time.time()
df = pd.read_csv('Processed_data.csv')
sett = pd.read_csv('Settings.csv')

counts = []

for key in sett['Genres']:
    val = df[key].sum()
    counts.append((key,val))
    
output = pd.DataFrame(counts, columns = ['Genre', 'Count'])

sns.barplot(data=output,y = 'Genre', x = 'Count')
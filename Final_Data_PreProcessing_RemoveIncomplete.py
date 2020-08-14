# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 15:13:45 2020

@author: Nathan
"""
import time
import pandas as pd

t_0 = time.time()
df = pd.read_csv('Compiled_data.csv', low_memory=False)
df_reduced = df.loc[df['Classified'] == True]
df_reduced.to_csv('Processed_data.csv', index = False)

print('Runtime: ' + str(time.time() - t_0))
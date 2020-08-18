# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 15:37:01 2020

@author: Nathan
"""

import pandas as pd
import seaborn as sns

#loads in the data
df = pd.read_csv('Processed_data.csv')
sett = pd.read_csv('Settings.csv')

#data storage array
counts = []

#iteration through genres
for key in sett['Genres']:
    val = df[key].sum()
    counts.append((key,val))

#Gets the data into a formatted dataframe for plotting
output = pd.DataFrame(counts, columns = ['Genre', 'Count'])

#plots data
sns.barplot(data=output,y = 'Genre', x = 'Count')
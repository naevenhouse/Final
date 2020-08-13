# -*- coding: utf-8 -*-
"""
ECE 5831
Final
Nathaniel Evenhouse
"""
#required packages
import os
import time
import pandas as pd
from goodreads import client
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import matplotlib.pyplot as plt

dataFolder = 'Data'

#initialize client for goodreads
gc = client.GoodreadsClient('fm1h6CpTTcPHEgwUAvOD1w', 'l62WO2kz3lmJifV7VkGZY4SAcWzkjtUw3Unj7zjE')
gc.authenticate('fm1h6CpTTcPHEgwUAvOD1w', 'l62WO2kz3lmJifV7VkGZY4SAcWzkjtUw3Unj7zjE')

#get the data files from the directory
dataFiles = os.listdir(dataFolder)

#gets time for exection time tracking
t0 = time.time()

#getting data paths
dataFiles = os.listdir('Data')

#loads in the datasets
df = {}
for file in dataFiles:
    df[file] = pd.read_csv(dataFolder+'/'+file, error_bad_lines = False)
    #df[file].index = df[file]['Id']
    
#append loaded dataframes
df_all = df[dataFiles[0]]
first = True
for file in dataFiles:
    if first:
        first=False
    else:
        df_all.append(df[file])

df=df_all

#pulls data from goodreads website
genres = []
i=0
for ID in df['Id']:
    try:
        book = gc.book(ID)
        if book.popular_shelves:
            genres.append(book.popular_shelves)
        if i%10 == 0:
            print(i/10)
            print(genres)
            break
        i+=1
        time.sleep(1)
    except:
        print("error in ID: " + str(ID))
        break

#adds data from list to dataframe
df['Genres'] = np.asarray(genres)

#remove unncessary columns
df.drop(['Publisher'], axis=1)

#fixing rating counts and converting to usable data
df['RatingDist1'] = df['RatingDist1'].str[2:].astype(float,errors = 'ignore')
df['RatingDist2'] = df['RatingDist2'].str[2:].astype(float,errors = 'ignore')
df['RatingDist3'] = df['RatingDist3'].str[2:].astype(float,errors = 'ignore')
df['RatingDist4'] = df['RatingDist4'].str[2:].astype(float,errors = 'ignore')
df['RatingDist5'] = df['RatingDist5'].str[2:].astype(float,errors = 'ignore')
df['RatingDistTotal'] = df['RatingDistTotal'].str[6:].astype(float,errors = 'ignore')
df['Rating'] = df['Rating'].astype(float,errors = 'ignore')
df['Name'] = pd.Categorical(df['Name'])
df['Publisher'] = pd.Categorical(df['Publisher'])
df['Language'] = pd.Categorical(df['Language'])
df['Authors'] = pd.Categorical(df['Authors'])

#pull additional data from Goodreads

print(df.head())

#print(df.dtypes)

#dataset = tf.data.Dataset.from_tensor_slices(df.values)




#processing time overall
print("runtime: " + str(time.time()-t0) + " seconds")
































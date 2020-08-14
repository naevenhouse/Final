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

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

dataFolder = 'Data'
settings  = pd.read_csv('Settings.csv',error_bad_lines = False)

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
    
#append loaded dataframes
df_all = df[dataFiles[0]]
first = True
for file in dataFiles:
    if first:
        first=False
    else:
        df_all = df_all.append(df[file], ignore_index=True)

df=df_all

for genre in settings['Genres']:
    df[genre]=False
df['Classified'] = False

#remove unncessary columns
#df = df.drop(['Publisher'], axis=1)

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
#print(df.keys())
#print(df.dtypes)

df.to_csv('Compiled_Data.csv', index=False)
#dataset = tf.data.Dataset.from_tensor_slices(df.values)

#processing time overall
print("runtime: " + str(time.time()-t0) + " seconds")


# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 17:53:53 2020

@author: Nathan
"""

import time
import pandas as pd
import tensorflow as tf
from tensorflow import keras

t_0 = time.time()
df = pd.read_csv('Processed_data.csv')

layers = [256,192,128,1]



df = df.fillna(0)

i = 0
numeric_keys = []
df_train = pd.DataFrame()
for key in df.keys():
    if df[key].dtypes!=str and df[key].dtypes!=object:
        numeric_keys.append(key)
    i+=1

df_train = df[numeric_keys]
df_train = df_train.astype('float64')


model = keras.Sequential()

for i in layers:
    model.add(tf.keras.layers.Dense(i))

model.compile(optimizer='adam', 
              loss=tf.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.build((None, len(df_train.loc[0])))

j=0
inp=1




while inp>=0:
    print('Book to rate: '+df.loc[j][8])
    
    inp = input('Enter a book rating: ')
    inp = float(inp)
    stuff = tf.constant(df_train.loc[j])
    y = model(stuff)
    model.fit(df_train.loc[j], inp)
    j=j+1
    
#predictions = model.predict(val_dataset)
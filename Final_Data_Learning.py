# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 17:53:53 2020

@author: Nathan
"""

import time
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn import preprocessing
import random as rnd

t_0 = time.time()
df = pd.read_csv('Processed_data.csv')

Network = [40,20,1]

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

x = df_train.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_train = pd.DataFrame(x_scaled)

num_books = len(df_train[df_train.keys()[0]])
print(num_books)

inputs = keras.Input(shape=len(df_train.loc[0]))
dense = layers.Dense(Network[0], activation = 'relu')
x = dense(inputs)

i = 1
for item in range(1,len(Network)-1):
    x = layers.Dense(Network[i], activation='relu')(x)
    i+=1
outputs = layers.Dense(1)(x)
model = keras.Model(inputs=inputs, outputs = outputs, name='Learned_user')

model.summary()

model.compile(
    loss='mse',
    optimizer='Adam',
    metrics=["mae"],
)

inp=1
while inp>=-10:
    j = rnd.randint(0,num_books)
    print('Book to rate: '+df.loc[j][8])
    pred = model.predict([list(df_train.loc[j])])
    print('Prediction: ' + str(pred*10))
    inp = input('Enter actual desired book rating: ')
    inp = float(inp)/10
    if inp>=0:
        history = model.fit([list(df_train.loc[j])], [inp], batch_size = 1, epochs = 1)

#predictions = model.predict(val_dataset)
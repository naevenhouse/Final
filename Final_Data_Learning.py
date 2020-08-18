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

#gets start time
t_0 = time.time()

#loads in data
df = pd.read_csv('Processed_data.csv')

#selects the shape of the network to build (sequential layer thickness).
Network = [256,128,64,32]

#replaces any na values in the dataframe with 0
df = df.fillna(0)

#Determines the numeric 
i = 0
numeric_keys = []
for key in df.keys():
    if df[key].dtypes!=str and df[key].dtypes!=object:
        numeric_keys.append(key)
    i+=1

#training data for the network, converts all data to floats
df_train = pd.DataFrame()
df_train = df[numeric_keys]
df_train = df_train.astype('float64')

#normalizes all of the data in the dataframe
x = df_train.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_train = pd.DataFrame(x_scaled)

#gets the number of books available for training
num_books = len(df_train[df_train.keys()[0]])
print(num_books)

#creates the network input layer based on the dataframe columns
inputs = keras.Input(shape=len(df_train.loc[0]))

#creates the first tensorflow network layer
dense = layers.Dense(Network[0], activation = 'relu')
x = dense(inputs)

#Creates all additional network laters
i = 1
for item in range(1,len(Network)):
    x = layers.Dense(Network[i], activation='relu')(x)
    i+=1

#Creates an output layer with 1 element
outputs = layers.Dense(1)(x)
model = keras.Model(inputs=inputs, outputs = outputs, name='Learned_user')

#reports a model summary to the user
model.summary()

#gives the network its learning settings, and initializes the network
model.compile(
    loss='mse',
    optimizer='Adam',
    metrics=["mae"],
)

#runs the learning in a loop until the user enters a value less than 0 for the 
#rating
inp=1
while inp>=0:
    j = rnd.randint(0,num_books)
    print('Book to rate: '+df.loc[j][8])
    pred = model.predict([list(df_train.loc[j])])
    print('Prediction: ' + str(pred*5.001))
    inp = input('Enter actual desired book rating: ')
    inp = float(inp)/5.001
    if inp>=0:
        history = model.fit([list(df_train.loc[j])], [inp], batch_size = 1, epochs = 1)

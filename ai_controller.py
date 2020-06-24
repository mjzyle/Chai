#!/usr/bin/python

import math
import tensorflow as tf
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import data_controller as dc
import boto3
from boto3.dynamodb.conditions import Key
from tensorflow import keras
from tensorflow.keras import layers


# Basic win/loss prediction network
def setup_model():
    model = keras.models.Sequential()
    model.add(layers.Dense(4, input_dim=128, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    #model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(0.001),
        #loss=tf.keras.losses.BinaryCrossentropy(),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    model.save('neural_network_model')


def train_model(eps=5):
    model = keras.models.load_model('neural_network_model')

    df = pd.read_csv('training_data.csv').drop(columns='Unnamed: 0')
    target = df.pop('win')
    dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))
    train_dataset = dataset.shuffle(len(df)).batch(1)

    model.fit(train_dataset, epochs=eps)

    model.save('neural_network_model')
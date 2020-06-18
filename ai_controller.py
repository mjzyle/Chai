#!/usr/bin/python

import math
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import data_controller as dc
from tensorflow import keras
from tensorflow.keras import layers


# Basic win/loss prediction network
def setup_model():
    model = keras.models.Sequential()
    model.add(layers.Dense(4, input_dim=128, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(0.001),
        #loss=tf.keras.losses.BinaryCrossentropy(),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    model.save('neural_network_model')


def train_model(eps):
    model = keras.models.load_model('neural_network_model')

    connection, cursor = dc.establish_db_connection()
    df = pd.read_sql("SELECT * FROM chai.training_data", connection).drop(columns=['training_data_id', 'game_id'])
    target = df.pop('win')
    dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))
    train_dataset = dataset.shuffle(len(df)).batch(1)

    model.fit(train_dataset, epochs=eps)

    model.save('neural_network_model')
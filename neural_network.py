import math
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers



# Initial win/loss prediction network
inputs = keras.Input(shape=(128,))
dense1 = layers.Dense(64, activation='relu')
dense2 = layers.Dense(64, activation='relu')
dense3 = layers.Dense(2, activation='relu')
outputs = dense3(dense2(dense1(inputs)))

model = keras.Model(inputs=inputs, outputs=outputs)

df = pd.read_csv('raw_data/training_data.csv').drop(columns='Unnamed: 0')
target = df.pop('win')
dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))

train_dataset = dataset.shuffle(len(df)).batch(1)

model.compile(
    optimizer=tf.keras.optimizers.RMSprop(0.001),
    loss=tf.keras.losses.BinaryCrossentropy(),
    metrics=['accuracy']
)

model.fit(train_dataset, epochs=15)
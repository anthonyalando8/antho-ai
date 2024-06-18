# import tensorflow as tf
# # print("TensorFlow version:", tf.__version__)
# # mnist = tf.keras.datasets.mnist
# import pandas as pd
# import numpy as np

# csv_file = pd.read_csv("C:\\Users\\antho\\Downloads\\Compressed\\13) Web-Hacking Dataset\\cases.csv")
# date_done = csv_file[['Date']].values
# country = csv_file[['Country']].values
# ip = csv_file[['IP']].values
# language = csv_file[['Lang']].values
# os = csv_file[['OS']].values
# url = csv_file[['URL']].values
# encoding = csv_file[['Encoding']].values
# server = csv_file[['WebServer']].values
# notify = csv_file[['Notify']].values
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dropout(0.2),
#     tf.keras.layers.Dense(10)
# ])
# loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# model.compile(optimizer='adam',
#         loss=loss_fn,
#         metrics=['accuracy'])
# model.fit(url, country, epochs=5)

# class tensor_model:
#     def __init__(self) -> None:
#         (x_train, y_train), (x_test, y_test) = mnist.load_data()
#         x_train, x_test = x_train / 255.0, x_test / 255.0
#         model = tf.keras.models.Sequential([
#             tf.keras.layers.Flatten(input_shape=(28, 28)),
#             tf.keras.layers.Dense(128, activation='relu'),
#             tf.keras.layers.Dropout(0.2),
#             tf.keras.layers.Dense(10)
#         ])

#         predictions = model(x_train[:1]).numpy()
#         predictions
#         tf.nn.softmax(predictions).numpy()
#         loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
#         loss_fn(y_train[:1], predictions).numpy()
#         model.compile(optimizer='adam',
#               loss=loss_fn,
#               metrics=['accuracy'])
#         model.fit(x_train, y_train, epochs=5)

#         model.evaluate(x_test,  y_test, verbose=2)
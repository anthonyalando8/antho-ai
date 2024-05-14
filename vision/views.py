from django.shortcuts import render
from django.http import HttpResponse
import cv2 as cv
import numpy as np
import base64
# import tensorflow as tf

# # Create your views here.
# mnist = tf.keras.datasets.mnist

# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0

# model = tf.keras.models.Sequential([
#   tf.keras.layers.Flatten(input_shape=(28, 28)),
#   tf.keras.layers.Dense(128, activation='relu'),
#   tf.keras.layers.Dropout(0.2),
#   tf.keras.layers.Dense(10)
# ])

# predictions = model(x_train[:1]).numpy()
# predictions

# tf.nn.softmax(predictions).numpy()

# loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# loss_fn(y_train[:1], predictions).numpy()

# model.compile(optimizer='adam',
#               loss=loss_fn,
#               metrics=['accuracy'])

# model.fit(x_train, y_train, epochs=5)

# model.evaluate(x_test,  y_test, verbose=2)
def index(request):

    if request.method == "POST":
        image = request.FILES.get("image-uploaded")
        image_data = image.read()
        nparr = np.frombuffer(image_data, np.uint8)
        image_read = cv.imdecode(nparr, cv.IMREAD_COLOR)
        h, w = image_read.shape[:2]
        encoded_image = cv.imencode(".jpg", image_read)
        base_64_encoded = base64.b64encode(encoded_image)
        return HttpResponse(base_64_encoded)
    else:
        context ={
            "user": request.user,
        }
        return render(request, 'vision/vision.html', context)

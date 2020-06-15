# -*- coding: utf-8 -*-
"""Submission.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cHouioGhxBkA6erNCQBagcBGsUKWW2pw

# Paper Rock Scissors Recognition

### Import Package
"""

# Commented out IPython magic to ensure Python compatibility.
import zipfile,os
import time
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from google.colab import files
from keras.preprocessing import image
# %matplotlib inline

print("Tensorflow version:",tf.__version__)

"""### Load Dataset"""

!wget --no-check-certificate \
  https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip \
  -O /tmp/rock_paper_scissors.zip

local_zip = '/tmp/rock_paper_scissors.zip'
zip_ref = zipfile.ZipFile(local_zip,'r')
zip_ref.extractall('/tmp')
zip_ref.close

"""### Image Augmentation"""

startTime = time.time()
train_img = ImageDataGenerator(
    rescale = 1./255,
    horizontal_flip = True,
    vertical_flip = True,
    shear_range = 0.2,
    fill_mode = 'nearest',
    validation_split = 0.2
)

validation_img = ImageDataGenerator(
    rescale = 1./255,
    horizontal_flip = True,
    vertical_flip = True,
    shear_range = 0.2,
    fill_mode = 'nearest',
    validation_split = 0.2
)

base_dir='/tmp/rockpaperscissors/rps-cv-images/'

train_gen = train_img.flow_from_directory(
    base_dir,
    target_size = (150,150),
    batch_size = 32,
    class_mode = 'categorical',
    subset = 'training'
)

validation_gen = validation_img.flow_from_directory(
    base_dir,
    target_size = (150,150),
    batch_size = 32,
    class_mode = 'categorical',
    subset = 'validation'
)

model = Sequential([
    # This is the first convolution
    Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(2, 2),
    # This is the second convolution
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    # This is the third convolution
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    # This is the fourth convolution
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dense(3, activation='softmax')
])

model.compile(
    loss='categorical_crossentropy',
    optimizer= 'Adam',
    metrics=['accuracy']
)

model.fit(
    train_gen,
    steps_per_epoch  = 50, 
    validation_data  = validation_gen,
    validation_steps = 50,
    epochs = 5, 
    verbose = 2
)

endTime = time.time()

waktu = (endTime - startTime)/60
print(waktu)

"""### Predict Model Testing"""

uploaded = files.upload()

for fn in uploaded.keys():
  path = fn
  img = image.load_img(path, target_size=(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  img_class = model.predict_classes(x)
  img_predict = img_class[0]
  pred = []
  pred.append(img_predict)
 
  images = np.vstack([x])
  classes = model.predict(images, batch_size = 10)

  print(fn)
  print(pred)
  print(classes)
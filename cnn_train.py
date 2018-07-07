import config

import tensorflow as tf
from keras import layers
from keras import backend
from keras.models import Model
from keras.optimizers import RMSprop

import os, sys


### CONFIGURE TENSORFLOW ###

# Error Messages
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

# TensorFlow Backend
tf_config = tf.ConfigProto(gpu_options = tf.GPUOptions(allow_growth = True))
backend.set_session(tf.Session(config = tf_config))


### DATASET ###

# Directories
base_dir = config.data_path
training_dir = os.path.join(base_dir, "training")
validation_dir = os.path.join(base_dir, "validation")

# Training Directories
training_a_dir = os.path.join(training_dir, config.search_terms_a[0])
training_b_dir = os.path.join(training_dir, config.search_terms_b[0])

# Validation Directories
validation_a_dir = os.path.join(validation_dir, config.search_terms_a[0])
validation_b_dir = os.path.join(validation_dir, config.search_terms_b[0])

# Training Image List
training_a_fnames = os.listdir(training_a_dir)
training_b_fnames = os.listdir(training_b_dir)


### CNN MODEL ###

# Input Layer
# [150 x 150 images, and 3 colour channels]
img_input = layers.Input(shape = (150, 150, 3))

# Hidden Layer 1 (CONVOLUTIONAL)
# [16 3 x 3 filters, with 2 x 2 max-pooling]
x = layers.Conv2D(16, 3, activation = "relu")(img_input)
x = layers.MaxPooling2D(2)(x)

# Hidden Layer 2 (CONVOLUTIONAL)
# [32 3 x 3 filters, with 2 x 2 max-pooling]
x = layers.Conv2D(32, 3, activation = "relu")(x)
x = layers.MaxPooling2D(2)(x)

# Hidden Layer 3 (CONVOLUTIONAL)
# [64 3 x 3 filters, with 2 x 2 max-pooling]
x = layers.Conv2D(64, 3, activation = "relu")(x)
x = layers.MaxPooling2D(2)(x)

# Hidden Layer 4 (FULLY CONNECTED)
# [512 neurons]
x = layers.Flatten()(x)
x = layers.Dense(512, activation = "relu")(x)

# Output Layer
output = layers.Dense(1, activation = "sigmoid")(x)

# Create Model
model = Model(img_input, output)

# Optimiser
model.compile(loss = "binary_crossentropy",
              optimizer = RMSprop(lr = 0.001),
              metrics = ["acc"])

# Review Model
model_summary = True
if model_summary:
    print(model.summary())

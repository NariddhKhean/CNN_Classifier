import config

import tensorflow as tf
from keras import layers
from keras import backend
from keras.models import Model
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard

import math
import os


### CONFIGURE TENSORFLOW ###

# Error Messages
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

# TensorFlow Backend
tf_config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
backend.set_session(tf.Session(config=tf_config))


### TRAIN AND SAVE MODEL FUNCTION ###

def train_model():
    """Defines, trains, and saves convolution neural network model."""

    # Define Directories
    base_directory       = config.data_path
    training_directory   = os.path.join(base_directory, 'training')
    validation_directory = os.path.join(base_directory, 'validation')

    # Define Training Directories
    training_class_directories = []
    for search_term in config.search_terms:
        training_class_directory = os.path.join(training_directory, search_term)
        training_class_directories.append(training_class_directory)

    # Define Validation Directories
    validation_class_directories = []
    for search_term in config.search_terms:
        validation_class_directory = os.path.join(validation_directory, search_term)
        validation_class_directories.append(validation_class_directory)

    # Define Training Image List
    training_class_images = []
    for training_class_directory in training_class_directories:
        training_class_images.append(os.listdir(training_class_directory))

    # Input Layer
    img_input = layers.Input(shape=(config.target_size, config.target_size, 3))

    x = layers.Conv2D(32, 3)(img_input)
    x = layers.LeakyReLU(alpha=0.01)(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Conv2D(64, 3)(x)
    x = layers.LeakyReLU(alpha=0.01)(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Conv2D(128, 3)(x)
    x = layers.LeakyReLU(alpha=0.01)(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Flatten()(x)

    x = layers.Dense(128)(x)
    x = layers.LeakyReLU(alpha=0.01)(x)

    x = layers.Dense(32)(x)
    x = layers.LeakyReLU(alpha=0.01)(x)

    # Output Layer
    output = layers.Dense(len(config.search_terms), activation='softmax')(x)

    # Create Model
    model = Model(img_input, output)

    # Optimiser
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=config.learning_rate),
                  metrics=['acc'])

    # Review Model
    print(model.summary())

    # Generate Image Data
    training_datagen = ImageDataGenerator(rescale=1./255,
                                          horizontal_flip=True,
                                          rotation_range=15)
    validation_datagen = ImageDataGenerator(rescale=1./255,
                                            horizontal_flip=True,
                                            rotation_range=15)

    # Steps per Epoch for Training Data
    training_class_image_count = []
    for training_class_directory in training_class_directories:
        training_image_count = len(os.listdir(os.path.join(training_directory, training_class_directory)))
        training_class_image_count.append(training_image_count)
    training_min_image_count = min(training_class_image_count)
    training_steps_per_epoch = math.floor(training_min_image_count / config.batch_size)

    # Steps per Epoch for Validation Data
    validation_class_image_count = []
    for validation_class_directory in validation_class_directories:
        validation_image_count = len(os.listdir(os.path.join(validation_directory, validation_class_directory)))
        validation_class_image_count.append(validation_image_count)
    validation_min_image_count = min(validation_class_image_count)
    validation_steps_per_epoch = math.floor(validation_min_image_count / config.batch_size)

    # Flow Images in Batches
    training_generator = training_datagen.flow_from_directory(training_directory,
                                                              target_size=(config.target_size, config.target_size),
                                                              batch_size=config.batch_size)

    # Flow Validation Images in Batches
    validation_generator = validation_datagen.flow_from_directory(validation_directory,
                                                                  target_size=(config.target_size, config.target_size),
                                                                  batch_size=config.batch_size)

    # Setting Up TensorBoard Callback
    tensorboard = TensorBoard()

    # Fit Model
    model.fit_generator(training_generator,
                        steps_per_epoch=training_steps_per_epoch,
                        epochs=config.epochs,
                        verbose=1,
                        callbacks=[tensorboard],
                        validation_data=validation_generator,
                        validation_steps=validation_steps_per_epoch)

    # Save Model
    os.makedirs(config.model_directory)
    model.save(os.path.join(config.model_directory, config.model_name))

    # Summary
    print('\nSuccessfully trained CNN for {} epochs.'.format(config.epochs))


if __name__ == '__main__':
    train_model()

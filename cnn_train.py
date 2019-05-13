from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, Model
import json
import sys
import os

import _dirs

def check_directories():
    dirs = [_dirs.BASE_DIR, _dirs.DATA_DIR, _dirs.MODEL_DIR]
    for directory in dirs:
        if not os.path.isdir(directory):
            os.makedirs(directory)
    if os.listdir(_dirs.TRAINING_DIR) != os.listdir(_dirs.VALIDATION_DIR):
        sys.exit('Training classes does not match validation classes.')
    else:
        return os.listdir(_dirs.TRAINING_DIR)

def import_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    return config

def compile_model(config, labels):
    img_input = layers.Input(
        shape=(config['target_size'], config['target_size'], 3)
    )

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

    output = layers.Dense(len(labels), activation='softmax')(x)

    model = Model(img_input, output)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])

    print(model.summary())
    return model

def flow_from_directory(directory, config):
    datagen = ImageDataGenerator(
        rescale=1./255,
        horizontal_flip=True,
        rotation_range=15
    )
    flow = datagen.flow_from_directory(
        directory,
        target_size=(config['target_size'], config['target_size']),
        batch_size=config['batch_size']
    )
    return flow

def steps_per_epoch(directory, config, labels):
    class_dirs = [os.path.join(directory, label) for label in labels]
    class_counter = []
    for class_dir in class_dirs:
        class_path = os.path.join(directory, class_dir)
        count = len(os.listdir(class_path))
        class_counter.append(count)
    min_count = min(class_counter)
    steps_per_epoch = min_count // config['batch_size']
    return steps_per_epoch

def train_model(config, labels):
    """Defines, trains, and saves convolution neural network model."""

    # Image Generators
    training_generator   = flow_from_directory(_dirs.TRAINING_DIR, config)
    validation_generator = flow_from_directory(_dirs.VALIDATION_DIR, config)

    # Fit Model
    model = compile_model(config, labels)
    model.fit_generator(
        training_generator,
        steps_per_epoch=steps_per_epoch(_dirs.TRAINING_DIR, config, labels),
        epochs=config['epochs'],
        verbose=1,
        validation_data=validation_generator,
        validation_steps=steps_per_epoch(_dirs.VALIDATION_DIR, config, labels)
    )

    # Save Model
    if not os.path.isdir(_dirs.MODEL_DIR):
        os.makedirs(_dirs.MODEL_DIR)
    model.save(os.path.join(_dirs.MODEL_DIR, 'model.h5'))
    print('\nSuccessfully trained model.h5 for {} epochs.'.format(config['epochs']))


if __name__ == '__main__':

    labels = check_directories()
    config = import_config('.\_config.json')

    train_model(config, labels)
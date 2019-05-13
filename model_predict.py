import tensorflow as tf
from PIL import Image
import numpy as np
import urllib
import json
import sys
import os

import _dirs


def import_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    return config

def predict(url, config):
    """ Predicts the class of a new image.

    Arguments:
        url -- String indicating the url to an image for classification.
    """

    # Load Trained Model
    model = tf.keras.models.load_model(
        os.path.join(_dirs.MODEL_DIR, 'model.h5')
    )

    # Request for Image from URL
    img = Image.open(urllib.request.urlopen(url))

    # Resize, Scale, and Reshape for Input
    img = img.resize((config['target_size'], config['target_size']))
    img = np.array(img)
    img = img / 255
    img = np.reshape(img, (1, config['target_size'], config['target_size'], 3))

    # Determine Classes
    classes = sorted(config['search_terms'])

    # Predict
    prediction = model.predict(img)[0]
    prediction_index = np.argmax(prediction)

    # Output
    print('Prediction: {} with {:.2f}% confidence.'.format(classes[prediction_index].capitalize(), 100 * prediction[prediction_index]))

if __name__ == '__main__':

    config = import_config('.\_config.json')
    predict(sys.argv[1], config)

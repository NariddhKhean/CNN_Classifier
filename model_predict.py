import config

import tensorflow as tf
from keras.models import load_model

from PIL import Image
import numpy as np
import urllib
import sys
import os


### CONFIGURE TENSORFLOW ###

# Error Messages
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


### PREDICT FUNCTION ###

def predict(url):
    """ Predicts the class of a new image.

    Arguments:
        url -- String indicating the url to an image for classification.
    """

    # Load Trained Model
    model = load_model(os.path.join(config.model_directory, config.model_name))

    # Request for Image from URL
    img = Image.open(urllib.request.urlopen(url))

    # Resize, Scale, and Reshape for Input
    img = img.resize((config.target_size, config.target_size))
    img = np.array(img)
    img = img / 255
    img = np.reshape(img, (1, config.target_size, config.target_size, 3))

    # Determine Classes
    classes = sorted(config.search_terms)

    # Predict
    prediction = model.predict(img)[0]
    prediction_index = np.argmax(prediction)

    # Output
    print('Prediction: {} with {:.2f}% confidence.'.format(classes[prediction_index].capitalize(), 100 * prediction[prediction_index]))

if __name__ == '__main__':
    predict(sys.argv[1])

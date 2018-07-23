import config

import tensorflow as tf
from keras.models import load_model

from PIL import Image
import numpy as np
import os, sys, urllib


### CONFIGURE TENSORFLOW ###

# Error Messages
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


### PREDICT FUNCTION ###

def predict(url):

    # Load Trained Model
    model = load_model(os.path.join(config.model_dir, config.model_name))

    # Request for Image from URL
    img = Image.open(urllib.request.urlopen(url))

    # Resize, Scale, and Reshape for Input
    img = img.resize((config.target_size, config.target_size))
    img = np.array(img)
    img = img / 255
    img = np.reshape(img, (1, config.target_size, config.target_size, 3))

    # Predict
    prediction = model.predict(img)[0][0]

    # Output
    if prediction < 0.5:
        certainty = 1 - prediction
        print("\nPrediction: '{}' with {:.3f}% certainty.".format(config.search_terms_a[0], certainty * 100))
    else:
        print("\nPrediction: '{}' with {:.3f}% certainty.".format(config.search_terms_b[0], prediction * 100))


if __name__ == "__main__":
    predict(sys.argv[1])

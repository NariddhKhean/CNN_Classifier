import config

from keras.models import load_model


### LOAD MODEL ###

# Load Trained Model
model = load_model(os.path.join(config.model_dir, config.model_name))


### TODO: Use loaded model to make predictions for new inputs

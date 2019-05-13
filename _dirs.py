import os

CHROMEDRIVER_PATH = os.path.join(
    os.path.expanduser('~'),
    'AppData',
    'Local',
    'Chromedriver',
    'chromedriver.exe'
)

BASE_DIR = os.path.join(
    os.path.expanduser('~'),
    'Documents',
    'CNN_Classifier'
)

DATA_DIR  = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

TRAINING_DIR   = os.path.join(DATA_DIR, 'training')
VALIDATION_DIR = os.path.join(DATA_DIR, 'validation')

"""
.
+-- data\
|   +-- training\
|   +-- validation\
+-- models\
+-- _config.json
+-- cnn_train.py
+-- directories.py
+-- model_predict.py
+-- web_scraper.py
"""
import os


### WEB SCRAPE PARAMETERS ###

# Search Terms
search_terms = ['apples', 'oranges', 'bananas', 'pears', 'pineapples', 'strawberries', 'lemons', 'watermelons']

# Output Directores
user_path = os.path.expanduser('~')
data_path = os.path.join(user_path, 'Documents', 'Data', 'data')

# Chromedriver Path
chromedriver_path = os.path.join(user_path, 'AppData', 'Local', 'Chromedriver' ,'chromedriver.exe')

# Scrape Limit
scrape_limit = 5000

# Training/Validation Ratio
training_factor = 0.8


### CNN HYPERPARAMETERS ###

# Input Images
target_size = 142

# Adam Optimiser
learning_rate = 0.001

# Training
batch_size = 8
epochs = 16

# Trained Model
model_directory = os.path.join(user_path, 'Documents', 'Data', 'model')
model_name = 'model.h5'

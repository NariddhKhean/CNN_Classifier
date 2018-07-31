import os


### WEB SCRAPE PARAMETERS ###

# Search Terms
search_terms = ['apples', 'oranges', 'bananas', 'pears', 'pineapples', 'strawberries', 'lemons', 'watermelons']

# Output Directores
user_path = os.path.expanduser('~')
data_path = os.path.join(user_path, 'Desktop', 'data')

# Chromedriver Path
chromedriver_path = os.path.join(user_path, 'AppData', 'Local', 'Chromedriver' ,'chromedriver.exe')

# Scrape Limit
scrape_limit = 5000

# Training/Division Ratio
training_factor = 0.8


### CNN HYPERPARAMETERS ###

# Training
learning_rate = 0.001
target_size = 164
batch_size = 16
epochs = 16

# Trained Model
model_directory = os.path.join(user_path, 'Desktop', 'model')
model_name = 'model.h5'

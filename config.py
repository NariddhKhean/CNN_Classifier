import os


### WEB SCRAPE ###

# Search Terms
search_terms_a = ["apples", "apple"]
search_terms_b = ["oranges", "orange"]

# Output Directores
user_path = os.path.expanduser("~")
data_path = os.path.join(user_path, "Desktop", "data")
output_dir_a = os.path.join(data_path, search_terms_a[0])
output_dir_b = os.path.join(data_path, search_terms_b[0])

# Chromedriver Path
chromedriver_path = os.path.join(user_path, "AppData", "Local", "Chromedriver" ,"chromedriver.exe")

# Scrape Limit
scrape_limit = 250


### DATASET DIVISION ###

# Training/Division Ratio
training_factor = 0.8


### CNN HYPERPARAMETERS ###

# Training
batch_size = 10
epochs = 100

# Trained Model
model_dir = os.path.join(user_path, "Desktop", "model")
model_name = "{}_vs_{}.h5".format(search_terms_a[0], search_terms_b[0])

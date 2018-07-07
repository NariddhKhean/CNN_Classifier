import config

import os, shutil


### DATASET DIVISION ###

# Web Scraped Data Directories
output_dir_a = config.output_dir_a
output_dir_b = config.output_dir_b

# Create Training Directories
train_dir_a = os.path.join(config.data_path, "train", config.search_terms_a[0])
train_dir_b = os.path.join(config.data_path, "train", config.search_terms_b[0])
os.makedirs(train_dir_a)
os.makedirs(train_dir_b)

# Create Validation Directories
validation_dir_a = os.path.join(config.data_path, "validation", config.search_terms_a[0])
validation_dir_b = os.path.join(config.data_path, "validation", config.search_terms_b[0])
os.makedirs(validation_dir_a)
os.makedirs(validation_dir_b)

# List Files in Output Directories
files_a = os.listdir(output_dir_a)
files_b = os.listdir(output_dir_b)

# Count Files in Output Directories
file_count_a = len(files_a)
file_count_b = len(files_b)

# Define Number of Files to Move
train_file_count_a = round(config.training_factor * file_count_a)
train_file_count_b = round(config.training_factor * file_count_b)

# Move Training Files into Training Directories
for i in range(train_file_count_a):
	shutil.move(os.path.join(output_dir_a, files_a[i]), train_dir_a)
for i in range(train_file_count_b):
	shutil.move(os.path.join(output_dir_b, files_b[i]), train_dir_b)

# Move Validation Files into Validation Directories
for f in os.listdir(output_dir_a):
	shutil.move(os.path.join(output_dir_a, f), validation_dir_a)
for f in os.listdir(output_dir_b):
	shutil.move(os.path.join(output_dir_b, f), validation_dir_b)

# Remove Empty Output Directories
os.rmdir(config.output_dir_a)
os.rmdir(config.output_dir_b)

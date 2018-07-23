import config

import os, shutil


### DATASET DIVISION ###

def dataset_division(search_terms, output_directory, debugging=True):

    # Debugging: Start Message
    if debugging:
        print('\nMoving files into training and validation directories...')

    # Create Training Directory
    training_dir = os.path.join(config.data_path, 'training', search_terms[0])
    os.makedirs(training_dir)

    # Create Validation Directory
    validation_dir = os.path.join(config.data_path, 'validation', search_terms[0])
    os.makedirs(validation_dir)

    # List and Count Files in Output Directory
    files = os.listdir(output_directory)
    file_count = len(files)
    training_file_count = round(config.training_factor * file_count)

    # Move Training Files into Training Directories
    for i in range(training_file_count):
        shutil.move(os.path.join(output_directory, files[i]), training_dir)

    # Move Validation Files into Validation Directories
    for f in os.listdir(output_directory):
        shutil.move(os.path.join(output_directory, f), validation_dir)

    # Remove Empty Output Directories
    os.rmdir(output_directory)

    # Debugging: Count and Confirmation
    if debugging:
        print('\nSuccessfully collected {} training images, and {} validation images, labelled "{}".'
              .format(training_file_count, file_count - training_file_count, search_terms[0]))


### EXECUTE DATASET DIVISION ###

dataset_division(config.search_terms_a, config.output_dir_a)
dataset_division(config.search_terms_b, config.output_dir_b)

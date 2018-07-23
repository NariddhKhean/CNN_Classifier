import config

from google_images_download import google_images_download
from PIL import Image
import shutil
import os


### WEB SCRAPE FUNCTION ###

def web_scrape(search_terms, output_directory):
    """ Web scrapes images from Google Images.

    Arguments:
        search_terms     -- Array of strings to Google Image search.
        output_directory -- String indicating the path for web scraped images.
    """

    # Instantiate Class
    response = google_images_download.googleimagesdownload()

    # Format Keywords
    keywords = ','.join(search_terms)

    # Define Arguments
    arguments = {'keywords': keywords,
                 'limit': config.scrape_limit,
                 'format': 'jpg',
                 'output_directory': output_directory,
                 'no_directory': True,
                 'chromedriver': config.chromedriver_path}

    # Execute Web Scrape
    response.download(arguments)


### CLEAN WEB SCRAPED DATA FUNCTION ###

def clean_web_scraped_data(output_directory, debugging=True):
    """ Removes all incompatible images for the neural network.

    Arguments:
        output_directory -- String indicating the path for web scraped images.
        debugging        -- Boolean for showing summaries.
    """

    # Debugging: Start Message
    if debugging:
        print('\nDetecting incompatible images in {}...'.format(output_directory))

    # Remove Incompatible Files
    removed = 0
    for image in os.listdir(output_directory):
        if image.endswith('.jpg'):

            # Try Opening '.jpg' Files
            try:
                im = Image.open(os.path.join(output_directory, image))
                im.close()

            # Delete Unopenable Files
            except(OSError):
                os.remove(os.path.join(output_directory, image))
                removed += 1

        # Remove All Other File Types
        else:
            os.remove(os.path.join(output_directory, image))
            removed =+1

    # Debugging: Count and Confirmation
    if debugging:
        if removed == 0:
            print('No incompatible images detected.')
        elif removed == 1:
            print('Successfully removed 1 incompatible image.')
        else:
            print('Successfully removed {} incompatible images.'.format(removed))


### TRAINING/VALIDATION DATASET DIVISION ###

def dataset_division(search_terms, output_directory, debugging=True):
    """ Divides web scraped images into a training and validation dataset.

    Arguements:
        search_terms     -- Array of strings to Google Image search.
        output_directory -- String indicating the path for web scraped images.
        debugging        -- Boolean for showing summaries.
    """

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


### SCRAPE, CLEAN, AND DIVIDE FUNCTION ###

def scrape_clean_divide(search_terms, output_directory, debugging=True):
    """ Executes the web scrape, the cleaning, and the division.

    Arguments:
        search_terms     -- Array of strings to Google Image search.
        output_directory -- String indicating the path for web scraped images.
        debugging        -- Boolean for showing summaries.
    """

    # Web Scrape
    web_scrape(search_terms, output_directory)

    # Clean Web Scraped Data
    clean_web_scraped_data(output_directory, debugging)

    # Dataset Division
    dataset_division(search_terms, output_directory, debugging)


### EXECUTE WEB SCRAPE, CLEAN, AND DIVIDE ###

if __name__ == '__main__':
    scrape_clean_divide(config.search_terms_a, config.output_dir_a)
    scrape_clean_divide(config.search_terms_b, config.output_dir_b)

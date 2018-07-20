import config

from google_images_download import google_images_download
from PIL import Image
import os


### WEB SCRAPE FUNCTION ###

def web_scrape(search_terms, output_directory):

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


### SCRAPE AND CLEAN FUNCTION ###

def scrape_and_clean(search_terms, output_directory, debugging=True):

    # Web Scrape
    web_scrape(search_terms, output_directory)

    # Clean Web Scraped Data
    clean_web_scraped_data(output_directory, debugging)

    # Debugging: Summary
    if debugging:
        print('\nSuccessfully web scraped {} images labelled "{}".'.format(len(os.listdir(output_directory)), search_terms[0]))


### EXECUTE WEB SCRAPE AND CLEAN DATA ###

scrape_and_clean(config.search_terms_a, config.output_dir_a)
scrape_and_clean(config.search_terms_b, config.output_dir_b)

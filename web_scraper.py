from google_images_download import google_images_download
from PIL import Image
import shutil
import json
import os

import _dirs


class WebScrape:
    """Builds a training and validation dataset of images from a Google Images search query.

    Arguments:
    search_term -- String that represents the search query to web scrape.
    """

    def __init__(self, search_term, config):
        self.search_term     = search_term
        self.class_directory = os.path.join(_dirs.DATA_DIR, search_term)
        self.config          = config

    def web_scrape(self):
        """Web scrapes images into a directory of the same name as the search query."""

        # Instantiate Web Scraper
        response = google_images_download.googleimagesdownload()

        # Define Arguments
        arguments = {'keywords': self.search_term,
                     'limit': config['scrape_limit'],
                     'format': 'jpg',
                     'output_directory': self.class_directory,
                     'no_directory': True,
                     'chromedriver': _dirs.CHROMEDRIVER_PATH}

        # Execute Web Scrape
        response.download(arguments)

    def clean_images(self):
        """Removes all incompatible images."""

        # Console Summary
        print('\nDetecting incompatible images in {}...'.format(self.class_directory))

        # Remove Incompatible Files
        removed = 0
        for image in os.listdir(self.class_directory):
            if image.endswith('.jpg'):

                # Try Opening '.jpg' Files
                try:
                    im = Image.open(os.path.join(self.class_directory, image))
                    im.close()

                # Delete Unopenable Files
                except(OSError):
                    os.remove(os.path.join(self.class_directory, image))
                    removed += 1

            # Remove All Other File Types
            else:
                os.remove(os.path.join(self.class_directory, image))
                removed =+1

        # Console Summary
        if removed == 0:
            print('\nNo incompatible images detected.')
        elif removed == 1:
            print('\nSuccessfully removed 1 incompatible image.')
        else:
            print('\nSuccessfully removed {} incompatible images.'.format(removed))

    def divide_dataset(self):
        """Divides images into a training and validation dataset."""

        # Console Summary
        print('\nMoving files into training and validation directories...')

        # Create Training Directory
        training_directory = os.path.join(_dirs.DATA_DIR, 'training', self.search_term)
        os.makedirs(training_directory)

        # Create Validation Directory
        validation_directory = os.path.join(_dirs.DATA_DIR, 'validation', self.search_term)
        os.makedirs(validation_directory)

        # List and Count Images in Class Directory
        images                = os.listdir(self.class_directory)
        images_count          = len(images)
        training_images_count = round(config['training_factor'] * images_count)

        # Move Training Images into Training Directory
        for i in range(training_images_count):
            shutil.move(os.path.join(self.class_directory, images[i]), training_directory)

        # Move Validation Images into Training Directory
        for image in os.listdir(self.class_directory):
            shutil.move(os.path.join(self.class_directory, image), validation_directory)

        # Remove Empty Class Directories
        os.rmdir(self.class_directory)

        # Console Summary
        print('\nSuccessfully collected {} training images, and {} validation images, labelled "{}".'
              .format(training_images_count, images_count - training_images_count, self.search_term))

def import_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    return config


if __name__ == '__main__':

    config = import_config('.\_config.json')

    for search_term in config['search_terms']:
        dataset = WebScrape(search_term, config)
        dataset.web_scrape()
        dataset.clean_images()
        dataset.divide_dataset()

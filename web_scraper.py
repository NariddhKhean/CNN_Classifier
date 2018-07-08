import config

from google_images_download import google_images_download
from PIL import Image
import os


### WEB SCRAPE ###

# Search Terms
keywords_a = ",".join(config.search_terms_a)
keywords_b = ",".join(config.search_terms_b)

# Instantiate Class
response = google_images_download.googleimagesdownload()

# Insert Variables into Arguments
arguments_a = {"keywords": keywords_a,
               "limit": config.scrape_limit,
               "format": config.file_format,
               "output_directory": config.output_dir_a,
               "no_directory": True,
               "chromedriver": config.chromedriver_path}
arguments_b = {"keywords": keywords_b,
               "limit": config.scrape_limit,
               "format": config.file_format,
               "output_directory": config.output_dir_b,
               "no_directory": True,
               "chromedriver": config.chromedriver_path}

# Execute Web Scrape
response.download(arguments_a)
response.download(arguments_b)


### CLEAN TRAINING DATA ###

# Debug Statement
print("Detecting corrupted images...")

# Remove Unopenable Files in Directory "a"
removed_a = 0
for image in os.listdir(config.output_dir_a):
    if image.endswith(".jpg"):
        try:
            im = Image.open(os.path.join(config.output_dir_a, image))
            im.close()
        except(OSError):
            os.remove(os.path.join(config.output_dir_a, image))
            removed_a += 1
    else:
        os.remove(os.path.join(config.output_dir_a, image))
        removed_a += 1

# Remove Unopenable Files in Directory "b"
removed_b = 0
for image in os.listdir(config.output_dir_b):
    if image.endswith(".jpg"):
        try:
            im = Image.open(os.path.join(config.output_dir_b, image))
            im.close()
        except(OSError):
            os.remove(os.path.join(config.output_dir_b, image))
            removed_b += 1
    else:
        os.remove(os.path.join(config.output_dir_b, image))
        removed_b += 1

# Print Confirmation
if removed_a + removed_b == 0:
    print("No corrupted images.")
elif removed_a + removed_b == 1:
    print("Sucessfully removed 1 corrupted image.")
else:
    print("Sucessfully removed {} corrupted images.".format(removed_a + removed_b))


### SUMMARY ###

# Print Summary
print("\nSucessfully web scraped {} images labelled '{}'.".format(len(os.listdir(config.output_dir_a)), config.search_terms_a[0]))
print("\nSucessfully web scraped {} images labelled '{}'.".format(len(os.listdir(config.output_dir_b)), config.search_terms_b[0]))

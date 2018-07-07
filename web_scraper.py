import config

from google_images_download import google_images_download
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
               "no_numbering": True}
arguments_b = {"keywords": keywords_b,
               "limit": config.scrape_limit,
               "format": config.file_format,
               "output_directory": config.output_dir_b,
               "no_directory": True,
               "no_numbering": True}

# Execute Web Scrape
response.download(arguments_a)
response.download(arguments_b)

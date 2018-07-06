import config
from google_images_download import google_images_download

# Search Terms
keywords = ",".join(config.search_terms)

# Instantiate Class
response = google_images_download.googleimagesdownload()

# Insert Variables into Arguments
arguments = {"keywords": keywords, "limit": config.scrape_limit, "format": config.file_format, "output_directory": config.output_dir}

# Execute Web Scrape
response.download(arguments)

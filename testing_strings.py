from google_images_download import google_images_download
import sys, os

# Variables
file_format	 = "jpg"
scrape_limit = 100

# Search Terms
search_terms = ["apples", "oranges"]
keywords	 = ",".join(search_terms)

# Output Directory
user_path  = os.path.expanduser("~")
output_dir = os.path.join(user_path, "Desktop", "data")

# Instantiate Class
response = google_images_download.googleimagesdownload()

# Insert Variables into Arguments
arguements = {"keywords": keywords,
			  "limit": scrape_limit,
			  "format": file_format,
			  "output_directory": output_dir}

# Execute Web Scrape
absolute_image_paths = response.download(arguements)

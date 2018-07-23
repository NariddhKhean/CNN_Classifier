# CNN_Classifier

*(Work in Progress: 95% complete)*

Web scrape images based on two lists of _Google Images_ search queries, to generate a training dataset for binary classification. Train and save a deep convolutional neural network. Load the trained model to classify new images from an image's url.

_"Apples are red with thin, edible skin, and white flesh. Whereas oranges are rounder, with orange-coloured skin and orange-coloured flesh. And the skin of an orange is generally discarded before consumption. You know what just happened there? I just compared apples to oranges. It can be done!"_

<div style="text-align: right"> - Ronny Chieng. </div>

## Getting Started
The main component of the web scraper is _[Google Images Download](https://github.com/hardikvasa/google-images-download)_; a small, ready-to-run program that downloads images from a Google Images search from keywords.
> Note: If you would like to scrape more than 100 images per keyword, you'll also need to install _[Selenium](https://www.seleniumhq.org/)_ and _[Chromedriver](http://chromedriver.chromium.org/)_.

The deep convolutional neural network was developed using _[Keras](https://keras.io/)_, a high-level neural network API, with _[TensorFlow](https://www.tensorflow.org/)_ as its backend.

### Prerequisites
To install _Google Images Download_ and _Keras_, you can use pip:
```
pip install google_images_download
```
```
pip install keras
```
Alternatively, you can view their respective documentation for different installation methods and troubleshooting.

To install TensorFlow, it's best to refer to their [documentation](https://www.tensorflow.org/install/).
> Note: To considerably speed up training time, install TensorFlow with GPU support.

### Configuration

`search_terms_a` = List of search terms considered to be the first of the two classifications.

`search_terms_b` = List of search terms considered to be the second of the two classifications.

`data_path` = Path to directory for web scraped images.

`chromedriver_path` = Path to chromedriver.exe.

`scrape_limit` = Maximum number of images that the script will attempt to scrape.

`training_factor` = Ratio for training images to validation images.

`batch_size` = Number of images within a batch.

`epochs` = Number of times the model trains on each image.

`target_size` = Target pixel width and height of training images.

`model_dir` = Path to directory where the trained model is saved and loaded for prediction.

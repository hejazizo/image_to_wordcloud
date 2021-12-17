# Image to Word Cloud Converter
Converts a list of image to a word cloud.

Note: The code is optimized for persian language, but it can be easily modified to work for other languages.

## How To Run
### Install Requirements
1. Install requirements by running `pip install -r requirements.txt`
2. Install Google's Tesseract-OCR Engine from [here](https://tesseract-ocr.github.io/tessdoc/Installation.html).
3. For persian language image to text conversion, you should put `data/fas.traineddata` in your tesseract-ocr data directory. For my local computer with Ubuntu 20.04, it is: `/usr/share/tesseract-ocr/4.00/tessdata/`

### Run Scripts
To generate word cloud and get stats, in main repo directory, run the following command in your terminal to add `src` to your `PYTHONPATH`:
```
export PYTHONPATH=${PWD}
```

Then run:
```
python src/image_to_wordcloud.py --images_directory src/data/images --output_directory src/data
```
and wordcloud will be generated in `src/data/wordcloud.png` from the images in `src/data/images`.

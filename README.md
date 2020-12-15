# How to Run

## Install Requirements
1. Install requirements by running `pip install -r requirements.txt`
2. Install Google's Tesseract-OCR Engine from [here](https://tesseract-ocr.github.io/tessdoc/Installation.html).
3. For persian language image to text conversion, you should put `data/fas.traineddata` in your tesseract-ocr installation directory. For my local computer with Ubuntu 20.04, it is: `/usr/share/tesseract-ocr/4.00/tessdata/`
4. change image and text inputs in scripts to your desired inputs.

## Run Scripts
- `python ask_me_a_question_processor.py`: converts screenshot of ask me a question responses to txt.
- `python word_cloud.py`: makes a word cloud out of a txt file.

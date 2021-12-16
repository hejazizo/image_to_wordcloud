# How to Run

## Install Requirements
1. Install requirements by running `pip install -r requirements.txt`
2. Install Google's Tesseract-OCR Engine from [here](https://tesseract-ocr.github.io/tessdoc/Installation.html).
3. For persian language image to text conversion, you should put `data/fas.traineddata` in your tesseract-ocr data directory. For my local computer with Ubuntu 20.04, it is: `/usr/share/tesseract-ocr/4.00/tessdata/`

## Run Scripts
To generate word cloud and get stats, in main repo directory, run the following command in your terminal to add `src` to your `PYTHONPATH`:
```
export PYTHONPATH=${PWD}
```

Then run:
```
python src/stats.py --chat_json path_to_telegram_chat_export  --output_dir path_to_save_output_images --mask mask_image_path
```
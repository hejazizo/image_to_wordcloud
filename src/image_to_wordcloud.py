import argparse
import re
from pathlib import Path
from typing import Union

import arabic_reshaper
import demoji
import pytesseract
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from PIL import Image
from tqdm import tqdm
from wordcloud import WordCloud

from src.constants import FA_ALPHABETS
from src.data import DATA_DIR
import numpy as np


class ImageToWordcloud:
    def __init__(self):
        self.normalizer = Normalizer()

        # load stopwords
        logger.info(f"Loading stopwords from {DATA_DIR / 'stopwords.txt'}")
        stop_words = open(DATA_DIR / 'stopwords.txt').readlines()
        stop_words = map(str.strip, stop_words)
        self.stop_words = set(map(self.normalizer.normalize, stop_words))

    def __call__(
        self,
        images_directory: Union[Path, str], output_dir: Union[Path, str],
        mask_image_path: Union[Path, str] = None,
    ):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        text = self.image_to_txt(images_directory)
        text = self.separate_items(text)
        text = self.de_emojify(text)
        text = self.remove_stopwords(text)
        self.generate_word_cloud(text, output_dir, mask_image_path)

    def generate_word_cloud(
        self,
        text: str,
        output_dir: Union[str, Path],
        mask_image_path: Union[str, Path] = None,
        width: int = 800, height: int = 600,
        max_font_size: int = 250,
        background_color: str = 'white',
    ):
        mask = None
        if mask_image_path:
            logger.info(f"Loading mask image from {mask_image_path}...")
            mask = np.array(Image.open(DATA_DIR / 'mask.jpg'))
        wordcloud = WordCloud(
            width=width, height=height,
            font_path=str(DATA_DIR / 'Vazir.ttf'),
            background_color=background_color,
            max_font_size=max_font_size,
            mask=mask,
        )
        text = arabic_reshaper.reshape(self.de_emojify(text))
        text = get_display(text)

        logger.info("Generating word cloud...")
        wordcloud.generate(text)

        logger.info(f"Saving word cloud to {output_dir}")
        wordcloud.to_file(str(Path(output_dir) / 'word_cloud.png'))

    def image_to_txt(self, images_directory: Union[Path, str]):
        images_txt = []
        for image_path in tqdm(list(Path(images_directory).iterdir()), desc='Converting images to text...'):
            images_txt.append(pytesseract.image_to_string(Image.open(image_path), config='--psm 3', lang='eng+fas'))

        return ''.join(images_txt)

    def remove_stopwords(self, text):
        """Removes stop-words from the text.

        :param text: Text that may contain stop-words.
        """
        tokens = word_tokenize(self.normalizer.normalize(text))
        tokens = list(filter(lambda item: item not in self.stop_words, tokens))
        return ' '.join(tokens)

    def de_emojify(self, text):
        """Removes emojis and some special characters from the text.

        :param text: Text that contains emoji
        """
        regrex_pattern = re.compile(pattern="[\u2069\u2066]+", flags=re.UNICODE)
        text = regrex_pattern.sub('', text)
        return demoji.replace(text, " ")

    def separate_items(self, txt):
        """
        Receives a list of items, removes non persian lines,
        and concats consecutive lines to form a full response.

        This is a legacy function, should get refactored later.
        """
        items = []
        item = []
        end = False

        for line in txt.split('\n'):
            # if response has at least one persian character
            if set(line).intersection(FA_ALPHABETS):
                item.append(line)
            else:
                # otherwise end the user response
                end = True

            # if one user response is finished and it's not empty
            if end and item:
                items.append(' '.join(item))

            # if one user response is finished
            if end:
                item = []
                end = False

        return '\n\n'.join(items)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_directory', type=str, default=DATA_DIR / 'images')
    parser.add_argument('--output_directory', type=str, default=DATA_DIR)
    parser.add_argument('--mask_image_path', type=str, default=None)
    args = parser.parse_args()
    image_to_wordcloud = ImageToWordcloud()
    image_to_wordcloud(
        args.images_directory,
        args.output_directory,
        args.mask_image_path
    )

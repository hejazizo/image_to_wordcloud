

from collections import Counter
from pathlib import Path

import arabic_reshaper
import numpy as np
from bidi.algorithm import get_display
from hazm import *
from PIL import Image
from wordcloud import WordCloud

from constants import STOP_WORDS

# -------------------------------------------------- #
#
# tokenize and process text
#
# -------------------------------------------------- #
# read the input text
with Path('./input.txt').open() as f:
    text = f.read()

# tokenize it using hazm for persian words
tokens = word_tokenize(text)
tokens = [w for w in tokens if w not in STOP_WORDS]
text = ' '.join(tokens)

# we also dump most common words and their frequencies
with open('./most_common_words.txt', 'w') as f:
    most_common = [f'{w[0]}: {w[1]}' for w in Counter(tokens).most_common(100)]
    f.write('\n'.join(most_common))
    print('most common words dumped.')

# Make text readable for a non-Arabic library like wordcloud
text = arabic_reshaper.reshape(text)
text = get_display(text)

# -------------------------------------------------- #
#
# create word cloud
#
# -------------------------------------------------- #
# if you want a mask, you can uncomment this line and mask argument in WordCloud
# otherwise it would be plain rectangle.
# mask_image = np.array(Image.open("mask.jpg"))

# Generate a word cloud image
wordcloud = WordCloud(
    background_color="white",

    # uncomment this if you need a mask for your word cloud
    # mask=mask_image,
    width=500, height=900,

    # customize font for word cloud text
    font_path='data/fonts/NotoNaskhArabic/NotoNaskhArabic-Regular.ttf').generate(text)

# export the image
wordcloud.to_file("wordcloud.png")
print('word cloud exported.')

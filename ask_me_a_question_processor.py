try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

from constants import FA_ALPHABETS
from pathlib import Path


def separate_items(items):
    """
    Receives a list of items, removes non persian lines,
    and concats consecutive lines to form a full response.
    """
    items = []
    item = []
    for line in txt.split('\n'):
        # if response has at least one persian character
        if set(line).intersection(fa_alph):
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

    return items


image_path = Path("image.jpg")

# Simple image to string
# for lang='eng+fas' to work download persian language data and put it in tesseract-ocr data directory
# for my local system it is: /usr/share/tesseract-ocr/4.00/tessdata/

# Note: psm is a hyperparameter that can be tuned for better results
txt = pytesseract.image_to_string(Image.open(image_path), config='--psm 3', lang='eng+fas')

# separate responses from extracted txt
items = separate_items(items)

# dump output
with open('output.txt', 'w') as f:
    f.write('\n\n'.join(items))
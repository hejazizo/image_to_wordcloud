try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

from constants import FA_ALPHABETS
from pathlib import Path
from tqdm import tqdm


def separate_items(txt):
    """
    Receives a list of items, removes non persian lines,
    and concats consecutive lines to form a full response.
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

    return items

# input image
image_path = Path("./images")

# Simple image to string
# Note: psm is a hyperparameter that can be tuned for better results
output_txt = ""
for image_path in tqdm(image_path.iterdir()):
    txt = pytesseract.image_to_string(Image.open(image_path), config='--psm 3', lang='eng+fas')
    output_txt += txt

# separate responses from extracted txt
items = separate_items(output_txt)

print(len(items))

# dump output
with open('output/tesseract.txt', 'w') as f:
    f.write('\n\n'.join(items))
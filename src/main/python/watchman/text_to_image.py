import anki_vector
import sys
import time
 
from anki_vector.util import degrees
 
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Cannot import from PIL. Do `pip3 install --user Pillow` to install")
 
 
def make_text_image(text_to_draw, x, y, font=None):
    '''Make a PIL.Image with the given text printed on it
 
   Args:
       text_to_draw (string): the text to draw to the image
       x (int): x pixel location
       y (int): y pixel location
       font (PIL.ImageFont): the font to use
 
   Returns:
       :class:(`PIL.Image.Image`): a PIL image with the text drawn on it
   '''
    dimensions = (184, 96)
 
    # make a blank image for the text, initialized to opaque black
    text_image = Image.new(
        'RGBA', dimensions, (0, 0, 0, 255))
 
    # get a drawing context
    dc = ImageDraw.Draw(text_image)
 
    # draw the text
    dc.text((x, y), text_to_draw, fill=(255, 255, 255, 255), font=font)
 
    return text_image
 
 
# Get font file from computer (change directory as needed)
try:
    font_file = ImageFont.truetype("arial.ttf", 20)
except IOError:
    try:
        font_file = ImageFont.truetype(
            "/usr/share/fonts/noto/NotoSans-Medium.ttf", 20)
    except IOError:
        pass

from PIL import ImageOps


# Converting to Gray-scale
def toGrayscale(image):
    return image.convert("L")


# Resizing the image for terminal output.
# factor=0.5 corrects for terminal chars being ~2x taller than wide (standard ASCII).
# factor=1.0 is used for braille mode — the 2×4 pixel block structure already
# compensates for the terminal aspect ratio, so no additional correction is needed.
def resize(image, new_width=100, factor=0.5):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * factor)
    return image.resize((new_width, new_height))


# Invert all pixel RGB values (photo-negative effect)
def invert_colors(image):
    return ImageOps.invert(image.convert("RGB"))

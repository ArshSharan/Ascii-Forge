
from PIL import ImageOps


# Converting to Gray-scale
def toGrayscale(image):
    return image.convert("L")


# Resizing the image for terminal
# Applies a 0.5 height correction to compensate for non-square terminal chars
def resize(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)
    return image.resize((new_width, new_height))


# Invert all pixel RGB values (photo-negative effect)
def invert_colors(image):
    return ImageOps.invert(image.convert("RGB"))

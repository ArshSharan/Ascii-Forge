from image_loader import load_image
from processor import resize, toGrayscale
from ascii_mapper import map_pixels_to_ascii
from renderer import format_ascii

image = load_image("../assets/Image.jpg")
image = resize(image)
image = toGrayscale(image)

ascii_str = map_pixels_to_ascii(image)
ascii_img = format_ascii(ascii_str, image.width)

print(ascii_img)
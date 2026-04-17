ASCII_CHARS = "@%#*+=-:. "

def map_pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""

    for pixel in pixels:
        index = int(pixel / 255 * (len(ASCII_CHARS) - 1))
        ascii_str += ASCII_CHARS[index]

    return ascii_str
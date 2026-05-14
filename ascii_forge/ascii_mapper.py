DEFAULT_ASCII_CHARS = "@%#*+=-:. "


def map_pixels_to_ascii(image, chars: str = DEFAULT_ASCII_CHARS):
    """Map grayscale pixels to ASCII characters.

    Args:
        image: Grayscale PIL Image.
        chars: Character ramp string ordered dense → sparse.
               Defaults to the built-in ramp.

    Returns:
        A flat string of ASCII characters (no newlines).
    """
    pixels = image.getdata()
    ascii_str = ""
    ramp = chars if chars else DEFAULT_ASCII_CHARS

    for pixel in pixels:
        index = int(pixel / 255 * (len(ramp) - 1))
        ascii_str += ramp[index]

    return ascii_str

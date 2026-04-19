def generate_ascii(image, colored=False, invert=False):
    """
    Convert a PIL image into an ASCII string.

    Args:
        image:   PIL Image — grayscale ("L") or RGB depending on `colored`.
        colored: If True, wraps each char in ANSI escape codes using RGB pixel color.
        invert:  If True, flips the grayscale value used for character selection
                 (dense chars on bright areas, sparse on dark). Display colors unchanged.

    Returns:
        A multi-line string of ASCII characters ready to print.
    """
    pixels = list(image.getdata())
    width = image.width

    ASCII_CHARS = "@%#*+=-:. "
    ascii_img = ""

    for i in range(0, len(pixels), width):
        row = pixels[i : i + width]

        for pixel in row:
            if colored:
                r, g, b = pixel
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            else:
                gray = pixel  # already grayscale

            # Invert only the brightness used for char selection — not the display color
            if invert:
                gray = 255 - gray

            index = int(gray / 255 * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[index]

            if colored:
                ascii_img += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
            else:
                ascii_img += char

        ascii_img += "\n"

    return ascii_img

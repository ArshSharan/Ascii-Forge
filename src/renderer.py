def format_ascii(ascii_str, width):
    return "\n".join(
        [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
    )

# Rendering colored ASCII directly in terminal using ANSI escape codes
def render_color_ascii(image):
    pixels = list(image.getdata())
    width = image.width

    ASCII_CHARS = "@%#*+=-:. "

    for i in range(0, len(pixels), width):
        row = pixels[i:i + width]

        for r, g, b in row:
            # Convert to grayscale (for choosing ASCII char)
            gray = int(0.299*r + 0.587*g + 0.114*b)

            # Map grayscale to ASCII
            index = int(gray / 255 * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[index]

            # Print with color
            print(f"\033[38;2;{r};{g};{b}m{char}\033[0m", end="")

        print()

def generate_ascii(image, colored=False, invert=False):
    pixels = list(image.getdata())
    width = image.width

    ASCII_CHARS = "@%#*+=-:. "
    ascii_img = ""

    for i in range(0, len(pixels), width):
        row = pixels[i:i + width]

        for pixel in row:
            if colored:
                r, g, b = pixel
                gray = int(0.299*r + 0.587*g + 0.114*b)
            else:
                gray = pixel  # already grayscale

            # Invert only the brightness used for char selection, not the display color
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
from image_loader import load_image
from processor import resize
from ascii_mapper import map_pixels_to_ascii
from renderer import format_ascii, render_color_ascii

IMAGE_PATH = "../assets/Image2.jpg"

def run_grayscale():
    image = load_image(IMAGE_PATH)
    image = resize(image)
    image = image.convert("L")

    ascii_str = map_pixels_to_ascii(image)
    ascii_img = format_ascii(ascii_str, image.width)

    print(ascii_img)


def run_color():
    image = load_image(IMAGE_PATH)
    image = resize(image)

    render_color_ascii(image)


if __name__ == "__main__":
    mode = input("Choose mode (gray/color): ").strip().lower()

    if mode == "color":
        run_color()
    else:
        run_grayscale()
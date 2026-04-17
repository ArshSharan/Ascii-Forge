import argparse
from image_loader import load_image
from processor import resize
from renderer import generate_ascii


def main():
    parser = argparse.ArgumentParser(
        description="ASCII Forge - Convert images to ASCII art"
    )

    parser.add_argument("image", help="Path to input image")
    parser.add_argument("--mode", choices=["gray", "color"], default="gray",
                        help="Rendering mode")
    parser.add_argument("--width", type=int, default=100,
                        help="Output width")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    # Load image
    image = load_image(args.image)
    image = resize(image, args.width)

    # Convert if grayscale mode
    if args.mode == "gray":
        image = image.convert("L")
        ascii_img = generate_ascii(image, colored=False)
    else:
        ascii_img = generate_ascii(image, colored=True)

    # Print to terminal
    print(ascii_img)

    # Save if output specified
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ascii_img)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
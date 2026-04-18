import argparse
from src.image_loader import load_image
from src.processor import resize
from src.renderer import generate_ascii

def main():
    parser = argparse.ArgumentParser(
        prog="ascii-forge",
        description="""
=== ASCII Forge ===
Convert images into high-quality ASCII art directly in your terminal.

Examples:
  python main.py image.jpg
  python main.py image.jpg --mode color
  python main.py image.jpg --width 150 --output out.txt
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "image",
        help="Path to input image (jpg/png)"
    )

    parser.add_argument(
        "--mode",
        choices=["gray", "color"],
        default="gray",
        help="Rendering mode: gray (default) or color"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=100,
        help="Width of ASCII output (default: 100)"
    )

    parser.add_argument(
        "--output",
        help="Save output to file (e.g., output.txt)"
    )

    args = parser.parse_args()

    # Load + process
    image = load_image(args.image)
    image = resize(image, args.width)

    if args.mode == "gray":
        image = image.convert("L")
        ascii_img = generate_ascii(image, colored=False)
    else:
        ascii_img = generate_ascii(image, colored=True)

    print(ascii_img)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ascii_img)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
import argparse
import os
from src.image_loader import load_image
from src.processor import resize
from src.renderer import generate_ascii
from src.html_exporter import save_html


def main():
    parser = argparse.ArgumentParser(
        prog="ascii-forge",
        description="""\
=== ASCII Forge ===
Convert images into high-quality ASCII art directly in your terminal.

Examples:
  ascii-forge image.jpg
  ascii-forge image.jpg --mode color
  ascii-forge image.jpg --width 150 --output out.txt
  ascii-forge image.jpg --mode color --html output/art.html
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
        help="Width of ASCII output in characters (default: 100)"
    )

    parser.add_argument(
        "--output",
        help="Save plain-text / ANSI output to file (e.g., output.txt)"
    )

    parser.add_argument(
        "--invert",
        action="store_true",
        help="Invert pixel colors before rendering (photo-negative effect).\n"
             "Improves contrast on light-background subjects. Works with all modes."
    )

    parser.add_argument(
        "--html",
        metavar="FILE",
        help="Export colored ASCII art as a self-contained HTML file\n"
             "(e.g., --html output/art.html). Requires --mode color."
    )

    args = parser.parse_args()

    # ── Load & resize ──────────────────────────────────────────────────────────
    image = load_image(args.image)
    image = resize(image, args.width)

    # ── HTML export path ───────────────────────────────────────────────────────
    if args.html:
        # HTML export always works from the RGB image (color data required)
        rgb_image = image.convert("RGB")

        # Auto-create parent directory if it doesn't exist
        html_dir = os.path.dirname(args.html)
        if html_dir:
            os.makedirs(html_dir, exist_ok=True)

        image_name = os.path.basename(args.image)
        title = f"ASCII Forge — {image_name}"

        save_html(rgb_image, args.html, title=title, invert=args.invert)
        print(f"HTML export saved to: {args.html}")

        # If the user only asked for HTML, we're done — skip terminal render
        if not args.output:
            return

    # ── Terminal render ────────────────────────────────────────────────────────
    if args.mode == "gray":
        image = image.convert("L")
        ascii_img = generate_ascii(image, colored=False, invert=args.invert)
    else:
        ascii_img = generate_ascii(image, colored=True, invert=args.invert)

    print(ascii_img)

    # ── Optional plain-text / ANSI save ───────────────────────────────────────
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ascii_img)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
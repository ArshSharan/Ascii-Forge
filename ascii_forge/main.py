import argparse
import os
import sys
from ascii_forge.image_loader import load_image
from ascii_forge.processor import resize, invert_colors
from ascii_forge.renderer import generate_ascii
from ascii_forge.html_exporter import save_html
from ascii_forge.braille_mapper import image_to_braille, image_to_braille_color

# Ensure Unicode (braille) characters print correctly on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")



def main():
    parser = argparse.ArgumentParser(
        prog="ascii-forger",
        description="""\
=== ASCII Forger ===
Convert images into high-quality ASCII art directly in your terminal.

Examples:
  ascii-forger image.jpg
  ascii-forger image.jpg --mode color
  ascii-forger image.jpg --mode braille --width 80
  ascii-forger image.jpg --mode braille-color --invert
  ascii-forger image.jpg --width 150 --output out.txt
  ascii-forger image.jpg --mode color --html outputs/art.html
  ascii-forger image.jpg --mode braille --html outputs/braille.html
  ascii-forger image.jpg --invert --html outputs/inverted.html
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "image",
        help="Path to input image (jpg/png)"
    )

    parser.add_argument(
        "--mode",
        choices=["gray", "color", "braille", "braille-color"],
        default="gray",
        help=(
            "Rendering mode (default: gray):\n"
            "  gray          — standard ASCII, grayscale\n"
            "  color         — standard ASCII, ANSI true-color\n"
            "  braille       — Unicode braille dots, grayscale (4x resolution)\n"
            "  braille-color — Unicode braille dots, ANSI true-color"
        )
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
             "Works with all modes including braille."
    )

    parser.add_argument(
        "--html",
        metavar="FILE",
        help="Export ASCII art as a self-contained HTML file\n"
             "(e.g., --html outputs/art.html)"
    )

    args = parser.parse_args()

    # ── Load & resize ──────────────────────────────────────────────────────────
    image = load_image(args.image)
    image = resize(image, args.width)

    image_name = os.path.basename(args.image)

    # ── Invert colors (applied once, before all downstream processing) ─────────
    if args.invert:
        image = invert_colors(image)

    # ── HTML export ──────────────────────────────────────────────────────────
    if args.html:
        rgb_image = image.convert("RGB")
        html_dir = os.path.dirname(args.html)
        if html_dir:
            os.makedirs(html_dir, exist_ok=True)

        save_html(
            rgb_image,
            args.html,
            title=image_name,
            invert=args.invert,
            image_name=image_name,
            output_width=args.width,
            mode=args.mode,
        )
        print(f"HTML export saved to: {args.html}")

        if not args.output:
            return

    # ── Terminal render ──────────────────────────────────────────────────────────
    if args.mode == "gray":
        ascii_img = generate_ascii(image.convert("L"), colored=False, invert=False)
    elif args.mode == "color":
        ascii_img = generate_ascii(image, colored=True, invert=False)
    elif args.mode == "braille":
        ascii_img = image_to_braille(image, invert=False)
    else:  # braille-color
        ascii_img = image_to_braille_color(image, invert=False)

    print(ascii_img)

    # ── Optional plain-text / ANSI save ───────────────────────────────────────────
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ascii_img)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()

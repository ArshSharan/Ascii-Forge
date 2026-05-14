"""
image_exporter.py
-----------------
Render ASCII art as a raster (PNG / JPEG) or vector (SVG) image file.

Format is inferred from the output path extension:
  .png          → Pillow ImageDraw, lossless
  .jpg / .jpeg  → Pillow ImageDraw, JPEG quality 95
  .svg          → pure-Python SVG string, infinitely scalable
"""

from __future__ import annotations

import os
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

# ── Constants ───────────────────────────────────────────────────────────────

DEFAULT_ASCII_CHARS = "@%#*+=-:. "

# Monospace font search list (Windows → Linux → macOS → built-in fallback)
_FONT_CANDIDATES = [
    "cour.ttf",           # Courier New — Windows
    "DejaVuSansMono.ttf", # DejaVu — most Linux distros
    "LiberationMono-Regular.ttf",
    "UbuntuMono-R.ttf",
    "Menlo.ttc",          # macOS
]

_FONT_SIZE = 10  # px — balances resolution vs. file size


# ── Internal helpers ─────────────────────────────────────────────────────────

def _load_font(size: int = _FONT_SIZE) -> ImageFont.FreeTypeFont:
    """Return the first available monospace TrueType font, or the built-in default."""
    for name in _FONT_CANDIDATES:
        try:
            return ImageFont.truetype(name, size)
        except (IOError, OSError):
            continue
    # Pillow built-in bitmap font — always available, fixed size
    return ImageFont.load_default()


def _build_char_grid(
    image,
    chars: str = DEFAULT_ASCII_CHARS,
    invert: bool = False,
) -> List[List[Tuple[str, int, int, int]]]:
    """
    Convert an RGB PIL image into a 2-D grid of (char, r, g, b) tuples.

    Each cell corresponds to one pixel in the (already-resized) image.
    """
    ramp = chars if chars else DEFAULT_ASCII_CHARS
    rgb_image = image.convert("RGB")
    pixels = list(rgb_image.getdata())
    width = rgb_image.width

    grid: List[List[Tuple[str, int, int, int]]] = []

    for row_start in range(0, len(pixels), width):
        row_data = pixels[row_start : row_start + width]
        row: List[Tuple[str, int, int, int]] = []
        for r, g, b in row_data:
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            if invert:
                gray = 255 - gray
            index = int(gray / 255 * (len(ramp) - 1))
            row.append((ramp[index], r, g, b))
        grid.append(row)

    return grid


# ── Raster export (PNG / JPEG) ────────────────────────────────────────────────

def _render_raster(
    grid: List[List[Tuple[str, int, int, int]]],
    font: ImageFont.FreeTypeFont,
) -> Image.Image:
    """Paint the char grid onto a black Pillow canvas and return the Image."""

    # Measure a single character cell
    # getbbox returns (left, top, right, bottom)
    sample_bbox = font.getbbox("@")
    char_w = sample_bbox[2] - sample_bbox[0]
    char_h = sample_bbox[3] - sample_bbox[1]

    # Add a small vertical gap so lines don't collide
    line_h = int(char_h * 1.25)

    cols = max(len(row) for row in grid)
    rows = len(grid)

    img_w = cols * char_w
    img_h = rows * line_h

    canvas = Image.new("RGB", (img_w, img_h), color=(0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    for y, row in enumerate(grid):
        for x, (char, r, g, b) in enumerate(row):
            if char == " ":
                continue
            draw.text(
                (x * char_w, y * line_h),
                char,
                fill=(r, g, b),
                font=font,
            )

    return canvas


def save_png(
    image,
    output_path: str,
    chars: str = DEFAULT_ASCII_CHARS,
    invert: bool = False,
) -> None:
    """Export ASCII art as a PNG file."""
    font = _load_font()
    grid = _build_char_grid(image, chars=chars, invert=invert)
    canvas = _render_raster(grid, font)
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)


def save_jpeg(
    image,
    output_path: str,
    chars: str = DEFAULT_ASCII_CHARS,
    invert: bool = False,
) -> None:
    """Export ASCII art as a JPEG file (quality 95)."""
    font = _load_font()
    grid = _build_char_grid(image, chars=chars, invert=invert)
    canvas = _render_raster(grid, font)
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    canvas.save(output_path, format="JPEG", quality=95)


# ── SVG export ────────────────────────────────────────────────────────────────

def save_svg(
    image,
    output_path: str,
    chars: str = DEFAULT_ASCII_CHARS,
    invert: bool = False,
    font_size: int = _FONT_SIZE,
) -> None:
    """
    Export ASCII art as a scalable SVG file.

    Each character is a <tspan> inside a per-row <text> element, colored with
    its source pixel's RGB value. No external dependencies — pure Python strings.
    """
    grid = _build_char_grid(image, chars=chars, invert=invert)

    # Approximate monospace metrics: 0.6 em wide, 1.2 em tall
    char_w = font_size * 0.601
    line_h = font_size * 1.25

    svg_w = int(char_w * max(len(row) for row in grid)) + font_size
    svg_h = int(line_h * len(grid)) + font_size

    lines: list[str] = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_w}" height="{svg_h}" '
        f'style="background:#000;">'
    )
    lines.append(
        f'<style>text{{font-family:"Fira Code","Courier New",Courier,monospace;'
        f'font-size:{font_size}px;white-space:pre;}}</style>'
    )

    for row_idx, row in enumerate(grid):
        y = int((row_idx + 1) * line_h)
        # Build one <text> per row with inline <tspan fill="..."> per char
        spans: list[str] = []
        for char, r, g, b in row:
            safe = (
                char.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
            )
            if safe == " ":
                spans.append("&#160;")  # non-breaking space preserves spacing
            else:
                spans.append(f'<tspan fill="rgb({r},{g},{b})">{safe}</tspan>')

        lines.append(f'<text x="0" y="{y}">{"".join(spans)}</text>')

    lines.append("</svg>")

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Public dispatch ───────────────────────────────────────────────────────────

def save_image(
    image,
    output_path: str,
    chars: str = DEFAULT_ASCII_CHARS,
    invert: bool = False,
) -> None:
    """
    Export ASCII art to an image file.

    The output format is inferred from the file extension:
      .png          → lossless raster (Pillow)
      .jpg / .jpeg  → JPEG quality-95 raster (Pillow)
      .svg          → scalable vector (pure Python)

    Args:
        image:       PIL Image (already resized).
        output_path: Destination file path.
        chars:       Character ramp (dense → sparse).
        invert:      When True, flip the brightness→char mapping.

    Raises:
        ValueError: If the file extension is not a supported format.
    """
    ext = os.path.splitext(output_path)[1].lower()
    if ext == ".png":
        save_png(image, output_path, chars=chars, invert=invert)
    elif ext in (".jpg", ".jpeg"):
        save_jpeg(image, output_path, chars=chars, invert=invert)
    elif ext == ".svg":
        save_svg(image, output_path, chars=chars, invert=invert)
    else:
        raise ValueError(
            f"Unsupported export format '{ext}'. "
            "Use .png, .jpg, .jpeg, or .svg"
        )

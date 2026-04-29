"""
braille_mapper.py
-----------------
Converts a PIL image into Unicode Braille art.

Each braille character (U+2800–U+28FF) encodes an 8-dot 2×4 grid.
We map every 2-wide × 4-tall pixel block to one braille character,
achieving ~4× the effective resolution of standard ASCII rendering.

Dot layout within a 2×4 cell (Unicode Braille standard):

    col 0  col 1
    ·1     ·4     ← row 0   bits: 0, 3
    ·2     ·5     ← row 1   bits: 1, 4
    ·3     ·6     ← row 2   bits: 2, 5
    ·7     ·8     ← row 3   bits: 6, 7

A dot is "on" if its pixel intensity crosses the threshold.
"""

# Unicode Braille block base address
_BRAILLE_BASE = 0x2800

# (col_offset, row_offset, bit_position) for each of the 8 dots
_DOT_MAP = [
    (0, 0, 0),  # dot 1 → bit 0
    (0, 1, 1),  # dot 2 → bit 1
    (0, 2, 2),  # dot 3 → bit 2
    (1, 0, 3),  # dot 4 → bit 3
    (1, 1, 4),  # dot 5 → bit 4
    (1, 2, 5),  # dot 6 → bit 5
    (0, 3, 6),  # dot 7 → bit 6
    (1, 3, 7),  # dot 8 → bit 7
]

_THRESHOLD = 128  # grayscale cutoff: >= threshold → dot ON


def _prepare_image(image, target_mode: str):
    """
    Ensure image dimensions are exact multiples of 2 (width) and 4 (height),
    required for clean 2×4 block tiling. Returns the cropped image.
    """
    img = image.convert(target_mode)
    w, h = img.size
    w_clean = (w // 2) * 2
    h_clean = (h // 4) * 4
    if w_clean != w or h_clean != h:
        img = img.crop((0, 0, w_clean, h_clean))
    return img


def image_to_braille(image, invert: bool = False) -> str:
    """
    Convert a PIL image to grayscale Braille Unicode art.

    Each 2×4 pixel block becomes one braille character. A pixel is
    treated as a lit dot when its grayscale value meets the threshold
    (or falls below it when inverted).

    Args:
        image:  PIL Image (any mode — converted internally to 'L').
        invert: If True, dark pixels become lit dots (light-on-dark rendering).

    Returns:
        A multi-line string of braille characters ready for print().
    """
    gray = _prepare_image(image, "L")
    w, h = gray.size
    pixels = gray.load()

    rows = []
    for y in range(0, h, 4):
        chars = []
        for x in range(0, w, 2):
            bits = 0
            for col, row, bit in _DOT_MAP:
                px, py = x + col, y + row
                if px < w and py < h:
                    val = pixels[px, py]
                    dot_on = (val < _THRESHOLD) if invert else (val >= _THRESHOLD)
                    if dot_on:
                        bits |= (1 << bit)
            chars.append(chr(_BRAILLE_BASE + bits))
        rows.append("".join(chars))

    return "\n".join(rows)


def image_to_braille_color(image, invert: bool = False) -> str:
    """
    Convert a PIL image to ANSI true-color Braille Unicode art.

    Dot on/off follows the same threshold logic as image_to_braille().
    The ANSI color applied to each character is the average RGB of its
    2×4 pixel block, preserving the original image palette.

    Args:
        image:  PIL Image (any mode — converted internally to 'RGB' and 'L').
        invert: If True, dark pixels become lit dots.

    Returns:
        A multi-line string with ANSI escape codes, suitable for terminals
        that support true-color (24-bit) ANSI sequences.
    """
    rgb = _prepare_image(image, "RGB")
    gray = _prepare_image(image, "L")
    w, h = rgb.size
    rgb_px = rgb.load()
    gray_px = gray.load()

    rows = []
    for y in range(0, h, 4):
        chars = []
        for x in range(0, w, 2):
            bits = 0
            r_sum = g_sum = b_sum = n = 0

            for col, row, bit in _DOT_MAP:
                px, py = x + col, y + row
                if px < w and py < h:
                    val = gray_px[px, py]
                    r, g, b = rgb_px[px, py]
                    r_sum += r; g_sum += g; b_sum += b; n += 1

                    dot_on = (val < _THRESHOLD) if invert else (val >= _THRESHOLD)
                    if dot_on:
                        bits |= (1 << bit)

            char = chr(_BRAILLE_BASE + bits)
            if n:
                r_avg = r_sum // n
                g_avg = g_sum // n
                b_avg = b_sum // n
                chars.append(f"\033[38;2;{r_avg};{g_avg};{b_avg}m{char}\033[0m")
            else:
                chars.append(char)

        rows.append("".join(chars))

    return "\n".join(rows)

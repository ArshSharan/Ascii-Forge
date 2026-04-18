import html as html_lib


ASCII_CHARS = "@%#*+=-:. "


def _pixel_to_char(gray: int) -> str:
    """Map a 0-255 grayscale intensity to an ASCII character."""
    index = int(gray / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


def generate_html(image, title: str = "ASCII Forge Output") -> str:
    """
    Convert a PIL image into a self-contained HTML string.

    Each character is wrapped in a <span> with an inline color style
    matching the original pixel's RGB value. The output is a complete,
    browser-renderable HTML document with embedded dark-mode styling.

    Args:
        image: PIL Image object (RGB mode).
        title: Title shown in the browser tab.

    Returns:
        A complete HTML string ready to be written to a .html file.
    """
    pixels = list(image.getdata())
    width = image.width

    rows_html = []

    for i in range(0, len(pixels), width):
        row = pixels[i : i + width]
        row_spans = []

        for pixel in row:
            # Handle both RGB tuples and grayscale single values
            if isinstance(pixel, (tuple, list)):
                r, g, b = pixel[0], pixel[1], pixel[2]
            else:
                r = g = b = pixel

            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            char = _pixel_to_char(gray)

            # Escape the character for safe HTML embedding
            safe_char = html_lib.escape(char) if char not in (" ",) else "&nbsp;"

            row_spans.append(
                f'<span style="color:rgb({r},{g},{b})">{safe_char}</span>'
            )

        rows_html.append("".join(row_spans))

    body_content = "<br>".join(rows_html)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_lib.escape(title)}</title>
  <style>
    /* ── ASCII Forge — HTML Export ── */
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: #0d0d0d;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 2rem 1rem;
      font-family: 'Courier New', Courier, monospace;
    }}

    header {{
      text-align: center;
      margin-bottom: 1.5rem;
    }}

    header h1 {{
      font-size: 1.4rem;
      font-weight: 700;
      letter-spacing: 0.25em;
      text-transform: uppercase;
      background: linear-gradient(90deg, #a78bfa, #60a5fa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}

    header p {{
      font-size: 0.75rem;
      color: #6b7280;
      margin-top: 0.4rem;
      letter-spacing: 0.1em;
    }}

    .ascii-canvas {{
      display: inline-block;
      line-height: 1.15;
      font-size: 10px;
      letter-spacing: 0.05em;
      white-space: pre;
      background: #000;
      padding: 1rem 1.2rem;
      border-radius: 8px;
      border: 1px solid #1f2937;
      box-shadow: 0 0 40px rgba(96, 165, 250, 0.08);
    }}

    footer {{
      margin-top: 1.5rem;
      font-size: 0.7rem;
      color: #374151;
      letter-spacing: 0.08em;
    }}
  </style>
</head>
<body>
  <header>
    <h1>⬡ ASCII Forge</h1>
    <p>Generated with ascii-forge &mdash; terminal-based ASCII art engine</p>
  </header>

  <div class="ascii-canvas">
{body_content}
  </div>

  <footer>ascii-forge &copy; {html_lib.escape(title)}</footer>
</body>
</html>
"""
    return html_doc


def save_html(image, output_path: str, title: str = "ASCII Forge Output") -> None:
    """
    Generate and write an HTML ASCII art file to disk.

    Args:
        image: PIL Image object (RGB mode).
        output_path: Destination file path (e.g., 'output/art.html').
        title: Optional page title (defaults to 'ASCII Forge Output').
    """
    html_content = generate_html(image, title=title)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

import html as html_lib
import datetime


ASCII_CHARS = "@%#*+=-:. "


def _pixel_to_char(gray: int) -> str:
    """Map a 0-255 grayscale intensity to an ASCII character."""
    index = int(gray / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


def generate_html(
    image,
    title: str = "ASCII Forge Output",
    invert: bool = False,
    image_name: str = "",
    output_width: int = 100,
    mode: str = "color",
) -> str:
    """
    Convert a PIL image into a self-contained HTML string.

    Each character is wrapped in a <span style="color:rgb(...)"> tag using
    the original pixel's RGB value. Character density is optionally inverted.

    Args:
        image:        PIL Image object (RGB mode).
        title:        Title shown in the browser tab.
        invert:       When True, flips the grayscale value for char selection.
                      Original pixel colors are always preserved.
        image_name:   Source filename, displayed in the metadata bar.
        output_width: Width used for generation, displayed in the metadata bar.
        mode:         Rendering mode label ('gray' or 'color').

    Returns:
        A complete, self-contained HTML string ready to write to a .html file.
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

            # Invert char density mapping only — colors stay original
            if invert:
                gray = 255 - gray

            char = _pixel_to_char(gray)
            safe_char = html_lib.escape(char) if char != " " else "&nbsp;"
            row_spans.append(f'<span style="color:rgb({r},{g},{b})">{safe_char}</span>')

        rows_html.append("".join(row_spans))

    body_content = "\n".join(rows_html)

    # ── Metadata badge values ─────────────────────────────────────────────────
    safe_image_name = html_lib.escape(image_name) if image_name else "image"
    mode_label      = "color" if mode == "color" else "grayscale"
    invert_badge    = '<span class="badge badge-invert">&#8644; inverted</span>' if invert else ""
    year            = datetime.datetime.now().year
    escaped_title   = html_lib.escape(title)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ASCII Forge &#x2014; {escaped_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg:           #09090f;
      --canvas-bg:    #000000;
      --border-glow:  rgba(99, 102, 241, 0.22);
      --border-glow2: rgba(56, 189, 248, 0.10);
      --accent:       #818cf8;
      --accent2:      #38bdf8;
      --text-dim:     #374151;
      --text-muted:   #6b7280;
      --text-soft:    #9ca3af;
    }}

    body {{
      background-color: var(--bg);
      background-image:
        radial-gradient(ellipse at 15% 12%, rgba(99,102,241,0.06) 0%, transparent 52%),
        radial-gradient(ellipse at 85% 88%, rgba(56,189,248,0.05) 0%, transparent 52%);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 3.5rem 1.5rem 3rem;
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }}

    /* ── Header ─────────────────────────────────────────────────────── */
    .forge-header {{
      text-align: center;
      margin-bottom: 2rem;
    }}

    .forge-logo {{
      font-size: 1.55rem;
      font-weight: 700;
      letter-spacing: 0.32em;
      text-transform: uppercase;
      background: linear-gradient(130deg, #c4b5fd 0%, #818cf8 42%, #38bdf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 0.5rem;
      user-select: none;
    }}

    .forge-subtitle {{
      font-size: 0.68rem;
      color: var(--text-muted);
      letter-spacing: 0.2em;
      text-transform: uppercase;
    }}

    /* ── Metadata badges ─────────────────────────────────────────────── */
    .meta-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      justify-content: center;
      margin-bottom: 1.75rem;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.28rem;
      padding: 0.22rem 0.72rem;
      border-radius: 9999px;
      font-size: 0.67rem;
      font-weight: 500;
      letter-spacing: 0.04em;
      border: 1px solid rgba(99,102,241,0.12);
      background: rgba(255,255,255,0.025);
      color: var(--text-soft);
    }}

    .badge-mode {{
      border-color: rgba(56,189,248,0.25);
      color: #7dd3fc;
      background: rgba(56,189,248,0.06);
    }}

    .badge-invert {{
      border-color: rgba(167,139,250,0.3);
      color: #c4b5fd;
      background: rgba(99,102,241,0.07);
    }}

    /* ── Canvas with gradient-border trick ───────────────────────────── */
    .canvas-wrapper {{
      border-radius: 11px;
      padding: 1px;
      background: linear-gradient(
        135deg,
        var(--border-glow) 0%,
        var(--border-glow2) 55%,
        rgba(99,102,241,0.05) 100%
      );
      box-shadow:
        0 0 80px rgba(99,102,241,0.07),
        0 25px 70px rgba(0,0,0,0.55);
      max-width: 100%;
      overflow-x: auto;
    }}

    .ascii-canvas {{
      display: block;
      line-height: 1.2;
      font-family: 'Fira Code', 'Courier New', Courier, monospace;
      font-size: 9.5px;
      font-weight: 300;
      letter-spacing: 0.035em;
      white-space: pre;
      background: var(--canvas-bg);
      padding: 1.25rem 1.5rem;
      border-radius: 10px;
    }}

    /* ── Footer ────────────────────────────────────────────────────── */
    .forge-footer {{
      margin-top: 2rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 0.62rem;
      color: var(--text-dim);
      letter-spacing: 0.07em;
    }}

    .forge-footer a {{
      color: var(--text-dim);
      text-decoration: none;
    }}

    .forge-footer a:hover {{ color: var(--text-muted); }}
    .forge-footer .sep   {{ opacity: 0.25; }}
  </style>
</head>
<body>

  <header class="forge-header">
    <div class="forge-logo">&#x2B21;&nbsp; ASCII&nbsp;FORGE</div>
    <div class="forge-subtitle">terminal&#x2011;based ASCII art engine</div>
  </header>

  <div class="meta-bar">
    <span class="badge">&#128196; {safe_image_name}</span>
    <span class="badge">&#8596; {output_width} chars</span>
    <span class="badge badge-mode">{mode_label}</span>
    {invert_badge}
  </div>

  <div class="canvas-wrapper">
    <div class="ascii-canvas">{body_content}</div>
  </div>

  <footer class="forge-footer">
    <span>ascii-forge</span>
    <span class="sep">&#183;</span>
    <a href="https://github.com/ArshSharan/Ascii-Forge" target="_blank" rel="noopener">
      github.com/ArshSharan/Ascii-Forge
    </a>
    <span class="sep">&#183;</span>
    <span>&#169; {year}</span>
  </footer>

</body>
</html>
"""
    return html_doc


def save_html(
    image,
    output_path: str,
    title: str = "ASCII Forge Output",
    invert: bool = False,
    image_name: str = "",
    output_width: int = 100,
    mode: str = "color",
) -> None:
    """
    Generate and write an HTML ASCII art file to disk.

    Args:
        image:        PIL Image object (RGB mode).
        output_path:  Destination file path (e.g., 'outputs/art.html').
        title:        Page title string.
        invert:       When True, inverts the character density mapping.
        image_name:   Source filename shown in the metadata bar.
        output_width: Output width (chars) shown in the metadata bar.
        mode:         Rendering mode ('gray' or 'color') shown in the metadata bar.
    """
    html_content = generate_html(
        image,
        title=title,
        invert=invert,
        image_name=image_name,
        output_width=output_width,
        mode=mode,
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

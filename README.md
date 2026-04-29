# ASCII Forger

[![PyPI version](https://img.shields.io/pypi/v/ascii-forger)](https://pypi.org/project/ascii-forger/)
[![Python 3.8+](https://img.shields.io/pypi/pyversions/ascii-forger)](https://pypi.org/project/ascii-forger/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ASCII Forger is a terminal-based ASCII rendering engine that converts images into high-fidelity ASCII art. It supports grayscale, color, and **braille Unicode** rendering modes and is designed as a modular, extensible command-line tool.

The project focuses on bridging image processing concepts with terminal rendering, providing a practical implementation of pixel-to-character mapping, perceptual brightness scaling, ANSI-based color encoding, and Unicode braille dot rendering.

---

## Features

- Convert images to ASCII art directly in the terminal
- Grayscale and color rendering modes
- **Braille Unicode mode** — 4× effective resolution using Unicode dot-matrix characters (`⣿⠿⡇`)
- **HTML export** — save colored ASCII art as a self-contained `.html` file, viewable in any browser
- **Invert mode** — flip pixel colors for a photo-negative effect, ideal for light-background subjects
- Adjustable output width for resolution control
- File output support (plain text / ANSI)
- Modular and extensible architecture
- CLI-based usage with argument parsing

---

## How It Works

The system follows a structured pipeline:

1. **Image Loading**
   The input image is loaded using Pillow.

2. **Resizing**
   The image is resized while maintaining aspect ratio. A correction factor is applied to account for non-square terminal characters.

3. **Grayscale Conversion (optional)**
   For grayscale mode, the image is converted using luminance weighting.

4. **Pixel Mapping**
   Each pixel is mapped to an ASCII character based on its intensity.

5. **Rendering**
   - `gray` — standard ASCII, brightness → character density, grayscale output
   - `color` — standard ASCII with ANSI true-color per character
   - `braille` — each 2×4 pixel block is encoded as a Unicode braille character (`U+2800`–`U+28FF`), achieving ~4× spatial resolution per terminal column
   - `braille-color` — braille dot encoding with ANSI true-color (average RGB of each block)

6. **HTML Export (optional)**
   Each character is wrapped in a `<span style="color:rgb(...)">` tag, producing a pixel-accurate, browser-renderable HTML file with no external dependencies.

---

## Project Structure

```
ascii-forge/
│
├── ascii_forge/           # Main package
│   ├── __init__.py
│   ├── main.py
│   ├── image_loader.py
│   ├── processor.py
│   ├── ascii_mapper.py
│   ├── renderer.py
│   ├── html_exporter.py
│   └── braille_mapper.py  # Braille Unicode renderer (new in v0.2.0)
│
├── assets/            # Local test images (ignored by Git)
├── outputs/           # Generated outputs (ignored by Git)
│
├── pyproject.toml     # Package configuration (PyPI-ready)
├── requirements.txt
├── README.md
└── SETUP.md
```

---

## Installation

### Recommended — `pipx` *(for CLI tools)*

[pipx](https://pipx.pypa.io) installs CLI tools into isolated environments and **automatically adds the command to your PATH** — no venv activation, no PATH fiddling required.

```bash
# Install pipx if you don't have it
pip install pipx
pipx ensurepath

# Then install ascii-forger
pipx install ascii-forger
```

After that, `ascii-forger` works in **any terminal, anywhere on your system**.

**Upgrade to a new version:**

```bash
pipx upgrade ascii-forger
```

---

### Alternative — `pip install`

```bash
pip install ascii-forger
```

> **Note for Windows users:** If the `ascii-forger` command is not found after `pip install`, your Python `Scripts\` directory may not be on your PATH. Either use `pipx` (above) or add `%APPDATA%\Python\Python3XX\Scripts` to your system PATH manually.

**Upgrade to a new version:**

```bash
pip install --upgrade ascii-forger
```

---

### From Source *(for development)*

Clone the repository:

```bash
git clone https://github.com/ArshSharan/Ascii-Forge.git
cd Ascii-Forge
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install in editable mode:

```bash
pip install -e .
```

> Uses `pyproject.toml` for packaging (PEP 517/518 compliant).

---

## Usage

Basic usage:

```bash
ascii-forger path/to/image.jpg
```

Color rendering:

```bash
ascii-forger path/to/image.jpg --mode color
```

Custom width:

```bash
ascii-forger path/to/image.jpg --width 150
```

Save output to file:

```bash
ascii-forger path/to/image.jpg --output output.txt
```

Export as HTML (browser-viewable, colored):

```bash
ascii-forger path/to/image.jpg --html outputs/art.html
```

HTML export with custom width:

```bash
ascii-forger path/to/image.jpg --width 150 --html outputs/art.html
```

Full example (terminal render + HTML export simultaneously):

```bash
ascii-forger path/to/image.jpg --mode color --width 120 --output output.txt --html outputs/art.html
```

Invert colors (photo-negative, great for light-background portraits):

```bash
ascii-forger path/to/image.jpg --invert
```

Invert with HTML export:

```bash
ascii-forger path/to/image.jpg --invert --html outputs/inverted.html
```

Braille Unicode rendering (4× resolution, grayscale):

```bash
ascii-forger path/to/image.jpg --mode braille --width 80
```

Braille with true-color:

```bash
ascii-forger path/to/image.jpg --mode braille-color --width 100
```

Braille + invert + HTML export:

```bash
ascii-forger path/to/image.jpg --mode braille --invert --html outputs/braille.html
```

---

## Command-Line Arguments

| Argument   | Description                                                                                         | Default  |
|------------|-----------------------------------------------------------------------------------------------------|----------|
| `image`    | Path to input image                                                                                 | Required |
| `--mode`   | `gray` \| `color` \| `braille` \| `braille-color`                                                  | `gray`   |
| `--width`  | Output width in characters                                                                          | `100`    |
| `--output` | File path to save plain-text / ANSI output                                                          | None     |
| `--html`   | File path to save a self-contained HTML export (e.g. `outputs/art.html`)                           | None     |
| `--invert` | Invert pixel colors before rendering (photo-negative). Works with all modes.                        | Off      |

---

## Notes on Color Output

Color mode uses ANSI escape sequences. As a result:

- Output files will contain ANSI codes
- Standard text editors may not render colors
- Terminal environments that support ANSI will display colors correctly

## Notes on HTML Export

- The `--html` flag produces a **self-contained HTML file** — no internet connection or external assets required
- Colors are embedded as inline `rgb()` styles, so the output is fully portable
- The file can be opened in any modern browser
- Parent output directories are created automatically if they don't exist
- HTML export is independent of `--mode`; it always uses the full-color pixel data

## Notes on Invert Mode

`--invert` flips the **character density mapping** only — it does **not** alter pixel colors:

- Without invert: dark pixel → dense char (`@`), bright pixel → sparse char (` `)
- With invert: bright pixel → dense char (`@`), dark pixel → sparse char (` `)
- This makes light-background subjects (e.g. portraits with white backgrounds) appear much more defined
- Works with all modes: `gray`, `color`, `braille`, `braille-color`, and `--html`
- Pixel colors in color/HTML output are always the original, unmodified values

## Notes on Braille Mode

Braille mode (`--mode braille` / `--mode braille-color`) uses Unicode characters from the **Braille Patterns block** (`U+2800`–`U+28FF`):

- Each braille character encodes a **2×4 pixel block** (8 individual dots) → ~**4× the spatial resolution** of standard ASCII
- `braille` — grayscale dot mapping; each pixel above a brightness threshold becomes a lit dot
- `braille-color` — same dot mapping but each character is ANSI-colored with the average RGB of its 2×4 block
- `--invert` flips the threshold so dark pixels become lit dots (useful for dark subjects on light backgrounds)
- `--html` exports a braille HTML file; the browser font stack includes `Segoe UI Symbol` (Windows), `Noto Sans Mono` (Linux), and `Apple Symbols` (macOS) to guarantee correct rendering

---

## Dependencies

- [Pillow](https://pypi.org/project/Pillow/) — image loading and processing

---

## Future Enhancements

- Custom character set support (`--chars`) for power users
- Edge detection mode for sharper, outline-style ASCII output
- Python importable API (`from ascii_forge import to_ascii, to_braille`)
- GIF → Animated HTML export (play ASCII art in any browser)
- Image export — save ASCII art directly as a PNG, JPEG, or SVG file
- Performance optimizations using NumPy vectorization

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Author

**Arsh Sharan**

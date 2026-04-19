# ASCII Forger

[![PyPI version](https://img.shields.io/pypi/v/ascii-forger)](https://pypi.org/project/ascii-forger/)
[![Python 3.8+](https://img.shields.io/pypi/pyversions/ascii-forger)](https://pypi.org/project/ascii-forger/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ASCII Forger is a terminal-based ASCII rendering engine that converts images into high-fidelity ASCII art. It supports both grayscale and color rendering and is designed as a modular, extensible command-line tool.

The project focuses on bridging image processing concepts with terminal rendering, providing a practical implementation of pixel-to-character mapping, perceptual brightness scaling, and ANSI-based color encoding.

---

## Features

- Convert images to ASCII art directly in the terminal
- Grayscale and color rendering modes
- **HTML export** — save colored ASCII art as a self-contained `.html` file, viewable in any browser
- **Invert mode** — flip character density for clearer output on light-background subjects
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
   - Grayscale mode outputs plain ASCII text
   - Color mode uses ANSI escape codes to preserve pixel color in terminal output

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
│   └── html_exporter.py
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

### From PyPI *(recommended)*

```bash
pip install ascii-forger
```

This installs the `ascii-forger` command globally (or into your active environment).

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

Invert character density (great for light-background portraits):

```bash
ascii-forger path/to/image.jpg --invert
```

Invert with HTML export:

```bash
ascii-forger path/to/image.jpg --invert --html outputs/inverted.html
```

---

## Command-Line Arguments

| Argument   | Description                                                                            | Default  |
|------------|----------------------------------------------------------------------------------------|----------|
| `image`    | Path to input image                                                                    | Required |
| `--mode`   | Rendering mode: `gray` or `color`                                                      | `gray`   |
| `--width`  | Output width in characters                                                             | `100`    |
| `--output` | File path to save plain-text / ANSI output                                             | None     |
| `--html`   | File path to save a self-contained HTML export (e.g. `outputs/art.html`)              | None     |
| `--invert` | Flip character density mapping — dense chars on bright areas, sparse on dark areas   | Off      |

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
- Works with all modes: `gray`, `color`, and `--html`
- Pixel colors in color/HTML output are always the original, unmodified values

---

## Dependencies

- [Pillow](https://pypi.org/project/Pillow/) — image loading and processing

---

## Future Enhancements

- Edge detection mode for sharper, outline-style ASCII output
- Real-time video and webcam ASCII rendering
- Performance optimizations using NumPy vectorization
- ASCII → PNG/SVG image rendering

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Author

**Arsh Sharan**

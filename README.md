# ASCII Forge

ASCII Forge is a terminal-based ASCII rendering engine that converts images into high-fidelity ASCII art. It supports both grayscale and color rendering and is designed as a modular, extensible command-line tool.

The project focuses on bridging image processing concepts with terminal rendering, providing a practical implementation of pixel-to-character mapping, perceptual brightness scaling, and ANSI-based color encoding.

---

## Features

- Convert images to ASCII art directly in the terminal
- Grayscale and color rendering modes
- Adjustable output width for resolution control
- File output support
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

---

## Project Structure

```
ascii-forge/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── image_loader.py
│   ├── processor.py
│   ├── ascii_mapper.py
│   └── renderer.py
│
├── assets/            # Local test images (ignored by Git)
├── output/            # Generated outputs (ignored by Git)
│
├── setup.py
├── requirements.txt
├── README.md
└── SETUP.md
```

---

## Installation (Development Mode)

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

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the package in editable mode:

```bash
pip install -e .
```

---

## Usage

Basic usage:

```bash
ascii-forge path/to/image.jpg
```

Color rendering:

```bash
ascii-forge path/to/image.jpg --mode color
```

Custom width:

```bash
ascii-forge path/to/image.jpg --width 150
```

Save output to file:

```bash
ascii-forge path/to/image.jpg --output output.txt
```

Full example:

```bash
ascii-forge path/to/image.jpg --mode color --width 120 --output output.txt
```

---

## Command-Line Arguments

| Argument   | Description                                      | Default  |
|------------|--------------------------------------------------|----------|
| `image`    | Path to input image                              | Required |
| `--mode`   | Rendering mode: `gray` or `color`                | `gray`   |
| `--width`  | Output width in characters                       | `100`    |
| `--output` | File path to save ASCII output                   | None     |

---

## Notes on Color Output

Color mode uses ANSI escape sequences. As a result:

- Output files will contain ANSI codes
- Standard text editors may not render colors
- Terminal environments that support ANSI will display colors correctly

---

## Dependencies

- [Pillow](https://pypi.org/project/Pillow/)
- [NumPy](https://numpy.org/)
- OpenCV *(optional, for future extensions)*

---

## Future Enhancements

- HTML export for browser-based rendering
- Edge detection mode for sharper ASCII output
- Real-time video and webcam ASCII rendering
- Packaging and publishing to PyPI
- Performance optimizations using NumPy vectorization

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Author

**Arsh Sharan**

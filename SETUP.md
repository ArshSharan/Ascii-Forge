# Setup and Usage Guide

This document provides step-by-step instructions to install and use ASCII Forger as a command-line tool.

---

## 1. Prerequisites

Ensure the following are installed:

- Python 3.8 or higher
- pip (Python package manager)

---

## 2. Clone the Repository

```bash
git clone https://github.com/ArshSharan/Ascii-Forge.git
cd Ascii-Forge
```

---

## 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

### Windows (PowerShell)

```powershell
.venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Install the CLI Tool

### Option A — from PyPI *(recommended for end users)*

```bash
pip install ascii-forger
```

### Option B — from source *(for development)*

```bash
pip install -e .
```

This registers the `ascii-forger` command using `pyproject.toml` (PEP 517 compliant).

---

## 6. Running the Tool

### Basic Usage

```bash
ascii-forger assets/image.jpg
```

---

### Color Mode

```bash
ascii-forger assets/image.jpg --mode color
```

---

### Custom Width

```bash
ascii-forger assets/image.jpg --width 150
```

---

### Save Output to File

```bash
ascii-forger assets/image.jpg --output output.txt
```

---

### Full Command Example

```bash
ascii-forger assets/image.jpg --mode color --width 120 --output output.txt
```

---

### Export as HTML

Generate a self-contained HTML file viewable in any browser:

```bash
ascii-forger assets/image.jpg --html outputs/art.html
```

With a custom width:

```bash
ascii-forger assets/image.jpg --width 150 --html outputs/art.html
```

Combine HTML export with terminal output in one command:

```bash
ascii-forger assets/image.jpg --mode color --width 120 --output output.txt --html outputs/art.html
```

---

### Invert Mode

Flip the character density for clearer output on light-background subjects:

```bash
ascii-forger assets/image.jpg --invert
```

Combine with HTML export:

```bash
ascii-forger assets/image.jpg --invert --html outputs/inverted.html
```

Combine with color mode and HTML:

```bash
ascii-forger assets/image.jpg --invert --mode color --html outputs/inverted.html
```

---

## 7. Understanding Output

### Grayscale Mode
- Produces plain ASCII text
- Fully compatible with any text editor

### Color Mode
- Uses ANSI escape sequences
- Displays correctly only in compatible terminals
- Output files will not show colors in basic editors

### HTML Export (`--html`)
- Generates a **self-contained `.html` file** with inline `rgb()` color styles
- No internet connection or external dependencies required
- Open the file in any modern browser (Chrome, Firefox, Edge, etc.)
- Output directories (e.g. `outputs/`) are created automatically if missing
- HTML output is always full-color regardless of `--mode`

### Invert Mode (`--invert`)
- Flips the **character density mapping** only — pixel colors are **not** altered
- Default: dark pixel → dense char (`@`), bright pixel → sparse char (` `)
- Inverted: bright pixel → dense char (`@`), dark pixel → sparse char (` `)
- Best used when the subject is darker than the background (e.g. portrait on white)
- Compatible with all modes: `gray`, `color`, and `--html`

---

## 8. Troubleshooting

### Command Not Found

If `ascii-forger` is not recognized:

- Ensure virtual environment is activated
- Re-run:

```bash
pip install -e .
```

---

### File Not Found Error

Ensure the image path is correct relative to your current directory:

```bash
ascii-forger assets/image.jpg
```

Avoid incorrect paths like:

```bash
ascii-forger ../assets/image.jpg
```

---

### No Color in Output

Use a terminal that supports ANSI colors:

- Windows Terminal
- VS Code integrated terminal

---

## 9. Updating the Tool

After making code changes:

```bash
pip install -e .
```

---

## 10. Uninstalling

```bash
pip uninstall ascii-forger
```

---

## Summary

You have now:

- Installed ASCII Forger as a CLI tool
- Learned how to run it with different configurations
- Understood output behavior across grayscale, color, and HTML modes

This setup enables further extensions such as edge detection, real-time rendering, and PyPI distribution.

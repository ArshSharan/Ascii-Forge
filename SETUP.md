# Setup and Usage Guide

This document provides step-by-step instructions to install and use ASCII Forge as a command-line tool.

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

Install the project in editable mode:

```bash
pip install -e .
```

This registers the command:

```bash
ascii-forge
```

---

## 6. Running the Tool

### Basic Usage

```bash
ascii-forge assets/image.jpg
```

---

### Color Mode

```bash
ascii-forge assets/image.jpg --mode color
```

---

### Custom Width

```bash
ascii-forge assets/image.jpg --width 150
```

---

### Save Output to File

```bash
ascii-forge assets/image.jpg --output output.txt
```

---

### Full Command Example

```bash
ascii-forge assets/image.jpg --mode color --width 120 --output output.txt
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

---

## 8. Troubleshooting

### Command Not Found

If `ascii-forge` is not recognized:

- Ensure virtual environment is activated
- Re-run:

```bash
pip install -e .
```

---

### File Not Found Error

Ensure the image path is correct relative to your current directory:

```bash
ascii-forge assets/image.jpg
```

Avoid incorrect paths like:

```bash
ascii-forge ../assets/image.jpg
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
pip uninstall ascii-forge
```

---

## Summary

You have now:

- Installed ASCII Forge as a CLI tool
- Learned how to run it with different configurations
- Understood output behavior and limitations

This setup enables further extensions such as HTML export, edge detection, and real-time rendering.

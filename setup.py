from setuptools import setup, find_packages

setup(
    name="ascii-forge",
    version="0.1",
    description="Terminal-based ASCII art generator",
    author="Arsh Sharan",
    packages=find_packages(),
    install_requires=[
        "pillow",
        "numpy",
        "opencv-python"
    ],
    entry_points={
        "console_scripts": [
            "ascii-forge=src.main:main"
        ]
    },
)
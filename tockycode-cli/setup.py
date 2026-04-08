from setuptools import setup, find_packages

with open("README.md", "w") as f:
    f.write("""# TockyCode - Professional AI Code Generator

A 100% free, local AI-powered code generation tool that runs entirely on your machine.

## Features
- Professional code generation in multiple languages
- Local AI models (no internet required)
- CLI and GUI interfaces
- APK for Android
- AppImage for Linux

## Installation

### From .deb package:
```bash
sudo dpkg -i tockycode_1.0.0_all.deb
```

### From AppImage:
```bash
chmod +x TockyCode-1.0.0.AppImage
./TockyCode-1.0.0.AppImage
```

## Usage

```bash
tockycode generate -p "create a function to calculate fibonacci"
tockycode analyze -f main.py
tockycode --version
```
""")

setup(
    name="tockycode",
    version="1.0.0",
    description="Professional AI Code Generator - 100% Free, Local",
    author="TockyCode Team",
    author_email="info@tockycode.com",
    url="https://github.com/tockycode/tockycode",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "tockycode=tockycode.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
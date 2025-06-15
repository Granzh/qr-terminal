#  QR Terminal

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Platform](https://img.shields.io/badge/platform-linux-blue?logo=linux&style=flat-square)](https://github.com/yourusername/qr-terminal)

**Generate QR codes in terminal from any command output via pipes**

QR Terminal is a command-line utility for Linux that converts any text output into QR codes directly in your terminal.

##  Features

-  **Piping Support**: Works with any command through `|`
-  **File Export**: Save to PNG and SVG formats
-  **Quality Control**: 4 levels of error correction
-  **Flexible Settings**: Sizes, borders, color inversion
-  **Informative**: Shows data size and preview

##  Quick Start

### Installation

```bash
# From source 
git clone https://github.com/Granzh/qr-terminal
cd qr-terminal
pip install -e .
```

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt install python3-dev libjpeg-dev zlib1g-dev

# Fedora/RHEL
sudo dnf install python3-devel libjpeg-devel zlib-devel

# Arch Linux
sudo pacman -S python gcc libjpeg zlib

# macOS
brew install jpeg zlib
```

### First Usage

```bash
# Simple example
echo "Hello, World!" | qrterm

# Your IP address
curl -s ifconfig.me | qrterm
```

## Usage Examples

### Basic Commands

```bash
# Simple text
echo "Hello World" | qrterm

# Direct text input
qrterm "My secret code"

# File contents
cat /etc/hostname | qrterm

# Command output
date | qrterm

# Current directory
pwd | qrterm
```
### Files and Data

```bash
# System information
uname -a | qrterm

# Process list
ps aux | head -10 | qrterm

# Configuration file contents
cat ~/.bashrc | head -20 | qrterm

# Encode file as base64
base64 small_file.txt | qrterm

# Log output
tail -n 20 /var/log/syslog | qrterm
```

### Quality Settings

```bash
# High quality for important data
cat important.txt | qrterm --error-correction H

# Compact QR code
echo "test" | qrterm --border 1 --box-size 1

# Large QR code
echo "test" | qrterm --box-size 2 --border 6

# Colored with inversion
echo "colorful" | qrterm --color --invert
```

### File Output

```bash
# Save as PNG
echo "https://example.com" | qrterm --output website.png

# Save as SVG
curl -s ifconfig.me | qrterm --output my-ip.svg

# Quiet mode for scripts
echo "data" | qrterm --output data.png --quiet
```

##  Command Line Options

### Core Options

| Option               | Short | Description                      | Default |
| -------------------- | ----- | -------------------------------- | ------- |
| `--error-correction` | `-e`  | Error correction level (L/M/Q/H) | M       |
| `--border`           | `-b`  | Border size in blocks            | 4       |
| `--box-size`         | `-s`  | Size of each block               | 1       |
| `--version`          | `-v`  | QR code version (1-40)           | 1       |
| `--help`             | `-h`  | for help                         |         |

### Display Options

| Option     | Short | Description                      |
| ---------- | ----- | -------------------------------- |
| `--invert` | `-i`  | Invert colors (white background) |
| `--quiet`  | `-q`  | Quiet mode (QR code only)        |

### Output Options

|Option|Short|Description|
|---|---|---|
|`--output`|`-o`|Save to file (.png or .svg)|

### Error Correction Levels

- **L (Low)**: ~7% - for clean environments
- **M (Medium)**: ~15% - standard usage
- **Q (Quartile)**: ~25% - industrial usage
- **H (High)**: ~30% - maximum reliability

## License

This project is licensed under the MIT License. See the LICENSE file for details.

##  Acknowledgments

- [python-qrcode](https://github.com/lincolnloop/python-qrcode) - core QR code generation library
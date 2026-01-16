# MyFileDiff

A powerful and intuitive file comparison tool that displays side-by-side differences between two text files with beautiful color-coded highlighting.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## Features

- **🎨 Color-Coded GUI** - Beautiful graphical interface with intuitive color highlighting
- **📁 Interactive File Selection** - Browse and select files directly from the GUI
- **💻 CLI Mode** - Traditional command-line interface for terminal enthusiasts
- **🔄 Synchronized Scrolling** - Both file panes scroll together for easy comparison
- **📊 Visual Legend** - Clear indication of what each color represents
- **⚡ Fast Comparison** - Efficient line-by-line diff algorithm using Python's difflib
- **🔍 UTF-8 Support** - Handles text files with UTF-8 encoding
- **0️⃣ No External Dependencies** - Uses built-in Python tkinter for GUI

## Color Scheme

- **🟢 Light Green** - Identical lines in both files
- **🟡 Light Yellow** - Modified lines (content differs)
- **🔴 Light Red** - Deleted lines (only in file1)
- **🔵 Light Blue** - Added lines (only in file2)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/swarnangsu/MyFileDiff.git
cd MyFileDiff
```

2. Ensure you have Python 3.7 or higher installed:
```bash
python --version
```

No additional dependencies required! The tool uses Python's built-in libraries.

## Usage

### GUI Mode (Default)

```bash
python MyFileDiff/MyFileDiff.py file1.txt file2.txt
```

This opens a graphical window with:
- Side-by-side file comparison
- Color-coded differences
- Synchronized scrolling
- Visual legend

### CLI Mode

For terminal-based comparison:

```bash
python MyFileDiff/MyFileDiff.py file1.txt file2.txt --cli
```

Output uses text indicators:
- `' '` (space) = Identical lines
- `'|'` = Modified lines
- `'-'` = Deleted lines
- `'+'` = Added lines

### Examples

Try it with the included sample files:

```bash
# GUI mode
python MyFileDiff/MyFileDiff.py sample_file1.txt sample_file2.txt

# CLI mode
python MyFileDiff/MyFileDiff.py sample_file1.txt sample_file2.txt --cli
```

## Exit Codes

- `0` - Files are identical
- `1` - Files are different
- `2` - Error occurred (file not found, encoding issue, etc.)

## Testing

Run the test suite with pytest:

```bash
pytest test_myfilediff.py -v
```

Run specific tests:

```bash
pytest test_myfilediff.py::TestFileDiffViewer::test_identical_files -v
```

## Project Structure

```
MyFileDiff/
├── MyFileDiff/
│   ├── MyFileDiff.py          # Main application
│   └── MyFileDiff.pyproj      # Visual Studio project file
├── MyFileDiff.slnx             # Visual Studio solution file
├── test_myfilediff.py          # Unit tests
├── sample_file1.txt            # Sample file for testing
├── sample_file2.txt            # Sample file for testing
├── CLAUDE.md                   # Claude Code guidance
└── README.md                   # This file
```

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- For testing: pytest

## Platform Support

- ✅ Windows
- ✅ Linux
- ✅ macOS

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with Python's `difflib` for efficient diff algorithm
- GUI powered by tkinter
- Inspired by classic diff tools like vimdiff and meld

## Author

Created as a demonstration of Python GUI programming and file comparison algorithms.

---

**Enjoy comparing files! 🚀**

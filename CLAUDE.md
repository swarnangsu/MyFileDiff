# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MyFileDiff is a file comparison tool that displays side-by-side differences between two text files with color-coded highlighting. Features both a GUI (default) and CLI mode. Built as a Visual Studio Python project using tkinter for the graphical interface.

## Project Structure

```
MyFileDiff/
├── MyFileDiff/
│   ├── MyFileDiff.py          # Main application with FileDiffGUI and FileDiffViewer classes
│   └── MyFileDiff.pyproj      # Visual Studio Python project file
├── MyFileDiff.slnx             # Visual Studio solution file
├── test_myfilediff.py          # Comprehensive unit tests (pytest)
├── sample_file1.txt            # Sample file for manual testing
├── sample_file2.txt            # Sample file for manual testing
└── CLAUDE.md                   # This file
```

## Common Commands

### Running the Tool (GUI Mode - Default)
```bash
cd /c/users/swarna/source/repos/MyFileDiff
py MyFileDiff/MyFileDiff.py sample_file1.txt sample_file2.txt
```

Opens a graphical window with color-coded, side-by-side file comparison.

### Running in CLI Mode
```bash
cd /c/users/swarna/source/repos/MyFileDiff
py MyFileDiff/MyFileDiff.py sample_file1.txt sample_file2.txt --cli
```

Displays comparison in terminal with text indicators instead of colors.

### Running Tests
```bash
cd /c/users/swarna/source/repos/MyFileDiff
pytest test_myfilediff.py -v
```

Run specific test:
```bash
pytest test_myfilediff.py::TestFileDiffViewer::test_identical_files -v
```

Note: Current tests cover the CLI mode (FileDiffViewer class). GUI tests would require additional mocking of tkinter components.

### Running in Visual Studio
- Open `MyFileDiff.slnx` in Visual Studio
- Configure command-line arguments in project properties (Debug > Start with Arguments)
- Example args: `sample_file1.txt sample_file2.txt` or `sample_file1.txt sample_file2.txt --cli`
- Use F5 to run or debug

### Python Command
On this Windows system, use `py` command (Python launcher). You can also use `python` or `python3` if configured in your PATH.

## Architecture

### Core Components

**FileDiffGUI Class** (`MyFileDiff.py:11`)
- GUI implementation using tkinter for visual file comparison
- Creates 1200x700 window with two synchronized text widgets
- Implements color-coded display of differences
- Uses ttk (themed tkinter) for modern widget styling

**FileDiffViewer Class** (`MyFileDiff.py:260`)
- CLI implementation for terminal-based file comparison
- Maintains original functionality with text-based indicators
- Fallback option when GUI is not available or user prefers CLI

**Key Methods (both classes):**
- `read_file()`: Reads and validates UTF-8 text files
- `get_diff_opcodes()`: Uses difflib.SequenceMatcher to compute line-by-line differences
- `display_diff()`: Orchestrates comparison and output rendering

**GUI-Specific Methods:**
- `setup_ui()`: Creates window layout with headers, text widgets, scrollbars, and legend
- `_on_scroll()`: Synchronizes scrolling between left and right text panes

### Color Scheme (GUI Mode)

The GUI uses distinct background colors for different line types:
- **Light Green** (#E8F5E9) - Identical lines in both files
- **Light Yellow** (#FFF9C4) - Modified lines (content differs)
- **Light Red** (#FFCDD2) - Deleted lines (only in file1)
- **Light Blue** (#BBDEFB) - Added lines (only in file2)

A legend is displayed at the bottom of the GUI window.

### CLI Mode Indicators

Terminal output uses these status characters:
- `' '` (space) = Lines are identical
- `'|'` = Lines are modified
- `'-'` = Line deleted from file2 (only in file1)
- `'+'` = Line added to file2 (only in file2)

### Exit Codes

- `0`: Files are identical
- `1`: Files are different
- `2`: Error occurred (file not found, wrong arguments, encoding issues, GUI error)

## GUI Implementation Details

- Window size: 1200x700 pixels
- Font: Courier 10pt (monospace) for proper alignment
- Text widgets are read-only after content is loaded
- Synchronized scrolling keeps both panes aligned
- Window title updates to show "IDENTICAL" or "DIFFERENT" after comparison
- Error messages displayed via messagebox.showerror()
- Falls back to CLI mode if tkinter is unavailable

## Testing Strategy

Tests use pytest with these fixtures:
- `tmp_path`: Creates temporary test files
- `capsys`: Captures stdout/stderr output
- `monkeypatch`: Modifies sys.argv for testing main()

Test categories:
- File I/O operations (read, error handling)
- Line truncation and formatting (CLI mode)
- Diff operations (identical, additions, deletions, modifications)
- Main function argument handling
- Edge cases (empty files, missing files)

Note: Existing tests focus on FileDiffViewer (CLI mode) class. GUI tests would require mocking tkinter components.

## Key Implementation Details

- Uses Python's built-in `tkinter` library (no external GUI dependencies)
- Based on `difflib.SequenceMatcher` for efficient line-by-line comparison
- Uses UTF-8 encoding; binary files will raise UnicodeDecodeError
- All file operations use pathlib.Path for cross-platform compatibility
- CLI mode: Terminal width defaults to 80 characters, split evenly between columns
- CLI mode: Lines exceeding column width are truncated with '...' indicator
- GUI mode: Full line content displayed (horizontal scrolling available)

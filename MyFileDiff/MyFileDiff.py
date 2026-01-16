"""MyFileDiff - A tool to display side-by-side file differences with GUI."""

import sys
import difflib
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from pathlib import Path
from typing import List, Tuple, Optional


class FileDiffGUI:
    """GUI for displaying file differences."""

    def __init__(self, file1_path: Optional[str] = None, file2_path: Optional[str] = None):
        """Initialize the GUI diff viewer.

        Args:
            file1_path: Path to the first file (optional)
            file2_path: Path to the second file (optional)
        """
        self.file1_path = Path(file1_path) if file1_path else None
        self.file2_path = Path(file2_path) if file2_path else None
        self.root = tk.Tk()
        self.root.title("MyFileDiff - File Comparison Tool")
        self.root.geometry("1200x750")

        # Color scheme for different line types
        self.colors = {
            'equal': '#E8F5E9',      # Light green - identical lines
            'replace': '#FFF9C4',    # Light yellow - modified lines
            'delete': '#FFCDD2',     # Light red - deleted lines
            'insert': '#BBDEFB',     # Light blue - inserted lines
            'bg_normal': 'white'
        }

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface components."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # File selection controls
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Left file selection
        ttk.Label(control_frame, text="File 1:", font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.file1_entry = ttk.Entry(control_frame, width=50)
        self.file1_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        if self.file1_path:
            self.file1_entry.insert(0, str(self.file1_path))

        self.file1_button = ttk.Button(control_frame, text="Browse...", command=self.browse_file1)
        self.file1_button.grid(row=0, column=2, padx=(0, 20))

        # Right file selection
        ttk.Label(control_frame, text="File 2:", font=('Arial', 9)).grid(row=0, column=3, sticky=tk.W, padx=(0, 5))
        self.file2_entry = ttk.Entry(control_frame, width=50)
        self.file2_entry.grid(row=0, column=4, sticky=(tk.W, tk.E), padx=(0, 5))
        if self.file2_path:
            self.file2_entry.insert(0, str(self.file2_path))

        self.file2_button = ttk.Button(control_frame, text="Browse...", command=self.browse_file2)
        self.file2_button.grid(row=0, column=5, padx=(0, 20))

        # Compare button
        self.compare_button = ttk.Button(control_frame, text="Compare Files", command=self.compare_files, style='Accent.TButton')
        self.compare_button.grid(row=0, column=6, padx=(0, 5))

        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(4, weight=1)

        # Headers for each file
        self.left_header = ttk.Label(
            main_frame,
            text=str(self.file1_path) if self.file1_path else "No file selected",
            font=('Courier', 10, 'bold'),
            background='#E3F2FD',
            padding=5
        )
        self.left_header.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=(0, 5))

        self.right_header = ttk.Label(
            main_frame,
            text=str(self.file2_path) if self.file2_path else "No file selected",
            font=('Courier', 10, 'bold'),
            background='#E3F2FD',
            padding=5
        )
        self.right_header.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(0, 5))

        # Text widgets for file content
        self.left_text = tk.Text(
            main_frame,
            wrap=tk.NONE,
            font=('Courier', 10),
            width=60,
            height=30
        )
        self.left_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        self.right_text = tk.Text(
            main_frame,
            wrap=tk.NONE,
            font=('Courier', 10),
            width=60,
            height=30
        )
        self.right_text.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        # Scrollbars
        left_scroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.left_text.yview)
        left_scroll.grid(row=2, column=0, sticky=(tk.E, tk.N, tk.S), padx=(0, 5))
        self.left_text.configure(yscrollcommand=left_scroll.set)

        right_scroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.right_text.yview)
        right_scroll.grid(row=2, column=1, sticky=(tk.E, tk.N, tk.S), padx=(5, 0))
        self.right_text.configure(yscrollcommand=right_scroll.set)

        # Synchronize scrolling
        self.left_text.configure(yscrollcommand=lambda *args: self._on_scroll(left_scroll, right_scroll, *args))
        self.right_text.configure(yscrollcommand=lambda *args: self._on_scroll(right_scroll, left_scroll, *args))

        # Legend
        legend_frame = ttk.Frame(main_frame, padding="5")
        legend_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        legend_items = [
            ("Identical", self.colors['equal']),
            ("Modified", self.colors['replace']),
            ("Deleted", self.colors['delete']),
            ("Added", self.colors['insert'])
        ]

        ttk.Label(legend_frame, text="Legend:", font=('Courier', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        for label, color in legend_items:
            item_frame = tk.Frame(legend_frame, background=color, borderwidth=1, relief=tk.SOLID)
            item_frame.pack(side=tk.LEFT, padx=5)
            tk.Label(item_frame, text=f" {label} ", background=color, font=('Courier', 9)).pack()

        # Configure text tags for colors
        for tag, color in self.colors.items():
            self.left_text.tag_configure(tag, background=color)
            self.right_text.tag_configure(tag, background=color)

    def browse_file1(self) -> None:
        """Open file dialog to select first file."""
        filename = filedialog.askopenfilename(
            title="Select First File",
            filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            self.file1_entry.delete(0, tk.END)
            self.file1_entry.insert(0, filename)
            self.file1_path = Path(filename)

    def browse_file2(self) -> None:
        """Open file dialog to select second file."""
        filename = filedialog.askopenfilename(
            title="Select Second File",
            filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            self.file2_entry.delete(0, tk.END)
            self.file2_entry.insert(0, filename)
            self.file2_path = Path(filename)

    def compare_files(self) -> None:
        """Trigger file comparison."""
        # Get file paths from entry widgets
        file1_str = self.file1_entry.get().strip()
        file2_str = self.file2_entry.get().strip()

        if not file1_str or not file2_str:
            messagebox.showwarning("Missing Files", "Please select both files to compare.")
            return

        self.file1_path = Path(file1_str)
        self.file2_path = Path(file2_str)

        # Update headers
        self.left_header.config(text=str(self.file1_path))
        self.right_header.config(text=str(self.file2_path))

        # Clear previous content
        self.left_text.config(state=tk.NORMAL)
        self.right_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)
        self.right_text.delete(1.0, tk.END)

        # Perform comparison
        self.display_diff()

    def _on_scroll(self, scrollbar1: ttk.Scrollbar, scrollbar2: ttk.Scrollbar, *args) -> None:
        """Synchronize scrolling between two text widgets."""
        scrollbar1.set(*args)
        self.left_text.yview_moveto(args[0])
        self.right_text.yview_moveto(args[0])

    def read_file(self, file_path: Path) -> List[str]:
        """Read file and return lines.

        Args:
            file_path: Path to the file

        Returns:
            List of lines from the file

        Raises:
            FileNotFoundError: If file doesn't exist
            UnicodeDecodeError: If file encoding is not UTF-8
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                'utf-8', b'', 0, 1,
                f"Cannot decode {file_path} as UTF-8. Binary file?"
            )

    def get_diff_opcodes(self, lines1: List[str], lines2: List[str]) -> List[Tuple]:
        """Get diff operations between two sets of lines.

        Args:
            lines1: Lines from first file
            lines2: Lines from second file

        Returns:
            List of diff opcodes
        """
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        return matcher.get_opcodes()

    def display_diff(self) -> int:
        """Display the side-by-side diff in GUI.

        Returns:
            0 if files are identical, 1 if different, 2 if error
        """
        try:
            lines1 = self.read_file(self.file1_path)
            lines2 = self.read_file(self.file2_path)
        except (FileNotFoundError, UnicodeDecodeError) as e:
            messagebox.showerror("Error", str(e))
            return 2

        opcodes = self.get_diff_opcodes(lines1, lines2)
        has_differences = False

        left_line_num = 1
        right_line_num = 1

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                # Lines are the same
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    line_left = lines1[i].rstrip('\n\r')
                    line_right = lines2[j].rstrip('\n\r')

                    self.left_text.insert(tk.END, line_left + '\n', 'equal')
                    self.right_text.insert(tk.END, line_right + '\n', 'equal')

                    left_line_num += 1
                    right_line_num += 1

            elif tag == 'replace':
                # Lines are different
                has_differences = True
                max_lines = max(i2 - i1, j2 - j1)

                for k in range(max_lines):
                    if i1 + k < i2:
                        line_left = lines1[i1 + k].rstrip('\n\r')
                        self.left_text.insert(tk.END, line_left + '\n', 'replace')
                        left_line_num += 1
                    else:
                        self.left_text.insert(tk.END, '\n', 'bg_normal')

                    if j1 + k < j2:
                        line_right = lines2[j1 + k].rstrip('\n\r')
                        self.right_text.insert(tk.END, line_right + '\n', 'replace')
                        right_line_num += 1
                    else:
                        self.right_text.insert(tk.END, '\n', 'bg_normal')

            elif tag == 'delete':
                # Lines only in file1
                has_differences = True
                for i in range(i1, i2):
                    line = lines1[i].rstrip('\n\r')
                    self.left_text.insert(tk.END, line + '\n', 'delete')
                    self.right_text.insert(tk.END, '\n', 'bg_normal')
                    left_line_num += 1

            elif tag == 'insert':
                # Lines only in file2
                has_differences = True
                for j in range(j1, j2):
                    line = lines2[j].rstrip('\n\r')
                    self.left_text.insert(tk.END, '\n', 'bg_normal')
                    self.right_text.insert(tk.END, line + '\n', 'insert')
                    right_line_num += 1

        # Make text widgets read-only
        self.left_text.configure(state=tk.DISABLED)
        self.right_text.configure(state=tk.DISABLED)

        # Show result in title
        if has_differences:
            self.root.title("MyFileDiff - Files are DIFFERENT")
            return 1
        else:
            self.root.title("MyFileDiff - Files are IDENTICAL")
            return 0

    def run(self) -> int:
        """Run the GUI application.

        Returns:
            Exit code (0 = identical, 1 = different, 2 = error)
        """
        # If files were provided, compare them automatically
        if self.file1_path and self.file2_path:
            result = self.display_diff()
        else:
            result = 0  # Default for no comparison yet

        self.root.mainloop()
        return result


class FileDiffViewer:
    """Handles file comparison and side-by-side display (CLI mode)."""

    def __init__(self, file1_path: str, file2_path: str, width: int = 80):
        """Initialize the diff viewer.

        Args:
            file1_path: Path to the first file
            file2_path: Path to the second file
            width: Terminal width for display (default: 80)
        """
        self.file1_path = Path(file1_path)
        self.file2_path = Path(file2_path)
        self.width = width
        self.col_width = (width - 5) // 2  # 5 chars for separator and status

    def read_file(self, file_path: Path) -> List[str]:
        """Read file and return lines.

        Args:
            file_path: Path to the file

        Returns:
            List of lines from the file

        Raises:
            FileNotFoundError: If file doesn't exist
            UnicodeDecodeError: If file encoding is not UTF-8
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                'utf-8', b'', 0, 1,
                f"Cannot decode {file_path} as UTF-8. Binary file?"
            )

    def truncate_line(self, line: str, width: int) -> str:
        """Truncate line to specified width.

        Args:
            line: Line to truncate
            width: Maximum width

        Returns:
            Truncated line with ellipsis if needed
        """
        line = line.rstrip('\n\r')
        if len(line) > width:
            return line[:width-3] + '...'
        return line.ljust(width)

    def get_diff_opcodes(self, lines1: List[str], lines2: List[str]) -> List[Tuple]:
        """Get diff operations between two sets of lines.

        Args:
            lines1: Lines from first file
            lines2: Lines from second file

        Returns:
            List of diff opcodes
        """
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        return matcher.get_opcodes()

    def print_header(self) -> None:
        """Print the comparison header."""
        print("=" * self.width)
        left_header = self.truncate_line(str(self.file1_path), self.col_width)
        right_header = self.truncate_line(str(self.file2_path), self.col_width)
        print(f"{left_header} | {right_header}")
        print("=" * self.width)

    def print_side_by_side(self, left: Optional[str], right: Optional[str],
                          status: str) -> None:
        """Print a side-by-side comparison line.

        Args:
            left: Left side content (None if not present)
            right: Right side content (None if not present)
            status: Status character (' ', '+', '-', '|')
        """
        left_text = self.truncate_line(left if left else '', self.col_width)
        right_text = self.truncate_line(right if right else '', self.col_width)
        print(f"{left_text} {status} {right_text}")

    def display_diff(self) -> int:
        """Display the side-by-side diff.

        Returns:
            0 if files are identical, 1 if different, 2 if error
        """
        try:
            lines1 = self.read_file(self.file1_path)
            lines2 = self.read_file(self.file2_path)
        except (FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

        self.print_header()

        opcodes = self.get_diff_opcodes(lines1, lines2)
        has_differences = False

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                # Lines are the same
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    self.print_side_by_side(lines1[i], lines2[j], ' ')

            elif tag == 'replace':
                # Lines are different
                has_differences = True
                max_lines = max(i2 - i1, j2 - j1)
                for k in range(max_lines):
                    left = lines1[i1 + k] if i1 + k < i2 else None
                    right = lines2[j1 + k] if j1 + k < j2 else None
                    self.print_side_by_side(left, right, '|')

            elif tag == 'delete':
                # Lines only in file1
                has_differences = True
                for i in range(i1, i2):
                    self.print_side_by_side(lines1[i], None, '-')

            elif tag == 'insert':
                # Lines only in file2
                has_differences = True
                for j in range(j1, j2):
                    self.print_side_by_side(None, lines2[j], '+')

        print("=" * self.width)

        if has_differences:
            print("\nLegend: ' ' = identical, '|' = modified, '-' = deleted, '+' = added")
            return 1
        else:
            print("\nFiles are identical")
            return 0


def main() -> int:
    """Main entry point for the diff tool.

    Returns:
        Exit code (0 = identical, 1 = different, 2 = error)
    """
    # Check for CLI flag
    use_cli = '--cli' in sys.argv

    # Remove --cli from args if present
    args = [arg for arg in sys.argv[1:] if arg != '--cli']

    # Handle different argument scenarios
    if len(args) == 0:
        # No files provided - open GUI with blank view
        if use_cli:
            print("Usage: python MyFileDiff.py <file1> <file2> [--cli]", file=sys.stderr)
            print("\nCompares two files and displays differences side-by-side")
            print("Options:")
            print("  --cli    Use command-line interface instead of GUI (default: GUI)")
            return 2
        else:
            try:
                gui = FileDiffGUI()
                return gui.run()
            except tk.TclError as e:
                print(f"GUI Error: {e}", file=sys.stderr)
                return 2

    elif len(args) == 2:
        # Two files provided
        file1, file2 = args[0], args[1]

        if use_cli:
            viewer = FileDiffViewer(file1, file2)
            return viewer.display_diff()
        else:
            try:
                gui = FileDiffGUI(file1, file2)
                return gui.run()
            except tk.TclError as e:
                print(f"GUI Error: {e}", file=sys.stderr)
                print("Try using --cli flag for command-line mode", file=sys.stderr)
                return 2
    else:
        # Invalid number of arguments
        print("Usage: python MyFileDiff.py [<file1> <file2>] [--cli]", file=sys.stderr)
        print("\nCompares two files and displays differences side-by-side")
        print("Options:")
        print("  No arguments: Opens GUI with file selection")
        print("  <file1> <file2>: Compare specified files")
        print("  --cli: Use command-line interface instead of GUI (requires file arguments)")
        return 2


if __name__ == "__main__":
    sys.exit(main())

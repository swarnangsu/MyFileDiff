"""Unit tests for MyFileDiff tool."""

import pytest
import sys
import tempfile
from pathlib import Path

# Add the MyFileDiff directory to the path
sys.path.insert(0, str(Path(__file__).parent / "MyFileDiff"))

from MyFileDiff import FileDiffViewer, main


class TestFileDiffViewer:
    """Test cases for FileDiffViewer class."""

    def test_read_file_success(self, tmp_path):
        """Test reading a file successfully."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3\n", encoding='utf-8')

        viewer = FileDiffViewer(str(test_file), str(test_file))
        lines = viewer.read_file(test_file)

        assert len(lines) == 3
        assert lines[0] == "Line 1\n"
        assert lines[1] == "Line 2\n"
        assert lines[2] == "Line 3\n"

    def test_read_file_not_found(self, tmp_path):
        """Test reading a non-existent file."""
        non_existent = tmp_path / "does_not_exist.txt"
        viewer = FileDiffViewer(str(non_existent), str(non_existent))

        with pytest.raises(FileNotFoundError):
            viewer.read_file(non_existent)

    def test_truncate_line_short(self):
        """Test truncating a line that's shorter than width."""
        viewer = FileDiffViewer("file1.txt", "file2.txt")
        result = viewer.truncate_line("Short line", 20)

        assert len(result) == 20
        assert result.startswith("Short line")

    def test_truncate_line_long(self):
        """Test truncating a line that's longer than width."""
        viewer = FileDiffViewer("file1.txt", "file2.txt")
        long_line = "A" * 100
        result = viewer.truncate_line(long_line, 20)

        assert len(result) == 20
        assert result.endswith("...")

    def test_identical_files(self, tmp_path):
        """Test comparing two identical files."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        content = "Line 1\nLine 2\nLine 3\n"
        file1.write_text(content, encoding='utf-8')
        file2.write_text(content, encoding='utf-8')

        viewer = FileDiffViewer(str(file1), str(file2))
        result = viewer.display_diff()

        assert result == 0  # Files are identical

    def test_different_files(self, tmp_path, capsys):
        """Test comparing two different files."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Line 1\nLine 2\nLine 3\n", encoding='utf-8')
        file2.write_text("Line 1\nModified Line 2\nLine 3\n", encoding='utf-8')

        viewer = FileDiffViewer(str(file1), str(file2))
        result = viewer.display_diff()

        assert result == 1  # Files are different

        captured = capsys.readouterr()
        assert "Legend:" in captured.out

    def test_file_with_additions(self, tmp_path):
        """Test file with additional lines."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Line 1\nLine 2\n", encoding='utf-8')
        file2.write_text("Line 1\nLine 2\nLine 3\n", encoding='utf-8')

        viewer = FileDiffViewer(str(file1), str(file2))
        result = viewer.display_diff()

        assert result == 1  # Files are different

    def test_file_with_deletions(self, tmp_path):
        """Test file with deleted lines."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Line 1\nLine 2\nLine 3\n", encoding='utf-8')
        file2.write_text("Line 1\nLine 3\n", encoding='utf-8')

        viewer = FileDiffViewer(str(file1), str(file2))
        result = viewer.display_diff()

        assert result == 1  # Files are different

    def test_empty_files(self, tmp_path):
        """Test comparing two empty files."""
        file1 = tmp_path / "empty1.txt"
        file2 = tmp_path / "empty2.txt"

        file1.write_text("", encoding='utf-8')
        file2.write_text("", encoding='utf-8')

        viewer = FileDiffViewer(str(file1), str(file2))
        result = viewer.display_diff()

        assert result == 0  # Both empty, so identical


class TestMainFunction:
    """Test cases for main function."""

    def test_main_with_no_arguments(self, monkeypatch, capsys):
        """Test main function with no arguments."""
        monkeypatch.setattr(sys, 'argv', ['MyFileDiff.py'])

        result = main()

        assert result == 2  # Error code
        captured = capsys.readouterr()
        assert "Usage:" in captured.err

    def test_main_with_one_argument(self, monkeypatch, capsys):
        """Test main function with only one argument."""
        monkeypatch.setattr(sys, 'argv', ['MyFileDiff.py', 'file1.txt'])

        result = main()

        assert result == 2  # Error code
        captured = capsys.readouterr()
        assert "Usage:" in captured.err

    def test_main_with_nonexistent_files(self, monkeypatch, capsys):
        """Test main function with non-existent files."""
        monkeypatch.setattr(sys, 'argv',
                          ['MyFileDiff.py', 'nonexistent1.txt', 'nonexistent2.txt'])

        result = main()

        assert result == 2  # Error code
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_main_with_identical_files(self, tmp_path, monkeypatch):
        """Test main function with identical files."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        content = "Test content\n"
        file1.write_text(content, encoding='utf-8')
        file2.write_text(content, encoding='utf-8')

        monkeypatch.setattr(sys, 'argv',
                          ['MyFileDiff.py', str(file1), str(file2)])

        result = main()

        assert result == 0  # Files identical

    def test_main_with_different_files(self, tmp_path, monkeypatch):
        """Test main function with different files."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Content A\n", encoding='utf-8')
        file2.write_text("Content B\n", encoding='utf-8')

        monkeypatch.setattr(sys, 'argv',
                          ['MyFileDiff.py', str(file1), str(file2)])

        result = main()

        assert result == 1  # Files different

"""Unit tests for markdown parser module.

This module tests all parser functions including markdown section extraction,
list item parsing, field value extraction, and checkbox field extraction.
"""

from pathlib import Path

import pytest

from claude_planner.generator.parser import (
    extract_checkbox_fields,
    extract_field_value,
    extract_list_items,
    parse_markdown_content,
    parse_markdown_file,
)


class TestParseMarkdownFile:
    """Test cases for parse_markdown_file function."""

    def test_parse_valid_file(self, tmp_path: Path) -> None:
        """Test parsing a valid markdown file."""
        file_path = tmp_path / "test.md"
        content = """# Title

## Section 1
Content for section 1

## Section 2
Content for section 2
"""
        file_path.write_text(content, encoding="utf-8")

        result = parse_markdown_file(file_path)

        assert "Section 1" in result
        assert "Section 2" in result
        assert result["Section 1"] == "Content for section 1"
        assert result["Section 2"] == "Content for section 2"

    def test_parse_file_not_found(self, tmp_path: Path) -> None:
        """Test parsing a non-existent file raises FileNotFoundError."""
        file_path = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError) as exc_info:
            parse_markdown_file(file_path)

        assert "File not found" in str(exc_info.value)

    def test_parse_file_read_error(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that file read errors are properly handled."""
        file_path = tmp_path / "test.md"
        file_path.write_text("test", encoding="utf-8")

        # Mock read_text to raise an exception
        def mock_read_text(*args: object, **kwargs: object) -> str:
            raise PermissionError("Access denied")

        monkeypatch.setattr(Path, "read_text", mock_read_text)

        with pytest.raises(ValueError) as exc_info:
            parse_markdown_file(file_path)

        assert "Failed to read file" in str(exc_info.value)


class TestParseMarkdownContent:
    """Test cases for parse_markdown_content function."""

    def test_parse_basic_sections(self) -> None:
        """Test parsing basic markdown sections."""
        content = """## Section 1
Content here

## Section 2
More content"""

        result = parse_markdown_content(content)

        assert len(result) == 2
        assert "Section 1" in result
        assert "Section 2" in result
        assert result["Section 1"] == "Content here"
        assert result["Section 2"] == "More content"

    def test_parse_with_h1_ignored(self) -> None:
        """Test that H1 headings are ignored, only H2+ are tracked."""
        content = """# Main Title

## Section 1
Content"""

        result = parse_markdown_content(content)

        assert len(result) == 1
        assert "Main Title" not in result
        assert "Section 1" in result

    def test_parse_multiple_heading_levels(self) -> None:
        """Test parsing with different heading levels."""
        content = """## Level 2
Content 2

### Level 3
Content 3

#### Level 4
Content 4"""

        result = parse_markdown_content(content)

        assert len(result) == 3
        assert "Level 2" in result
        assert "Level 3" in result
        assert "Level 4" in result

    def test_parse_empty_sections(self) -> None:
        """Test parsing sections with no content."""
        content = """## Section 1

## Section 2
Content"""

        result = parse_markdown_content(content)

        assert len(result) == 2
        assert result["Section 1"] == ""
        assert result["Section 2"] == "Content"

    def test_parse_multiline_content(self) -> None:
        """Test parsing sections with multiline content."""
        content = """## Section 1
Line 1
Line 2
Line 3"""

        result = parse_markdown_content(content)

        assert result["Section 1"] == "Line 1\nLine 2\nLine 3"

    def test_parse_empty_content(self) -> None:
        """Test parsing empty content returns empty dict."""
        result = parse_markdown_content("")

        assert result == {}

    def test_parse_no_sections(self) -> None:
        """Test parsing content with no section headings."""
        content = "Just some text\nNo headings here"

        result = parse_markdown_content(content)

        assert result == {}

    def test_parse_heading_with_extra_whitespace(self) -> None:
        """Test parsing headings with extra whitespace."""
        content = """##   Section With Spaces
Content here"""

        result = parse_markdown_content(content)

        assert "Section With Spaces" in result
        assert result["Section With Spaces"] == "Content here"


class TestExtractListItems:
    """Test cases for extract_list_items function."""

    def test_extract_unordered_list(self) -> None:
        """Test extracting items from unordered list."""
        text = """- Item 1
- Item 2
- Item 3"""

        result = extract_list_items(text)

        assert len(result) == 3
        assert result[0] == "Item 1"
        assert result[1] == "Item 2"
        assert result[2] == "Item 3"

    def test_extract_ordered_list(self) -> None:
        """Test extracting items from ordered list."""
        text = """1. First item
2. Second item
3. Third item"""

        result = extract_list_items(text)

        assert len(result) == 3
        assert result[0] == "First item"
        assert result[1] == "Second item"
        assert result[2] == "Third item"

    def test_extract_mixed_markers(self) -> None:
        """Test extracting items with different list markers."""
        text = """- Item with dash
* Item with asterisk
+ Item with plus"""

        result = extract_list_items(text)

        assert len(result) == 3
        assert "Item with dash" in result
        assert "Item with asterisk" in result
        assert "Item with plus" in result

    def test_extract_with_extra_whitespace(self) -> None:
        """Test extracting items with extra whitespace."""
        text = """  -   Item with spaces
  -   Another item   """

        result = extract_list_items(text)

        assert len(result) == 2
        assert result[0] == "Item with spaces"
        assert result[1] == "Another item"

    def test_extract_empty_lines_ignored(self) -> None:
        """Test that empty lines are ignored."""
        text = """- Item 1

- Item 2

- Item 3"""

        result = extract_list_items(text)

        assert len(result) == 3

    def test_extract_non_list_lines_ignored(self) -> None:
        """Test that non-list lines are ignored."""
        text = """Some text
- Item 1
More text
- Item 2"""

        result = extract_list_items(text)

        assert len(result) == 2
        assert result == ["Item 1", "Item 2"]

    def test_extract_empty_text(self) -> None:
        """Test extracting from empty text returns empty list."""
        result = extract_list_items("")

        assert result == []


class TestExtractFieldValue:
    """Test cases for extract_field_value function."""

    def test_extract_basic_field(self) -> None:
        """Test extracting a basic field value."""
        text = "- **Project Name**: My Project"

        result = extract_field_value(text, "Project Name")

        assert result == "My Project"

    def test_extract_field_without_dash(self) -> None:
        """Test extracting field value without leading dash."""
        text = "**Field**: Value"

        result = extract_field_value(text, "Field")

        assert result == "Value"

    def test_extract_field_case_insensitive(self) -> None:
        """Test that field extraction is case insensitive."""
        text = "- **project name**: My Project"

        result = extract_field_value(text, "Project Name")

        assert result == "My Project"

    def test_extract_field_with_checkbox(self) -> None:
        """Test extracting field value with checkbox removed."""
        text = "- **Field**: [x] Value"

        result = extract_field_value(text, "Field")

        assert result == "Value"

    def test_extract_field_multiline(self) -> None:
        """Test extracting from multiline text returns first match."""
        text = """- **Field 1**: Value 1
- **Field 2**: Value 2
- **Field 3**: Value 3"""

        result = extract_field_value(text, "Field 2")

        assert result == "Value 2"

    def test_extract_field_not_found(self) -> None:
        """Test that missing field returns empty string."""
        text = "- **Other Field**: Value"

        result = extract_field_value(text, "Missing Field")

        assert result == ""

    def test_extract_field_with_special_chars(self) -> None:
        """Test extracting field with special characters in name."""
        text = "- **Field (Special)**: Value"

        result = extract_field_value(text, "Field (Special)")

        assert result == "Value"

    def test_extract_empty_text(self) -> None:
        """Test extracting from empty text returns empty string."""
        result = extract_field_value("", "Any Field")

        assert result == ""


class TestExtractCheckboxFields:
    """Test cases for extract_checkbox_fields function."""

    def test_extract_checked_boxes(self) -> None:
        """Test extracting checked checkbox fields."""
        text = """- [x] Web App
- [x] API
- [x] CLI"""

        result = extract_checkbox_fields(text)

        assert len(result) == 3
        assert result["Web App"] is True
        assert result["API"] is True
        assert result["CLI"] is True

    def test_extract_unchecked_boxes(self) -> None:
        """Test extracting unchecked checkbox fields."""
        text = """- [ ] Feature 1
- [ ] Feature 2"""

        result = extract_checkbox_fields(text)

        assert len(result) == 2
        assert result["Feature 1"] is False
        assert result["Feature 2"] is False

    def test_extract_mixed_checkboxes(self) -> None:
        """Test extracting mixed checked/unchecked checkboxes."""
        text = """- [x] Completed Task
- [ ] Pending Task
- [x] Another Done"""

        result = extract_checkbox_fields(text)

        assert len(result) == 3
        assert result["Completed Task"] is True
        assert result["Pending Task"] is False
        assert result["Another Done"] is True

    def test_extract_checkbox_case_insensitive(self) -> None:
        """Test that [X] (uppercase) is also recognized as checked."""
        text = """- [X] Uppercase Check
- [x] Lowercase Check"""

        result = extract_checkbox_fields(text)

        assert result["Uppercase Check"] is True
        assert result["Lowercase Check"] is True

    def test_extract_checkbox_without_dash(self) -> None:
        """Test extracting checkbox without leading dash."""
        text = """[x] Checked
[ ] Unchecked"""

        result = extract_checkbox_fields(text)

        assert result["Checked"] is True
        assert result["Unchecked"] is False

    def test_extract_checkbox_with_extra_whitespace(self) -> None:
        """Test extracting checkbox with extra whitespace."""
        text = """  -   [x]   Item with spaces   """

        result = extract_checkbox_fields(text)

        assert "Item with spaces" in result
        assert result["Item with spaces"] is True

    def test_extract_empty_text(self) -> None:
        """Test extracting from empty text returns empty dict."""
        result = extract_checkbox_fields("")

        assert result == {}

    def test_extract_non_checkbox_lines_ignored(self) -> None:
        """Test that non-checkbox lines are ignored."""
        text = """Some text
- [x] Checkbox
More text
- [ ] Another"""

        result = extract_checkbox_fields(text)

        assert len(result) == 2
        assert "Checkbox" in result
        assert "Another" in result

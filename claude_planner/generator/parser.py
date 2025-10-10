"""Markdown parser for PROJECT_BRIEF.md files.

This module provides functions to parse PROJECT_BRIEF.md files and extract
structured content from markdown sections.
"""

import re
from pathlib import Path


def parse_markdown_file(file_path: Path) -> dict[str, str]:
    """Parse a markdown file and extract sections by heading.

    Args:
        file_path: Path to the markdown file to parse

    Returns:
        Dictionary mapping section headings to their content

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file cannot be read

    Example:
        >>> from pathlib import Path
        >>> sections = parse_markdown_file(Path("PROJECT_BRIEF.md"))
        >>> "Basic Information" in sections
        True
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Failed to read file {file_path}: {e}") from e

    return parse_markdown_content(content)


def parse_markdown_content(content: str) -> dict[str, str]:
    """Parse markdown content and extract sections by heading.

    Splits content into sections based on ## headings. Each section includes
    all content until the next heading of the same or higher level.

    Args:
        content: Markdown content as a string

    Returns:
        Dictionary mapping section headings to their content (excluding the heading line)

    Example:
        >>> content = "## Section 1\\nContent here\\n## Section 2\\nMore content"
        >>> sections = parse_markdown_content(content)
        >>> len(sections)
        2
        >>> "Section 1" in sections
        True
    """
    sections: dict[str, str] = {}
    lines = content.split("\n")

    current_section: str | None = None
    current_content: list[str] = []

    for line in lines:
        # Check if this is a heading line (## or higher)
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)

        if heading_match:
            # Save previous section if it exists
            if current_section is not None:
                sections[current_section] = "\n".join(current_content).strip()

            # Start new section
            heading_level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            # Only track ## level headings and below
            if heading_level >= 2:
                current_section = heading_text
                current_content = []
        elif current_section is not None:
            # Add line to current section content
            current_content.append(line)

    # Save final section
    if current_section is not None:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def extract_list_items(text: str) -> list[str]:
    """Extract list items from markdown text.

    Handles both unordered (-) and ordered (1.) list formats.
    Removes the list markers and returns clean text.

    Args:
        text: Markdown text containing list items

    Returns:
        List of extracted items (without markers)

    Example:
        >>> text = "- Item 1\\n- Item 2\\n- Item 3"
        >>> items = extract_list_items(text)
        >>> len(items)
        3
        >>> items[0]
        'Item 1'
    """
    items: list[str] = []
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match unordered list item (-, *, +)
        unordered_match = re.match(r"^[-*+]\s+(.+)$", line)
        if unordered_match:
            items.append(unordered_match.group(1).strip())
            continue

        # Match ordered list item (1., 2., etc.)
        ordered_match = re.match(r"^\d+\.\s+(.+)$", line)
        if ordered_match:
            items.append(ordered_match.group(1).strip())
            continue

    return items


def extract_field_value(text: str, field_name: str) -> str:
    """Extract a field value from markdown text.

    Looks for patterns like "- **Field Name**: value" or "**Field Name**: value".

    Args:
        text: Markdown text to search
        field_name: Name of the field to extract

    Returns:
        Extracted value, or empty string if not found

    Example:
        >>> text = "- **Project Name**: My Project\\n- **Type**: CLI"
        >>> extract_field_value(text, "Project Name")
        'My Project'
    """
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        # Pattern: - **Field**: value or **Field**: value
        pattern = rf"^-?\s*\*\*{re.escape(field_name)}\*\*:\s*(.+)$"
        match = re.match(pattern, line, re.IGNORECASE)

        if match:
            value = match.group(1).strip()
            # Remove markdown checkboxes like [x] or [ ]
            value = re.sub(r"^\[[ x]\]\s*", "", value)
            return value

    return ""


def extract_checkbox_fields(text: str) -> dict[str, bool]:
    """Extract checkbox fields from markdown text.

    Looks for patterns like "- [x] Field" or "- [ ] Field".

    Args:
        text: Markdown text containing checkboxes

    Returns:
        Dictionary mapping field names to checked status (True if [x], False if [ ])

    Example:
        >>> text = "- [x] Web App\\n- [ ] Mobile App\\n- [x] API"
        >>> fields = extract_checkbox_fields(text)
        >>> fields["Web App"]
        True
        >>> fields["Mobile App"]
        False
    """
    fields: dict[str, bool] = {}
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        # Pattern: - [x] or - [ ]
        checked_match = re.match(r"^-?\s*\[x\]\s+(.+)$", line, re.IGNORECASE)
        if checked_match:
            fields[checked_match.group(1).strip()] = True
            continue

        unchecked_match = re.match(r"^-?\s*\[\s\]\s+(.+)$", line)
        if unchecked_match:
            fields[unchecked_match.group(1).strip()] = False
            continue

    return fields

"""Tests for claude.md Jinja2 template rendering.

This module tests that the base claude.md.j2 template correctly renders
with various input data, properly substitutes variables, and generates
valid markdown output.
"""

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


@pytest.fixture
def template_env() -> Environment:
    """Create Jinja2 environment with templates directory."""
    templates_dir = Path(__file__).parent.parent / "claude_planner" / "templates"
    return Environment(loader=FileSystemLoader(str(templates_dir)))


@pytest.fixture
def minimal_template_data() -> dict[str, str | int | bool]:
    """Minimal required data for template rendering."""
    return {
        "project_name": "Test Project",
        "file_structure": "test/\n├── src/\n└── tests/",
        "test_coverage_requirement": 80,
        "test_command_all": "pytest tests/ -v",
        "test_command_specific": "pytest tests/test_file.py -v",
        "test_command_coverage": "pytest --cov=src --cov-report=html",
        "linter": "ruff",
        "type_checker": "mypy",
        "commit_type": "feat",
        "tech_stack": {"Language": "Python 3.11+", "Testing": "pytest"},
        "dependencies": ["pytest==7.4.3", "ruff==0.1.6"],
        "install_command": "pip install -e .",
        "docstring_style": "Google",
        "max_line_length": 100,
        "lint_command": "ruff check src",
        "type_check_command": "mypy src",
        "build_command": "python -m build",
        "has_cli": False,
        "custom_rules": [],
        "version": "1.0",
        "last_updated": "2024-10-10",
    }


@pytest.fixture
def full_template_data(minimal_template_data: dict) -> dict:
    """Full template data including CLI and custom rules."""
    data = minimal_template_data.copy()
    data.update(
        {
            "has_cli": True,
            "cli_command": "test-cli",
            "custom_rules": [
                {
                    "title": "Template Development",
                    "content": "Use Jinja2 syntax for all templates.",
                },
                {
                    "title": "Validation Rules",
                    "content": "Validate all inputs before processing.",
                },
            ],
        }
    )
    return data


class TestClaudeTemplateLoading:
    """Test template loading and availability."""

    def test_template_exists(self, template_env: Environment) -> None:
        """Test that claude.md.j2 template can be loaded."""
        try:
            template = template_env.get_template("base/claude.md.j2")
            assert template is not None
        except TemplateNotFound:
            pytest.fail("Template base/claude.md.j2 not found")

    def test_template_has_content(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that template file is not empty."""
        template = template_env.get_template("base/claude.md.j2")
        # Render with minimal data to check content
        rendered = template.render(**minimal_template_data)
        assert rendered is not None
        assert len(rendered) > 100  # Should have substantial content


class TestClaudeTemplateRendering:
    """Test template rendering with various data."""

    def test_render_with_minimal_data(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test template renders successfully with minimal required data."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert result is not None
        assert len(result) > 0

    def test_render_with_full_data(
        self, template_env: Environment, full_template_data: dict
    ) -> None:
        """Test template renders successfully with full data including optional fields."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**full_template_data)

        assert result is not None
        assert len(result) > 0

    def test_project_name_substitution(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that project_name variable is correctly substituted."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert "Test Project" in result
        assert "# Claude Code Development Rules - Test Project" in result

    def test_file_structure_substitution(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that file_structure variable is correctly substituted."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert "test/\n├── src/\n└── tests/" in result

    def test_test_coverage_requirement_substitution(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that test_coverage_requirement variable is correctly substituted."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert ">80%" in result
        assert "Coverage >80%" in result

    def test_tech_stack_loop(self, template_env: Environment, minimal_template_data: dict) -> None:
        """Test that tech_stack dictionary is correctly looped and rendered."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert "**Language**: Python 3.11+" in result
        assert "**Testing**: pytest" in result

    def test_dependencies_loop(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that dependencies list is correctly looped and rendered."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert "pytest==7.4.3" in result
        assert "ruff==0.1.6" in result

    def test_cli_section_when_has_cli_true(
        self, template_env: Environment, full_template_data: dict
    ) -> None:
        """Test that CLI section is included when has_cli is True."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**full_template_data)

        assert "### 9. CLI Design Standards" in result
        assert "test-cli <command> [options] [arguments]" in result

    def test_cli_section_when_has_cli_false(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that CLI section is excluded when has_cli is False."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert "### 9. CLI Design Standards" not in result
        assert "test-cli" not in result

    def test_custom_rules_when_empty(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that custom rules section is excluded when list is empty."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert "## Project-Specific Rules" not in result

    def test_custom_rules_when_present(
        self, template_env: Environment, full_template_data: dict
    ) -> None:
        """Test that custom rules section is included with content when present."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**full_template_data)

        assert "## Project-Specific Rules" in result
        assert "### Template Development" in result
        assert "Use Jinja2 syntax for all templates." in result
        assert "### Validation Rules" in result
        assert "Validate all inputs before processing." in result


class TestClaudeTemplateStructure:
    """Test that rendered template has expected structure."""

    def test_has_main_heading(self, template_env: Environment, minimal_template_data: dict) -> None:
        """Test that rendered output has main H1 heading."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        # Check for H1 heading
        assert re.search(r"^# Claude Code Development Rules", result, re.MULTILINE)

    def test_has_all_core_sections(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that all core sections are present in rendered output."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        expected_sections = [
            "## Core Operating Principles",
            "### 1. Single Session Execution",
            "### 2. Read Before Acting",
            "### 3. File Management",
            "### 4. Testing Requirements",
            "### 5. Completion Protocol",
            "### 6. Technology Decisions",
            "### 7. Error Handling",
            "### 8. Code Quality Standards",
            "### 10. Build Verification",
            "## Checklist: Starting a New Session",
            "## Checklist: Ending a Session",
        ]

        for section in expected_sections:
            assert section in result, f"Missing section: {section}"

    def test_has_checklists(self, template_env: Environment, minimal_template_data: dict) -> None:
        """Test that rendered output includes checklist items."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        # Check for checkbox markdown syntax
        assert "- [ ]" in result
        assert "- ✅" in result or "- [x]" in result

    def test_has_code_blocks(self, template_env: Environment, minimal_template_data: dict) -> None:
        """Test that rendered output includes code blocks."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        # Check for code block markers
        assert "```" in result
        assert "```bash" in result
        assert "```python" in result

    def test_version_and_metadata(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that version and metadata are included at bottom."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        assert "**Version**: 1.0" in result
        assert "**Last Updated**: 2024-10-10" in result
        assert "**Project**: Test Project" in result


class TestClaudeTemplateEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_tech_stack(self, template_env: Environment, minimal_template_data: dict) -> None:
        """Test rendering with empty tech_stack dictionary."""
        data = minimal_template_data.copy()
        data["tech_stack"] = {}

        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**data)

        assert result is not None
        # Section header should still be present
        assert "**Tech Stack:**" in result

    def test_empty_dependencies(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test rendering with empty dependencies list."""
        data = minimal_template_data.copy()
        data["dependencies"] = []

        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**data)

        assert result is not None
        # Section should still render correctly
        assert "**Key Dependencies:**" in result

    def test_long_project_name(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test rendering with very long project name."""
        data = minimal_template_data.copy()
        data["project_name"] = "A Very Long Project Name That Should Still Render"

        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**data)

        assert "A Very Long Project Name That Should Still Render" in result

    def test_special_characters_in_project_name(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test rendering with special characters in project name."""
        data = minimal_template_data.copy()
        data["project_name"] = "Project-Name_2024 (v1.0)"

        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**data)

        assert "Project-Name_2024 (v1.0)" in result

    def test_multiline_file_structure(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test rendering with complex multiline file structure."""
        data = minimal_template_data.copy()
        data["file_structure"] = (
            "project/\n├── src/\n│   ├── core/\n│   └── utils/\n├── tests/\n└── docs/"
        )

        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**data)

        assert "project/" in result
        assert "├── src/" in result
        assert "│   ├── core/" in result


class TestClaudeTemplateValidation:
    """Test that rendered output is valid markdown."""

    def test_no_unclosed_code_blocks(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that all code blocks are properly closed."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        # Count opening and closing code block markers
        opening_blocks = result.count("```")
        assert opening_blocks % 2 == 0, "Unmatched code block markers"

    def test_no_template_syntax_in_output(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that no unrendered Jinja2 syntax remains in output."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        # Check for common Jinja2 syntax patterns
        assert "{{" not in result, "Unrendered variable substitution found"
        assert "}}" not in result, "Unrendered variable substitution found"
        assert "{%" not in result, "Unrendered template tag found"
        assert "%}" not in result, "Unrendered template tag found"
        assert "{#" not in result, "Unrendered comment found"
        assert "#}" not in result, "Unrendered comment found"

    def test_consistent_heading_hierarchy(
        self, template_env: Environment, minimal_template_data: dict
    ) -> None:
        """Test that heading levels are properly nested (no skipping levels)."""
        template = template_env.get_template("base/claude.md.j2")
        result = template.render(**minimal_template_data)

        # Extract all headings
        headings = re.findall(r"^(#{1,6})\s+(.+)$", result, re.MULTILINE)

        # Should have headings
        assert len(headings) > 0

        # First heading should be H1
        assert headings[0][0] == "#"

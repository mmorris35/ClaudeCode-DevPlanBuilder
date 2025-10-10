"""Tests for CLI template.

This module tests that the CLI template correctly extends the base
templates and renders with CLI specific tech stack and phases.
"""

from pathlib import Path

import pytest
import yaml
from jinja2 import Environment, FileSystemLoader

from claude_planner.generator.renderer import render_all, render_claude_md, render_plan_md


@pytest.fixture
def template_env() -> Environment:
    """Create Jinja2 environment with templates directory."""
    templates_dir = Path(__file__).parent.parent / "claude_planner" / "templates"
    return Environment(loader=FileSystemLoader(str(templates_dir)))


@pytest.fixture
def cli_config() -> dict:
    """Load CLI config.yaml."""
    config_path = (
        Path(__file__).parent.parent / "claude_planner" / "templates" / "cli" / "config.yaml"
    )
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def claude_template_data() -> dict:
    """Template data for claude.md rendering."""
    return {
        "project_name": "DevTool CLI",
        "file_structure": (
            "devtool/\n├── devtool/\n│   ├── commands/\n│   ├── core/\n│   └── cli.py\n└── tests/"
        ),
        "test_coverage_requirement": 80,
        "test_command_all": "pytest tests/ -v",
        "test_command_specific": "pytest tests/test_cli.py -v",
        "test_command_coverage": "pytest --cov=devtool --cov-report=html",
        "linter": "ruff",
        "type_checker": "mypy",
        "commit_type": "feat",
        "tech_stack": {
            "Framework": "Click",
            "Language": "Python 3.11+",
            "Packaging": "setuptools",
            "Deployment": "PyPI",
        },
        "dependencies": [
            "click==8.1.7",
            "rich==13.7.0",
        ],
        "install_command": "pip install -e '.[dev]'",
        "docstring_style": "Google",
        "max_line_length": 100,
        "lint_command": "ruff check devtool tests",
        "type_check_command": "mypy devtool",
        "build_command": "python -m build",
        "has_cli": True,
        "cli_command": "devtool",
        "custom_rules": [],
        "version": "1.0",
        "last_updated": "2024-10-10",
    }


@pytest.fixture
def plan_template_data() -> dict:
    """Template data for DEVELOPMENT_PLAN.md rendering."""
    return {
        "project_name": "DevTool CLI",
        "goal": "Build a developer productivity CLI tool with Click framework",
        "target_users": "Software developers and DevOps engineers",
        "timeline": "3 weeks",
        "tech_stack": {
            "Framework": "Click",
            "Language": "Python 3.11+",
            "Packaging": "setuptools",
            "Deployment": "PyPI",
        },
        "phases": [
            {
                "id": 0,
                "title": "Foundation",
                "timeline": "Week 1, Days 1-2",
                "goal": "Set up project infrastructure",
                "tasks": [
                    {
                        "id": "0.1",
                        "title": "Repository Setup",
                        "subtasks": [
                            {
                                "id": "0.1.1",
                                "title": "Initialize Repository (Single Session)",
                                "status": "pending",
                                "prerequisites": [],
                                "deliverables": [
                                    "Create .gitignore",
                                    "Create README.md",
                                    "Setup project structure",
                                ],
                                "success_criteria": [
                                    ".gitignore configured",
                                    "README documented",
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "id": 1,
                "title": "Command Structure",
                "timeline": "Week 1, Days 3-4",
                "goal": "Define CLI command structure",
                "tasks": [
                    {
                        "id": "1.1",
                        "title": "Command Groups",
                        "subtasks": [
                            {
                                "id": "1.1.1",
                                "title": "Main CLI Entry Point (Single Session)",
                                "status": "pending",
                                "prerequisites": ["0.1.1"],
                                "deliverables": [
                                    "Create main CLI group",
                                    "Add version command",
                                ],
                                "success_criteria": [
                                    "CLI runs successfully",
                                    "Help text displays",
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "id": 2,
                "title": "Command Implementation",
                "timeline": "Week 1, Days 5 - Week 2, Day 2",
                "goal": "Implement core CLI commands",
                "tasks": [
                    {
                        "id": "2.1",
                        "title": "Core Commands",
                        "subtasks": [
                            {
                                "id": "2.1.1",
                                "title": "Init Command (Single Session)",
                                "status": "pending",
                                "prerequisites": ["1.1.1"],
                                "deliverables": [
                                    "Create init command",
                                    "Add directory scaffolding",
                                    "Add configuration generation",
                                ],
                                "success_criteria": [
                                    "Init command works",
                                    "Files created correctly",
                                ],
                            }
                        ],
                    }
                ],
            },
        ],
        "current_phase": 0,
        "next_subtask": "0.1.1",
    }


class TestCLIConfig:
    """Test CLI template configuration."""

    def test_config_exists(self, cli_config: dict) -> None:
        """Test that CLI config.yaml exists and is valid."""
        assert cli_config is not None
        assert "name" in cli_config
        assert "description" in cli_config

    def test_config_name(self, cli_config: dict) -> None:
        """Test that config has correct name."""
        assert cli_config["name"] == "cli"

    def test_config_extends_base(self, cli_config: dict) -> None:
        """Test that config extends base template."""
        assert "extends" in cli_config
        assert cli_config["extends"] == "base"

    def test_config_project_types(self, cli_config: dict) -> None:
        """Test that config defines project types."""
        assert "project_types" in cli_config
        assert isinstance(cli_config["project_types"], list)
        assert "CLI" in cli_config["project_types"]
        assert "cli" in cli_config["project_types"]

    def test_config_default_tech_stack(self, cli_config: dict) -> None:
        """Test that config defines default tech stack."""
        assert "default_tech_stack" in cli_config
        tech_stack = cli_config["default_tech_stack"]
        assert "framework" in tech_stack
        assert "language" in tech_stack
        assert "packaging" in tech_stack
        assert "Click" in tech_stack["framework"]
        assert "Python" in tech_stack["language"]
        assert "setuptools" in tech_stack["packaging"]

    def test_config_default_phases(self, cli_config: dict) -> None:
        """Test that config defines default phases."""
        assert "default_phases" in cli_config
        phases = cli_config["default_phases"]
        assert isinstance(phases, list)
        assert "Foundation" in phases
        assert "Command Structure" in phases
        assert "Command Implementation" in phases
        assert "Argument Parsing" in phases
        assert "Distribution" in phases


class TestCLIClaudeTemplate:
    """Test CLI claude.md template rendering."""

    def test_template_exists(self, template_env: Environment) -> None:
        """Test that CLI claude.md.j2 template exists."""
        try:
            template = template_env.get_template("cli/claude.md.j2")
            assert template is not None
        except Exception as e:
            pytest.fail(f"Template cli/claude.md.j2 not found: {e}")

    def test_template_extends_base(self) -> None:
        """Test that CLI template extends base template."""
        template_path = (
            Path(__file__).parent.parent / "claude_planner" / "templates" / "cli" / "claude.md.j2"
        )
        source = template_path.read_text(encoding="utf-8")
        assert "extends" in source or "base/claude.md.j2" in source

    def test_render_with_cli_data(self, tmp_path: Path, claude_template_data: dict) -> None:
        """Test rendering claude.md with CLI specific data."""
        output_path = tmp_path / "claude.md"

        render_claude_md("cli", output_path, **claude_template_data)

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "DevTool CLI" in content
        assert "Click" in content
        assert "Python 3.11+" in content

    def test_render_includes_base_sections(
        self, tmp_path: Path, claude_template_data: dict
    ) -> None:
        """Test that rendered output includes all base template sections."""
        output_path = tmp_path / "claude.md"

        render_claude_md("cli", output_path, **claude_template_data)

        content = output_path.read_text(encoding="utf-8")
        # Check for core sections from base template
        assert "## Core Operating Principles" in content
        assert "### 1. Single Session Execution" in content
        assert "### 4. Testing Requirements" in content
        assert "### 5. Completion Protocol" in content

    def test_render_includes_cli_section(self, tmp_path: Path, claude_template_data: dict) -> None:
        """Test that rendered output includes CLI Design Standards section."""
        output_path = tmp_path / "claude.md"

        render_claude_md("cli", output_path, **claude_template_data)

        content = output_path.read_text(encoding="utf-8")
        # Should include CLI section since has_cli is True
        assert "### 9. CLI Design Standards" in content
        assert "devtool" in content  # cli_command


class TestCLIPlanTemplate:
    """Test CLI plan.md template rendering."""

    def test_template_exists(self, template_env: Environment) -> None:
        """Test that CLI plan.md.j2 template exists."""
        try:
            template = template_env.get_template("cli/plan.md.j2")
            assert template is not None
        except Exception as e:
            pytest.fail(f"Template cli/plan.md.j2 not found: {e}")

    def test_template_extends_base(self) -> None:
        """Test that CLI plan template extends base template."""
        template_path = (
            Path(__file__).parent.parent / "claude_planner" / "templates" / "cli" / "plan.md.j2"
        )
        source = template_path.read_text(encoding="utf-8")
        assert "extends" in source or "base/plan.md.j2" in source

    def test_render_with_cli_phases(self, tmp_path: Path, plan_template_data: dict) -> None:
        """Test rendering plan.md with CLI specific phases."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md("cli", output_path, **plan_template_data)

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "DevTool CLI" in content
        assert "## Phase 0: Foundation" in content
        assert "## Phase 1: Command Structure" in content
        assert "## Phase 2: Command Implementation" in content

    def test_render_includes_base_structure(self, tmp_path: Path, plan_template_data: dict) -> None:
        """Test that rendered output includes base template structure."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md("cli", output_path, **plan_template_data)

        content = output_path.read_text(encoding="utf-8")
        # Check for core sections from base template
        assert "## 🎯 How to Use This Plan" in content
        assert "## Project Overview" in content
        assert "## Technology Stack" in content
        assert "## Progress Tracking" in content


class TestCLIFullRendering:
    """Test rendering complete CLI project."""

    def test_render_all_cli_files(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test rendering all files for a CLI project."""
        output_dir = tmp_path / "cli"

        # Combine template data (render_all needs all variables)
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("cli", output_dir, **all_vars)

        assert "claude_md" in files
        assert "plan_md" in files
        assert files["claude_md"].exists()
        assert files["plan_md"].exists()

    def test_cli_tech_stack_consistency(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test that tech stack is consistent across both files."""
        output_dir = tmp_path / "consistency"
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("cli", output_dir, **all_vars)

        claude_content = files["claude_md"].read_text(encoding="utf-8")
        plan_content = files["plan_md"].read_text(encoding="utf-8")

        # Tech stack should appear in both files
        assert "Click" in claude_content
        assert "Click" in plan_content
        assert "Python 3.11+" in claude_content
        assert "Python 3.11+" in plan_content

    def test_cli_project_structure(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test that rendered files have proper CLI project structure."""
        output_dir = tmp_path / "structure"
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("cli", output_dir, **all_vars)

        claude_content = files["claude_md"].read_text(encoding="utf-8")
        plan_content = files["plan_md"].read_text(encoding="utf-8")

        # Check for CLI specific phases
        assert "Command Structure" in plan_content
        assert "Command Implementation" in plan_content

        # Check for appropriate file structure
        assert "commands/" in claude_content or "cli.py" in claude_content

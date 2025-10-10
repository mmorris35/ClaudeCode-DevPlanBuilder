"""Tests for API template.

This module tests that the API template correctly extends the base
templates and renders with API specific tech stack and phases.
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
def api_config() -> dict:
    """Load API config.yaml."""
    config_path = (
        Path(__file__).parent.parent / "claude_planner" / "templates" / "api" / "config.yaml"
    )
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def claude_template_data() -> dict:
    """Template data for claude.md rendering."""
    return {
        "project_name": "Task Management API",
        "file_structure": (
            "task-api/\n├── app/\n│   ├── models/\n│   ├── routes/\n│   └── core/\n└── tests/"
        ),
        "test_coverage_requirement": 80,
        "test_command_all": "pytest tests/ -v",
        "test_command_specific": "pytest tests/test_api.py -v",
        "test_command_coverage": "pytest --cov=app --cov-report=html",
        "linter": "ruff",
        "type_checker": "mypy",
        "commit_type": "feat",
        "tech_stack": {
            "Framework": "FastAPI",
            "Database": "PostgreSQL",
            "Cache": "Redis",
            "Deployment": "Docker + AWS",
        },
        "dependencies": [
            "fastapi==0.104.1",
            "uvicorn==0.24.0",
            "sqlalchemy==2.0.23",
            "psycopg2-binary==2.9.9",
            "redis==5.0.1",
        ],
        "install_command": "pip install -e '.[dev]'",
        "docstring_style": "Google",
        "max_line_length": 100,
        "lint_command": "ruff check app tests",
        "type_check_command": "mypy app",
        "build_command": "python -m build",
        "has_cli": False,
        "custom_rules": [],
        "version": "1.0",
        "last_updated": "2024-10-10",
    }


@pytest.fixture
def plan_template_data() -> dict:
    """Template data for DEVELOPMENT_PLAN.md rendering."""
    return {
        "project_name": "Task Management API",
        "goal": "Build a RESTful API for task management with FastAPI and PostgreSQL",
        "target_users": "Frontend developers and mobile app developers",
        "timeline": "3 weeks",
        "tech_stack": {
            "Framework": "FastAPI",
            "Database": "PostgreSQL",
            "Cache": "Redis",
            "Deployment": "Docker + AWS",
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
                "title": "Data Models",
                "timeline": "Week 1, Days 3-4",
                "goal": "Define database models and schemas",
                "tasks": [
                    {
                        "id": "1.1",
                        "title": "SQLAlchemy Models",
                        "subtasks": [
                            {
                                "id": "1.1.1",
                                "title": "Task Model (Single Session)",
                                "status": "pending",
                                "prerequisites": ["0.1.1"],
                                "deliverables": [
                                    "Create Task model",
                                    "Add database migrations",
                                ],
                                "success_criteria": [
                                    "Model defined correctly",
                                    "Migrations work",
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "id": 2,
                "title": "API Endpoints",
                "timeline": "Week 1, Days 5 - Week 2, Day 2",
                "goal": "Implement RESTful API endpoints",
                "tasks": [
                    {
                        "id": "2.1",
                        "title": "Task Endpoints",
                        "subtasks": [
                            {
                                "id": "2.1.1",
                                "title": "CRUD Endpoints (Single Session)",
                                "status": "pending",
                                "prerequisites": ["1.1.1"],
                                "deliverables": [
                                    "Create GET /tasks endpoint",
                                    "Create POST /tasks endpoint",
                                    "Create PUT /tasks/{id} endpoint",
                                    "Create DELETE /tasks/{id} endpoint",
                                ],
                                "success_criteria": [
                                    "All CRUD operations work",
                                    "Proper status codes",
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


class TestAPIConfig:
    """Test API template configuration."""

    def test_config_exists(self, api_config: dict) -> None:
        """Test that API config.yaml exists and is valid."""
        assert api_config is not None
        assert "name" in api_config
        assert "description" in api_config

    def test_config_name(self, api_config: dict) -> None:
        """Test that config has correct name."""
        assert api_config["name"] == "api"

    def test_config_extends_base(self, api_config: dict) -> None:
        """Test that config extends base template."""
        assert "extends" in api_config
        assert api_config["extends"] == "base"

    def test_config_project_types(self, api_config: dict) -> None:
        """Test that config defines project types."""
        assert "project_types" in api_config
        assert isinstance(api_config["project_types"], list)
        assert "API" in api_config["project_types"]
        assert "api" in api_config["project_types"]

    def test_config_default_tech_stack(self, api_config: dict) -> None:
        """Test that config defines default tech stack."""
        assert "default_tech_stack" in api_config
        tech_stack = api_config["default_tech_stack"]
        assert "framework" in tech_stack
        assert "database" in tech_stack
        assert "cache" in tech_stack
        assert "FastAPI" in tech_stack["framework"]
        assert "PostgreSQL" in tech_stack["database"]
        assert "Redis" in tech_stack["cache"]

    def test_config_default_phases(self, api_config: dict) -> None:
        """Test that config defines default phases."""
        assert "default_phases" in api_config
        phases = api_config["default_phases"]
        assert isinstance(phases, list)
        assert "Foundation" in phases
        assert "Data Models" in phases
        assert "API Endpoints" in phases
        assert "Authentication" in phases
        assert "Documentation" in phases


class TestAPIClaudeTemplate:
    """Test API claude.md template rendering."""

    def test_template_exists(self, template_env: Environment) -> None:
        """Test that API claude.md.j2 template exists."""
        try:
            template = template_env.get_template("api/claude.md.j2")
            assert template is not None
        except Exception as e:
            pytest.fail(f"Template api/claude.md.j2 not found: {e}")

    def test_template_extends_base(self) -> None:
        """Test that API template extends base template."""
        template_path = (
            Path(__file__).parent.parent / "claude_planner" / "templates" / "api" / "claude.md.j2"
        )
        source = template_path.read_text(encoding="utf-8")
        assert "extends" in source or "base/claude.md.j2" in source

    def test_render_with_api_data(self, tmp_path: Path, claude_template_data: dict) -> None:
        """Test rendering claude.md with API specific data."""
        output_path = tmp_path / "claude.md"

        render_claude_md("api", output_path, **claude_template_data)

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "Task Management API" in content
        assert "FastAPI" in content
        assert "PostgreSQL" in content
        assert "Redis" in content

    def test_render_includes_base_sections(
        self, tmp_path: Path, claude_template_data: dict
    ) -> None:
        """Test that rendered output includes all base template sections."""
        output_path = tmp_path / "claude.md"

        render_claude_md("api", output_path, **claude_template_data)

        content = output_path.read_text(encoding="utf-8")
        # Check for core sections from base template
        assert "## Core Operating Principles" in content
        assert "### 1. Single Session Execution" in content
        assert "### 4. Testing Requirements" in content
        assert "### 5. Completion Protocol" in content


class TestAPIPlanTemplate:
    """Test API plan.md template rendering."""

    def test_template_exists(self, template_env: Environment) -> None:
        """Test that API plan.md.j2 template exists."""
        try:
            template = template_env.get_template("api/plan.md.j2")
            assert template is not None
        except Exception as e:
            pytest.fail(f"Template api/plan.md.j2 not found: {e}")

    def test_template_extends_base(self) -> None:
        """Test that API plan template extends base template."""
        template_path = (
            Path(__file__).parent.parent / "claude_planner" / "templates" / "api" / "plan.md.j2"
        )
        source = template_path.read_text(encoding="utf-8")
        assert "extends" in source or "base/plan.md.j2" in source

    def test_render_with_api_phases(self, tmp_path: Path, plan_template_data: dict) -> None:
        """Test rendering plan.md with API specific phases."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md("api", output_path, **plan_template_data)

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "Task Management API" in content
        assert "## Phase 0: Foundation" in content
        assert "## Phase 1: Data Models" in content
        assert "## Phase 2: API Endpoints" in content

    def test_render_includes_base_structure(self, tmp_path: Path, plan_template_data: dict) -> None:
        """Test that rendered output includes base template structure."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md("api", output_path, **plan_template_data)

        content = output_path.read_text(encoding="utf-8")
        # Check for core sections from base template
        assert "## 🎯 How to Use This Plan" in content
        assert "## Project Overview" in content
        assert "## Technology Stack" in content
        assert "## Progress Tracking" in content


class TestAPIFullRendering:
    """Test rendering complete API project."""

    def test_render_all_api_files(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test rendering all files for an API project."""
        output_dir = tmp_path / "api"

        # Combine template data (render_all needs all variables)
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("api", output_dir, **all_vars)

        assert "claude_md" in files
        assert "plan_md" in files
        assert files["claude_md"].exists()
        assert files["plan_md"].exists()

    def test_api_tech_stack_consistency(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test that tech stack is consistent across both files."""
        output_dir = tmp_path / "consistency"
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("api", output_dir, **all_vars)

        claude_content = files["claude_md"].read_text(encoding="utf-8")
        plan_content = files["plan_md"].read_text(encoding="utf-8")

        # Tech stack should appear in both files
        assert "FastAPI" in claude_content
        assert "FastAPI" in plan_content
        assert "PostgreSQL" in claude_content
        assert "PostgreSQL" in plan_content
        assert "Redis" in claude_content
        assert "Redis" in plan_content

    def test_api_project_structure(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test that rendered files have proper API project structure."""
        output_dir = tmp_path / "structure"
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("api", output_dir, **all_vars)

        claude_content = files["claude_md"].read_text(encoding="utf-8")
        plan_content = files["plan_md"].read_text(encoding="utf-8")

        # Check for API specific phases
        assert "Data Models" in plan_content
        assert "API Endpoints" in plan_content

        # Check for appropriate file structure
        assert "app/" in claude_content or "models/" in claude_content

"""Tests for web-app template.

This module tests that the web-app template correctly extends the base
templates and renders with web-app specific tech stack and phases.
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
def web_app_config() -> dict:
    """Load web-app config.yaml."""
    config_path = (
        Path(__file__).parent.parent / "claude_planner" / "templates" / "web-app" / "config.yaml"
    )
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def claude_template_data() -> dict:
    """Template data for claude.md rendering."""
    return {
        "project_name": "E-Commerce Platform",
        "file_structure": "ecommerce/\n├── frontend/\n├── backend/\n└── tests/",
        "test_coverage_requirement": 80,
        "test_command_all": "pytest tests/ -v",
        "test_command_specific": "pytest tests/test_api.py -v",
        "test_command_coverage": "pytest --cov=backend --cov-report=html",
        "linter": "ruff",
        "type_checker": "mypy",
        "commit_type": "feat",
        "tech_stack": {
            "Frontend": "React + Next.js",
            "Backend": "Python + FastAPI",
            "Database": "PostgreSQL",
            "Deployment": "Vercel + AWS",
        },
        "dependencies": [
            "fastapi==0.104.1",
            "uvicorn==0.24.0",
            "sqlalchemy==2.0.23",
            "psycopg2-binary==2.9.9",
        ],
        "install_command": "pip install -e '.[dev]'",
        "docstring_style": "Google",
        "max_line_length": 100,
        "lint_command": "ruff check backend frontend",
        "type_check_command": "mypy backend",
        "build_command": "npm run build && python -m build",
        "has_cli": False,
        "custom_rules": [],
        "version": "1.0",
        "last_updated": "2024-10-10",
    }


@pytest.fixture
def plan_template_data() -> dict:
    """Template data for DEVELOPMENT_PLAN.md rendering."""
    return {
        "project_name": "E-Commerce Platform",
        "goal": "Build a full-stack e-commerce platform with React frontend and FastAPI backend",
        "target_users": "Online shoppers and store administrators",
        "timeline": "4 weeks",
        "tech_stack": {
            "Frontend": "React + Next.js",
            "Backend": "Python + FastAPI",
            "Database": "PostgreSQL",
            "Deployment": "Vercel + AWS",
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
                                    "Initialize monorepo structure",
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
                "title": "Frontend Development",
                "timeline": "Week 1, Days 3-5",
                "goal": "Build React frontend with Next.js",
                "tasks": [
                    {
                        "id": "1.1",
                        "title": "UI Components",
                        "subtasks": [
                            {
                                "id": "1.1.1",
                                "title": "Product Catalog (Single Session)",
                                "status": "pending",
                                "prerequisites": ["0.1.1"],
                                "deliverables": [
                                    "Create ProductList component",
                                    "Add API integration",
                                ],
                                "success_criteria": [
                                    "Products display correctly",
                                    "Responsive design works",
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "id": 2,
                "title": "Backend Development",
                "timeline": "Week 2, Days 1-3",
                "goal": "Build FastAPI backend with PostgreSQL",
                "tasks": [
                    {
                        "id": "2.1",
                        "title": "API Endpoints",
                        "subtasks": [
                            {
                                "id": "2.1.1",
                                "title": "Product API (Single Session)",
                                "status": "pending",
                                "prerequisites": ["0.1.1"],
                                "deliverables": [
                                    "Create product endpoints",
                                    "Add database models",
                                ],
                                "success_criteria": [
                                    "CRUD operations work",
                                    "API documented",
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


class TestWebAppConfig:
    """Test web-app template configuration."""

    def test_config_exists(self, web_app_config: dict) -> None:
        """Test that web-app config.yaml exists and is valid."""
        assert web_app_config is not None
        assert "name" in web_app_config
        assert "description" in web_app_config

    def test_config_name(self, web_app_config: dict) -> None:
        """Test that config has correct name."""
        assert web_app_config["name"] == "web-app"

    def test_config_extends_base(self, web_app_config: dict) -> None:
        """Test that config extends base template."""
        assert "extends" in web_app_config
        assert web_app_config["extends"] == "base"

    def test_config_project_types(self, web_app_config: dict) -> None:
        """Test that config defines project types."""
        assert "project_types" in web_app_config
        assert isinstance(web_app_config["project_types"], list)
        assert "Web App" in web_app_config["project_types"]

    def test_config_default_tech_stack(self, web_app_config: dict) -> None:
        """Test that config defines default tech stack."""
        assert "default_tech_stack" in web_app_config
        tech_stack = web_app_config["default_tech_stack"]
        assert "frontend" in tech_stack
        assert "backend" in tech_stack
        assert "database" in tech_stack
        assert "React" in tech_stack["frontend"]
        assert "FastAPI" in tech_stack["backend"]
        assert "PostgreSQL" in tech_stack["database"]

    def test_config_default_phases(self, web_app_config: dict) -> None:
        """Test that config defines default phases."""
        assert "default_phases" in web_app_config
        phases = web_app_config["default_phases"]
        assert isinstance(phases, list)
        assert "Foundation" in phases
        assert "Frontend Development" in phases
        assert "Backend Development" in phases
        assert "Database Setup" in phases


class TestWebAppClaudeTemplate:
    """Test web-app claude.md template rendering."""

    def test_template_exists(self, template_env: Environment) -> None:
        """Test that web-app claude.md.j2 template exists."""
        try:
            template = template_env.get_template("web-app/claude.md.j2")
            assert template is not None
        except Exception as e:
            pytest.fail(f"Template web-app/claude.md.j2 not found: {e}")

    def test_template_extends_base(self) -> None:
        """Test that web-app template extends base template."""
        template_path = (
            Path(__file__).parent.parent
            / "claude_planner"
            / "templates"
            / "web-app"
            / "claude.md.j2"
        )
        source = template_path.read_text(encoding="utf-8")
        assert "extends" in source or "base/claude.md.j2" in source

    def test_render_with_web_app_data(self, tmp_path: Path, claude_template_data: dict) -> None:
        """Test rendering claude.md with web-app specific data."""
        output_path = tmp_path / "claude.md"

        render_claude_md("web-app", output_path, **claude_template_data)

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "E-Commerce Platform" in content
        assert "React + Next.js" in content
        assert "Python + FastAPI" in content
        assert "PostgreSQL" in content

    def test_render_includes_base_sections(
        self, tmp_path: Path, claude_template_data: dict
    ) -> None:
        """Test that rendered output includes all base template sections."""
        output_path = tmp_path / "claude.md"

        render_claude_md("web-app", output_path, **claude_template_data)

        content = output_path.read_text(encoding="utf-8")
        # Check for core sections from base template
        assert "## Core Operating Principles" in content
        assert "### 1. Single Session Execution" in content
        assert "### 4. Testing Requirements" in content
        assert "### 5. Completion Protocol" in content


class TestWebAppPlanTemplate:
    """Test web-app plan.md template rendering."""

    def test_template_exists(self, template_env: Environment) -> None:
        """Test that web-app plan.md.j2 template exists."""
        try:
            template = template_env.get_template("web-app/plan.md.j2")
            assert template is not None
        except Exception as e:
            pytest.fail(f"Template web-app/plan.md.j2 not found: {e}")

    def test_template_extends_base(self) -> None:
        """Test that web-app plan template extends base template."""
        template_path = (
            Path(__file__).parent.parent / "claude_planner" / "templates" / "web-app" / "plan.md.j2"
        )
        source = template_path.read_text(encoding="utf-8")
        assert "extends" in source or "base/plan.md.j2" in source

    def test_render_with_web_app_phases(self, tmp_path: Path, plan_template_data: dict) -> None:
        """Test rendering plan.md with web-app specific phases."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md("web-app", output_path, **plan_template_data)

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "E-Commerce Platform" in content
        assert "## Phase 0: Foundation" in content
        assert "## Phase 1: Frontend Development" in content
        assert "## Phase 2: Backend Development" in content

    def test_render_includes_base_structure(self, tmp_path: Path, plan_template_data: dict) -> None:
        """Test that rendered output includes base template structure."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md("web-app", output_path, **plan_template_data)

        content = output_path.read_text(encoding="utf-8")
        # Check for core sections from base template
        assert "## 🎯 How to Use This Plan" in content
        assert "## Project Overview" in content
        assert "## Technology Stack" in content
        assert "## Progress Tracking" in content


class TestWebAppFullRendering:
    """Test rendering complete web-app project."""

    def test_render_all_web_app_files(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test rendering all files for a web-app project."""
        output_dir = tmp_path / "webapp"

        # Combine template data (render_all needs all variables)
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("web-app", output_dir, **all_vars)

        assert "claude_md" in files
        assert "plan_md" in files
        assert files["claude_md"].exists()
        assert files["plan_md"].exists()

    def test_web_app_tech_stack_consistency(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test that tech stack is consistent across both files."""
        output_dir = tmp_path / "consistency"
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("web-app", output_dir, **all_vars)

        claude_content = files["claude_md"].read_text(encoding="utf-8")
        plan_content = files["plan_md"].read_text(encoding="utf-8")

        # Tech stack should appear in both files
        assert "React + Next.js" in claude_content
        assert "React + Next.js" in plan_content
        assert "Python + FastAPI" in claude_content
        assert "Python + FastAPI" in plan_content
        assert "PostgreSQL" in claude_content
        assert "PostgreSQL" in plan_content

    def test_web_app_project_structure(
        self, tmp_path: Path, claude_template_data: dict, plan_template_data: dict
    ) -> None:
        """Test that rendered files have proper web-app project structure."""
        output_dir = tmp_path / "structure"
        all_vars = {**claude_template_data, **plan_template_data}

        files = render_all("web-app", output_dir, **all_vars)

        claude_content = files["claude_md"].read_text(encoding="utf-8")
        plan_content = files["plan_md"].read_text(encoding="utf-8")

        # Check for web-app specific phases
        assert "Frontend Development" in plan_content
        assert "Backend Development" in plan_content

        # Check for appropriate file structure
        assert "frontend/" in claude_content or "backend/" in claude_content

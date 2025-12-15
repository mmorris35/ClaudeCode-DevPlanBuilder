"""Tests for template renderer module.

This module tests the template rendering engine that generates
claude.md and DEVELOPMENT_PLAN.md files from Jinja2 templates.
"""

from pathlib import Path

import pytest

from claude_planner.generator.renderer import (
    _create_jinja_env,
    _get_templates_dir,
    _slugify,
    render_agent_md,
    render_all,
    render_claude_md,
    render_plan_md,
)


class TestHelperFunctions:
    """Test helper functions for renderer."""

    def test_get_templates_dir(self) -> None:
        """Test that templates directory path is correct."""
        templates_dir = _get_templates_dir()

        assert templates_dir.exists()
        assert templates_dir.is_dir()
        assert templates_dir.name == "templates"

    def test_create_jinja_env(self) -> None:
        """Test that Jinja2 environment is created correctly."""
        env = _create_jinja_env()

        assert env is not None
        assert env.loader is not None


class TestSlugify:
    """Test _slugify helper function."""

    def test_basic_slug(self) -> None:
        """Test basic slugification."""
        assert _slugify("My Project") == "my-project"

    def test_multiple_spaces(self) -> None:
        """Test handling of multiple spaces."""
        assert _slugify("My  Cool   Project") == "my-cool-project"

    def test_underscores(self) -> None:
        """Test underscore conversion."""
        assert _slugify("my_cool_project") == "my-cool-project"

    def test_special_characters(self) -> None:
        """Test removal of special characters."""
        # Note: periods and other special chars are removed, not replaced with hyphens
        assert _slugify("CLI Tool v2.0!") == "cli-tool-v20"
        assert _slugify("My App (beta)") == "my-app-beta"

    def test_leading_trailing_hyphens(self) -> None:
        """Test removal of leading/trailing hyphens."""
        assert _slugify("  My Project  ") == "my-project"

    def test_consecutive_hyphens(self) -> None:
        """Test consolidation of consecutive hyphens."""
        assert _slugify("my---project") == "my-project"

    def test_already_slugified(self) -> None:
        """Test that already-slugified names are unchanged."""
        assert _slugify("my-project") == "my-project"

    def test_mixed_case(self) -> None:
        """Test mixed case handling."""
        assert _slugify("MyProject") == "myproject"


class TestRenderClaudeMd:
    """Test render_claude_md function."""

    def test_render_with_minimal_data(self, tmp_path: Path) -> None:
        """Test rendering claude.md with minimal required data."""
        output_path = tmp_path / "claude.md"

        render_claude_md(
            "base",
            output_path,
            project_name="Test Project",
            file_structure="test/\n├── src/\n└── tests/",
            test_coverage_requirement=80,
            test_command_all="pytest tests/ -v",
            test_command_specific="pytest tests/test_file.py -v",
            test_command_coverage="pytest --cov=src",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={"Language": "Python 3.11+"},
            dependencies=["pytest==7.4.3"],
            install_command="pip install -e .",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check src",
            type_check_command="mypy src",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
        )

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "# Claude Code Development Rules - Test Project" in content
        assert "Python 3.11+" in content

    def test_render_creates_parent_directories(self, tmp_path: Path) -> None:
        """Test that render_claude_md creates parent directories if they don't exist."""
        output_path = tmp_path / "nested" / "dir" / "claude.md"

        render_claude_md(
            "base",
            output_path,
            project_name="Test",
            file_structure="test/",
            test_coverage_requirement=80,
            test_command_all="pytest",
            test_command_specific="pytest test.py",
            test_command_coverage="pytest --cov",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={},
            dependencies=[],
            install_command="pip install",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check",
            type_check_command="mypy",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
        )

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_render_with_invalid_template(self, tmp_path: Path) -> None:
        """Test that render_claude_md raises error with invalid template."""
        output_path = tmp_path / "claude.md"

        with pytest.raises(FileNotFoundError, match="Template.*not found"):
            render_claude_md(
                "nonexistent",
                output_path,
                project_name="Test",
            )

    def test_render_overwrites_existing_file(self, tmp_path: Path) -> None:
        """Test that render_claude_md overwrites existing files."""
        output_path = tmp_path / "claude.md"

        # Write initial content
        output_path.write_text("Old content")

        # Render new content
        render_claude_md(
            "base",
            output_path,
            project_name="New Project",
            file_structure="test/",
            test_coverage_requirement=80,
            test_command_all="pytest",
            test_command_specific="pytest test.py",
            test_command_coverage="pytest --cov",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={},
            dependencies=[],
            install_command="pip install",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check",
            type_check_command="mypy",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
        )

        content = output_path.read_text(encoding="utf-8")
        assert "Old content" not in content
        assert "New Project" in content


class TestRenderPlanMd:
    """Test render_plan_md function."""

    def test_render_with_minimal_data(self, tmp_path: Path) -> None:
        """Test rendering DEVELOPMENT_PLAN.md with minimal required data."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md(
            "base",
            output_path,
            project_name="Test Project",
            goal="Build a test application",
            target_users="Developers",
            timeline="2 weeks",
            tech_stack={"Language": "Python 3.11+"},
            phases=[
                {
                    "id": 0,
                    "title": "Foundation",
                    "timeline": "Week 1",
                    "goal": "Setup",
                    "tasks": [
                        {
                            "id": "0.1",
                            "title": "Setup",
                            "subtasks": [
                                {
                                    "id": "0.1.1",
                                    "title": "Init (Single Session)",
                                    "status": "pending",
                                    "prerequisites": [],
                                    "deliverables": ["Create repo"],
                                    "success_criteria": ["Repo created"],
                                }
                            ],
                        }
                    ],
                }
            ],
            current_phase=0,
            next_subtask="0.1.1",
        )

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "# Test Project - Development Plan" in content
        assert "## Phase 0: Foundation" in content

    def test_render_creates_parent_directories(self, tmp_path: Path) -> None:
        """Test that render_plan_md creates parent directories if they don't exist."""
        output_path = tmp_path / "nested" / "DEVELOPMENT_PLAN.md"

        render_plan_md(
            "base",
            output_path,
            project_name="Test",
            goal="Test",
            target_users="Users",
            timeline="1 week",
            tech_stack={},
            phases=[],
            current_phase=0,
            next_subtask="0.1.1",
        )

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_render_with_invalid_template(self, tmp_path: Path) -> None:
        """Test that render_plan_md raises error with invalid template."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        with pytest.raises(FileNotFoundError, match="Template.*not found"):
            render_plan_md(
                "nonexistent",
                output_path,
                project_name="Test",
            )

    def test_render_with_multiple_phases(self, tmp_path: Path) -> None:
        """Test rendering with multiple phases, tasks, and subtasks."""
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md(
            "base",
            output_path,
            project_name="Multi-Phase Project",
            goal="Build application",
            target_users="Users",
            timeline="4 weeks",
            tech_stack={"Language": "Python"},
            phases=[
                {
                    "id": 0,
                    "title": "Foundation",
                    "timeline": "Week 1",
                    "goal": "Setup",
                    "tasks": [
                        {
                            "id": "0.1",
                            "title": "Setup",
                            "subtasks": [
                                {
                                    "id": "0.1.1",
                                    "title": "Init (Single Session)",
                                    "status": "complete",
                                    "prerequisites": [],
                                    "deliverables": ["Create repo"],
                                    "success_criteria": ["Repo created"],
                                }
                            ],
                        }
                    ],
                },
                {
                    "id": 1,
                    "title": "Core Features",
                    "timeline": "Week 2",
                    "goal": "Build features",
                    "tasks": [
                        {
                            "id": "1.1",
                            "title": "Features",
                            "subtasks": [
                                {
                                    "id": "1.1.1",
                                    "title": "Feature A (Single Session)",
                                    "status": "pending",
                                    "prerequisites": ["0.1.1"],
                                    "deliverables": ["Implement feature"],
                                    "success_criteria": ["Feature works"],
                                }
                            ],
                        }
                    ],
                },
            ],
            current_phase=1,
            next_subtask="1.1.1",
        )

        content = output_path.read_text(encoding="utf-8")
        assert "## Phase 0: Foundation" in content
        assert "## Phase 1: Core Features" in content
        assert "- [x] 0.1.1" in content  # Completed
        assert "- [ ] 1.1.1" in content  # Pending


class TestRenderAll:
    """Test render_all function."""

    def test_render_all_creates_all_files(self, tmp_path: Path) -> None:
        """Test that render_all creates claude.md, DEVELOPMENT_PLAN.md, and agent.md."""
        output_dir = tmp_path / "output"

        files = render_all(
            "base",
            output_dir,
            # Claude.md variables
            project_name="Test Project",
            file_structure="test/",
            test_coverage_requirement=80,
            test_command_all="pytest",
            test_command_specific="pytest test.py",
            test_command_coverage="pytest --cov",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={"Language": "Python 3.11+"},
            dependencies=[],
            install_command="pip install",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check",
            type_check_command="mypy",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
            # Plan.md variables
            goal="Build app",
            target_users="Users",
            timeline="2 weeks",
            phases=[],
            current_phase=0,
            next_subtask="0.1.1",
        )

        assert "claude_md" in files
        assert "plan_md" in files
        assert "agent_md" in files
        assert files["claude_md"].exists()
        assert files["plan_md"].exists()
        assert files["agent_md"].exists()
        assert files["claude_md"].name == "claude.md"
        assert files["plan_md"].name == "DEVELOPMENT_PLAN.md"
        assert files["agent_md"].name == "test-project-executor.md"

    def test_render_all_creates_output_directory(self, tmp_path: Path) -> None:
        """Test that render_all creates output directory if it doesn't exist."""
        output_dir = tmp_path / "new" / "output"

        files = render_all(
            "base",
            output_dir,
            project_name="Test",
            file_structure="test/",
            test_coverage_requirement=80,
            test_command_all="pytest",
            test_command_specific="pytest test.py",
            test_command_coverage="pytest --cov",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={},
            dependencies=[],
            install_command="pip install",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check",
            type_check_command="mypy",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
            goal="Test",
            target_users="Users",
            timeline="1 week",
            phases=[],
            current_phase=0,
            next_subtask="0.1.1",
        )

        assert output_dir.exists()
        assert output_dir.is_dir()
        assert files["claude_md"].exists()
        assert files["plan_md"].exists()
        assert files["agent_md"].exists()

    def test_render_all_with_invalid_template(self, tmp_path: Path) -> None:
        """Test that render_all raises error with invalid template."""
        output_dir = tmp_path / "output"

        with pytest.raises(FileNotFoundError, match="Template.*not found"):
            render_all(
                "nonexistent",
                output_dir,
                project_name="Test",
            )

    def test_render_all_returns_correct_paths(self, tmp_path: Path) -> None:
        """Test that render_all returns correct file paths."""
        output_dir = tmp_path / "my_project"

        files = render_all(
            "base",
            output_dir,
            project_name="Test",
            file_structure="test/",
            test_coverage_requirement=80,
            test_command_all="pytest",
            test_command_specific="pytest test.py",
            test_command_coverage="pytest --cov",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={},
            dependencies=[],
            install_command="pip install",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check",
            type_check_command="mypy",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
            goal="Test",
            target_users="Users",
            timeline="1 week",
            phases=[],
            current_phase=0,
            next_subtask="0.1.1",
        )

        assert files["claude_md"] == output_dir / "claude.md"
        assert files["plan_md"] == output_dir / "DEVELOPMENT_PLAN.md"
        assert files["agent_md"] == output_dir / ".claude" / "agents" / "test-executor.md"

    def test_render_all_content_validation(self, tmp_path: Path) -> None:
        """Test that render_all produces files with correct content."""
        output_dir = tmp_path / "validation"

        files = render_all(
            "base",
            output_dir,
            project_name="Validation Test",
            file_structure="validation/\n├── src/\n└── tests/",
            test_coverage_requirement=85,
            test_command_all="pytest tests/ -v",
            test_command_specific="pytest tests/test.py -v",
            test_command_coverage="pytest --cov=src",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={"Language": "Python 3.12+", "Testing": "pytest"},
            dependencies=["pytest==8.0.0"],
            install_command="pip install -e .",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check src",
            type_check_command="mypy src",
            build_command="python -m build",
            has_cli=True,
            cli_command="my-cli",
            custom_rules=[],
            version="2.0",
            last_updated="2024-10-10",
            goal="Test validation",
            target_users="QA Engineers",
            timeline="3 weeks",
            tech_stack_plan={"Language": "Python 3.12+"},
            phases=[
                {
                    "id": 0,
                    "title": "Setup",
                    "timeline": "Week 1",
                    "goal": "Initialize",
                    "tasks": [
                        {
                            "id": "0.1",
                            "title": "Init",
                            "subtasks": [
                                {
                                    "id": "0.1.1",
                                    "title": "Repository (Single Session)",
                                    "status": "pending",
                                    "prerequisites": [],
                                    "deliverables": ["Create .gitignore"],
                                    "success_criteria": ["Git initialized"],
                                }
                            ],
                        }
                    ],
                }
            ],
            current_phase=0,
            next_subtask="0.1.1",
        )

        # Validate claude.md content
        claude_content = files["claude_md"].read_text(encoding="utf-8")
        assert "Validation Test" in claude_content
        assert "Python 3.12+" in claude_content
        assert "pytest==8.0.0" in claude_content
        assert "### 9. CLI Design Standards" in claude_content  # Has CLI

        # Validate plan.md content
        plan_content = files["plan_md"].read_text(encoding="utf-8")
        assert "Validation Test" in plan_content
        assert "QA Engineers" in plan_content
        assert "3 weeks" in plan_content
        assert "## Phase 0: Setup" in plan_content

    def test_render_plan_with_empty_task_lists(self, tmp_path: Path) -> None:
        """Test rendering plan with phases that have empty task lists.

        This tests the "minimal generator" pattern where phases are created
        but tasks/subtasks are left empty to be populated by Claude Code.
        """
        output_path = tmp_path / "DEVELOPMENT_PLAN.md"

        render_plan_md(
            "base",
            output_path,
            project_name="Minimal Plan",
            goal="Test minimal plan generation",
            target_users="Developers",
            timeline="2 weeks",
            tech_stack={"Language": "Python 3.11+"},
            key_features=["User auth", "Data storage", "API endpoints"],
            phases=[
                {
                    "id": "0",
                    "title": "Foundation",
                    "goal": "Setup project infrastructure",
                    "description": "Initialize repository and development environment",
                    "tasks": [],  # Empty task list - to be populated by Claude Code
                },
                {
                    "id": "1",
                    "title": "Core Features",
                    "goal": "Implement main functionality",
                    "description": "Build core features",
                    "tasks": [],  # Empty task list
                },
            ],
        )

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")

        # Verify phase headers exist
        assert "## Phase 0: Foundation" in content
        assert "## Phase 1: Core Features" in content

        # Verify phase goals exist
        assert "Setup project infrastructure" in content
        assert "Implement main functionality" in content

        # Verify instructional message for empty phases
        assert "Tasks and subtasks for this phase will be populated" in content
        assert "Claude Code" in content
        assert "User auth, Data storage, API endpoints" in content

        # Verify no task/subtask structure appears (since lists are empty)
        assert "### Task" not in content
        assert "**Subtask" not in content


class TestRenderAgentMd:
    """Test render_agent_md function."""

    def test_render_with_minimal_data(self, tmp_path: Path) -> None:
        """Test rendering agent.md with minimal required data."""
        output_path = tmp_path / ".claude" / "agents" / "test-project-executor.md"

        render_agent_md(
            "base",
            output_path,
            project_name="Test Project",
            project_name_slug="test-project",
            goal="Build a test application",
            tech_stack={"Language": "Python 3.11+", "Testing": "pytest"},
            file_structure="test/\n├── src/\n└── tests/",
            phases=[
                {"id": "0", "title": "Foundation"},
                {"id": "1", "title": "Core Features"},
            ],
        )

        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")

        # Check YAML frontmatter
        assert "---" in content
        assert "name: test-project-executor" in content
        assert "tools: Read, Write, Edit, Bash, Glob, Grep" in content
        assert "model: haiku" in content

        # Check project context
        assert "# Test Project Development Plan Executor" in content
        assert "Build a test application" in content

        # Check tech stack table
        assert "| Language | Python 3.11+ |" in content

        # Check phases
        assert "| 0 | Foundation |" in content
        assert "| 1 | Core Features |" in content

    def test_render_creates_parent_directories(self, tmp_path: Path) -> None:
        """Test that render_agent_md creates parent directories."""
        output_path = tmp_path / ".claude" / "agents" / "test-executor.md"

        render_agent_md(
            "base",
            output_path,
            project_name="Test",
            project_name_slug="test",
            tech_stack={},
            file_structure="",
            phases=[],
        )

        assert output_path.exists()
        assert output_path.parent.exists()
        assert output_path.parent.name == "agents"

    def test_render_with_invalid_template(self, tmp_path: Path) -> None:
        """Test that render_agent_md raises error with invalid template."""
        output_path = tmp_path / "agent.md"

        with pytest.raises(FileNotFoundError, match="Template.*not found"):
            render_agent_md(
                "nonexistent",
                output_path,
                project_name="Test",
            )

    def test_render_with_custom_model(self, tmp_path: Path) -> None:
        """Test rendering agent with custom model."""
        output_path = tmp_path / "agent.md"

        render_agent_md(
            "base",
            output_path,
            project_name="Test",
            project_name_slug="test",
            agent_model="opus",
            tech_stack={},
            file_structure="",
            phases=[],
        )

        content = output_path.read_text(encoding="utf-8")
        assert "model: opus" in content

    def test_render_with_key_features(self, tmp_path: Path) -> None:
        """Test rendering agent with key features list."""
        output_path = tmp_path / "agent.md"

        render_agent_md(
            "base",
            output_path,
            project_name="Feature App",
            project_name_slug="feature-app",
            goal="Do cool things",
            key_features=["User auth", "Data export", "Reports"],
            tech_stack={"Language": "Python"},
            file_structure="src/",
            phases=[],
        )

        content = output_path.read_text(encoding="utf-8")
        assert "**Key Features:**" in content
        assert "- User auth" in content
        assert "- Data export" in content
        assert "- Reports" in content

    def test_render_cli_template(self, tmp_path: Path) -> None:
        """Test rendering CLI-specific agent template."""
        output_path = tmp_path / "cli-app-executor.md"

        render_agent_md(
            "cli",
            output_path,
            project_name="CLI App",
            project_name_slug="cli-app",
            goal="A command-line tool",
            tech_stack={"Language": "Python 3.11+", "Framework": "Click"},
            file_structure="src/cli_app/",
            phases=[{"id": "0", "title": "Foundation"}],
        )

        content = output_path.read_text(encoding="utf-8")
        assert "name: cli-app-executor" in content
        assert "CLI-SPECIFIC PATTERNS" in content
        assert "Click Command Pattern" in content
        assert "CliRunner" in content

    def test_render_api_template(self, tmp_path: Path) -> None:
        """Test rendering API-specific agent template."""
        output_path = tmp_path / "api-service-executor.md"

        render_agent_md(
            "api",
            output_path,
            project_name="API Service",
            project_name_slug="api-service",
            goal="A REST API service",
            tech_stack={"Language": "Python 3.11+", "Framework": "FastAPI"},
            file_structure="src/api_service/",
            phases=[{"id": "0", "title": "Foundation"}],
        )

        content = output_path.read_text(encoding="utf-8")
        assert "name: api-service-executor" in content
        assert "API-SPECIFIC PATTERNS" in content
        assert "FastAPI Router Pattern" in content
        assert "Pydantic Schema Pattern" in content

    def test_render_webapp_template(self, tmp_path: Path) -> None:
        """Test rendering web app-specific agent template."""
        output_path = tmp_path / "web-app-executor.md"

        render_agent_md(
            "web-app",
            output_path,
            project_name="Web App",
            project_name_slug="web-app",
            goal="A web application",
            tech_stack={"Frontend": "React", "Backend": "FastAPI"},
            file_structure="src/",
            phases=[{"id": "0", "title": "Foundation"}],
        )

        content = output_path.read_text(encoding="utf-8")
        assert "name: web-app-executor" in content
        assert "WEB APP-SPECIFIC PATTERNS" in content
        assert "React Component Pattern" in content
        assert "React Hook Pattern" in content


class TestRenderAllWithAgent:
    """Test render_all function including agent generation."""

    def test_render_all_creates_agent_file(self, tmp_path: Path) -> None:
        """Test that render_all creates the agent file in addition to other files."""
        output_dir = tmp_path / "output"

        files = render_all(
            "base",
            output_dir,
            project_name="Test Project",
            file_structure="test/",
            test_coverage_requirement=80,
            test_command_all="pytest",
            test_command_specific="pytest test.py",
            test_command_coverage="pytest --cov",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={"Language": "Python 3.11+"},
            dependencies=[],
            install_command="pip install",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check",
            type_check_command="mypy",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
            goal="Build app",
            target_users="Users",
            timeline="2 weeks",
            phases=[],
            current_phase=0,
            next_subtask="0.1.1",
        )

        # Check all three files are returned
        assert "claude_md" in files
        assert "plan_md" in files
        assert "agent_md" in files

        # Check agent file exists
        assert files["agent_md"].exists()
        assert files["agent_md"].name == "test-project-executor.md"
        assert ".claude/agents" in str(files["agent_md"])

    def test_render_all_agent_path_correct(self, tmp_path: Path) -> None:
        """Test that agent file is in correct directory structure."""
        output_dir = tmp_path / "my_project"

        files = render_all(
            "base",
            output_dir,
            project_name="My Cool Project",
            file_structure="test/",
            test_coverage_requirement=80,
            test_command_all="pytest",
            test_command_specific="pytest test.py",
            test_command_coverage="pytest --cov",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={},
            dependencies=[],
            install_command="pip install",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check",
            type_check_command="mypy",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
            goal="Test",
            target_users="Users",
            timeline="1 week",
            phases=[],
            current_phase=0,
            next_subtask="0.1.1",
        )

        expected_path = output_dir / ".claude" / "agents" / "my-cool-project-executor.md"
        assert files["agent_md"] == expected_path
        assert expected_path.exists()

    def test_render_all_agent_content_has_project_info(self, tmp_path: Path) -> None:
        """Test that rendered agent has correct project information."""
        output_dir = tmp_path / "content_test"

        files = render_all(
            "base",
            output_dir,
            project_name="Content Test App",
            file_structure="src/content_test/\n├── __init__.py\n└── main.py",
            test_coverage_requirement=85,
            test_command_all="pytest tests/ -v",
            test_command_specific="pytest tests/test.py -v",
            test_command_coverage="pytest --cov=src",
            linter="ruff",
            type_checker="mypy",
            commit_type="feat",
            tech_stack={"Language": "Python 3.12+", "Testing": "pytest"},
            dependencies=["pytest"],
            install_command="pip install -e .",
            docstring_style="Google",
            max_line_length=100,
            lint_command="ruff check src",
            type_check_command="mypy src",
            build_command="python -m build",
            has_cli=False,
            custom_rules=[],
            version="1.0",
            last_updated="2024-10-10",
            goal="Test content rendering",
            key_features=["Feature A", "Feature B"],
            target_users="Developers",
            timeline="3 weeks",
            phases=[
                {"id": "0", "title": "Foundation"},
                {"id": "1", "title": "Implementation"},
            ],
            current_phase=0,
            next_subtask="0.1.1",
        )

        agent_content = files["agent_md"].read_text(encoding="utf-8")

        # Check YAML frontmatter
        assert "name: content-test-app-executor" in agent_content
        assert "model: haiku" in agent_content

        # Check project name and goal
        assert "Content Test App" in agent_content
        assert "Test content rendering" in agent_content

        # Check tech stack
        assert "| Language | Python 3.12+ |" in agent_content

        # Check key features
        assert "Feature A" in agent_content
        assert "Feature B" in agent_content

        # Check phases
        assert "| 0 | Foundation |" in agent_content
        assert "| 1 | Implementation |" in agent_content

        # Check file structure
        assert "src/content_test/" in agent_content

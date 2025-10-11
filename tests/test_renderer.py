"""Tests for template renderer module.

This module tests the template rendering engine that generates
claude.md and DEVELOPMENT_PLAN.md files from Jinja2 templates.
"""

from pathlib import Path

import pytest

from claude_planner.generator.renderer import (
    _create_jinja_env,
    _get_templates_dir,
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

    def test_render_all_creates_both_files(self, tmp_path: Path) -> None:
        """Test that render_all creates both claude.md and DEVELOPMENT_PLAN.md."""
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
        assert files["claude_md"].exists()
        assert files["plan_md"].exists()
        assert files["claude_md"].name == "claude.md"
        assert files["plan_md"].name == "DEVELOPMENT_PLAN.md"

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

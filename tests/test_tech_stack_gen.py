"""Tests for tech_stack_gen module."""

import pytest

from claude_planner.generator.tech_stack_gen import generate_tech_stack
from claude_planner.models import ProjectBrief


class TestGenerateTechStack:
    """Test suite for generate_tech_stack function."""

    def test_basic_api_project_uses_template_defaults(self):
        """Test that API projects use template defaults."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build REST API",
            target_users="Developers",
            timeline="2 weeks",
        )

        stack = generate_tech_stack(brief)

        # Should use API template defaults
        assert stack.framework == "FastAPI"
        assert stack.database == "PostgreSQL"
        assert stack.additional_tools.get("cache") == "Redis"
        assert stack.deployment == "Docker + AWS"

    def test_basic_cli_project_uses_template_defaults(self):
        """Test that CLI projects use template defaults."""
        brief = ProjectBrief(
            project_name="My CLI Tool",
            project_type="CLI",
            primary_goal="Build command-line tool",
            target_users="Developers",
            timeline="1 week",
        )

        stack = generate_tech_stack(brief)

        # Should use CLI template defaults
        assert stack.framework == "Click"
        assert stack.language == "Python 3.11+"
        assert stack.deployment == "PyPI"
        assert stack.additional_tools.get("packaging") == "setuptools"

    def test_must_use_items_added_to_additional_tools(self):
        """Test that must_use items are passed through to additional_tools."""
        brief = ProjectBrief(
            project_name="Custom API",
            project_type="API",
            primary_goal="Build API with specific tools",
            target_users="Developers",
            timeline="2 weeks",
            must_use_tech=["Django", "MongoDB", "Celery"],
        )

        stack = generate_tech_stack(brief)

        # Must_use items should be in additional_tools
        assert "Django" in stack.additional_tools.values()
        assert "MongoDB" in stack.additional_tools.values()
        assert "Celery" in stack.additional_tools.values()

    def test_cannot_use_blocks_framework_default(self):
        """Test that cannot_use blocks template framework default."""
        brief = ProjectBrief(
            project_name="No FastAPI",
            project_type="API",
            primary_goal="Build API without FastAPI",
            target_users="Developers",
            timeline="2 weeks",
            cannot_use_tech=["FastAPI"],
        )

        stack = generate_tech_stack(brief)

        # FastAPI should be blocked even though it's the API template default
        assert stack.framework != "FastAPI"
        assert stack.framework == ""

    def test_cannot_use_blocks_database_default(self):
        """Test that cannot_use blocks template database default."""
        brief = ProjectBrief(
            project_name="No PostgreSQL",
            project_type="API",
            primary_goal="Build API without PostgreSQL",
            target_users="Developers",
            timeline="2 weeks",
            cannot_use_tech=["PostgreSQL"],
        )

        stack = generate_tech_stack(brief)

        assert stack.database != "PostgreSQL"
        assert stack.database == ""

    def test_cannot_use_blocks_cache(self):
        """Test that cannot_use blocks cache from template."""
        brief = ProjectBrief(
            project_name="No Redis",
            project_type="API",
            primary_goal="Build API without Redis",
            target_users="Developers",
            timeline="2 weeks",
            cannot_use_tech=["Redis"],
        )

        stack = generate_tech_stack(brief)

        # Redis should not be in additional_tools
        assert "Redis" not in stack.additional_tools.values()
        assert stack.additional_tools.get("cache") != "Redis"

    def test_cannot_use_blocks_deployment_with_substring(self):
        """Test that cannot_use blocks deployment if constraint is substring."""
        brief = ProjectBrief(
            project_name="No Docker",
            project_type="API",
            primary_goal="Build API without Docker",
            target_users="Developers",
            timeline="2 weeks",
            cannot_use_tech=["Docker"],
        )

        stack = generate_tech_stack(brief)

        # "Docker + AWS" should be blocked by "Docker" constraint
        assert stack.deployment != "Docker + AWS"
        assert stack.deployment == ""

    def test_cannot_use_blocks_packaging(self):
        """Test that cannot_use blocks packaging from template."""
        brief = ProjectBrief(
            project_name="No Setuptools",
            project_type="CLI",
            primary_goal="Build CLI without setuptools",
            target_users="Developers",
            timeline="1 week",
            cannot_use_tech=["setuptools"],
        )

        stack = generate_tech_stack(brief)

        assert stack.additional_tools.get("packaging") != "setuptools"

    def test_conflicting_constraints_raises_error(self):
        """Test that conflicting must_use and cannot_use raises ValueError."""
        brief = ProjectBrief(
            project_name="Conflicting",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            must_use_tech=["FastAPI"],
            cannot_use_tech=["FastAPI"],
        )

        with pytest.raises(ValueError, match="Conflicting constraints"):
            generate_tech_stack(brief)

    def test_conflicting_constraints_case_insensitive(self):
        """Test that constraint conflict detection is case-insensitive."""
        brief = ProjectBrief(
            project_name="Conflicting",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            must_use_tech=["FastAPI"],
            cannot_use_tech=["fastapi"],
        )

        with pytest.raises(ValueError, match="Conflicting constraints"):
            generate_tech_stack(brief)

    def test_common_defaults_for_python(self):
        """Test that common defaults are applied for Python projects."""
        brief = ProjectBrief(
            project_name="Python Project",
            project_type="API",
            primary_goal="Build Python project",
            target_users="Developers",
            timeline="2 weeks",
            cannot_use_tech=["FastAPI", "PostgreSQL"],  # Block template defaults
        )

        stack = generate_tech_stack(brief)

        # Should apply common Python defaults
        assert stack.language == "Python 3.11+"
        assert stack.testing == "pytest"
        assert stack.linting == "ruff"
        assert stack.type_checking == "mypy"

    def test_common_default_ci_cd(self):
        """Test that GitHub Actions is default CI/CD."""
        brief = ProjectBrief(
            project_name="Project",
            project_type="API",
            primary_goal="Build project",
            target_users="Developers",
            timeline="2 weeks",
        )

        stack = generate_tech_stack(brief)

        assert stack.ci_cd == "GitHub Actions"

    def test_empty_must_use_tech(self):
        """Test that empty must_use_tech works correctly."""
        brief = ProjectBrief(
            project_name="Default Project",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            must_use_tech=[],
        )

        stack = generate_tech_stack(brief)

        # Should use template defaults
        assert stack.framework == "FastAPI"
        assert stack.database == "PostgreSQL"

    def test_empty_cannot_use_tech(self):
        """Test that empty cannot_use_tech works correctly."""
        brief = ProjectBrief(
            project_name="Default Project",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            cannot_use_tech=[],
        )

        stack = generate_tech_stack(brief)

        # Should use template defaults without blocking
        assert stack.framework == "FastAPI"
        assert stack.database == "PostgreSQL"

    def test_must_use_and_template_defaults_coexist(self):
        """Test that must_use items and template defaults can coexist."""
        brief = ProjectBrief(
            project_name="Mixed Project",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            must_use_tech=["Celery", "RabbitMQ"],
        )

        stack = generate_tech_stack(brief)

        # Template defaults should still apply
        assert stack.framework == "FastAPI"
        assert stack.database == "PostgreSQL"

        # Must_use items should be in additional_tools
        assert "Celery" in stack.additional_tools.values()
        assert "RabbitMQ" in stack.additional_tools.values()

    def test_case_insensitive_cannot_use_blocking(self):
        """Test that cannot_use blocking is case-insensitive."""
        brief = ProjectBrief(
            project_name="Case Test",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            cannot_use_tech=["fastapi"],  # lowercase
        )

        stack = generate_tech_stack(brief)

        # Should block "FastAPI" (title case) from template
        assert stack.framework != "FastAPI"

    def test_multiple_must_use_items(self):
        """Test multiple must_use items are all added."""
        brief = ProjectBrief(
            project_name="Multi Tool",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            must_use_tech=["Tool1", "Tool2", "Tool3", "Tool4"],
        )

        stack = generate_tech_stack(brief)

        # All must_use items should be present
        assert "Tool1" in stack.additional_tools.values()
        assert "Tool2" in stack.additional_tools.values()
        assert "Tool3" in stack.additional_tools.values()
        assert "Tool4" in stack.additional_tools.values()

    def test_language_fallback_when_no_template_default(self):
        """Test that Python 3.11+ is used when no language in template."""
        brief = ProjectBrief(
            project_name="Web App",
            project_type="Web App",
            primary_goal="Build web app",
            target_users="Users",
            timeline="3 weeks",
        )

        stack = generate_tech_stack(brief)

        # Web-app template doesn't have language, should use fallback
        assert stack.language == "Python 3.11+"

    def test_all_tech_stack_fields_populated(self):
        """Test that all TechStack fields are populated (no None values)."""
        brief = ProjectBrief(
            project_name="Complete Project",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        stack = generate_tech_stack(brief)

        # All fields should have values (string or dict, not None)
        assert isinstance(stack.language, str)
        assert isinstance(stack.framework, str)
        assert isinstance(stack.database, str)
        assert isinstance(stack.testing, str)
        assert isinstance(stack.linting, str)
        assert isinstance(stack.type_checking, str)
        assert isinstance(stack.deployment, str)
        assert isinstance(stack.ci_cd, str)
        assert isinstance(stack.additional_tools, dict)

    def test_testing_defaults_based_on_language_python(self):
        """Test that testing defaults are set based on Python language."""
        brief = ProjectBrief(
            project_name="Python Project",
            project_type="API",
            primary_goal="Build project",
            target_users="Developers",
            timeline="2 weeks",
            cannot_use_tech=["FastAPI", "PostgreSQL"],
        )

        stack = generate_tech_stack(brief)

        assert "python" in stack.language.lower()
        assert stack.testing == "pytest"
        assert stack.linting == "ruff"
        assert stack.type_checking == "mypy"

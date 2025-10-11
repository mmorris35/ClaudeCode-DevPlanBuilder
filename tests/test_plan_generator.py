"""Integration tests for plan_generator module."""

import pytest

from claude_planner.generator.plan_generator import generate_plan
from claude_planner.models import DevelopmentPlan, ProjectBrief


class TestGeneratePlan:
    """Test suite for generate_plan integration function."""

    def test_generates_complete_plan(self):
        """Test that generate_plan returns a complete DevelopmentPlan."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build REST API",
            target_users="Developers",
            timeline="2 weeks",
        )

        plan = generate_plan(brief)

        assert isinstance(plan, DevelopmentPlan)
        assert plan.project_name == "My API"
        assert plan.tech_stack is not None
        assert len(plan.phases) > 0

    def test_api_project_structure(self):
        """Test API project generates expected structure."""
        brief = ProjectBrief(
            project_name="Task API",
            project_type="API",
            primary_goal="Build task management API",
            target_users="Developers",
            timeline="3 weeks",
        )

        plan = generate_plan(brief)

        assert plan.project_name == "Task API"
        # API template should have multiple phases
        assert len(plan.phases) >= 3
        # Phase 0 should be Foundation
        assert plan.phases[0].id == "0"
        assert "Foundation" in plan.phases[0].title

    def test_cli_project_structure(self):
        """Test CLI project generates expected structure."""
        brief = ProjectBrief(
            project_name="My CLI Tool",
            project_type="CLI",
            primary_goal="Build command-line tool",
            target_users="Developers",
            timeline="1 week",
        )

        plan = generate_plan(brief)

        assert plan.project_name == "My CLI Tool"
        assert len(plan.phases) > 0
        assert plan.phases[0].title == "Foundation"

    def test_web_app_project_structure(self):
        """Test Web App project generates expected structure."""
        brief = ProjectBrief(
            project_name="My Web App",
            project_type="Web App",
            primary_goal="Build web application",
            target_users="End users",
            timeline="4 weeks",
        )

        plan = generate_plan(brief)

        assert plan.project_name == "My Web App"
        assert len(plan.phases) > 0
        assert plan.phases[0].title == "Foundation"

    def test_tech_stack_integration(self):
        """Test that tech stack is properly integrated."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        plan = generate_plan(brief)

        assert plan.tech_stack is not None
        # API template defaults
        assert plan.tech_stack.framework == "FastAPI"
        assert plan.tech_stack.database == "PostgreSQL"

    def test_phases_integration(self):
        """Test that phases are properly integrated."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        plan = generate_plan(brief)

        # Should have phases from template
        assert len(plan.phases) > 0
        # Phases should have sequential IDs
        for i, phase in enumerate(plan.phases):
            assert phase.id == str(i)

    def test_minimal_brief(self):
        """Test with minimal brief."""
        brief = ProjectBrief(
            project_name="Minimal",
            project_type="API",
            primary_goal="Build",
            target_users="Users",
            timeline="1 week",
        )

        plan = generate_plan(brief)

        assert plan.project_name == "Minimal"
        assert plan.tech_stack is not None
        assert len(plan.phases) > 0

    def test_brief_with_constraints(self):
        """Test brief with must_use and cannot_use constraints."""
        brief = ProjectBrief(
            project_name="Custom API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            must_use_tech=["Django", "MySQL"],
            cannot_use_tech=["PostgreSQL"],
        )

        plan = generate_plan(brief)

        # must_use items should be in additional_tools
        assert "Django" in plan.tech_stack.additional_tools.values()
        assert "MySQL" in plan.tech_stack.additional_tools.values()
        # cannot_use should block template defaults
        assert plan.tech_stack.database != "PostgreSQL"

    def test_brief_with_features(self):
        """Test brief with key_features."""
        brief = ProjectBrief(
            project_name="Feature API",
            project_type="API",
            primary_goal="Build API with features",
            target_users="Developers",
            timeline="3 weeks",
            key_features=["User authentication", "Payment processing", "Email notifications"],
        )

        plan = generate_plan(brief)

        # Plan should be generated regardless of features
        assert plan.project_name == "Feature API"
        assert len(plan.phases) > 0

    def test_foundation_phase_always_first(self):
        """Test that Foundation is always Phase 0."""
        brief = ProjectBrief(
            project_name="My Project",
            project_type="API",
            primary_goal="Build",
            target_users="Users",
            timeline="2 weeks",
        )

        plan = generate_plan(brief)

        assert plan.phases[0].id == "0"
        assert plan.phases[0].title == "Foundation"

    def test_plan_validation_no_project_name(self):
        """Test that validation fails without project name."""
        brief = ProjectBrief(
            project_name="",
            project_type="API",
            primary_goal="Build",
            target_users="Users",
            timeline="1 week",
        )

        with pytest.raises(ValueError, match="Project name is required"):
            generate_plan(brief)

    def test_different_project_types_different_phases(self):
        """Test that different project types get different phase counts."""
        api_brief = ProjectBrief(
            project_name="API",
            project_type="API",
            primary_goal="Build",
            target_users="Users",
            timeline="2 weeks",
        )

        cli_brief = ProjectBrief(
            project_name="CLI",
            project_type="CLI",
            primary_goal="Build",
            target_users="Users",
            timeline="1 week",
        )

        api_plan = generate_plan(api_brief)
        cli_plan = generate_plan(cli_brief)

        # Different templates have different phase counts
        assert len(api_plan.phases) != len(cli_plan.phases)

    def test_complete_integration_api_project(self):
        """Test complete integration with realistic API project."""
        brief = ProjectBrief(
            project_name="TaskMaster API",
            project_type="API",
            primary_goal="Build task management REST API",
            target_users="Mobile and web developers",
            timeline="4 weeks",
            key_features=[
                "User authentication and authorization",
                "CRUD operations for tasks",
                "Task filtering and search",
                "Real-time updates",
            ],
            must_use_tech=["Python", "PostgreSQL"],
            deployment_target="AWS",
        )

        plan = generate_plan(brief)

        # Verify complete plan structure
        assert plan.project_name == "TaskMaster API"
        assert plan.tech_stack is not None
        assert len(plan.phases) > 0

        # Verify tech stack has constraints applied
        assert "Python" in plan.tech_stack.additional_tools.values()
        assert "PostgreSQL" in plan.tech_stack.additional_tools.values()

        # Verify phases
        assert plan.phases[0].title == "Foundation"
        phase_titles = [p.title for p in plan.phases]
        assert "Foundation" in phase_titles

    def test_complete_integration_cli_project(self):
        """Test complete integration with realistic CLI project."""
        brief = ProjectBrief(
            project_name="DevTools CLI",
            project_type="CLI",
            primary_goal="Build developer productivity CLI tool",
            target_users="Software developers",
            timeline="2 weeks",
            key_features=[
                "Project scaffolding",
                "Code generation",
                "Configuration management",
            ],
            must_use_tech=["Python", "Click"],
        )

        plan = generate_plan(brief)

        assert plan.project_name == "DevTools CLI"
        assert plan.tech_stack is not None
        assert len(plan.phases) > 0
        assert plan.phases[0].title == "Foundation"

    def test_plan_has_tech_stack_fields_populated(self):
        """Test that tech stack has all fields populated."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        plan = generate_plan(brief)

        # Tech stack should have fields populated
        assert plan.tech_stack.language != ""
        assert plan.tech_stack.testing != ""
        assert plan.tech_stack.linting != ""
        assert plan.tech_stack.ci_cd != ""

    def test_phase_ids_are_sequential(self):
        """Test that phase IDs are sequential."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        plan = generate_plan(brief)

        for i, phase in enumerate(plan.phases):
            assert phase.id == str(i)

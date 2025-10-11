"""Tests for phase_gen module."""

from claude_planner.generator.phase_gen import generate_phases
from claude_planner.models import ProjectBrief


class TestGeneratePhases:
    """Test suite for generate_phases function."""

    def test_api_project_generates_default_phases(self):
        """Test that API projects get default API phases."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build REST API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        # Check we got phases
        assert len(phases) > 0

        # Check phase titles match API template defaults
        phase_titles = [p.title for p in phases]
        assert "Foundation" in phase_titles
        assert "Data Models" in phase_titles
        assert "API Endpoints" in phase_titles
        assert "Authentication" in phase_titles

    def test_cli_project_generates_default_phases(self):
        """Test that CLI projects get default CLI phases."""
        brief = ProjectBrief(
            project_name="My CLI Tool",
            project_type="CLI",
            primary_goal="Build command-line tool",
            target_users="Developers",
            timeline="1 week",
        )

        phases = generate_phases(brief)

        assert len(phases) > 0
        phase_titles = [p.title for p in phases]
        assert "Foundation" in phase_titles

    def test_web_app_project_generates_default_phases(self):
        """Test that Web App projects get default web phases."""
        brief = ProjectBrief(
            project_name="My Web App",
            project_type="Web App",
            primary_goal="Build web application",
            target_users="Users",
            timeline="4 weeks",
        )

        phases = generate_phases(brief)

        assert len(phases) > 0
        phase_titles = [p.title for p in phases]
        assert "Foundation" in phase_titles

    def test_foundation_is_always_phase_zero(self):
        """Test that Foundation is always Phase 0."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        assert phases[0].id == "0"
        assert phases[0].title == "Foundation"

    def test_phases_have_sequential_ids(self):
        """Test that phase IDs are sequential starting from 0."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        for i, phase in enumerate(phases):
            assert phase.id == str(i)

    def test_all_phases_have_required_fields(self):
        """Test that all generated phases have required fields."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        for phase in phases:
            assert phase.id is not None
            assert phase.title is not None
            assert phase.goal is not None
            assert isinstance(phase.days, str)
            assert isinstance(phase.description, str)
            assert isinstance(phase.tasks, list)

    def test_phases_have_empty_task_lists(self):
        """Test that generated phases start with empty task lists."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        for phase in phases:
            assert phase.tasks == []

    def test_phase_goals_are_derived_from_title(self):
        """Test that phase goals are automatically derived from titles."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        for phase in phases:
            # Goal should mention the phase title
            assert phase.title.lower() in phase.goal.lower()

    def test_api_project_specific_phases(self):
        """Test that API projects have API-specific phases."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)
        phase_titles = [p.title for p in phases]

        # API template should have these phases
        expected_phases = [
            "Foundation",
            "Data Models",
            "API Endpoints",
            "Authentication",
            "Validation & Error Handling",
            "Documentation",
            "Testing",
            "Deployment",
        ]

        for expected in expected_phases:
            assert expected in phase_titles, f"Missing phase: {expected}"

    def test_cli_project_specific_phases(self):
        """Test that CLI projects have CLI-specific phases."""
        brief = ProjectBrief(
            project_name="My CLI",
            project_type="CLI",
            primary_goal="Build CLI",
            target_users="Developers",
            timeline="1 week",
        )

        phases = generate_phases(brief)
        phase_titles = [p.title for p in phases]

        # CLI template should have Foundation plus CLI-specific phases
        assert "Foundation" in phase_titles

    def test_phases_return_type(self):
        """Test that generate_phases returns a list of Phase objects."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        assert isinstance(phases, list)
        assert len(phases) > 0

        from claude_planner.models import Phase

        for phase in phases:
            assert isinstance(phase, Phase)

    def test_minimal_brief_generates_phases(self):
        """Test that minimal brief still generates phases."""
        brief = ProjectBrief(
            project_name="Minimal",
            project_type="API",
            primary_goal="Build",
            target_users="Users",
            timeline="1 week",
        )

        phases = generate_phases(brief)

        assert len(phases) > 0
        assert phases[0].title == "Foundation"

    def test_different_project_types_generate_different_phases(self):
        """Test that different project types get different phase lists."""
        api_brief = ProjectBrief(
            project_name="API",
            project_type="API",
            primary_goal="Build",
            target_users="Devs",
            timeline="2 weeks",
        )

        cli_brief = ProjectBrief(
            project_name="CLI",
            project_type="CLI",
            primary_goal="Build",
            target_users="Devs",
            timeline="1 week",
        )

        api_phases = generate_phases(api_brief)
        cli_phases = generate_phases(cli_brief)

        # Different templates should produce different phase counts/names
        api_titles = [p.title for p in api_phases]
        cli_titles = [p.title for p in cli_phases]

        # Both should have Foundation
        assert "Foundation" in api_titles
        assert "Foundation" in cli_titles

        # But should have different phase counts (API has more phases)
        assert len(api_phases) != len(cli_phases)

    def test_phase_days_field_empty(self):
        """Test that days field is empty (for Claude to determine)."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        for phase in phases:
            assert phase.days == ""

    def test_phase_description_field_empty(self):
        """Test that description field is empty (for Claude to populate)."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        for phase in phases:
            assert phase.description == ""

    def test_case_insensitive_project_type(self):
        """Test that project type matching is case-insensitive."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="api",  # lowercase
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        assert len(phases) > 0
        assert phases[0].title == "Foundation"

    def test_rest_api_project_type_alias(self):
        """Test that 'REST API' is recognized as API template."""
        brief = ProjectBrief(
            project_name="My REST API",
            project_type="REST API",
            primary_goal="Build REST API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        phase_titles = [p.title for p in phases]
        # Should get API template phases
        assert "API Endpoints" in phase_titles

    def test_generated_phases_count_matches_template(self):
        """Test that number of phases matches template defaults."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)

        # API template has 8 default phases
        assert len(phases) == 8

    def test_foundation_phase_properties(self):
        """Test that Foundation phase has correct properties."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        phases = generate_phases(brief)
        foundation = phases[0]

        assert foundation.id == "0"
        assert foundation.title == "Foundation"
        assert "foundation" in foundation.goal.lower()
        assert foundation.days == ""
        assert foundation.description == ""
        assert foundation.tasks == []

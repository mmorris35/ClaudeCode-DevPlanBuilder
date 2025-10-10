"""Unit tests for ProjectBrief converter module."""

import pytest

from claude_planner.generator.brief_converter import convert_to_project_brief
from claude_planner.models import ProjectBrief


class TestConvertToProjectBrief:
    """Test cases for convert_to_project_brief function."""

    def test_convert_with_all_required_fields(self) -> None:
        """Test conversion with all required fields present."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Test Project",
            "project_type": ["CLI Tool"],
            "primary_goal": "Build a great tool",
            "target_users": "Developers",
            "timeline": "2 weeks",
            "team_size": "3",
        }
        requirements: dict[str, list[str]] = {
            "input": ["File 1"],
            "output": ["Output 1"],
            "key_features": ["Feature 1", "Feature 2"],
            "nice_to_have": ["Nice 1"],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": ["Python"],
            "cannot_use": ["PHP"],
            "deployment_target": ["Linux"],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {"Speed": "Fast"},
            "security": {"Auth": "Required"},
            "scalability": {"Users": "1000+"},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {"Senior": True},
            "existing_knowledge": ["Python", "Git"],
            "infrastructure": ["AWS"],
        }

        result = convert_to_project_brief(
            basic_info, requirements, tech_constraints, quality_requirements, team_info
        )

        assert isinstance(result, ProjectBrief)
        assert result.project_name == "Test Project"
        assert result.project_type == "CLI Tool"
        assert result.primary_goal == "Build a great tool"
        assert result.target_users == "Developers"
        assert result.timeline == "2 weeks"
        assert result.team_size == "3"
        assert result.key_features == ["Feature 1", "Feature 2"]
        assert result.nice_to_have_features == ["Nice 1"]
        assert result.must_use_tech == ["Python"]
        assert result.cannot_use_tech == ["PHP"]
        assert result.deployment_target == "Linux"
        assert result.performance_requirements == {"Speed": "Fast"}
        assert result.security_requirements == {"Auth": "Required"}
        assert result.scalability_requirements == {"Users": "1000+"}
        assert result.team_composition == "Senior: Yes"
        assert result.existing_knowledge == ["Python", "Git"]
        assert result.infrastructure_access == ["AWS"]

    def test_convert_with_multiple_project_types(self) -> None:
        """Test conversion with multiple project types."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Multi Project",
            "project_type": ["CLI Tool", "Library", "API"],
            "primary_goal": "Build tools",
            "target_users": "Developers",
            "timeline": "1 week",
            "team_size": "1",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": [],
            "infrastructure": [],
        }

        result = convert_to_project_brief(
            basic_info, requirements, tech_constraints, quality_requirements, team_info
        )

        assert result.project_type == "CLI Tool, Library, API"

    def test_convert_with_minimal_fields(self) -> None:
        """Test conversion with only required fields."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Minimal Project",
            "project_type": ["API"],
            "primary_goal": "Simple goal",
            "target_users": "Users",
            "timeline": "1 day",
            "team_size": "",  # Empty, should default to "1"
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": [],
            "infrastructure": [],
        }

        result = convert_to_project_brief(
            basic_info, requirements, tech_constraints, quality_requirements, team_info
        )

        assert result.project_name == "Minimal Project"
        assert result.team_size == "1"  # Should default
        assert result.key_features == []
        assert result.deployment_target is None
        assert result.team_composition is None

    def test_convert_missing_project_name(self) -> None:
        """Test conversion fails when project_name is missing."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "",  # Empty
            "project_type": ["CLI"],
            "primary_goal": "Goal",
            "target_users": "Users",
            "timeline": "1 week",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": [],
            "infrastructure": [],
        }

        with pytest.raises(ValueError) as exc_info:
            convert_to_project_brief(
                basic_info, requirements, tech_constraints, quality_requirements, team_info
            )

        assert "project_name" in str(exc_info.value).lower()

    def test_convert_missing_project_type(self) -> None:
        """Test conversion fails when project_type is missing."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Test",
            "project_type": [],  # Empty list
            "primary_goal": "Goal",
            "target_users": "Users",
            "timeline": "1 week",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": [],
            "infrastructure": [],
        }

        with pytest.raises(ValueError) as exc_info:
            convert_to_project_brief(
                basic_info, requirements, tech_constraints, quality_requirements, team_info
            )

        assert "project_type" in str(exc_info.value).lower()

    def test_convert_missing_primary_goal(self) -> None:
        """Test conversion fails when primary_goal is missing."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Test",
            "project_type": ["CLI"],
            "primary_goal": "",
            "target_users": "Users",
            "timeline": "1 week",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": [],
            "infrastructure": [],
        }

        with pytest.raises(ValueError) as exc_info:
            convert_to_project_brief(
                basic_info, requirements, tech_constraints, quality_requirements, team_info
            )

        assert "primary_goal" in str(exc_info.value).lower()

    def test_convert_missing_target_users(self) -> None:
        """Test conversion fails when target_users is missing."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Test",
            "project_type": ["CLI"],
            "primary_goal": "Goal",
            "target_users": "",
            "timeline": "1 week",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": [],
            "infrastructure": [],
        }

        with pytest.raises(ValueError) as exc_info:
            convert_to_project_brief(
                basic_info, requirements, tech_constraints, quality_requirements, team_info
            )

        assert "target_users" in str(exc_info.value).lower()

    def test_convert_missing_timeline(self) -> None:
        """Test conversion fails when timeline is missing."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Test",
            "project_type": ["CLI"],
            "primary_goal": "Goal",
            "target_users": "Users",
            "timeline": "",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": [],
            "infrastructure": [],
        }

        with pytest.raises(ValueError) as exc_info:
            convert_to_project_brief(
                basic_info, requirements, tech_constraints, quality_requirements, team_info
            )

        assert "timeline" in str(exc_info.value).lower()

    def test_convert_multiple_deployment_targets(self) -> None:
        """Test conversion with multiple deployment targets."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Test",
            "project_type": ["CLI"],
            "primary_goal": "Goal",
            "target_users": "Users",
            "timeline": "1 week",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": ["Linux", "macOS", "Windows"],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": [],
            "infrastructure": [],
        }

        result = convert_to_project_brief(
            basic_info, requirements, tech_constraints, quality_requirements, team_info
        )

        assert result.deployment_target == "Linux, macOS, Windows"

    def test_convert_team_composition_multiple_roles(self) -> None:
        """Test conversion with multiple team composition roles."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Test",
            "project_type": ["CLI"],
            "primary_goal": "Goal",
            "target_users": "Users",
            "timeline": "1 week",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {
                "Senior": True,
                "Junior": False,
                "Mid-level": True,
            },
            "existing_knowledge": [],
            "infrastructure": [],
        }

        result = convert_to_project_brief(
            basic_info, requirements, tech_constraints, quality_requirements, team_info
        )

        # Order might vary, so check all parts are present
        assert result.team_composition is not None
        assert "Senior: Yes" in result.team_composition
        assert "Junior: No" in result.team_composition
        assert "Mid-level: Yes" in result.team_composition

    def test_convert_handles_invalid_team_info_types(self) -> None:
        """Test conversion handles invalid types in team_info gracefully."""
        basic_info: dict[str, str | list[str]] = {
            "project_name": "Test",
            "project_type": ["CLI"],
            "primary_goal": "Goal",
            "target_users": "Users",
            "timeline": "1 week",
        }
        requirements: dict[str, list[str]] = {
            "input": [],
            "output": [],
            "key_features": [],
            "nice_to_have": [],
        }
        tech_constraints: dict[str, list[str]] = {
            "must_use": [],
            "cannot_use": [],
            "deployment_target": [],
        }
        quality_requirements: dict[str, dict[str, str]] = {
            "performance": {},
            "security": {},
            "scalability": {},
        }
        # Pass wrong types for existing_knowledge and infrastructure
        team_info: dict[str, list[str] | dict[str, bool]] = {
            "team_composition": {},
            "existing_knowledge": "Not a list",  # type: ignore
            "infrastructure": "Not a list",  # type: ignore
        }

        result = convert_to_project_brief(
            basic_info, requirements, tech_constraints, quality_requirements, team_info
        )

        # Should default to empty lists when types are wrong
        assert result.existing_knowledge == []
        assert result.infrastructure_access == []

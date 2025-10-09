"""Tests for data models."""

from claude_planner.models import ProjectBrief


class TestProjectBrief:
    """Tests for the ProjectBrief dataclass."""

    def test_create_minimal_brief(self) -> None:
        """Test creating a ProjectBrief with only required fields."""
        brief = ProjectBrief(
            project_name="Test Project",
            project_type="CLI Tool",
            primary_goal="Build a CLI tool",
            target_users="Developers",
            timeline="2 weeks",
        )

        assert brief.project_name == "Test Project"
        assert brief.project_type == "CLI Tool"
        assert brief.primary_goal == "Build a CLI tool"
        assert brief.target_users == "Developers"
        assert brief.timeline == "2 weeks"
        assert brief.team_size == "1"  # Default value

    def test_create_full_brief(self) -> None:
        """Test creating a ProjectBrief with all fields populated."""
        brief = ProjectBrief(
            project_name="Full Project",
            project_type="Web App",
            primary_goal="Build a web application",
            target_users="End users",
            timeline="4 weeks",
            team_size="5",
            key_features=["Feature 1", "Feature 2"],
            nice_to_have_features=["Nice feature 1"],
            must_use_tech=["Python", "React"],
            cannot_use_tech=["PHP"],
            deployment_target="AWS",
            budget_constraints="$10k",
            performance_requirements={"response_time": "<100ms"},
            security_requirements={"authentication": "OAuth2"},
            scalability_requirements={"users": "1000 concurrent"},
            availability_requirements={"uptime": "99.9%"},
            team_composition="2 backend, 2 frontend, 1 designer",
            existing_knowledge=["Python", "JavaScript"],
            learning_budget="1 week",
            infrastructure_access=["AWS", "GitHub"],
            success_criteria=["Launch by deadline", "Pass all tests"],
            external_systems=[{"name": "Payment API", "type": "REST"}],
            data_sources=[{"name": "User DB", "type": "PostgreSQL"}],
            data_destinations=[{"name": "Analytics", "type": "BigQuery"}],
            known_challenges=["Scalability", "Security"],
            reference_materials=["https://docs.example.com"],
            questions_and_clarifications=["Q: Which DB?", "A: PostgreSQL"],
            architecture_vision="Microservices architecture",
            use_cases=["User registration", "Data export"],
            deliverables=["Web app", "API", "Documentation"],
        )

        assert brief.project_name == "Full Project"
        assert len(brief.key_features) == 2
        assert len(brief.must_use_tech) == 2
        assert brief.deployment_target == "AWS"
        assert brief.performance_requirements["response_time"] == "<100ms"
        assert len(brief.success_criteria) == 2

    def test_default_values(self) -> None:
        """Test that default values are properly initialized."""
        brief = ProjectBrief(
            project_name="Test",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="1 week",
        )

        assert brief.key_features == []
        assert brief.nice_to_have_features == []
        assert brief.must_use_tech == []
        assert brief.cannot_use_tech == []
        assert brief.deployment_target is None
        assert brief.budget_constraints is None
        assert brief.performance_requirements == {}
        assert brief.security_requirements == {}
        assert brief.scalability_requirements == {}
        assert brief.availability_requirements == {}
        assert brief.team_composition is None
        assert brief.existing_knowledge == []
        assert brief.learning_budget is None
        assert brief.infrastructure_access == []
        assert brief.success_criteria == []
        assert brief.external_systems == []
        assert brief.data_sources == []
        assert brief.data_destinations == []
        assert brief.known_challenges == []
        assert brief.reference_materials == []
        assert brief.questions_and_clarifications == []
        assert brief.architecture_vision is None
        assert brief.use_cases == []
        assert brief.deliverables == []

    def test_validate_valid_brief(self) -> None:
        """Test that validation passes for a valid brief."""
        brief = ProjectBrief(
            project_name="Valid Project",
            project_type="CLI",
            primary_goal="Build tool",
            target_users="Users",
            timeline="1 week",
        )

        errors = brief.validate()
        assert errors == []
        assert brief.is_valid() is True

    def test_validate_missing_project_name(self) -> None:
        """Test validation fails when project_name is missing."""
        brief = ProjectBrief(
            project_name="",
            project_type="CLI",
            primary_goal="Build tool",
            target_users="Users",
            timeline="1 week",
        )

        errors = brief.validate()
        assert len(errors) == 1
        assert "project_name" in errors[0]
        assert brief.is_valid() is False

    def test_validate_missing_project_type(self) -> None:
        """Test validation fails when project_type is missing."""
        brief = ProjectBrief(
            project_name="Test",
            project_type="",
            primary_goal="Build tool",
            target_users="Users",
            timeline="1 week",
        )

        errors = brief.validate()
        assert len(errors) == 1
        assert "project_type" in errors[0]
        assert brief.is_valid() is False

    def test_validate_missing_primary_goal(self) -> None:
        """Test validation fails when primary_goal is missing."""
        brief = ProjectBrief(
            project_name="Test",
            project_type="CLI",
            primary_goal="",
            target_users="Users",
            timeline="1 week",
        )

        errors = brief.validate()
        assert len(errors) == 1
        assert "primary_goal" in errors[0]
        assert brief.is_valid() is False

    def test_validate_missing_target_users(self) -> None:
        """Test validation fails when target_users is missing."""
        brief = ProjectBrief(
            project_name="Test",
            project_type="CLI",
            primary_goal="Build tool",
            target_users="",
            timeline="1 week",
        )

        errors = brief.validate()
        assert len(errors) == 1
        assert "target_users" in errors[0]
        assert brief.is_valid() is False

    def test_validate_missing_timeline(self) -> None:
        """Test validation fails when timeline is missing."""
        brief = ProjectBrief(
            project_name="Test",
            project_type="CLI",
            primary_goal="Build tool",
            target_users="Users",
            timeline="",
        )

        errors = brief.validate()
        assert len(errors) == 1
        assert "timeline" in errors[0]
        assert brief.is_valid() is False

    def test_validate_multiple_missing_fields(self) -> None:
        """Test validation reports all missing required fields."""
        brief = ProjectBrief(
            project_name="",
            project_type="",
            primary_goal="",
            target_users="",
            timeline="",
        )

        errors = brief.validate()
        assert len(errors) == 5
        assert brief.is_valid() is False

    def test_validate_whitespace_only_fields(self) -> None:
        """Test validation fails for whitespace-only required fields."""
        brief = ProjectBrief(
            project_name="   ",
            project_type="   ",
            primary_goal="   ",
            target_users="   ",
            timeline="   ",
        )

        errors = brief.validate()
        assert len(errors) == 5
        assert brief.is_valid() is False

    def test_lists_are_mutable(self) -> None:
        """Test that list fields can be modified after creation."""
        brief = ProjectBrief(
            project_name="Test",
            project_type="CLI",
            primary_goal="Build",
            target_users="Users",
            timeline="1 week",
        )

        brief.key_features.append("Feature 1")
        brief.key_features.append("Feature 2")

        assert len(brief.key_features) == 2
        assert "Feature 1" in brief.key_features

    def test_dicts_are_mutable(self) -> None:
        """Test that dict fields can be modified after creation."""
        brief = ProjectBrief(
            project_name="Test",
            project_type="CLI",
            primary_goal="Build",
            target_users="Users",
            timeline="1 week",
        )

        brief.performance_requirements["latency"] = "<100ms"
        brief.performance_requirements["throughput"] = "1000 req/s"

        assert len(brief.performance_requirements) == 2
        assert brief.performance_requirements["latency"] == "<100ms"

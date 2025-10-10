"""Tests for data models."""

from claude_planner.models import Phase, ProjectBrief, Subtask, Task


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


class TestSubtask:
    """Tests for the Subtask dataclass."""

    def test_create_minimal_subtask(self) -> None:
        """Test creating a Subtask with minimal fields."""
        subtask = Subtask(
            id="1.1.1",
            title="Create models (Single Session)",
            deliverables=["Create file", "Add tests", "Write docs"],
        )

        assert subtask.id == "1.1.1"
        assert subtask.title == "Create models (Single Session)"
        assert len(subtask.deliverables) == 3
        assert subtask.status == "pending"

    def test_create_full_subtask(self) -> None:
        """Test creating a Subtask with all fields."""
        subtask = Subtask(
            id="2.3.4",
            title="Implement parser (Single Session)",
            deliverables=["Parse file", "Extract data", "Validate", "Add tests"],
            prerequisites=["1.1.1", "1.1.2"],
            files_to_create=["parser.py", "test_parser.py"],
            files_to_modify=["__init__.py"],
            success_criteria=["Tests pass", "Coverage >80%"],
            technology_decisions=["Use regex", "Use PyYAML"],
            status="completed",
            completion_notes={"implementation": "Done", "tests": "12 tests"},
        )

        assert len(subtask.deliverables) == 4
        assert len(subtask.prerequisites) == 2
        assert subtask.status == "completed"

    def test_validate_valid_subtask(self) -> None:
        """Test validation passes for a valid subtask."""
        subtask = Subtask(
            id="1.1.1",
            title="Create models (Single Session)",
            deliverables=["Item 1", "Item 2", "Item 3"],
        )

        errors = subtask.validate()
        assert errors == []
        assert subtask.is_valid() is True

    def test_validate_invalid_id_format(self) -> None:
        """Test validation fails for invalid ID format."""
        subtask = Subtask(
            id="invalid",
            title="Test (Single Session)",
            deliverables=["Item 1", "Item 2", "Item 3"],
        )

        errors = subtask.validate()
        assert any("format X.Y.Z" in error for error in errors)
        assert subtask.is_valid() is False

    def test_validate_missing_single_session_suffix(self) -> None:
        """Test validation fails when title is missing (Single Session) suffix."""
        subtask = Subtask(
            id="1.1.1", title="Create models", deliverables=["Item 1", "Item 2", "Item 3"]
        )

        errors = subtask.validate()
        assert any("(Single Session)" in error for error in errors)
        assert subtask.is_valid() is False

    def test_validate_too_few_deliverables(self) -> None:
        """Test validation fails when there are too few deliverables."""
        subtask = Subtask(id="1.1.1", title="Test (Single Session)", deliverables=["Only one"])

        errors = subtask.validate()
        assert any("minimum is 3" in error for error in errors)
        assert subtask.is_valid() is False

    def test_validate_too_many_deliverables(self) -> None:
        """Test validation fails when there are too many deliverables."""
        subtask = Subtask(
            id="1.1.1",
            title="Test (Single Session)",
            deliverables=["1", "2", "3", "4", "5", "6", "7", "8"],
        )

        errors = subtask.validate()
        assert any("maximum is 7" in error for error in errors)
        assert subtask.is_valid() is False

    def test_validate_invalid_status(self) -> None:
        """Test validation fails for invalid status."""
        subtask = Subtask(
            id="1.1.1",
            title="Test (Single Session)",
            deliverables=["Item 1", "Item 2", "Item 3"],
            status="invalid_status",
        )

        errors = subtask.validate()
        assert any("Status 'invalid_status'" in error for error in errors)
        assert subtask.is_valid() is False


class TestTask:
    """Tests for the Task dataclass."""

    def test_create_minimal_task(self) -> None:
        """Test creating a Task with minimal fields."""
        task = Task(id="1.1", title="Setup Project")

        assert task.id == "1.1"
        assert task.title == "Setup Project"
        assert task.description == ""
        assert len(task.subtasks) == 0

    def test_create_task_with_subtasks(self) -> None:
        """Test creating a Task with subtasks."""
        task = Task(id="1.1", title="Setup", description="Setup the project")
        task.subtasks.append(
            Subtask(
                id="1.1.1",
                title="Init (Single Session)",
                deliverables=["Item 1", "Item 2", "Item 3"],
            )
        )
        task.subtasks.append(
            Subtask(
                id="1.1.2",
                title="Config (Single Session)",
                deliverables=["Item 1", "Item 2", "Item 3"],
            )
        )

        assert len(task.subtasks) == 2
        assert task.subtasks[0].id == "1.1.1"

    def test_validate_valid_task(self) -> None:
        """Test validation passes for a valid task."""
        task = Task(id="1.1", title="Setup")
        task.subtasks.append(
            Subtask(
                id="1.1.1",
                title="Init (Single Session)",
                deliverables=["Item 1", "Item 2", "Item 3"],
            )
        )

        errors = task.validate()
        assert errors == []
        assert task.is_valid() is True

    def test_validate_invalid_id_format(self) -> None:
        """Test validation fails for invalid ID format."""
        task = Task(id="invalid", title="Test")
        task.subtasks.append(
            Subtask(
                id="1.1.1",
                title="Test (Single Session)",
                deliverables=["Item 1", "Item 2", "Item 3"],
            )
        )

        errors = task.validate()
        assert any("format X.Y" in error for error in errors)
        assert task.is_valid() is False

    def test_validate_no_subtasks(self) -> None:
        """Test validation fails when task has no subtasks."""
        task = Task(id="1.1", title="Test")

        errors = task.validate()
        assert any("at least one subtask" in error for error in errors)
        assert task.is_valid() is False

    def test_validate_propagates_subtask_errors(self) -> None:
        """Test validation includes errors from subtasks."""
        task = Task(id="1.1", title="Test")
        task.subtasks.append(Subtask(id="invalid", title="Bad", deliverables=["Only one"]))

        errors = task.validate()
        assert len(errors) > 1  # Multiple errors from invalid subtask
        assert task.is_valid() is False


class TestPhase:
    """Tests for the Phase dataclass."""

    def test_create_minimal_phase(self) -> None:
        """Test creating a Phase with minimal fields."""
        phase = Phase(id="0", title="Foundation", goal="Setup project")

        assert phase.id == "0"
        assert phase.title == "Foundation"
        assert phase.goal == "Setup project"
        assert phase.days == ""
        assert len(phase.tasks) == 0

    def test_create_phase_with_tasks(self) -> None:
        """Test creating a Phase with tasks."""
        phase = Phase(id="1", title="Development", goal="Build features", days="3-5")
        task = Task(id="1.1", title="Feature 1")
        task.subtasks.append(
            Subtask(
                id="1.1.1",
                title="Implement (Single Session)",
                deliverables=["Item 1", "Item 2", "Item 3"],
            )
        )
        phase.tasks.append(task)

        assert len(phase.tasks) == 1
        assert phase.tasks[0].id == "1.1"
        assert phase.days == "3-5"

    def test_validate_valid_phase(self) -> None:
        """Test validation passes for a valid phase."""
        phase = Phase(id="0", title="Foundation", goal="Setup")
        task = Task(id="0.1", title="Init")
        task.subtasks.append(
            Subtask(
                id="0.1.1",
                title="Setup (Single Session)",
                deliverables=["Item 1", "Item 2", "Item 3"],
            )
        )
        phase.tasks.append(task)

        errors = phase.validate()
        assert errors == []
        assert phase.is_valid() is True

    def test_validate_invalid_id(self) -> None:
        """Test validation fails for non-numeric ID."""
        phase = Phase(id="X", title="Test", goal="Test goal")
        task = Task(id="X.1", title="Task")
        task.subtasks.append(
            Subtask(
                id="X.1.1",
                title="Sub (Single Session)",
                deliverables=["Item 1", "Item 2", "Item 3"],
            )
        )
        phase.tasks.append(task)

        errors = phase.validate()
        assert any("must be a number" in error for error in errors)
        assert phase.is_valid() is False

    def test_validate_phase_zero_not_foundation(self) -> None:
        """Test validation warns when Phase 0 is not titled Foundation."""
        phase = Phase(id="0", title="Setup", goal="Setup project")
        task = Task(id="0.1", title="Task")
        task.subtasks.append(
            Subtask(
                id="0.1.1",
                title="Sub (Single Session)",
                deliverables=["Item 1", "Item 2", "Item 3"],
            )
        )
        phase.tasks.append(task)

        errors = phase.validate()
        assert any("Foundation" in error and "warning" in error for error in errors)
        assert phase.is_valid() is False

    def test_validate_no_tasks(self) -> None:
        """Test validation fails when phase has no tasks."""
        phase = Phase(id="1", title="Test", goal="Test goal")

        errors = phase.validate()
        assert any("at least one task" in error for error in errors)
        assert phase.is_valid() is False

    def test_validate_propagates_task_errors(self) -> None:
        """Test validation includes errors from tasks."""
        phase = Phase(id="1", title="Test", goal="Test goal")
        task = Task(id="invalid", title="Bad")
        task.subtasks.append(Subtask(id="bad", title="Bad", deliverables=["Only one"]))
        phase.tasks.append(task)

        errors = phase.validate()
        assert len(errors) > 1  # Multiple errors from invalid task/subtasks
        assert phase.is_valid() is False

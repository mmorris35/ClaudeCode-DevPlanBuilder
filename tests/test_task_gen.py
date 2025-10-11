"""Tests for task_gen module."""

from claude_planner.generator.task_gen import generate_tasks
from claude_planner.models import Phase, ProjectBrief


class TestGenerateTasks:
    """Test suite for generate_tasks function."""

    def test_returns_dict_with_phase_ids_as_keys(self):
        """Test that generate_tasks returns dict with phase IDs."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        phases = [
            Phase(id="0", title="Foundation", goal="Setup"),
            Phase(id="1", title="Core", goal="Build"),
        ]

        tasks_by_phase = generate_tasks(brief, phases)

        assert isinstance(tasks_by_phase, dict)
        assert "0" in tasks_by_phase
        assert "1" in tasks_by_phase

    def test_all_phases_have_entries_in_result(self):
        """Test that all phases get entries in result dict."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        phases = [
            Phase(id="0", title="Foundation", goal="Setup"),
            Phase(id="1", title="Models", goal="Create models"),
            Phase(id="2", title="API", goal="Build API"),
        ]

        tasks_by_phase = generate_tasks(brief, phases)

        assert len(tasks_by_phase) == len(phases)
        for phase in phases:
            assert phase.id in tasks_by_phase

    def test_task_lists_are_empty(self):
        """Test that task lists are empty (for Claude to populate)."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        phases = [
            Phase(id="0", title="Foundation", goal="Setup"),
            Phase(id="1", title="Core", goal="Build"),
        ]

        tasks_by_phase = generate_tasks(brief, phases)

        for tasks in tasks_by_phase.values():
            assert tasks == []

    def test_with_single_phase(self):
        """Test with single phase."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        phases = [Phase(id="0", title="Foundation", goal="Setup")]

        tasks_by_phase = generate_tasks(brief, phases)

        assert len(tasks_by_phase) == 1
        assert "0" in tasks_by_phase
        assert tasks_by_phase["0"] == []

    def test_with_many_phases(self):
        """Test with many phases."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="4 weeks",
        )
        phases = [Phase(id=str(i), title=f"Phase {i}", goal=f"Goal {i}") for i in range(10)]

        tasks_by_phase = generate_tasks(brief, phases)

        assert len(tasks_by_phase) == 10
        for i in range(10):
            assert str(i) in tasks_by_phase
            assert tasks_by_phase[str(i)] == []

    def test_preserves_phase_id_format(self):
        """Test that phase IDs are preserved as-is."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        phases = [
            Phase(id="0", title="Foundation", goal="Setup"),
            Phase(id="1", title="Core", goal="Build"),
            Phase(id="2", title="Final", goal="Deploy"),
        ]

        tasks_by_phase = generate_tasks(brief, phases)

        # IDs should be strings as provided
        assert list(tasks_by_phase.keys()) == ["0", "1", "2"]

    def test_empty_phases_list(self):
        """Test with empty phases list."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        phases = []

        tasks_by_phase = generate_tasks(brief, phases)

        assert tasks_by_phase == {}

    def test_with_api_project_phases(self):
        """Test with typical API project phases."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build REST API",
            target_users="Developers",
            timeline="3 weeks",
        )
        phases = [
            Phase(id="0", title="Foundation", goal="Setup"),
            Phase(id="1", title="Data Models", goal="Create models"),
            Phase(id="2", title="API Endpoints", goal="Build endpoints"),
            Phase(id="3", title="Authentication", goal="Add auth"),
        ]

        tasks_by_phase = generate_tasks(brief, phases)

        assert len(tasks_by_phase) == 4
        for phase in phases:
            assert tasks_by_phase[phase.id] == []

    def test_with_cli_project_phases(self):
        """Test with typical CLI project phases."""
        brief = ProjectBrief(
            project_name="My CLI",
            project_type="CLI",
            primary_goal="Build CLI tool",
            target_users="Developers",
            timeline="1 week",
        )
        phases = [
            Phase(id="0", title="Foundation", goal="Setup"),
            Phase(id="1", title="Command Structure", goal="Design commands"),
            Phase(id="2", title="Implementation", goal="Implement"),
        ]

        tasks_by_phase = generate_tasks(brief, phases)

        assert len(tasks_by_phase) == 3
        for phase in phases:
            assert tasks_by_phase[phase.id] == []

    def test_minimal_brief(self):
        """Test with minimal brief."""
        brief = ProjectBrief(
            project_name="Min",
            project_type="API",
            primary_goal="Build",
            target_users="Users",
            timeline="1 week",
        )
        phases = [Phase(id="0", title="Foundation", goal="Setup")]

        tasks_by_phase = generate_tasks(brief, phases)

        assert len(tasks_by_phase) == 1
        assert tasks_by_phase["0"] == []

    def test_brief_with_key_features_doesnt_affect_output(self):
        """Test that key_features in brief don't affect task generation."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            key_features=["User auth", "Payment processing", "Email notifications"],
        )
        phases = [Phase(id="0", title="Foundation", goal="Setup")]

        tasks_by_phase = generate_tasks(brief, phases)

        # Should still return empty lists regardless of features
        assert tasks_by_phase["0"] == []

    def test_brief_with_nice_to_have_doesnt_affect_output(self):
        """Test that nice_to_have_features don't affect task generation."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            nice_to_have_features=["Admin dashboard", "Analytics"],
        )
        phases = [Phase(id="0", title="Foundation", goal="Setup")]

        tasks_by_phase = generate_tasks(brief, phases)

        assert tasks_by_phase["0"] == []

    def test_return_value_is_mutable_dict(self):
        """Test that return value is a mutable dict."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        phases = [Phase(id="0", title="Foundation", goal="Setup")]

        tasks_by_phase = generate_tasks(brief, phases)

        # Should be able to modify the dict
        from claude_planner.models import Task

        tasks_by_phase["0"].append(Task(id="0.1", title="Test Task"))
        assert len(tasks_by_phase["0"]) == 1

    def test_return_value_lists_are_independent(self):
        """Test that task lists for different phases are independent."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        phases = [
            Phase(id="0", title="Foundation", goal="Setup"),
            Phase(id="1", title="Core", goal="Build"),
        ]

        tasks_by_phase = generate_tasks(brief, phases)

        # Modify one list
        from claude_planner.models import Task

        tasks_by_phase["0"].append(Task(id="0.1", title="Test Task"))

        # Other list should remain unchanged
        assert len(tasks_by_phase["0"]) == 1
        assert len(tasks_by_phase["1"]) == 0

    def test_phase_with_existing_tasks_ignored(self):
        """Test that existing tasks in Phase objects are ignored."""
        from claude_planner.models import Task

        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        # Create phase with pre-existing tasks
        phase = Phase(id="0", title="Foundation", goal="Setup")
        phase.tasks.append(Task(id="0.1", title="Existing Task"))

        tasks_by_phase = generate_tasks(brief, [phase])

        # Should return empty list, not the existing tasks
        assert tasks_by_phase["0"] == []

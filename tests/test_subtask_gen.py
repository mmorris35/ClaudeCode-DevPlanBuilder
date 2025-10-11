"""Tests for subtask_gen module."""

from claude_planner.generator.subtask_gen import generate_subtasks
from claude_planner.models import ProjectBrief, Task


class TestGenerateSubtasks:
    """Test suite for generate_subtasks function."""

    def test_returns_nested_dict_structure(self):
        """Test that generate_subtasks returns nested dict structure."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {
            "0": [Task(id="0.1", title="Setup")],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert isinstance(subtasks, dict)
        assert "0" in subtasks
        assert isinstance(subtasks["0"], dict)
        assert "0.1" in subtasks["0"]

    def test_all_phases_have_entries(self):
        """Test that all phases have entries in result."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {
            "0": [Task(id="0.1", title="Setup")],
            "1": [Task(id="1.1", title="Models")],
            "2": [Task(id="2.1", title="API")],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert len(subtasks) == 3
        assert "0" in subtasks
        assert "1" in subtasks
        assert "2" in subtasks

    def test_all_tasks_have_entries(self):
        """Test that all tasks have entries in result."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {
            "0": [
                Task(id="0.1", title="Setup"),
                Task(id="0.2", title="Config"),
            ],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert "0.1" in subtasks["0"]
        assert "0.2" in subtasks["0"]

    def test_subtask_lists_are_empty(self):
        """Test that subtask lists are empty (for Claude to populate)."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {
            "0": [Task(id="0.1", title="Setup")],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert subtasks["0"]["0.1"] == []

    def test_with_multiple_tasks_per_phase(self):
        """Test with multiple tasks per phase."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {
            "0": [
                Task(id="0.1", title="Setup"),
                Task(id="0.2", title="Config"),
                Task(id="0.3", title="Init"),
            ],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert len(subtasks["0"]) == 3
        assert subtasks["0"]["0.1"] == []
        assert subtasks["0"]["0.2"] == []
        assert subtasks["0"]["0.3"] == []

    def test_with_empty_task_lists(self):
        """Test with empty task lists."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {
            "0": [],
            "1": [],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert subtasks["0"] == {}
        assert subtasks["1"] == {}

    def test_with_no_phases(self):
        """Test with empty phases dict."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {}

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert subtasks == {}

    def test_preserves_phase_and_task_ids(self):
        """Test that phase and task IDs are preserved."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {
            "0": [Task(id="0.1", title="Setup")],
            "1": [Task(id="1.1", title="Models"), Task(id="1.2", title="Views")],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert list(subtasks.keys()) == ["0", "1"]
        assert list(subtasks["0"].keys()) == ["0.1"]
        assert list(subtasks["1"].keys()) == ["1.1", "1.2"]

    def test_task_with_existing_subtasks_ignored(self):
        """Test that existing subtasks in Task objects are ignored."""
        from claude_planner.models import Subtask

        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )

        # Create task with pre-existing subtasks
        task = Task(id="0.1", title="Setup")
        task.subtasks.append(
            Subtask(id="0.1.1", title="Existing (Single Session)", deliverables=[])
        )

        tasks_by_phase = {"0": [task]}

        subtasks = generate_subtasks(brief, tasks_by_phase)

        # Should return empty list, not the existing subtasks
        assert subtasks["0"]["0.1"] == []

    def test_complex_structure_multiple_phases_and_tasks(self):
        """Test complex structure with multiple phases and tasks."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="4 weeks",
        )
        tasks_by_phase = {
            "0": [
                Task(id="0.1", title="Setup"),
                Task(id="0.2", title="Config"),
            ],
            "1": [
                Task(id="1.1", title="Models"),
                Task(id="1.2", title="Views"),
                Task(id="1.3", title="Serializers"),
            ],
            "2": [
                Task(id="2.1", title="Tests"),
            ],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert len(subtasks) == 3
        assert len(subtasks["0"]) == 2
        assert len(subtasks["1"]) == 3
        assert len(subtasks["2"]) == 1

        # All should be empty lists
        for phase_subtasks in subtasks.values():
            for task_subtasks in phase_subtasks.values():
                assert task_subtasks == []

    def test_return_value_is_mutable(self):
        """Test that return value is mutable."""
        from claude_planner.models import Subtask

        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {"0": [Task(id="0.1", title="Setup")]}

        subtasks = generate_subtasks(brief, tasks_by_phase)

        # Should be able to modify the structure
        subtasks["0"]["0.1"].append(
            Subtask(id="0.1.1", title="Test (Single Session)", deliverables=[])
        )
        assert len(subtasks["0"]["0.1"]) == 1

    def test_subtask_lists_are_independent(self):
        """Test that subtask lists for different tasks are independent."""
        from claude_planner.models import Subtask

        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
        )
        tasks_by_phase = {
            "0": [
                Task(id="0.1", title="Setup"),
                Task(id="0.2", title="Config"),
            ],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        # Modify one list
        subtasks["0"]["0.1"].append(
            Subtask(id="0.1.1", title="Test (Single Session)", deliverables=[])
        )

        # Other list should remain unchanged
        assert len(subtasks["0"]["0.1"]) == 1
        assert len(subtasks["0"]["0.2"]) == 0

    def test_minimal_brief(self):
        """Test with minimal brief."""
        brief = ProjectBrief(
            project_name="Min",
            project_type="API",
            primary_goal="Build",
            target_users="Users",
            timeline="1 week",
        )
        tasks_by_phase = {"0": [Task(id="0.1", title="Setup")]}

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert subtasks["0"]["0.1"] == []

    def test_brief_features_dont_affect_output(self):
        """Test that key_features and nice_to_have don't affect output."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build API",
            target_users="Developers",
            timeline="2 weeks",
            key_features=["User auth", "Payment processing"],
            nice_to_have_features=["Analytics"],
        )
        tasks_by_phase = {"0": [Task(id="0.1", title="Setup")]}

        subtasks = generate_subtasks(brief, tasks_by_phase)

        # Should still return empty lists regardless of features
        assert subtasks["0"]["0.1"] == []

    def test_with_api_project_structure(self):
        """Test with typical API project structure."""
        brief = ProjectBrief(
            project_name="My API",
            project_type="API",
            primary_goal="Build REST API",
            target_users="Developers",
            timeline="3 weeks",
        )
        tasks_by_phase = {
            "0": [Task(id="0.1", title="Setup")],
            "1": [Task(id="1.1", title="Models")],
            "2": [Task(id="2.1", title="Endpoints")],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        for phase_id in ["0", "1", "2"]:
            for task_id in subtasks[phase_id]:
                assert subtasks[phase_id][task_id] == []

    def test_with_cli_project_structure(self):
        """Test with typical CLI project structure."""
        brief = ProjectBrief(
            project_name="My CLI",
            project_type="CLI",
            primary_goal="Build CLI tool",
            target_users="Developers",
            timeline="1 week",
        )
        tasks_by_phase = {
            "0": [Task(id="0.1", title="Setup")],
            "1": [Task(id="1.1", title="Commands")],
        }

        subtasks = generate_subtasks(brief, tasks_by_phase)

        assert subtasks["0"]["0.1"] == []
        assert subtasks["1"]["1.1"] == []

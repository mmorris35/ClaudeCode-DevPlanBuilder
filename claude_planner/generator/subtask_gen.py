"""Subtask generation module.

This module provides functions to generate subtasks for development tasks.
"""

from claude_planner.models import ProjectBrief, Subtask, Task


def generate_subtasks(
    brief: ProjectBrief, tasks_by_phase: dict[str, list[Task]]
) -> dict[str, dict[str, list[Subtask]]]:
    """Generate Subtask lists for each task.

    Strategy:
    1. Return empty subtask lists for each task
    2. Let Claude Code intelligently populate subtasks when generating plans

    This is intentionally simple - we don't try to algorithmically:
    - Break tasks into subtasks
    - Calculate subtask sizing (2-4 hours)
    - Auto-detect prerequisites
    - Ensure 3-7 deliverables per subtask
    - Determine optimal subtask counts (2-5)

    Claude Code will make intelligent decisions about subtask structure based on
    the project's natural language requirements.

    Args:
        brief: ProjectBrief with project requirements
        tasks_by_phase: Dictionary mapping phase IDs to task lists

    Returns:
        Nested dictionary mapping phase IDs -> task IDs -> empty subtask lists

    Example:
        >>> brief = ProjectBrief(
        ...     project_name="My API",
        ...     project_type="API",
        ...     primary_goal="Build API",
        ...     target_users="Developers",
        ...     timeline="2 weeks"
        ... )
        >>> tasks_by_phase = {"0": [Task(id="0.1", title="Setup")]}
        >>> subtasks = generate_subtasks(brief, tasks_by_phase)
        >>> subtasks["0"]["0.1"]
        []
    """
    # Return empty subtask lists for each task
    # Claude will populate these when generating the actual plan
    subtasks_by_phase_task: dict[str, dict[str, list[Subtask]]] = {}

    for phase_id, tasks in tasks_by_phase.items():
        subtasks_by_phase_task[phase_id] = {}
        for task in tasks:
            subtasks_by_phase_task[phase_id][task.id] = []

    return subtasks_by_phase_task

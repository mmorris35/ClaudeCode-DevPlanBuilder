"""Task generation module.

This module provides functions to generate tasks for development phases.
"""

from claude_planner.models import Phase, ProjectBrief, Task


def generate_tasks(brief: ProjectBrief, phases: list[Phase]) -> dict[str, list[Task]]:
    """Generate Task lists for each phase.

    Strategy:
    1. Return empty task lists for each phase
    2. Let Claude Code intelligently populate tasks when generating plans

    This is intentionally simple - we don't try to algorithmically:
    - Parse key_features to map features to tasks
    - Determine optimal task groupings
    - Calculate task dependencies
    - Decide how many tasks per phase

    Claude Code will make intelligent decisions about task structure based on
    the project's natural language requirements.

    Args:
        brief: ProjectBrief with project requirements
        phases: List of Phase objects from phase generator

    Returns:
        Dictionary mapping phase IDs to empty task lists

    Example:
        >>> brief = ProjectBrief(
        ...     project_name="My API",
        ...     project_type="API",
        ...     primary_goal="Build API",
        ...     target_users="Developers",
        ...     timeline="2 weeks"
        ... )
        >>> phases = [Phase(id="0", title="Foundation", goal="Setup")]
        >>> tasks_by_phase = generate_tasks(brief, phases)
        >>> tasks_by_phase["0"]
        []
    """
    # Return empty task lists for each phase
    # Claude will populate these when generating the actual plan
    tasks_by_phase: dict[str, list[Task]] = {}

    for phase in phases:
        tasks_by_phase[phase.id] = []

    return tasks_by_phase

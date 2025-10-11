"""Complete plan generation pipeline.

This module provides the main entry point for generating complete development plans
by orchestrating all generator components.
"""

from claude_planner.generator.phase_gen import generate_phases
from claude_planner.generator.subtask_gen import generate_subtasks
from claude_planner.generator.task_gen import generate_tasks
from claude_planner.generator.tech_stack_gen import generate_tech_stack
from claude_planner.models import DevelopmentPlan, ProjectBrief


def generate_plan(brief: ProjectBrief) -> DevelopmentPlan:
    """Generate complete development plan from project brief.

    This is the main orchestration function that chains all generators:
    1. Generate tech stack from brief
    2. Generate phases from brief and template
    3. Generate tasks for each phase (empty lists)
    4. Generate subtasks for each task (empty lists)
    5. Assemble into DevelopmentPlan
    6. Validate the plan structure

    Args:
        brief: ProjectBrief with project requirements

    Returns:
        Complete DevelopmentPlan with tech stack and phase structure

    Raises:
        ValueError: If plan validation fails

    Example:
        >>> brief = ProjectBrief(
        ...     project_name="My API",
        ...     project_type="API",
        ...     primary_goal="Build API",
        ...     target_users="Developers",
        ...     timeline="2 weeks"
        ... )
        >>> plan = generate_plan(brief)
        >>> plan.project_name
        'My API'
        >>> len(plan.phases) > 0
        True
    """
    # Step 1: Generate tech stack
    tech_stack = generate_tech_stack(brief)

    # Step 2: Generate phases from template
    phases = generate_phases(brief)

    # Step 3: Generate tasks for each phase (returns empty task lists)
    tasks_by_phase = generate_tasks(brief, phases)

    # Step 4: Generate subtasks for each task (returns empty subtask lists)
    _subtasks_by_phase_task = generate_subtasks(brief, tasks_by_phase)

    # Step 5: Assemble the complete plan
    # Note: Since our generators return empty lists, the phases will have empty
    # task/subtask structures. This is intentional - Claude Code will populate
    # the actual content when rendering templates.
    plan = DevelopmentPlan(
        project_name=brief.project_name,
        phases=phases,
        tech_stack=tech_stack,
    )

    # Step 6: Validate the plan structure
    # Check for basic structural validity
    validation_errors = _validate_plan_structure(plan)
    if validation_errors:
        error_msg = "\n".join(validation_errors)
        raise ValueError(f"Plan validation failed:\n{error_msg}")

    return plan


def _validate_plan_structure(plan: DevelopmentPlan) -> list[str]:
    """Validate basic plan structure.

    Args:
        plan: DevelopmentPlan to validate

    Returns:
        List of validation error messages. Empty if valid.
    """
    errors = []

    # Validate project name
    if not plan.project_name or not plan.project_name.strip():
        errors.append("Project name is required")

    # Validate has phases
    if not plan.phases:
        errors.append("Plan must have at least one phase")

    # Validate Phase 0 is Foundation
    if plan.phases:
        phase_0 = plan.phases[0]
        if phase_0.id != "0":
            errors.append("First phase must have ID '0'")
        if "Foundation" not in phase_0.title:
            errors.append("Phase 0 should be titled 'Foundation'")

    # Validate tech stack exists
    if not plan.tech_stack:
        errors.append("Plan must have a tech stack")

    return errors

"""Phase generation module.

This module provides functions to generate development phases from project requirements
and template defaults.
"""

from claude_planner.models import Phase, ProjectBrief
from claude_planner.templates.selector import load_template_config, select_template


def generate_phases(brief: ProjectBrief) -> list[Phase]:
    """Generate Phase list from ProjectBrief and template defaults.

    Strategy:
    1. Load template's default_phases list
    2. Always include Phase 0 (Foundation)
    3. Create Phase objects from template phase names
    4. Let Claude Code intelligently customize phases when generating plans

    This is intentionally simple - we don't try to algorithmically determine
    which phases to add/remove based on features, or calculate timeline splits.
    Claude Code will make intelligent decisions about phase customization.

    Args:
        brief: ProjectBrief with project requirements

    Returns:
        List of Phase objects with basic structure from template

    Example:
        >>> brief = ProjectBrief(
        ...     project_name="My API",
        ...     project_type="API",
        ...     primary_goal="Build API",
        ...     target_users="Developers",
        ...     timeline="2 weeks"
        ... )
        >>> phases = generate_phases(brief)
        >>> phases[0].title
        'Foundation'
        >>> phases[0].id
        '0'
    """
    # Get template for project type
    template_path = select_template(brief.project_type)
    template_config = load_template_config(template_path)

    # Get default phases from template
    default_phase_names = template_config.get("default_phases", [])

    # Ensure Foundation is always Phase 0
    if not default_phase_names or default_phase_names[0] != "Foundation":
        default_phase_names = ["Foundation"] + [
            name for name in default_phase_names if name != "Foundation"
        ]

    # Create Phase objects from template phase names
    phases: list[Phase] = []
    for i, phase_name in enumerate(default_phase_names):
        phase = Phase(
            id=str(i),
            title=phase_name,
            goal=f"Complete {phase_name.lower()} phase",
            days="",  # Claude will determine timeline distribution
            description="",
            tasks=[],
        )
        phases.append(phase)

    return phases

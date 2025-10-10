"""Tech stack generation module.

This module provides functions to generate technology stacks from project requirements,
respecting constraints and using template defaults as fallbacks.
"""

from claude_planner.models import ProjectBrief, TechStack
from claude_planner.templates.selector import load_template_config, select_template


def generate_tech_stack(brief: ProjectBrief) -> TechStack:
    """Generate TechStack from ProjectBrief requirements.

    Strategy:
    1. Load template defaults for the project type
    2. Check for conflicts between must_use and cannot_use
    3. Apply template defaults, respecting cannot_use constraints
    4. Pass through must_use items as additional_tools
    5. Apply common fallback defaults

    This is intentionally simple - we don't try to parse or interpret
    technology names. Claude Code will make intelligent decisions about
    tech selection when generating plans.

    Args:
        brief: ProjectBrief with project requirements and constraints

    Returns:
        TechStack with selected technologies

    Raises:
        ValueError: If must_use and cannot_use constraints conflict

    Example:
        >>> brief = ProjectBrief(
        ...     project_name="My API",
        ...     project_type="API",
        ...     primary_goal="Build API",
        ...     target_users="Developers",
        ...     timeline="2 weeks",
        ...     must_use_tech=["FastAPI", "PostgreSQL"]
        ... )
        >>> stack = generate_tech_stack(brief)
        >>> "FastAPI" in stack.additional_tools.values() or stack.framework == "FastAPI"
        True
    """
    # Get template for project type to use its defaults
    template_path = select_template(brief.project_type)
    template_config = load_template_config(template_path)
    template_defaults = template_config.get("default_tech_stack", {})

    # Normalize constraints to lowercase for comparison
    must_use = [tech.lower() for tech in brief.must_use_tech]
    cannot_use = [tech.lower() for tech in brief.cannot_use_tech]

    # Check for conflicts
    conflicts = set(must_use) & set(cannot_use)
    if conflicts:
        raise ValueError(
            f"Conflicting constraints: {conflicts} appears in both "
            "must_use_tech and cannot_use_tech"
        )

    # Build technology selections with explicit types
    language = ""
    framework = ""
    database = ""
    testing = ""
    linting = ""
    type_checking = ""
    deployment = ""
    ci_cd = ""
    additional_tools: dict[str, str] = {}

    # Apply template defaults, respecting cannot_use constraints
    if "language" in template_defaults:
        if template_defaults["language"].lower() not in cannot_use:
            language = template_defaults["language"]

    if "framework" in template_defaults:
        if template_defaults["framework"].lower() not in cannot_use:
            framework = template_defaults["framework"]

    if "database" in template_defaults:
        if template_defaults["database"].lower() not in cannot_use:
            database = template_defaults["database"]

    if "cache" in template_defaults:
        cache = template_defaults["cache"]
        if cache.lower() not in cannot_use:
            additional_tools["cache"] = cache

    if "deployment" in template_defaults:
        deployment_val = template_defaults["deployment"]
        # Check if any cannot_use constraint is in the deployment string
        blocked = any(constraint in deployment_val.lower() for constraint in cannot_use)
        if not blocked:
            deployment = deployment_val

    if "packaging" in template_defaults:
        packaging = template_defaults["packaging"]
        if packaging.lower() not in cannot_use:
            additional_tools["packaging"] = packaging

    # Add must_use items to additional_tools
    # (Claude will intelligently place them in the right categories when generating plans)
    for i, tech in enumerate(brief.must_use_tech):
        additional_tools[f"must_use_{i}"] = tech

    # Apply common fallback defaults for critical fields
    if not language:
        language = "Python 3.11+"

    if not testing:
        # Set based on language
        if "python" in language.lower():
            testing = "pytest"
        elif any(js in language.lower() for js in ["javascript", "typescript"]):
            testing = "jest"

    if not linting:
        # Set based on language
        if "python" in language.lower():
            linting = "ruff"
        elif any(js in language.lower() for js in ["javascript", "typescript"]):
            linting = "eslint"

    if not type_checking:
        # Set based on language
        if "python" in language.lower():
            type_checking = "mypy"
        elif "typescript" in language.lower():
            type_checking = "TypeScript"

    if not ci_cd:
        ci_cd = "GitHub Actions"

    # Create and return TechStack
    return TechStack(
        language=language,
        framework=framework,
        database=database,
        testing=testing,
        linting=linting,
        type_checking=type_checking,
        deployment=deployment,
        ci_cd=ci_cd,
        additional_tools=additional_tools,
    )

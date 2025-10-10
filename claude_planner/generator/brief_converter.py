"""Convert extracted field dictionaries to ProjectBrief model instances.

This module provides functions to map the structured dictionaries returned by
brief_extractor functions into validated ProjectBrief model instances.
"""

from claude_planner.models import ProjectBrief


def convert_to_project_brief(
    basic_info: dict[str, str | list[str]],
    requirements: dict[str, list[str]],
    tech_constraints: dict[str, list[str]],
    quality_requirements: dict[str, dict[str, str]],
    team_info: dict[str, list[str] | dict[str, bool]],
) -> ProjectBrief:
    """Convert extracted field dictionaries to a ProjectBrief model instance.

    Args:
        basic_info: Basic project information from extract_basic_info()
        requirements: Functional requirements from extract_requirements()
        tech_constraints: Technical constraints from extract_tech_constraints()
        quality_requirements: Quality requirements from extract_quality_requirements()
        team_info: Team information from extract_team_info()

    Returns:
        ProjectBrief instance populated with all extracted data

    Raises:
        ValueError: If required fields are missing or validation fails

    Example:
        >>> basic = {"project_name": "My Project", "project_type": ["CLI"], ...}
        >>> reqs = {"input": [], "output": [], "key_features": [], "nice_to_have": []}
        >>> tech = {"must_use": [], "cannot_use": [], "deployment_target": []}
        >>> quality = {"performance": {}, "security": {}, "scalability": {}}
        >>> team = {"team_composition": {}, "existing_knowledge": [], "infrastructure": []}
        >>> brief = convert_to_project_brief(basic, reqs, tech, quality, team)
        >>> brief.project_name
        'My Project'
    """
    # Extract and validate required fields from basic_info
    project_name = _get_string_field(basic_info, "project_name", required=True)
    primary_goal = _get_string_field(basic_info, "primary_goal", required=True)
    target_users = _get_string_field(basic_info, "target_users", required=True)
    timeline = _get_string_field(basic_info, "timeline", required=True)

    # Handle project_type - convert list to comma-separated string
    project_type_list = basic_info.get("project_type", [])
    if isinstance(project_type_list, list):
        if not project_type_list:
            raise ValueError("Required field 'project_type' is missing or empty")
        project_type = ", ".join(project_type_list)
    else:
        project_type = str(project_type_list)
        if not project_type.strip():
            raise ValueError("Required field 'project_type' is missing or empty")

    # Optional basic info fields - team_size defaults to "1" if empty
    team_size = _get_string_field(basic_info, "team_size", default="1")
    if not team_size.strip():
        team_size = "1"

    # Functional requirements
    key_features = requirements.get("key_features", [])
    nice_to_have_features = requirements.get("nice_to_have", [])

    # Technical constraints
    must_use_tech = tech_constraints.get("must_use", [])
    cannot_use_tech = tech_constraints.get("cannot_use", [])

    # Deployment target - convert list to string
    deployment_target_list = tech_constraints.get("deployment_target", [])
    deployment_target = ", ".join(deployment_target_list) if deployment_target_list else None

    # Quality requirements
    performance_requirements = quality_requirements.get("performance", {})
    security_requirements = quality_requirements.get("security", {})
    scalability_requirements = quality_requirements.get("scalability", {})

    # Team information
    existing_knowledge = team_info.get("existing_knowledge", [])
    if not isinstance(existing_knowledge, list):
        existing_knowledge = []

    infrastructure_access = team_info.get("infrastructure", [])
    if not isinstance(infrastructure_access, list):
        infrastructure_access = []

    # Team composition - convert dict to string representation
    team_composition_dict = team_info.get("team_composition", {})
    if isinstance(team_composition_dict, dict):
        # Format as "Senior: Yes, Junior: No" etc
        team_comp_parts = [
            f"{role}: {'Yes' if checked else 'No'}"
            for role, checked in team_composition_dict.items()
        ]
        team_composition = ", ".join(team_comp_parts) if team_comp_parts else None
    else:
        team_composition = None

    # Create ProjectBrief instance
    brief = ProjectBrief(
        project_name=project_name,
        project_type=project_type,
        primary_goal=primary_goal,
        target_users=target_users,
        timeline=timeline,
        team_size=team_size,
        key_features=key_features,
        nice_to_have_features=nice_to_have_features,
        must_use_tech=must_use_tech,
        cannot_use_tech=cannot_use_tech,
        deployment_target=deployment_target,
        performance_requirements=performance_requirements,
        security_requirements=security_requirements,
        scalability_requirements=scalability_requirements,
        team_composition=team_composition,
        existing_knowledge=existing_knowledge,
        infrastructure_access=infrastructure_access,
    )

    # Validate the brief
    errors = brief.validate()
    if errors:
        error_msg = "ProjectBrief validation failed:\n" + "\n".join(f"  - {err}" for err in errors)
        raise ValueError(error_msg)

    return brief


def _get_string_field(
    data: dict[str, str | list[str]],
    field_name: str,
    required: bool = False,
    default: str = "",
) -> str:
    """Extract a string field from a dictionary.

    Args:
        data: Dictionary containing the field
        field_name: Name of the field to extract
        required: Whether the field is required
        default: Default value if field is missing or empty

    Returns:
        String value of the field

    Raises:
        ValueError: If required field is missing or empty
    """
    value = data.get(field_name, default)

    # Convert to string if it's not already
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value) if value else ""
    else:
        value = str(value) if value is not None else ""

    # Check if required
    if required and not value.strip():
        raise ValueError(f"Required field '{field_name}' is missing or empty")

    return value.strip()

"""Field extraction from PROJECT_BRIEF.md markdown sections.

This module provides functions to extract structured data from parsed
PROJECT_BRIEF.md sections into dictionaries that can be used to populate
ProjectBrief model instances.
"""

import re

from claude_planner.generator.parser import (
    extract_checkbox_fields,
    extract_field_value,
    extract_list_items,
)


def extract_basic_info(sections: dict[str, str]) -> dict[str, str | list[str]]:
    """Extract basic project information from markdown sections.

    Args:
        sections: Dictionary of markdown sections keyed by heading name

    Returns:
        Dictionary containing:
        - project_name: str
        - project_type: list[str] (e.g., ["CLI Tool", "Library"])
        - primary_goal: str
        - target_users: str
        - timeline: str
        - team_size: str

    Example:
        >>> sections = {"Basic Information": "- **Project Name**: My Project\\n..."}
        >>> info = extract_basic_info(sections)
        >>> info["project_name"]
        'My Project'
    """
    basic_info_section = sections.get("Basic Information", "")

    # Extract simple fields
    project_name = extract_field_value(basic_info_section, "Project Name")
    primary_goal = extract_field_value(basic_info_section, "Primary Goal")
    target_users = extract_field_value(basic_info_section, "Target Users")
    timeline = extract_field_value(basic_info_section, "Timeline")
    team_size = extract_field_value(basic_info_section, "Team Size")

    # Extract project type - special case, checkboxes on same line
    # Format: "- **Project Type**: [x] CLI Tool + [x] Library + [ ] Web"
    # Note: extract_field_value removes first checkbox, so we get "CLI Tool + [x] Library + [ ] Web"
    project_type = []
    project_type_line = extract_field_value(basic_info_section, "Project Type")
    if project_type_line:
        # Split by + to get all project types
        parts = project_type_line.split("+")
        for part in parts:
            part = part.strip()
            # Check if this part starts with [x] (checked)
            if re.match(r"\[x\]", part, re.IGNORECASE):
                # Extract the text after [x]
                clean_part = re.sub(r"\[x\]\s*", "", part, flags=re.IGNORECASE).strip()
                if clean_part:
                    project_type.append(clean_part)
            elif not part.startswith("["):
                # First part has checkbox already removed by extract_field_value
                if part:
                    project_type.append(part)

    return {
        "project_name": project_name,
        "project_type": project_type,
        "primary_goal": primary_goal,
        "target_users": target_users,
        "timeline": timeline,
        "team_size": team_size,
    }


def extract_requirements(sections: dict[str, str]) -> dict[str, list[str]]:
    """Extract functional requirements from markdown sections.

    Args:
        sections: Dictionary of markdown sections keyed by heading name

    Returns:
        Dictionary containing:
        - input: list[str] - What the system receives
        - output: list[str] - What the system produces
        - key_features: list[str] - MVP must-have features
        - nice_to_have: list[str] - v2 features

    Example:
        >>> sections = {"Input": "- File 1\\n- File 2"}
        >>> reqs = extract_requirements(sections)
        >>> len(reqs["input"])
        2
    """
    # Extract list items from each requirements section
    input_items = extract_list_items(sections.get("Input", ""))
    output_items = extract_list_items(sections.get("Output", ""))
    key_features = extract_list_items(sections.get("Key Features", ""))
    nice_to_have = extract_list_items(sections.get("Nice-to-Have Features", ""))

    return {
        "input": input_items,
        "output": output_items,
        "key_features": key_features,
        "nice_to_have": nice_to_have,
    }


def extract_tech_constraints(sections: dict[str, str]) -> dict[str, list[str]]:
    """Extract technical constraints from markdown sections.

    Args:
        sections: Dictionary of markdown sections keyed by heading name

    Returns:
        Dictionary containing:
        - must_use: list[str] - Required technologies
        - cannot_use: list[str] - Prohibited technologies
        - deployment_target: list[str] - Deployment platforms/targets

    Example:
        >>> sections = {"Must Use": "- Python 3.11+\\n- Click"}
        >>> constraints = extract_tech_constraints(sections)
        >>> "Python 3.11+" in constraints["must_use"]
        True
    """
    must_use = extract_list_items(sections.get("Must Use", ""))
    cannot_use = extract_list_items(sections.get("Cannot Use", ""))
    deployment_target = extract_list_items(sections.get("Deployment Target", ""))

    return {
        "must_use": must_use,
        "cannot_use": cannot_use,
        "deployment_target": deployment_target,
    }


def extract_quality_requirements(
    sections: dict[str, str],
) -> dict[str, dict[str, str]]:
    """Extract quality requirements from markdown sections.

    Args:
        sections: Dictionary of markdown sections keyed by heading name

    Returns:
        Dictionary containing:
        - performance: dict[str, str] - Performance metrics and targets
        - security: dict[str, str] - Security requirements
        - scalability: dict[str, str] - Scalability constraints

    Example:
        >>> sections = {"Performance": "- **Generation Time**: <5 seconds"}
        >>> quality = extract_quality_requirements(sections)
        >>> quality["performance"]["Generation Time"]
        '<5 seconds'
    """
    performance_section = sections.get("Performance", "")
    security_section = sections.get("Security", "")
    scalability_section = sections.get("Scalability", "")

    # Extract key-value pairs from each section
    performance = {}
    for line in performance_section.split("\n"):
        if "**" in line and ":" in line:
            # Extract field name and value
            parts = line.split(":", 1)
            if len(parts) == 2:
                # Clean field name (remove **, -, etc.)
                field = parts[0].strip().replace("**", "").replace("-", "").strip()
                value = parts[1].strip()
                if field and value:
                    performance[field] = value

    security = {}
    for line in security_section.split("\n"):
        if "**" in line and ":" in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                field = parts[0].strip().replace("**", "").replace("-", "").strip()
                value = parts[1].strip()
                if field and value:
                    security[field] = value

    scalability = {}
    for line in scalability_section.split("\n"):
        if "**" in line and ":" in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                field = parts[0].strip().replace("**", "").replace("-", "").strip()
                value = parts[1].strip()
                if field and value:
                    scalability[field] = value

    return {
        "performance": performance,
        "security": security,
        "scalability": scalability,
    }


def extract_team_info(sections: dict[str, str]) -> dict[str, list[str] | dict[str, bool]]:
    """Extract team and resources information from markdown sections.

    Args:
        sections: Dictionary of markdown sections keyed by heading name

    Returns:
        Dictionary containing:
        - team_composition: dict[str, bool] - Checkbox fields for skill levels/roles
        - existing_knowledge: list[str] - List of known technologies/skills
        - infrastructure: list[str] - Available infrastructure and tools

    Example:
        >>> sections = {"Team Composition": "- [x] Senior"}
        >>> team = extract_team_info(sections)
        >>> team["team_composition"]["Senior"]
        True
    """
    team_composition_section = sections.get("Team Composition", "")
    existing_knowledge_section = sections.get("Existing Knowledge", "")
    infrastructure_section = sections.get("Infrastructure Access", "")

    # Extract checkbox fields for team composition
    team_composition = extract_checkbox_fields(team_composition_section)

    # Extract list items for knowledge and infrastructure
    existing_knowledge = extract_list_items(existing_knowledge_section)
    infrastructure = extract_list_items(infrastructure_section)

    return {
        "team_composition": team_composition,
        "existing_knowledge": existing_knowledge,
        "infrastructure": infrastructure,
    }

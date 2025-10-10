"""Template selection and management for project generation.

This module provides functions to discover, select, and load templates
based on project requirements.
"""

from pathlib import Path
from typing import Any

import yaml


def list_templates() -> list[str]:
    """List all available template names.

    Returns:
        List of template directory names (e.g., ['base', 'web-app', 'api', 'cli'])

    Example:
        >>> templates = list_templates()
        >>> 'web-app' in templates
        True
    """
    templates_dir = _get_templates_dir()
    template_names = []

    for path in templates_dir.iterdir():
        if path.is_dir() and not path.name.startswith("_"):
            # Check if it has a config.yaml file
            config_path = path / "config.yaml"
            if config_path.exists():
                template_names.append(path.name)

    return sorted(template_names)


def select_template(project_type: str) -> Path:
    """Select appropriate template based on project type.

    Args:
        project_type: Project type string from PROJECT_BRIEF.md (e.g., "CLI Tool", "Web App")

    Returns:
        Path to selected template directory

    Raises:
        ValueError: If no matching template is found

    Example:
        >>> path = select_template("CLI Tool")
        >>> path.name
        'cli'
    """
    templates_dir = _get_templates_dir()

    # Normalize project type for comparison (lowercase, remove special chars)
    normalized_type = project_type.lower().strip()

    # Check each template's config to see if it matches
    for template_name in list_templates():
        template_path = templates_dir / template_name
        config_path = template_path / "config.yaml"

        if not config_path.exists():
            continue

        config = load_template_config(template_path)
        project_types = config.get("project_types", [])

        # Check if any of the template's project types match
        for ptype in project_types:
            if _matches_project_type(normalized_type, ptype):
                return template_path

    # If no match found, return base template as fallback
    base_template = templates_dir / "base"
    if base_template.exists():
        return base_template

    raise ValueError(
        f"No matching template found for project type '{project_type}' "
        f"and no base template available"
    )


def load_template_config(template_path: Path) -> dict[str, Any]:
    """Load and parse template configuration from config.yaml.

    Args:
        template_path: Path to template directory

    Returns:
        Dictionary containing template configuration

    Raises:
        FileNotFoundError: If config.yaml doesn't exist
        ValueError: If config.yaml is invalid

    Example:
        >>> config = load_template_config(Path("templates/web-app"))
        >>> config["name"]
        'web-app'
        >>> config["description"]
        'Full-stack web application template'
    """
    config_path = template_path / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Template config not found: {config_path}")

    try:
        with config_path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            raise ValueError(f"Invalid config format in {config_path}: expected dict")

        # Validate required fields
        required_fields = ["name", "description", "version"]
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(
                f"Missing required fields in {config_path}: {', '.join(missing_fields)}"
            )

        return config

    except yaml.YAMLError as e:
        raise ValueError(f"Failed to parse YAML in {config_path}: {e}") from e
    except Exception as e:
        raise ValueError(f"Failed to load template config from {config_path}: {e}") from e


def _get_templates_dir() -> Path:
    """Get the templates directory path.

    Returns:
        Path to templates directory
    """
    # Get the directory containing this module
    module_dir = Path(__file__).parent
    return module_dir


def _matches_project_type(normalized_input: str, template_type: str) -> bool:
    """Check if project type matches template type.

    Args:
        normalized_input: Normalized project type from user (lowercase)
        template_type: Project type pattern from template config

    Returns:
        True if types match, False otherwise
    """
    normalized_template = template_type.lower().strip()
    return normalized_input == normalized_template or normalized_input in normalized_template

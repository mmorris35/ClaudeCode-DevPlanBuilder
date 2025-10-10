"""Template rendering engine for generating project files.

This module provides functions to render claude.md and DEVELOPMENT_PLAN.md
files from Jinja2 templates using project data.
"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


def _get_templates_dir() -> Path:
    """Get the path to the templates directory.

    Returns:
        Path to the templates directory.
    """
    return Path(__file__).parent.parent / "templates"


def _create_jinja_env() -> Environment:
    """Create and configure Jinja2 environment.

    Returns:
        Configured Jinja2 Environment with FileSystemLoader.
    """
    templates_dir = _get_templates_dir()
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    return env


def render_claude_md(template_name: str, output_path: Path, **template_vars: Any) -> None:
    """Render claude.md file from template.

    Args:
        template_name: Name of the template (e.g., 'base', 'web-app')
        output_path: Path where claude.md should be written
        **template_vars: Variables to pass to the template

    Raises:
        FileNotFoundError: If template file doesn't exist
        ValueError: If template rendering fails

    Example:
        >>> render_claude_md(
        ...     'base',
        ...     Path('output/claude.md'),
        ...     project_name='My Project',
        ...     tech_stack={'Language': 'Python 3.11+'}
        ... )
    """
    env = _create_jinja_env()

    try:
        template = env.get_template(f"{template_name}/claude.md.j2")
    except Exception as e:
        raise FileNotFoundError(f"Template {template_name}/claude.md.j2 not found") from e

    try:
        rendered_content = template.render(**template_vars)
    except Exception as e:
        raise ValueError(f"Failed to render template: {e}") from e

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write rendered content
    output_path.write_text(rendered_content, encoding="utf-8")


def render_plan_md(template_name: str, output_path: Path, **template_vars: Any) -> None:
    """Render DEVELOPMENT_PLAN.md file from template.

    Args:
        template_name: Name of the template (e.g., 'base', 'web-app')
        output_path: Path where DEVELOPMENT_PLAN.md should be written
        **template_vars: Variables to pass to the template

    Raises:
        FileNotFoundError: If template file doesn't exist
        ValueError: If template rendering fails

    Example:
        >>> render_plan_md(
        ...     'base',
        ...     Path('output/DEVELOPMENT_PLAN.md'),
        ...     project_name='My Project',
        ...     phases=[...]
        ... )
    """
    env = _create_jinja_env()

    try:
        template = env.get_template(f"{template_name}/plan.md.j2")
    except Exception as e:
        raise FileNotFoundError(f"Template {template_name}/plan.md.j2 not found") from e

    try:
        rendered_content = template.render(**template_vars)
    except Exception as e:
        raise ValueError(f"Failed to render template: {e}") from e

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write rendered content
    output_path.write_text(rendered_content, encoding="utf-8")


def render_all(template_name: str, output_dir: Path, **template_vars: Any) -> dict[str, Path]:
    """Render all project files from templates.

    Args:
        template_name: Name of the template (e.g., 'base', 'web-app')
        output_dir: Directory where files should be written
        **template_vars: Variables to pass to the templates

    Returns:
        Dictionary mapping file type to output path:
        {
            'claude_md': Path('output/claude.md'),
            'plan_md': Path('output/DEVELOPMENT_PLAN.md')
        }

    Raises:
        FileNotFoundError: If template files don't exist
        ValueError: If template rendering fails

    Example:
        >>> files = render_all(
        ...     'base',
        ...     Path('output'),
        ...     project_name='My Project',
        ...     tech_stack={'Language': 'Python 3.11+'},
        ...     phases=[...]
        ... )
        >>> files['claude_md']
        Path('output/claude.md')
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define output paths
    claude_md_path = output_dir / "claude.md"
    plan_md_path = output_dir / "DEVELOPMENT_PLAN.md"

    # Render both files
    render_claude_md(template_name, claude_md_path, **template_vars)
    render_plan_md(template_name, plan_md_path, **template_vars)

    # Return paths to generated files
    return {
        "claude_md": claude_md_path,
        "plan_md": plan_md_path,
    }

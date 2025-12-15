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


def render_agent_md(template_name: str, output_path: Path, **template_vars: Any) -> None:
    """Render agent executor markdown file from template.

    Generates a specialized agent file that references CLAUDE.md, PROJECT_BRIEF.md,
    and DEVELOPMENT_PLAN.md to execute development plan subtasks.

    Args:
        template_name: Name of the template (e.g., 'base', 'web-app')
        output_path: Path where agent file should be written
        **template_vars: Variables to pass to the template

    Raises:
        FileNotFoundError: If template file doesn't exist
        ValueError: If template rendering fails

    Example:
        >>> render_agent_md(
        ...     'base',
        ...     Path('output/.claude/agents/my-project-executor.md'),
        ...     project_name='My Project',
        ...     project_name_slug='my-project',
        ...     tech_stack={'Language': 'Python 3.11+'}
        ... )
    """
    env = _create_jinja_env()

    try:
        template = env.get_template(f"{template_name}/agent.md.j2")
    except Exception as e:
        raise FileNotFoundError(f"Template {template_name}/agent.md.j2 not found") from e

    try:
        rendered_content = template.render(**template_vars)
    except Exception as e:
        raise ValueError(f"Failed to render template: {e}") from e

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write rendered content
    output_path.write_text(rendered_content, encoding="utf-8")


def _slugify(name: str) -> str:
    """Convert a project name to a kebab-case slug.

    Args:
        name: The project name to convert.

    Returns:
        A kebab-case slug suitable for filenames.

    Example:
        >>> _slugify("My Cool Project")
        'my-cool-project'
        >>> _slugify("CLI Tool v2.0")
        'cli-tool-v2-0'
    """
    import re

    # Convert to lowercase
    slug = name.lower()
    # Replace spaces and underscores with hyphens
    slug = re.sub(r"[\s_]+", "-", slug)
    # Remove any characters that aren't alphanumeric or hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    # Remove consecutive hyphens
    slug = re.sub(r"-+", "-", slug)
    # Remove leading/trailing hyphens
    slug = slug.strip("-")
    return slug


def render_all(template_name: str, output_dir: Path, **template_vars: Any) -> dict[str, Path]:
    """Render all project files from templates.

    Generates CLAUDE.md, DEVELOPMENT_PLAN.md, and an agent executor file
    in .claude/agents/{project-name}-executor.md.

    Args:
        template_name: Name of the template (e.g., 'base', 'web-app')
        output_dir: Directory where files should be written
        **template_vars: Variables to pass to the templates. Must include
            'project_name' for agent file naming.

    Returns:
        Dictionary mapping file type to output path:
        {
            'claude_md': Path('output/claude.md'),
            'plan_md': Path('output/DEVELOPMENT_PLAN.md'),
            'agent_md': Path('output/.claude/agents/{project}-executor.md')
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
        >>> files['agent_md']
        Path('output/.claude/agents/my-project-executor.md')
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate project name slug for agent file
    project_name = template_vars.get("project_name", "project")
    project_name_slug = _slugify(project_name)

    # Add slug to template vars for agent template
    agent_vars = {**template_vars, "project_name_slug": project_name_slug}

    # Define output paths
    claude_md_path = output_dir / "claude.md"
    plan_md_path = output_dir / "DEVELOPMENT_PLAN.md"
    agent_md_path = output_dir / ".claude" / "agents" / f"{project_name_slug}-executor.md"

    # Render all files
    render_claude_md(template_name, claude_md_path, **template_vars)
    render_plan_md(template_name, plan_md_path, **template_vars)
    render_agent_md(template_name, agent_md_path, **agent_vars)

    # Return paths to generated files
    return {
        "claude_md": claude_md_path,
        "plan_md": plan_md_path,
        "agent_md": agent_md_path,
    }

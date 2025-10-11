"""Command-line interface for claude-code-planner.

This module provides the main CLI entry point using Click framework.
"""

import sys

import click

from claude_planner import __version__


@click.group()
@click.version_option(version=__version__, prog_name="claude-planner")
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose output for debugging",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Claude Code Project Planner - Generate development plans from project briefs.

    This tool takes a PROJECT_BRIEF.md file as input and generates complete
    claude.md and DEVELOPMENT_PLAN.md files ready to seed new Claude Code
    project repositories.

    \b
    Examples:
        # Generate a new project plan
        claude-planner generate my-api --brief PROJECT_BRIEF.md

        # List available templates
        claude-planner list-templates

        # Validate a generated plan
        claude-planner validate DEVELOPMENT_PLAN.md

        # Show version
        claude-planner --version

    For more information on a specific command, use:
        claude-planner <command> --help
    """
    # Store verbose flag in context for sub-commands to access
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    if verbose:
        click.echo("Verbose mode enabled", err=True)


def main() -> int:
    """Main entry point for the CLI application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        cli(obj={})
        return 0
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

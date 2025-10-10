"""Main parser pipeline for PROJECT_BRIEF.md files.

This module provides the complete parsing pipeline that integrates all parser
components to convert a PROJECT_BRIEF.md file into a validated ProjectBrief
model instance.
"""

from pathlib import Path

from claude_planner.generator.brief_converter import convert_to_project_brief
from claude_planner.generator.brief_extractor import (
    extract_basic_info,
    extract_quality_requirements,
    extract_requirements,
    extract_team_info,
    extract_tech_constraints,
)
from claude_planner.generator.parser import parse_markdown_file
from claude_planner.models import ProjectBrief


def parse_project_brief(brief_path: Path) -> ProjectBrief:
    """Parse PROJECT_BRIEF.md file and return validated ProjectBrief instance.

    This function orchestrates the complete parsing pipeline:
    1. Read and parse markdown file into sections
    2. Extract fields from each section
    3. Convert extracted fields to ProjectBrief model
    4. Validate the final ProjectBrief instance

    Args:
        brief_path: Path to PROJECT_BRIEF.md file

    Returns:
        Validated ProjectBrief instance with all extracted data

    Raises:
        FileNotFoundError: If brief file doesn't exist
        ValueError: If parsing, extraction, or validation fails

    Example:
        >>> from pathlib import Path
        >>> brief = parse_project_brief(Path("PROJECT_BRIEF.md"))
        >>> brief.project_name
        'Claude Code Project Planner'
        >>> brief.project_type
        'CLI Tool, Library'
    """
    # Validate input path
    if not brief_path.exists():
        raise FileNotFoundError(f"Brief file not found: {brief_path}")

    if not brief_path.is_file():
        raise ValueError(f"Brief path is not a file: {brief_path}")

    # Stage 1: Parse markdown file into sections
    try:
        sections = parse_markdown_file(brief_path)
    except FileNotFoundError as e:
        # Re-raise with better context
        raise FileNotFoundError(f"Failed to parse brief file {brief_path}: {e}") from e
    except Exception as e:
        raise ValueError(f"Failed to parse markdown from {brief_path}: {e}") from e

    # Stage 2: Extract fields from sections
    try:
        basic_info = extract_basic_info(sections)
    except Exception as e:
        raise ValueError(f"Failed to extract basic information from brief: {e}") from e

    try:
        requirements = extract_requirements(sections)
    except Exception as e:
        raise ValueError(f"Failed to extract requirements from brief: {e}") from e

    try:
        tech_constraints = extract_tech_constraints(sections)
    except Exception as e:
        raise ValueError(f"Failed to extract technical constraints from brief: {e}") from e

    try:
        quality_requirements = extract_quality_requirements(sections)
    except Exception as e:
        raise ValueError(f"Failed to extract quality requirements from brief: {e}") from e

    try:
        team_info = extract_team_info(sections)
    except Exception as e:
        raise ValueError(f"Failed to extract team information from brief: {e}") from e

    # Stage 3: Convert to ProjectBrief model
    try:
        brief = convert_to_project_brief(
            basic_info,
            requirements,
            tech_constraints,
            quality_requirements,
            team_info,
        )
    except ValueError as e:
        # Converter already provides good error messages
        raise ValueError(f"Failed to convert extracted fields to ProjectBrief: {e}") from e
    except Exception as e:
        raise ValueError(f"Unexpected error during ProjectBrief conversion: {e}") from e

    # Stage 4: Final validation (already done in convert_to_project_brief)
    # The brief is returned fully validated
    return brief

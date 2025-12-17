"""
DevPlan MCP Server - Generate development plans via Model Context Protocol.

This MCP server exposes the ClaudeCode-DevPlanBuilder functionality as MCP tools,
enabling Claude Code and other MCP clients to directly generate and manage
development plans.

File Name      : server.py
Author         : Mike Morris
Prerequisite   : Python 3.11+, mcp, pydantic
Copyright      : (c) 2025 Mike Morris
License        : MIT
"""

from __future__ import annotations

import json
import logging
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from enum import Enum
from typing import Any

import smithery
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

# Configure logging to stderr (required for stdio transport)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("devplan_mcp")


class ResponseFormat(str, Enum):
    """Output format for tool responses."""

    MARKDOWN = "markdown"
    JSON = "json"


# =============================================================================
# Input Schemas
# =============================================================================


class ParseBriefInput(BaseModel):
    """Input for parsing a PROJECT_BRIEF.md file."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    content: str = Field(
        ...,
        description="The full content of a PROJECT_BRIEF.md file to parse",
        min_length=100,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.JSON,
        description="Output format: 'json' for structured data, 'markdown' for human-readable",
    )


class GeneratePlanInput(BaseModel):
    """Input for generating a DEVELOPMENT_PLAN.md from a project brief."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    brief_content: str = Field(
        ...,
        description="PROJECT_BRIEF.md content OR JSON-serialized ProjectBrief",
        min_length=50,
    )
    template: str | None = Field(
        default=None,
        description=(
            "Template to use: 'cli', 'web_app', 'api', 'library'. Auto-detected if not specified."
        ),
    )


class GenerateClaudeMdInput(BaseModel):
    """Input for generating a claude.md rules file."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    brief_content: str = Field(
        ...,
        description="PROJECT_BRIEF.md content OR JSON-serialized ProjectBrief",
        min_length=50,
    )
    language: str = Field(
        default="python",
        description="Primary language: 'python', 'typescript', 'go', 'rust'",
    )
    test_coverage: int = Field(
        default=80,
        description="Required test coverage percentage",
        ge=0,
        le=100,
    )


class GenerateAgentInput(BaseModel):
    """Input for generating a project executor agent file."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    brief_content: str = Field(
        ...,
        description="PROJECT_BRIEF.md content OR JSON-serialized ProjectBrief",
        min_length=50,
    )
    project_name: str = Field(
        ...,
        description="Project name (used for agent file naming)",
        min_length=1,
    )
    project_type: str = Field(
        default="cli",
        description="Project type: 'cli', 'web_app', 'api', 'library'",
    )


class ValidatePlanInput(BaseModel):
    """Input for validating a DEVELOPMENT_PLAN.md file."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    content: str = Field(
        ...,
        description="The full content of a DEVELOPMENT_PLAN.md file to validate",
        min_length=100,
    )
    strict: bool = Field(
        default=False,
        description="Enable strict validation (warnings become errors)",
    )


class ListTemplatesInput(BaseModel):
    """Input for listing available templates."""

    model_config = ConfigDict(extra="forbid")

    project_type: str | None = Field(
        default=None,
        description="Filter by project type: 'cli', 'web', 'api', 'library'",
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format",
    )


class GetSubtaskInput(BaseModel):
    """Input for retrieving a specific subtask."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    plan_content: str = Field(
        ...,
        description="The DEVELOPMENT_PLAN.md content",
        min_length=100,
    )
    subtask_id: str = Field(
        ...,
        description="Subtask ID in format 'X.Y.Z' (e.g., '1.2.3')",
        pattern=r"^\d+\.\d+\.\d+$",
    )


class UpdateProgressInput(BaseModel):
    """Input for updating subtask completion status."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    plan_content: str = Field(
        ...,
        description="The DEVELOPMENT_PLAN.md content",
        min_length=100,
    )
    subtask_id: str = Field(
        ...,
        description="Subtask ID to mark complete (format: 'X.Y.Z')",
        pattern=r"^\d+\.\d+\.\d+$",
    )
    completion_notes: str = Field(
        ...,
        description="Notes about what was completed, issues encountered, etc.",
        min_length=10,
        max_length=2000,
    )


# =============================================================================
# Server Initialization
# =============================================================================


@asynccontextmanager
async def server_lifespan() -> AsyncIterator[dict[str, Any]]:
    """Manage server lifecycle - load templates on startup."""
    logger.info("DevPlan MCP server starting up...")

    # TODO: Load templates from package resources
    templates = {
        "cli": "Command-line application template",
        "web_app": "Full-stack web application template",
        "api": "REST/GraphQL API service template",
        "library": "Reusable library/package template",
    }

    yield {"templates": templates}

    logger.info("DevPlan MCP server shutting down...")


mcp = FastMCP("devplan_mcp", lifespan=server_lifespan)


# =============================================================================
# Tool Implementations
# =============================================================================


@mcp.tool(
    name="devplan_parse_brief",
    annotations={
        "title": "Parse Project Brief",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def devplan_parse_brief(params: ParseBriefInput) -> str:
    """Parse a PROJECT_BRIEF.md file into structured data.

    Takes the raw markdown content of a project brief and extracts all fields
    into a structured ProjectBrief object. Use this to validate brief content
    or prepare it for plan generation.

    Args:
        params: ParseBriefInput containing:
            - content (str): Full PROJECT_BRIEF.md content
            - response_format (ResponseFormat): 'json' or 'markdown'

    Returns:
        str: Parsed brief as JSON object or formatted markdown summary
    """
    logger.info("Parsing project brief...")

    # TODO: Implement actual parsing from ported parser module
    # For now, return a placeholder showing the expected structure
    parsed: dict[str, Any] = {
        "name": "Extracted project name",
        "type": "cli",
        "goal": "Extracted goal statement",
        "target_users": ["User type 1", "User type 2"],
        "timeline": "2 weeks",
        "tech_stack": {
            "language": "python",
            "framework": None,
            "database": None,
        },
        "features": [
            {"name": "Feature 1", "priority": "must-have"},
            {"name": "Feature 2", "priority": "should-have"},
        ],
    }

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(parsed, indent=2)

    # Markdown format
    return f"""# Parsed Project Brief

**Name**: {parsed["name"]}
**Type**: {parsed["type"]}
**Timeline**: {parsed["timeline"]}

## Goal
{parsed["goal"]}

## Target Users
{chr(10).join("- " + str(u) for u in parsed["target_users"])}

## Features
{chr(10).join(f"- [{f['priority']}] {f['name']}" for f in parsed["features"])}
"""


@mcp.tool(
    name="devplan_generate_plan",
    annotations={
        "title": "Generate Development Plan",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def devplan_generate_plan(params: GeneratePlanInput) -> str:
    """Generate a complete DEVELOPMENT_PLAN.md from a project brief.

    Creates a comprehensive, paint-by-numbers development plan with:
    - Numbered phases, tasks, and subtasks
    - 3-7 specific deliverables per subtask
    - Prerequisites and success criteria
    - Git workflow guidance (task-level branching)
    - Task Complete checkpoints with squash merge instructions

    IMPORTANT: Every task ends with a "Task X.Y Complete - Squash Merge to Main"
    checkpoint section containing PR commands and a completion checklist.

    Args:
        params: GeneratePlanInput containing:
            - brief_content (str): PROJECT_BRIEF.md or JSON brief
            - template (Optional[str]): Template type or auto-detect

    Returns:
        str: Complete DEVELOPMENT_PLAN.md content ready for use
    """
    logger.info(f"Generating development plan using template: {params.template or 'auto'}")

    # TODO: Implement actual generation from ported generator module
    return """# Development Plan

## Phase 0: Foundation

### Task 0.1: Project Setup

**Git Strategy:**
- **Branch**: `feature/0-1-setup` (from `main`)
- **Commit Prefix**: `chore`
- **Merge**: Squash when task complete

#### Subtask 0.1.1: Initialize Repository
- [ ] Create repository structure
- [ ] Initialize package manager
- [ ] Set up virtual environment
- [ ] Install base dependencies
- [ ] Create .gitignore

**Success Criteria**: `pip install -e .` succeeds

---

### ✅ Task 0.1 Complete - Squash Merge to Main

**When all subtasks (0.1.1) are complete:**

```bash
git push -u origin feature/0-1-setup
gh pr create --title "chore: project setup" --body "Task 0.1 complete"
gh pr merge --squash --delete-branch
```

**Checklist:**
- [ ] All subtasks complete
- [ ] All tests pass
- [ ] PR created and squash merged to main
- [ ] Feature branch deleted

---

*Plan generation placeholder - full implementation pending*
"""


@mcp.tool(
    name="devplan_generate_claude_md",
    annotations={
        "title": "Generate Claude Rules",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def devplan_generate_claude_md(params: GenerateClaudeMdInput) -> str:
    """Generate a claude.md rules file for a project.

    Creates project-specific rules defining how Claude Code should work,
    including testing requirements, code quality standards, git workflow,
    and build verification steps.

    Args:
        params: GenerateClaudeMdInput containing:
            - brief_content (str): PROJECT_BRIEF.md or JSON brief
            - language (str): Primary programming language
            - test_coverage (int): Required coverage percentage

    Returns:
        str: Complete claude.md content
    """
    logger.info(f"Generating claude.md for {params.language} project")

    # TODO: Implement actual generation
    return f"""# Claude Rules for Project

## Language & Stack
- Primary: {params.language}
- Test Coverage: {params.test_coverage}%

## Development Rules

### Before Each Subtask
1. Read this file and DEVELOPMENT_PLAN.md
2. Identify the subtask deliverables
3. Check prerequisites are met

### During Development
1. Write tests alongside code
2. Run linting before commits
3. Update completion notes

### After Each Subtask
1. All tests pass
2. Coverage >= {params.test_coverage}%
3. Commit to task branch

---

*Rules generation placeholder - full implementation pending*
"""


@mcp.tool(
    name="devplan_generate_agent",
    annotations={
        "title": "Generate Executor Agent",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def devplan_generate_agent(params: GenerateAgentInput) -> str:
    """Generate a project executor agent file for .claude/agents/.

    Creates a specialized agent that knows how to execute your development plan.
    The agent file should be saved to .claude/agents/{project-name}-executor.md

    IMPORTANT: This creates a Claude Code AGENT (in .claude/agents/), NOT a slash
    command. Agents are invoked with "Use the {name} agent to..." syntax.

    Args:
        params: GenerateAgentInput containing:
            - brief_content (str): PROJECT_BRIEF.md or JSON brief
            - project_name (str): Project name for the agent
            - project_type (str): cli, web_app, api, or library

    Returns:
        str: Complete agent markdown file content with YAML frontmatter.
             Save this to .claude/agents/{project-slug}-executor.md
    """
    import re

    logger.info(f"Generating executor agent for {params.project_name}")

    # Slugify project name for filename
    slug = params.project_name.lower()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")

    # TODO: Use actual template rendering from claude_planner package
    # Build description (must be on one line in YAML frontmatter)
    desc = (
        f"PROACTIVELY use this agent to execute {params.project_name} "
        "development subtasks. Expert at DEVELOPMENT_PLAN.md execution with "
        "cross-checking, git discipline, and verification. Invoke with "
        '"execute subtask X.Y.Z" to complete a subtask entirely in one session.'
    )
    # Build the haiku-executable explanation
    haiku_desc = (
        "The DEVELOPMENT_PLAN.md you execute must be **Haiku-executable**: "
        "every subtask contains complete, copy-pasteable code. You execute "
        "mechanically - you don't infer missing imports, design function "
        "signatures, or decide file structure. If the plan is vague, STOP "
        "and ask for clarification."
    )
    return f"""---
name: {slug}-executor
description: {desc}
tools: Read, Write, Edit, Bash, Glob, Grep
model: haiku
---

# {params.project_name} Development Plan Executor

You are an expert development plan executor for **{params.project_name}**.

## CRITICAL: Haiku-Executable Expectations

{haiku_desc}

**What you expect from each subtask:**
- Complete code blocks (not snippets or descriptions)
- Explicit file paths for every file
- Every import statement listed
- Full function signatures with type hints
- Complete test files with all test methods
- Verification commands with expected output

**If a subtask is missing these, report it as incomplete before proceeding.**

---

## MANDATORY INITIALIZATION SEQUENCE

### Step 1: Read Core Documents
```
1. Read CLAUDE.md - ALL coding standards and rules
2. Read DEVELOPMENT_PLAN.md - find current phase/subtask
3. Read PROJECT_BRIEF.md - architecture reference
```

### Step 2: Parse Subtask ID
From user prompt like "execute subtask 1.2.3":
- Phase = 1
- Task = 1.2
- Subtask = 1.2.3

### Step 3: Verify Prerequisites
For each prerequisite in the subtask:
1. Check DEVELOPMENT_PLAN.md shows `[x]`
2. Cross-check the actual code exists

**If ANY prerequisite fails verification, STOP and report to user.**

### Step 4: Check Git Branch State
```bash
git status
git branch --list
```

**Branch Rules:**
- If on `main` AND starting first subtask of task → create branch
- If continuing a task → verify on correct branch
- Branch naming: `feature/X.Y-short-description`

---

## EXECUTION PROTOCOL

### Phase A: Implement Deliverables
For EACH checkbox in deliverables:
1. Create/modify the file at specified path
2. Add type hints to ALL functions
3. Add docstrings with Args/Returns/Raises
4. Mark checkbox `[x]` when complete

### Phase B: Write Tests
- Test file pattern: `tests/test_{{module}}.py`
- Test success, failure, AND edge cases
- Target >80% coverage

### Phase C: Run Verification
ALL must pass before committing:
```bash
# Linting
ruff check src tests

# Type checking
mypy src

# Tests with coverage
pytest tests/ -v --cov
```

**If ANY fails, fix immediately. Do NOT proceed until all pass.**

### Phase D: Update Documentation
1. Mark deliverables `[x]` in DEVELOPMENT_PLAN.md
2. Mark success criteria `[x]` in DEVELOPMENT_PLAN.md
3. Fill Completion Notes section

### Phase E: Git Commit
```bash
git add .
git commit -m "type(scope): description"
```

---

## GIT DISCIPLINE (MANDATORY)

| Situation | Action |
|-----------|--------|
| Starting Task X.1 first subtask | `git checkout -b feature/X.1-description` |
| Continuing Task X.1 | Stay on `feature/X.1-description` |
| Completing Task X.1 last subtask | Squash merge to main, delete branch |

### NEVER Do These
- ❌ Commit broken code
- ❌ Skip verification steps
- ❌ Force push to main
- ❌ Create branch per subtask (only per task!)

---

## OUTPUT FORMAT

When complete, report:

```
## Subtask X.Y.Z Complete ✅

**Implemented:** [List of what was done]
**Files Created:** [paths]
**Files Modified:** [paths]
**Verification:** ruff ✅, mypy ✅, pytest X tests ✅
**Git:** Branch: `feature/X.Y-desc`, Commit: `abc1234`
**Next:** Subtask X.Y.Z+1 or Task Complete
```

---

## REMEMBER

1. Complete ENTIRE subtask in ONE session
2. Cross-check prerequisites exist in code
3. Match existing project patterns exactly
4. Every session ends with a commit
5. If blocked, document and report

---

**IMPORTANT**: Save this file to `.claude/agents/{slug}-executor.md`
"""


class ValidateAgentInput(BaseModel):
    """Input for validating a Claude Code agent file."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    content: str = Field(
        ...,
        description="The full content of an agent .md file to validate",
        min_length=50,
    )


@mcp.tool(
    name="devplan_validate_plan",
    annotations={
        "title": "Validate Development Plan",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def devplan_validate_plan(params: ValidatePlanInput) -> str:
    """Validate a DEVELOPMENT_PLAN.md for completeness and consistency.

    Checks:
    - All phases have tasks, all tasks have subtasks
    - Subtasks have 3-7 deliverables
    - Prerequisites reference valid subtask IDs
    - Success criteria are defined
    - Git strategy is specified for each task
    - Task Complete checkpoint sections exist after each task

    Args:
        params: ValidatePlanInput containing:
            - content (str): DEVELOPMENT_PLAN.md content
            - strict (bool): Treat warnings as errors

    Returns:
        str: Validation report with errors, warnings, and suggestions
    """
    logger.info(f"Validating plan (strict={params.strict})")

    # TODO: Implement actual validation
    return """# Plan Validation Report

## Summary
- Errors: 0
- Warnings: 3
- Suggestions: 3

## Warnings
1. Subtask 1.2.3 has 8 deliverables (recommended: 3-7)
2. Phase 3 has no estimated duration
3. Task 2.1 is missing "Task Complete - Squash Merge" checkpoint section

## Suggestions
1. Consider adding more detail to success criteria in Task 2.1
2. Subtask 0.1.1 could be split into smaller pieces
3. Add completion notes template to all subtasks

## Required Structure

Every task MUST end with a merge checkpoint:

```markdown
### ✅ Task X.Y Complete - Squash Merge to Main

**When all subtasks (X.Y.1, X.Y.2, ...) are complete:**

git push -u origin feature/X-Y-description
gh pr create --title "type: description" --body "Task X.Y complete"
gh pr merge --squash --delete-branch

**Checklist:**
- [ ] All subtasks complete
- [ ] All tests pass
- [ ] PR created and squash merged to main
- [ ] Feature branch deleted
```

---

*Validation placeholder - full implementation pending*
"""


@mcp.tool(
    name="devplan_validate_agent",
    annotations={
        "title": "Validate Executor Agent",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def devplan_validate_agent(params: ValidateAgentInput) -> str:
    """Validate a Claude Code executor agent file for correct frontmatter format.

    Checks for common mistakes:
    - Missing YAML frontmatter delimiters (---)
    - tools field as YAML list instead of comma-separated string
    - model field set to "sonnet" instead of "haiku"
    - Missing required fields (name, description, tools, model)
    - Multi-line description field

    Args:
        params: ValidateAgentInput containing:
            - content (str): Agent .md file content

    Returns:
        str: Validation report with errors and correct format examples
    """
    import re

    logger.info("Validating agent file...")

    errors: list[str] = []
    warnings: list[str] = []

    content = params.content

    # Check for frontmatter delimiters
    if not content.startswith("---"):
        errors.append("Missing opening frontmatter delimiter (---)")

    # Find frontmatter section
    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        errors.append("Could not parse YAML frontmatter. Ensure format is:\n---\nkey: value\n---")
    else:
        frontmatter = frontmatter_match.group(1)

        # Check for required fields
        if "name:" not in frontmatter:
            errors.append("Missing required field: name")
        if "description:" not in frontmatter:
            errors.append("Missing required field: description")
        if "tools:" not in frontmatter:
            errors.append("Missing required field: tools")
        if "model:" not in frontmatter:
            errors.append("Missing required field: model")

        # Check for YAML list format for tools (common mistake)
        if re.search(r"tools:\s*\n\s+-", frontmatter):
            errors.append(
                "tools field is a YAML list but MUST be a comma-separated string.\n"
                "  ❌ Wrong:\n"
                "     tools:\n"
                "       - Read\n"
                "       - Write\n"
                "  ✅ Correct:\n"
                "     tools: Read, Write, Edit, Bash, Glob, Grep"
            )

        # Check for wrong model
        model_match = re.search(r"model:\s*(\w+)", frontmatter)
        if model_match:
            model = model_match.group(1).lower()
            if model == "sonnet":
                errors.append(
                    "model is 'sonnet' but MUST be 'haiku'.\n"
                    "  Using sonnet defeats the purpose of having an executor agent.\n"
                    "  The executor should be lightweight (haiku) since plans are Haiku-executable."
                )
            elif model not in ("haiku", "opus"):
                warnings.append(f"Unusual model '{model}'. Expected 'haiku' for executor agents.")

        # Check for multi-line description
        desc_match = re.search(r"description:\s*(.+?)(?=\n\w+:|$)", frontmatter, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1)
            if "\n" in desc.strip():
                warnings.append("description field spans multiple lines. Should be a single line.")

    # Build report
    status = "❌ INVALID" if errors else ("⚠️ WARNINGS" if warnings else "✅ VALID")

    report = f"""# Agent Validation Report

## Status: {status}

"""

    if errors:
        report += "## Errors\n\n"
        for i, error in enumerate(errors, 1):
            report += f"{i}. {error}\n\n"

    if warnings:
        report += "## Warnings\n\n"
        for i, warning in enumerate(warnings, 1):
            report += f"{i}. {warning}\n\n"

    if not errors and not warnings:
        report += "No issues found. Agent frontmatter is correctly formatted.\n\n"

    # Build correct format example (split for line length)
    example_desc = (
        "PROACTIVELY use this agent to execute ProjectName development "
        'subtasks. Invoke with "execute subtask X.Y.Z".'
    )
    report += f"""---

## Correct Agent Frontmatter Format

```yaml
---
name: project-slug-executor
description: {example_desc}
tools: Read, Write, Edit, Bash, Glob, Grep
model: haiku
---
```

**Key Rules:**
1. Frontmatter MUST be between `---` delimiters
2. `tools` MUST be a comma-separated string (NOT a YAML list)
3. `model` MUST be `haiku` (NOT `sonnet`)
4. `description` MUST be on a single line
5. `name` should be lowercase with hyphens
"""

    return report


@mcp.tool(
    name="devplan_list_templates",
    annotations={
        "title": "List Available Templates",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def devplan_list_templates(params: ListTemplatesInput) -> str:
    """List available project templates.

    Returns templates for different project types (CLI, web app, API, library)
    with descriptions and typical use cases.

    Args:
        params: ListTemplatesInput containing:
            - project_type (Optional[str]): Filter by type
            - response_format (ResponseFormat): Output format

    Returns:
        str: List of templates with descriptions
    """
    logger.info(f"Listing templates (filter={params.project_type})")

    templates = [
        {
            "name": "cli",
            "description": "Command-line application",
            "use_cases": ["Developer tools", "Automation scripts", "System utilities"],
        },
        {
            "name": "web_app",
            "description": "Full-stack web application",
            "use_cases": ["SaaS products", "Internal tools", "Customer portals"],
        },
        {
            "name": "api",
            "description": "REST or GraphQL API service",
            "use_cases": ["Backend services", "Microservices", "Data APIs"],
        },
        {
            "name": "library",
            "description": "Reusable library or package",
            "use_cases": ["SDK development", "Shared utilities", "Open source packages"],
        },
    ]

    if params.project_type:
        templates = [t for t in templates if t["name"] == params.project_type]

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(templates, indent=2)

    # Markdown format
    lines = ["# Available Templates", ""]
    for template in templates:
        lines.append(f"## {template['name']}")
        lines.append(f"{template['description']}")
        lines.append("")
        lines.append("**Use Cases:**")
        for use_case in template["use_cases"]:
            lines.append(f"- {use_case}")
        lines.append("")

    return "\n".join(lines)


@mcp.tool(
    name="devplan_get_subtask",
    annotations={
        "title": "Get Subtask Details",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def devplan_get_subtask(params: GetSubtaskInput) -> str:
    """Get details for a specific subtask by ID.

    Extracts a subtask from the development plan with full context including
    the parent task, phase, prerequisites, deliverables, and success criteria.

    Args:
        params: GetSubtaskInput containing:
            - plan_content (str): DEVELOPMENT_PLAN.md content
            - subtask_id (str): ID in format 'X.Y.Z'

    Returns:
        str: Subtask details in JSON format
    """
    logger.info(f"Getting subtask {params.subtask_id}")

    # TODO: Implement actual subtask extraction
    return json.dumps(
        {
            "id": params.subtask_id,
            "name": "Example Subtask",
            "phase": "Phase 1: Core Features",
            "task": "Task 1.2: User Authentication",
            "branch": "feature/1-2-user-auth",
            "prerequisites": ["1.1.3"],
            "deliverables": [
                "Implement login endpoint",
                "Add password hashing",
                "Create JWT token generation",
                "Write authentication tests",
            ],
            "files": ["src/auth/login.py", "tests/test_auth.py"],
            "success_criteria": "All auth tests pass, coverage > 80%",
            "completed": False,
            "completion_notes": None,
        },
        indent=2,
    )


@mcp.tool(
    name="devplan_update_progress",
    annotations={
        "title": "Update Subtask Progress",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
async def devplan_update_progress(params: UpdateProgressInput) -> str:
    """Mark a subtask as complete and add completion notes.

    Updates the DEVELOPMENT_PLAN.md content with:
    - Checkbox marked as complete [x]
    - Completion notes added
    - Timestamp recorded

    Args:
        params: UpdateProgressInput containing:
            - plan_content (str): Current DEVELOPMENT_PLAN.md content
            - subtask_id (str): ID to mark complete
            - completion_notes (str): Notes about completion

    Returns:
        str: Updated DEVELOPMENT_PLAN.md content
    """
    logger.info(f"Marking subtask {params.subtask_id} as complete")

    # TODO: Implement actual plan update
    # This would parse the plan, find the subtask, update checkbox, add notes
    return f"""# Updated Plan

Subtask {params.subtask_id} marked complete.

**Completion Notes:**
{params.completion_notes}

---

*Progress update placeholder - returns modified plan content*
"""


# =============================================================================
# Resources
# =============================================================================


@mcp.resource("templates://list")
async def list_template_resource() -> str:
    """List all available templates as a resource."""
    return json.dumps(
        {
            "templates": ["cli", "web_app", "api", "library"],
            "description": "Available project templates for development plan generation",
        }
    )


@mcp.resource("templates://{name}")
async def get_template_resource(name: str) -> str:
    """Get a specific template by name."""
    templates = {
        "cli": "CLI application template content...",
        "web_app": "Web application template content...",
        "api": "API service template content...",
        "library": "Library template content...",
    }

    if name not in templates:
        return json.dumps({"error": f"Template '{name}' not found"})

    return templates[name]


# =============================================================================
# Smithery Entry Point
# =============================================================================


@smithery.server()
def create_server() -> FastMCP:
    """Create and return the FastMCP server instance for Smithery deployment.

    This function is called by Smithery to instantiate the server.
    The @smithery.server() decorator handles configuration and lifecycle.

    Returns:
        FastMCP: The configured MCP server instance
    """
    return mcp


# =============================================================================
# CLI Entry Point
# =============================================================================


def main() -> None:
    """Run the DevPlan MCP server (for local/standalone use)."""
    import argparse

    parser = argparse.ArgumentParser(description="DevPlan MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="devplan-mcp 0.1.0",
    )

    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="streamable_http", port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()

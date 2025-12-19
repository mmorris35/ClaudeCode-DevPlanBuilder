# DevPlan MCP Server Requirements

## Overview

Convert the ClaudeCode-DevPlanBuilder CLI tool into an MCP (Model Context Protocol) server that enables Claude Code and other MCP-enabled clients to directly invoke development planning tools.

## Source Repository

https://github.com/mmorris35/ClaudeCode-DevPlanBuilder

## Functional Requirements

### Tools to Expose

1. **devplan_parse_brief**
   - Input: PROJECT_BRIEF.md content (string)
   - Output: Parsed ProjectBrief structure (JSON)
   - Purpose: Parse a project brief into structured data

2. **devplan_generate_plan**
   - Input: ProjectBrief JSON or PROJECT_BRIEF.md content
   - Output: DEVELOPMENT_PLAN.md content
   - Purpose: Generate a complete development plan with phases, tasks, subtasks

3. **devplan_generate_claude_md**
   - Input: ProjectBrief JSON, tech_stack preferences
   - Output: claude.md content
   - Purpose: Generate project-specific rules for Claude Code

4. **devplan_validate_plan**
   - Input: DEVELOPMENT_PLAN.md content
   - Output: Validation report (errors, warnings, suggestions)
   - Purpose: Validate a development plan for completeness and consistency

5. **devplan_list_templates**
   - Input: None (or optional filter)
   - Output: List of available templates with descriptions
   - Purpose: Show available project type templates

6. **devplan_get_subtask**
   - Input: plan content, subtask_id (e.g., "1.2.3")
   - Output: Subtask details with deliverables, files, success criteria
   - Purpose: Extract specific subtask for execution

7. **devplan_update_progress**
   - Input: plan content, subtask_id, completion_notes
   - Output: Updated plan content with checkbox marked and notes added
   - Purpose: Update plan with completion status

### Resources to Expose

1. **templates://list**
   - List all available templates

2. **templates://{template_name}**
   - Get specific template content

## Technical Requirements

### Stack
- Python 3.11+
- FastMCP (MCP Python SDK)
- Pydantic v2 for input validation
- Jinja2 for templates (existing in source)

### Transport
- Primary: stdio (for local Claude Code integration)
- Secondary: streamable_http (for remote/multi-client scenarios)

### Dependencies from Source
- The existing claude_planner package modules:
  - models (ProjectBrief, Phase, Task, Subtask, TechStack)
  - parser (markdown parser, field extractor)
  - templates (template selector, Jinja2 renderer)
  - generators (tech stack, phase, task, subtask generators)
  - validators (validation rules engine)

## Non-Functional Requirements

### Performance
- Plan generation should complete within 5 seconds
- Validation should complete within 2 seconds

### Error Handling
- Clear, actionable error messages
- Validation errors should include line numbers where applicable
- Suggestions for fixing common issues

### Documentation
- Each tool must have comprehensive docstrings
- Input/output schemas fully documented
- Examples for each tool

## Out of Scope (Phase 1)

- Git integration (branch creation, commits)
- Interactive brief creation wizard
- Real-time progress tracking across sessions
- Multi-project management

## Success Criteria

1. All tools callable via MCP protocol
2. Can generate a complete plan from PROJECT_BRIEF.md
3. Can validate existing plans
4. Works with Claude Code via stdio transport
5. Passes MCP Inspector testing

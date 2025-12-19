# DevPlan MCP Server - Implementation Plan

## Phase 0: Project Setup (0.1)

### Task 0.1: Repository and Environment Setup

#### Subtask 0.1.1: Initialize Project Structure
- Create pyproject.toml with MCP dependencies
- Set up src/devplan_mcp package structure
- Create virtual environment
- Install development dependencies (pytest, ruff, mypy)
- **Files**: pyproject.toml, src/devplan_mcp/__init__.py

#### Subtask 0.1.2: Port Core Models
- Port ProjectBrief, Phase, Task, Subtask models from source repo
- Port TechStack and related models
- Add Pydantic v2 compatibility updates
- Write model tests
- **Files**: src/devplan_mcp/models.py, tests/test_models.py

#### Subtask 0.1.3: Port Parser Module
- Port markdown parser functionality
- Port field extractor
- Port ProjectBrief converter
- Write parser tests
- **Files**: src/devplan_mcp/parser.py, tests/test_parser.py

#### Subtask 0.1.4: Port Templates
- Copy Jinja2 templates from source repo
- Port template selector
- Port renderer utilities
- Write template tests
- **Files**: src/devplan_mcp/templates/, src/devplan_mcp/renderer.py

#### Subtask 0.1.5: Port Generators
- Port tech stack generator
- Port phase/task/subtask generators
- Port integration logic
- Write generator tests
- **Files**: src/devplan_mcp/generators.py, tests/test_generators.py

---

## Phase 1: MCP Server Core (1.1-1.2)

### Task 1.1: Server Initialization

#### Subtask 1.1.1: Create MCP Server Entry Point
- Initialize FastMCP server with name "devplan_mcp"
- Configure logging (stderr for stdio transport)
- Set up lifespan management for templates
- **Files**: src/devplan_mcp/server.py

#### Subtask 1.1.2: Define Input/Output Schemas
- Create Pydantic models for all tool inputs
- Define response format enum (markdown/json)
- Add validation constraints and descriptions
- **Files**: src/devplan_mcp/schemas.py

### Task 1.2: Implement Core Tools

#### Subtask 1.2.1: Implement devplan_parse_brief
- Parse PROJECT_BRIEF.md content to ProjectBrief
- Return structured JSON or formatted markdown
- Handle parsing errors gracefully
- **Files**: src/devplan_mcp/tools/parse_brief.py

#### Subtask 1.2.2: Implement devplan_generate_plan
- Accept brief as JSON or markdown string
- Generate DEVELOPMENT_PLAN.md content
- Support template selection parameter
- **Files**: src/devplan_mcp/tools/generate_plan.py

#### Subtask 1.2.3: Implement devplan_generate_claude_md
- Generate project-specific claude.md
- Support tech stack customization
- Include testing and quality gate configuration
- **Files**: src/devplan_mcp/tools/generate_claude.py

#### Subtask 1.2.4: Implement devplan_validate_plan
- Validate plan structure and completeness
- Check subtask sizing (3-7 deliverables)
- Verify prerequisites are valid
- Return validation report
- **Files**: src/devplan_mcp/tools/validate_plan.py

#### Subtask 1.2.5: Implement devplan_list_templates
- Return available project templates
- Include template descriptions and use cases
- Support filtering by project type
- **Files**: src/devplan_mcp/tools/list_templates.py

---

## Phase 2: Progress Management Tools (2.1)

### Task 2.1: Subtask Operations

#### Subtask 2.1.1: Implement devplan_get_subtask
- Extract subtask by ID (e.g., "1.2.3")
- Return full subtask details
- Include context (task name, phase, prerequisites)
- **Files**: src/devplan_mcp/tools/get_subtask.py

#### Subtask 2.1.2: Implement devplan_update_progress
- Mark subtask checkbox as complete
- Add completion notes
- Update the plan content
- Return modified plan
- **Files**: src/devplan_mcp/tools/update_progress.py

#### Subtask 2.1.3: Implement devplan_get_next_subtask
- Find next incomplete subtask
- Consider prerequisites
- Return subtask details
- **Files**: src/devplan_mcp/tools/get_next.py

---

## Phase 3: Resources and Testing (3.1-3.2)

### Task 3.1: MCP Resources

#### Subtask 3.1.1: Implement Template Resources
- Register templates://list resource
- Register templates://{name} resource
- Support template content retrieval
- **Files**: src/devplan_mcp/resources.py

### Task 3.2: Integration Testing

#### Subtask 3.2.1: Server Integration Tests
- Test server startup and shutdown
- Test tool registration
- Test resource registration
- **Files**: tests/test_server_integration.py

#### Subtask 3.2.2: End-to-End Workflow Tests
- Test complete brief -> plan workflow
- Test plan validation workflow
- Test progress update workflow
- **Files**: tests/test_e2e.py

#### Subtask 3.2.3: MCP Inspector Testing
- Verify all tools discoverable
- Test tool invocations
- Verify response formats
- Document test results
- **Files**: devlog/mcp-inspector-testing.md

---

## Phase 4: Documentation and Distribution (4.1)

### Task 4.1: Packaging

#### Subtask 4.1.1: Create README and Documentation
- Write installation instructions
- Document all tools with examples
- Add Claude Code configuration example
- **Files**: README.md, docs/

#### Subtask 4.1.2: Package Configuration
- Finalize pyproject.toml for distribution
- Add entry point for CLI: `devplan-mcp`
- Create GitHub Actions for CI/CD
- **Files**: pyproject.toml, .github/workflows/

---

## Git Workflow

Each **task** gets one feature branch:
- `feature/0-1-setup`
- `feature/1-1-server-init`
- `feature/1-2-core-tools`
- `feature/2-1-subtask-ops`
- `feature/3-1-resources`
- `feature/3-2-integration-tests`
- `feature/4-1-packaging`

Subtasks commit to their task's branch. Squash merge when task complete.

---

## Current Status

**Phase**: 0 (Setup)
**Current Subtask**: 0.1.1
**Notes**: Awaiting network access to clone source repo models

# 3 Core Files for claude-code-project-planner

Copy each section below into its respective file.

---
---
---

# FILE 1: PROJECT_BRIEF.md

```markdown
# Project Brief: Claude Code Project Planner

## Basic Information

- **Project Name**: Claude Code Project Planner
- **Project Type**: [x] CLI Tool + [x] Library
- **Primary Goal**: A tool that takes a PROJECT_BRIEF.md as input and produces complete, validated claude.md and DEVELOPMENT_PLAN.md files ready to seed new Claude Code project repositories
- **Target Users**: Developers (including yourself) who want to quickly bootstrap new projects with Claude Code
- **Timeline**: 2 weeks
- **Team Size**: 1 senior developer (you)

## Functional Requirements

### Input
What does the system receive?

- PROJECT_BRIEF.md file (filled-out questionnaire)
- Project ID/name for the new project
- Optional: Technology preferences override
- Optional: Template selection (web-app, api, cli)
- Configuration file for customizations (company standards, etc.)

### Output
What does the system produce?

- claude.md (customized behavior rules)
- DEVELOPMENT_PLAN.md (complete roadmap with all subtasks)
- Repository structure (directories, .gitignore, etc.)
- README.md (setup instructions)
- Validation report (quality checks)
- Optional: Git repository initialization

### Key Features
(MVP - must-haves)

1. **CLI Command**: `claude-planner generate my-project --brief PROJECT_BRIEF.md` creates complete project plan
2. **Template Library**: Pre-built templates (web-app, api, cli) from the Kit
3. **Validation Engine**: Check generated plans for quality (subtask size, prerequisites, etc.)
4. **Customization System**: Support company-specific rules via config file
5. **Interactive Mode**: Walk user through PROJECT_BRIEF.md if file not provided

### Nice-to-Have Features
(v2 - not MVP)

- Web UI for generating plans (no CLI needed)
- Integration with Claude API for auto-generation
- Project evolution (update existing DEVELOPMENT_PLAN.md)
- Export to other formats (Jira, Linear, Notion)
- Analytics on generated plans (average subtask count, etc.)
- Team templates (save and share custom templates)

## Technical Constraints

### Must Use
- Python 3.11+ (you're familiar, good CLI support)
- Click framework (excellent CLI library)
- Jinja2 (template engine for generating files)
- PyYAML (for config files)
- Git via subprocess (for repo initialization)

### Cannot Use
- GUI frameworks (CLI only for MVP)
- External APIs unless explicitly configured (should work offline)
- Databases (keep it simple, file-based)

### Deployment Target
- [x] Local only (runs on developer's machine)
- Must support: Linux, macOS, Windows 10+
- Distributed as: pip package (pypi) or standalone binary

### Budget Constraints
- [x] Free/open-source only

## Quality Requirements

### Performance
- **Generation Time**: <5 seconds for basic plan (without Claude API)
- **Generation Time with API**: <2 minutes for complete plan
- **Memory Usage**: <200 MB
- **Startup Time**: <1 second

### Security
- **Authentication**: N/A (local tool)
- **Data Sensitivity**: [x] Internal (project plans may contain company info)
- **Encryption**: N/A (files stored locally)
- **API Keys**: Support environment variables for Claude API key

### Scalability
- **Plan Size**: Handle projects with 200+ subtasks
- **Template Count**: Support 50+ custom templates
- **Concurrent Usage**: N/A (single-user tool)

### Availability
- **Offline Mode**: Must work without internet (for basic generation)
- **API Mode**: Optional Claude API integration for enhanced generation

## Team & Resources

### Team Composition
- **Skill Levels**: [x] Senior (you, with extensive Python and Claude Code experience)
- **Roles**: [x] Full-stack (CLI + library + documentation)

### Existing Knowledge
- Python (expert level)
- Click (CLI frameworks)
- Jinja2 (template engines)
- Git (version control)
- Claude Code (extensive experience)
- The Project Initialization Kit (you created it!)

### Learning Budget
- [ ] None - using only familiar technologies

### Infrastructure Access
- **Development**: [x] Local machines (your Ubuntu 24.04 + Mac Mini)
- **CI/CD**: [x] GitHub Actions (for testing and releases)
- **Distribution**: [x] PyPI (Python Package Index)

## Success Criteria

How will we know this project succeeded?

1. **Self-Hosting**: Use this tool to generate its own development plan (dogfooding)
2. **Speed**: Generate a complete plan in <5 seconds (without API) or <2 min (with API)
3. **Quality**: Generated plans pass validation with 0 errors
4. **Usability**: You can create new project plans without referring to docs
5. **Distribution**: Available on PyPI, installable via `pip install claude-code-planner`

## Integration Requirements

### External Systems
- System: Anthropic Claude API | Purpose: Optional AI-enhanced generation | API Type: REST | Auth: API key (optional)
- System: Git | Purpose: Repository initialization | API Type: CLI subprocess | Auth: None

### Data Sources
- Source: PROJECT_BRIEF.md | Type: Markdown file | Frequency: On-demand
- Source: Template library | Type: Jinja2 templates + YAML | Frequency: On-demand
- Source: Config file | Type: YAML | Frequency: Once per invocation

### Data Destinations
- Destination: New project directory | Type: Files (claude.md, DEVELOPMENT_PLAN.md, etc.) | Format: Markdown | Frequency: On-demand
- Destination: Git repository | Type: Version control | Format: Git | Frequency: Optional (on-demand)

## Known Challenges

1. **Template Flexibility**: Templates must be generic enough for any project yet specific enough to be useful. Need good abstraction.
2. **Subtask Sizing**: Automatically breaking features into "single session" subtasks is hard. May need AI assistance or conservative splitting.
3. **Prerequisite Detection**: Determining which subtasks depend on others requires understanding project structure. May need heuristics.
4. **Cross-Platform Path Handling**: Windows uses backslashes, Unix uses forward slashes. Need careful path handling.
5. **Validation Accuracy**: False positives (flagging good plans) or false negatives (missing issues) would reduce trust.

## Reference Materials

- The Project Initialization Kit (all artifacts created above)
- Click documentation: https://click.palletsprojects.com/
- Jinja2 documentation: https://jinja.palletsprojects.com/
- Anthropic API: https://docs.anthropic.com/
- Similar tools: cookiecutter (Python project templates), yeoman (JS scaffolding)

## Questions & Clarifications Needed

1. **Template Format**: Store as Jinja2 files or Python code? → Decision: Jinja2 (easier to edit, version)
2. **Validation Rules**: How strict? → Decision: Errors must block, warnings are OK
3. **Git Integration**: Auto-init or user does it? → Decision: Optional flag `--init-git`
4. **API Integration**: Default on or off? → Decision: Off by default (privacy), opt-in via `--use-api`
5. **Config Location**: Where to store user config? → Decision: `~/.claude-planner/config.yaml` or `./claude-planner.yaml` in project

**Decisions Made**:
- Jinja2 templates for flexibility
- Strict validation (block on errors, warn on issues)
- Optional git initialization (`--init-git` flag)
- Claude API opt-in only (`--use-api` flag)
- Config hierarchy: project dir > home dir > defaults

## Architecture Vision

```
Input: PROJECT_BRIEF.md
        ↓
    [Parser] → Extract requirements
        ↓
    [Template Selector] → Choose base template (web-app/api/cli)
        ↓
    [Plan Generator]
        ├─ [Tech Stack Generator] → Choose technologies
        ├─ [Phase Generator] → Break into phases
        ├─ [Task Generator] → Break into tasks
        └─ [Subtask Generator] → Break into single-session subtasks
        ↓
    [Template Engine] → Render claude.md + DEVELOPMENT_PLAN.md
        ↓
    [Validator] → Check quality
        ↓
    [Output] → Write files to disk
        ↓
    [Optional: Git Init] → Initialize repository
```

## Use Cases

### Use Case 1: Quick Project Bootstrap
```bash
# You have a PROJECT_BRIEF.md ready
claude-planner generate my-new-api --brief brief.md --template api

# Output:
# ✅ Generated claude.md
# ✅ Generated DEVELOPMENT_PLAN.md (47 subtasks)
# ✅ Validation passed (0 errors, 2 warnings)
# ✅ Project ready in: ./my-new-api/
```

### Use Case 2: Interactive Mode
```bash
# No brief file? Interactive prompts
claude-planner generate my-app --interactive

# Prompts you for:
# - Project type? (web-app/api/cli)
# - Tech stack preferences?
# - Timeline?
# - Key features?
# Then generates plan
```

### Use Case 3: Enhanced with Claude API
```bash
# Use Claude API for better plans
export ANTHROPIC_API_KEY=your_key
claude-planner generate my-app --brief brief.md --use-api

# Runs all 10 prompts through Claude API
# Higher quality but takes ~2 minutes
```

### Use Case 4: Seed New Repo
```bash
# Generate plan AND initialize git
claude-planner generate my-app --brief brief.md --init-git

# Output:
# ✅ Generated claude.md
# ✅ Generated DEVELOPMENT_PLAN.md
# ✅ Initialized git repository
# ✅ Created initial commit
#
# Next: cd my-app && git remote add origin <url>
```

## Project Deliverables

At the end of this 2-week project, you'll have:

1. **CLI Tool**: `claude-planner` command with `generate`, `validate`, `list-templates` commands
2. **Template Library**: 3+ project templates (web-app, api, cli)
3. **Validator**: Checks plans for quality issues
4. **Documentation**: README, usage guide, template creation guide
5. **Tests**: Unit tests for all core functionality (>80% coverage)
6. **Distribution**: Published to PyPI, installable via pip
7. **Example Plans**: Generate plans for 5 different projects to test

---

**Next Step**: Use this brief with the planning prompts to generate claude.md and DEVELOPMENT_PLAN.md for this project. Then use Claude Code to BUILD the tool using its own generated plan. Meta! 🎉
```

---
---
---

# FILE 2: claude.md

```markdown
# Claude Code Development Rules - Project Planner

> This document defines HOW Claude Code should work on the claude-code-project-planner project.
> Read at the start of every session to maintain consistency.

## Core Operating Principles

### 1. Single Session Execution
- ✅ Complete the ENTIRE subtask in this session
- ✅ End every session with a git commit
- ❌ If blocked, document why and mark as BLOCKED

### 2. Read Before Acting
**Every session must begin with:**
1. Read DEVELOPMENT_PLAN.md completely
2. Locate the specific subtask ID from the prompt
3. Verify prerequisites are marked `[x]` complete
4. Read completion notes from prerequisites for context

### 3. File Management

**Project Structure:**
```
claude-code-project-planner/
├── claude_planner/              # Main package
│   ├── __init__.py
│   ├── cli.py                   # Click CLI commands
│   ├── generator/               # Plan generation
│   │   ├── parser.py           # Parse PROJECT_BRIEF.md
│   │   ├── template_selector.py
│   │   ├── plan_builder.py
│   │   └── renderer.py         # Jinja2 rendering
│   ├── validator/              # Plan validation
│   │   ├── rules.py
│   │   └── reporter.py
│   ├── templates/              # Jinja2 templates
│   │   ├── web-app/
│   │   ├── api/
│   │   └── cli/
│   └── utils/
│       ├── git.py              # Git operations
│       └── config.py           # Config management
├── tests/
│   ├── test_parser.py
│   ├── test_generator.py
│   ├── test_validator.py
│   └── fixtures/
├── docs/
├── examples/                    # Example generated plans
├── pyproject.toml              # Project metadata
├── setup.py                    # Package setup
├── README.md
├── claude.md                   # This file
└── DEVELOPMENT_PLAN.md         # Development roadmap
```

**Creating Files:**
- Use exact paths specified in subtask
- Add proper module docstrings
- Include type hints on all functions

**Modifying Files:**
- Only modify files listed in subtask
- Preserve existing functionality
- Update related tests

### 4. Testing Requirements

**Unit Tests:**
- Write tests for EVERY new function/class
- Place in `tests/` with `test_` prefix
- Minimum coverage: 80% overall
- Test success, failure, and edge cases

**Running Tests:**
```bash
# All tests
pytest tests/ -v --cov=claude_planner --cov-report=term-missing

# Specific test file
pytest tests/test_parser.py -v

# With coverage report
pytest --cov=claude_planner --cov-report=html
open htmlcov/index.html
```

**Before Every Commit:**
- [ ] All tests pass
- [ ] Coverage >80%
- [ ] Linting passes (ruff)
- [ ] Type checking passes (mypy)

### 5. Completion Protocol

**When a subtask is complete:**

1. **Update DEVELOPMENT_PLAN.md** with completion notes:
```markdown
**Completion Notes:**
- **Implementation**: Brief description of what was built
- **Files Created**:
  - `claude_planner/parser.py` (234 lines)
  - `tests/test_parser.py` (156 lines)
- **Files Modified**:
  - `claude_planner/__init__.py` (added parser import)
- **Tests**: 12 unit tests (85% coverage)
- **Build**: ✅ Success (all tests pass, linting clean)
- **Branch**: feature/subtask-X-Y-Z
- **Notes**: Any deviations, issues, or future work
```

2. **Check all checkboxes** in the subtask (change `[ ]` to `[x]`)

3. **Git commit** with semantic message:
```bash
git add .
git commit -m "feat(parser): Implement PROJECT_BRIEF.md parser

- Parse YAML frontmatter and markdown content
- Extract all required fields with validation
- Add comprehensive tests for edge cases
- 85% coverage on parser module"
```

4. **Report completion** with summary

### 6. Technology Decisions

**Tech Stack:**
- **Language**: Python 3.11+
- **CLI Framework**: Click 8.1+
- **Template Engine**: Jinja2 3.1+
- **Config Format**: PyYAML 6.0+
- **Testing**: pytest 7.4+, pytest-cov
- **Linting**: ruff 0.1+
- **Type Checking**: mypy 1.7+
- **Distribution**: setuptools, wheel

**Key Dependencies:**
```
click==8.1.7
jinja2==3.1.2
pyyaml==6.0.1
pytest==7.4.3
pytest-cov==4.1.0
ruff==0.1.6
mypy==1.7.1
anthropic==0.21.0  # Optional, for --use-api
```

**Installing Dependencies:**
```bash
pip install -e ".[dev]"  # Editable install with dev dependencies
```

### 7. Error Handling

**If you encounter an error:**
1. Attempt to fix using project patterns
2. If blocked, update DEVELOPMENT_PLAN.md:
   ```markdown
   **Completion Notes:**
   - **Status**: ❌ BLOCKED
   - **Error**: [Detailed error message]
   - **Attempted**: [What was tried]
   - **Root Cause**: [Analysis]
   - **Suggested Fix**: [What should be done]
   ```
3. Do NOT mark subtask complete if blocked
4. Do NOT commit broken code
5. Report immediately

### 8. Code Quality Standards

**Python Style:**
- Follow PEP 8
- Type hints on all functions: `def func(x: int) -> str:`
- Docstrings: Google style
- Max line length: 100 characters
- Use `ruff` for linting
- Use `mypy` for type checking

**Example Function:**
```python
def parse_brief(brief_path: Path) -> ProjectBrief:
    """Parse PROJECT_BRIEF.md file and extract requirements.

    Args:
        brief_path: Path to PROJECT_BRIEF.md file

    Returns:
        ProjectBrief object with all extracted fields

    Raises:
        FileNotFoundError: If brief file doesn't exist
        ValueError: If brief is malformed or missing required fields

    Example:
        >>> brief = parse_brief(Path("PROJECT_BRIEF.md"))
        >>> brief.project_name
        'TaskMaster Pro'
    """
    if not brief_path.exists():
        raise FileNotFoundError(f"Brief file not found: {brief_path}")

    # Implementation...
```

**Imports:**
- Standard library first
- Third-party second
- Local imports last
- Alphabetical within each group

**No:**
- `print()` for output (use Click.echo or logging)
- `exit()` (raise exceptions instead)
- Bare `except:` (catch specific exceptions)
- Global variables (use classes or pass parameters)

### 9. CLI Design Standards

**Command Structure:**
```bash
claude-planner <command> [options] [arguments]
```

**All commands must:**
- Have `--help` text with examples
- Use Click's option validation
- Provide clear error messages
- Support `--verbose` for debug output
- Return proper exit codes (0=success, 1=error)

**Example Command:**
```python
@click.command()
@click.argument('project_name')
@click.option('--brief', type=click.Path(exists=True), required=True,
              help='Path to PROJECT_BRIEF.md file')
@click.option('--template', type=click.Choice(['web-app', 'api', 'cli']),
              default='web-app', help='Project template to use')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def generate(project_name: str, brief: str, template: str, verbose: bool):
    """Generate claude.md and DEVELOPMENT_PLAN.md for a new project.

    Example:
        claude-planner generate my-api --brief brief.md --template api
    """
    # Implementation...
```

### 10. Build Verification

**Before marking subtask complete:**

```bash
# Linting
ruff check claude_planner tests

# Type checking
mypy claude_planner

# Tests
pytest tests/ -v --cov=claude_planner --cov-report=term-missing

# Build package
python -m build

# Install and test CLI
pip install -e .
claude-planner --help
```

**All must pass with no errors.**

## Project-Specific Rules

### Template Development

**When creating Jinja2 templates:**
- Use `{{ variable }}` for substitution
- Use `{% for item in list %}` for loops
- Use `{% if condition %}` for conditionals
- Add comments: `{# This is a comment #}`
- Test templates with example data

**Template Variables:**
- `project_name` - Project name from brief
- `tech_stack` - Dictionary of technology choices
- `phases` - List of Phase objects
- `tasks` - List of Task objects per phase
- `subtasks` - List of Subtask objects per task

### Validation Rules

**Subtask Validation:**
- 3-7 deliverables (error if outside range)
- Prerequisites must reference existing subtasks (error if not found)
- Subtask ID format: `\d+\.\d+\.\d+` (error if malformed)
- Must have "(Single Session)" suffix (warning if missing)

**Plan Validation:**
- All phases must have at least 1 task
- All tasks must have at least 1 subtask
- No circular dependencies (error if found)
- Phase 0 must be "Foundation" (warning if not)

### Git Operations

**When using subprocess for git:**
```python
import subprocess

def git_init(project_dir: Path) -> None:
    """Initialize git repository in project directory."""
    subprocess.run(
        ['git', 'init'],
        cwd=project_dir,
        check=True,
        capture_output=True,
        text=True
    )
```

**Always:**
- Use `check=True` to catch errors
- Use `capture_output=True` for clean output
- Use `cwd=project_dir` to run in correct directory
- Handle `CalledProcessError` exceptions

## Checklist: Starting a New Session

- [ ] Read DEVELOPMENT_PLAN.md completely
- [ ] Locate subtask ID from prompt
- [ ] Verify prerequisites marked `[x]`
- [ ] Read prerequisite completion notes
- [ ] Understand success criteria
- [ ] Ready to code!

## Checklist: Ending a Session

- [ ] All subtask checkboxes checked
- [ ] All tests pass (pytest)
- [ ] Linting clean (ruff)
- [ ] Type checking clean (mypy)
- [ ] Completion notes written
- [ ] Git commit with semantic message
- [ ] User notified

---

**Version**: 1.0
**Last Updated**: 2024-10-09
**Project**: claude-code-project-planner
```

---
---
---

# FILE 3: DEVELOPMENT_PLAN.md

```markdown
# claude-code-project-planner - Development Plan

## 🎯 How to Use This Plan

**For Claude Code**: Read this plan, find the subtask ID from the prompt, complete ALL checkboxes, update completion notes, commit.

**For You**: Use this prompt (change only the subtask ID):
```
please re-read claude.md and DEVELOPMENT_PLAN.md (the entire documents, for context, I know it will eat tokens and take time), then continue with [X.Y.Z], following all of the development plan and claude.md rules.
```

---

## Project Overview

**Project Name**: claude-code-project-planner

**Goal**: A CLI tool that takes PROJECT_BRIEF.md as input and produces complete claude.md + DEVELOPMENT_PLAN.md files ready to seed new Claude Code project repositories

**Target Users**: Developers (including yourself) bootstrapping new projects

**Timeline**: 2 weeks (10 phases)

**MVP Scope**:
- ✅ CLI with `generate`, `validate`, `list-templates` commands
- ✅ Template library (web-app, api, cli)
- ✅ Validation engine
- ✅ Git integration (optional)
- ❌ Web UI (v2)
- ❌ Claude API integration (v2)

---

## Technology Stack

**Language**: Python 3.11+
**CLI Framework**: Click 8.1+
**Template Engine**: Jinja2 3.1+
**Config Format**: PyYAML 6.0+
**Testing**: pytest 7.4+, pytest-cov
**Linting**: ruff 0.1+
**Type Checking**: mypy 1.7+
**Distribution**: setuptools, PyPI

**Key Libraries**: click, jinja2, pyyaml, pytest

---

## Progress Tracking

### Phase 0: Foundation (Week 1, Days 1-2)
- [ ] 0.1.1: Initialize Git Repository
- [ ] 0.1.2: Python Package Structure
- [ ] 0.1.3: Development Dependencies
- [ ] 0.2.1: Pre-commit Hooks
- [ ] 0.2.2: CI/CD Pipeline

### Phase 1: Core Data Models (Week 1, Days 2-3)
- [ ] 1.1.1: ProjectBrief Dataclass
- [ ] 1.1.2: Phase/Task/Subtask Models
- [ ] 1.1.3: TechStack Model
- [ ] 1.2.1: Model Validation

### Phase 2: PROJECT_BRIEF Parser (Week 1, Days 3-4)
- [ ] 2.1.1: Markdown Parser
- [ ] 2.1.2: Field Extractor
- [ ] 2.1.3: Validator Integration
- [ ] 2.2.1: Parser Tests

### Phase 3: Template System (Week 1, Days 4-5)
- [ ] 3.1.1: Template Selector
- [ ] 3.1.2: Jinja2 Template - claude.md
- [ ] 3.1.3: Jinja2 Template - DEVELOPMENT_PLAN.md
- [ ] 3.2.1: Template Renderer
- [ ] 3.3.1: Web-App Template
- [ ] 3.3.2: API Template
- [ ] 3.3.3: CLI Template

### Phase 4: Plan Generator (Week 2, Days 1-2)
- [ ] 4.1.1: Tech Stack Generator
- [ ] 4.1.2: Phase Generator
- [ ] 4.1.3: Task Generator
- [ ] 4.1.4: Subtask Generator
- [ ] 4.2.1: Generator Tests

### Phase 5: CLI Commands (Week 2, Days 2-3)
- [ ] 5.1.1: CLI Entry Point
- [ ] 5.1.2: Generate Command
- [ ] 5.1.3: Validate Command
- [ ] 5.1.4: List Templates Command
- [ ] 5.2.1: CLI Tests

### Phase 6: Validation Engine (Week 2, Days 3-4)
- [ ] 6.1.1: Validation Rules
- [ ] 6.1.2: Subtask Validator
- [ ] 6.1.3: Plan Validator
- [ ] 6.1.4: Validation Reporter
- [ ] 6.2.1: Validator Tests

### Phase 7: Git Integration (Week 2, Day 4)
- [ ] 7.1.1: Git Init Utility
- [ ] 7.1.2: Initial Commit Creator
- [ ] 7.1.3: Git Integration Tests

### Phase 8: Testing & Documentation (Week 2, Day 5)
- [ ] 8.1.1: Integration Tests
- [ ] 8.1.2: End-to-End Tests
- [ ] 8.1.3: Coverage Report
- [ ] 8.2.1: README Documentation
- [ ] 8.2.2: Usage Guide
- [ ] 8.2.3: Template Creation Guide

### Phase 9: Packaging & Distribution (Week 2, Day 5)
- [ ] 9.1.1: setup.py Configuration
- [ ] 9.1.2: PyPI Package Build
- [ ] 9.1.3: Installation Test
- [ ] 9.1.4: PyPI Upload

### Phase 10: Dogfooding (Ongoing)
- [ ] 10.1.1: Use Tool to Generate 5 Example Plans
- [ ] 10.1.2: Iterate Based on Experience

**Current**: Phase 0
**Next**: 0.1.1

---

## Phase 0: Foundation (Week 1, Days 1-2)

**Goal**: Set up repository, package structure, and development tools

### Task 0.1: Repository Setup

**Subtask 0.1.1: Initialize Git Repository (Single Session)**

**Prerequisites**: None

**Deliverables**:
- [ ] Add `.gitignore` (Python standard)
- [ ] Create initial `README.md` with project overview
- [ ] Create `LICENSE` (MIT)
- [ ] Initial commit

**Technology Decisions**:
- Git (already initialized)
- GitHub for hosting

**Files to Create**:
- `.gitignore` - Python, IDE, OS files
- `README.md` - Project description, installation, quick start
- `LICENSE` - MIT License

**Files to Modify**:
- None (existing: PROJECT_BRIEF.md, claude.md, DEVELOPMENT_PLAN.md)

**Success Criteria**:
- [ ] `.gitignore` covers `__pycache__/`, `*.pyc`, `.venv/`, `dist/`, `build/`
- [ ] README has basic info
- [ ] First commit with semantic message

---

**Completion Notes**:
- **Implementation**:
- **Files Created**:
- **Files Modified**:
- **Tests**:
- **Build**:
- **Branch**:
- **Notes**:

---

**Subtask 0.1.2: Python Package Structure (Single Session)**

**Prerequisites**:
- [x] 0.1.1: Initialize Git Repository

**Deliverables**:
- [ ] Create `claude_planner/` package directory
- [ ] Create `__init__.py` with version
- [ ] Create subdirectories: `generator/`, `validator/`, `templates/`, `utils/`
- [ ] Create `tests/` directory
- [ ] Create `pyproject.toml` with basic metadata
- [ ] Verify package imports work

**Technology Decisions**:
- Package name: `claude-code-planner` (PyPI)
- Module name: `claude_planner` (Python)

**Files to Create**:
- `claude_planner/__init__.py` - Package init with `__version__`
- `claude_planner/generator/__init__.py`
- `claude_planner/validator/__init__.py`
- `claude_planner/templates/__init__.py`
- `claude_planner/utils/__init__.py`
- `tests/__init__.py`
- `pyproject.toml` - Project metadata

**Success Criteria**:
- [ ] Can run: `python -c "import claude_planner; print(claude_planner.__version__)"`
- [ ] Directory structure matches claude.md
- [ ] All `__init__.py` files exist

---

**Completion Notes**:
- **Implementation**:
- **Files Created**:
- **Files Modified**:
- **Tests**:
- **Build**:
- **Branch**:
- **Notes**:

---

**Subtask 0.1.3: Development Dependencies (Single Session)**

**Prerequisites**:
- [x] 0.1.2: Python Package Structure

**Deliverables**:
- [ ] Update `pyproject.toml` with all dependencies
- [ ] Create `requirements-dev.txt` for development tools
- [ ] Install dependencies: `pip install -e ".[dev]"`
- [ ] Verify all imports work
- [ ] Document installation in README

**Technology Decisions**:
- Use `pyproject.toml` for package metadata
- Use `requirements-dev.txt` for dev tools
- Editable install for development

**Files to Create**:
- `requirements-dev.txt` - Dev dependencies

**Files to Modify**:
- `pyproject.toml` - Add dependencies, optional dev dependencies
- `README.md` - Add installation section

**Success Criteria**:
- [ ] `pip install -e ".[dev]"` works
- [ ] Can import: `import click`, `import jinja2`, `import yaml`, `import pytest`
- [ ] README has installation instructions

**Example pyproject.toml**:
```toml
[project]
name = "claude-code-planner"
version = "0.1.0"
dependencies = [
    "click>=8.1.7",
    "jinja2>=3.1.2",
    "pyyaml>=6.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.6",
    "mypy>=1.7.1",
]
```

---

**Completion Notes**:
- **Implementation**:
- **Files Created**:
- **Files Modified**:
- **Tests**:
- **Build**:
- **Branch**:
- **Notes**:

---

### Task 0.2: Development Tools

**Subtask 0.2.1: Pre-commit Hooks (Single Session)**

**Prerequisites**:
- [x] 0.1.3: Development Dependencies

**Deliverables**:
- [ ] Create `.pre-commit-config.yaml`
- [ ] Add hooks: ruff (lint), mypy (type check)
- [ ] Install hooks: `pre-commit install`
- [ ] Test hooks work: `pre-commit run --all-files`
- [ ] Commit hook configuration

**Technology Decisions**:
- pre-commit framework
- ruff for linting
- mypy for type checking

**Files to Create**:
- `.pre-commit-config.yaml` - Hook configuration

**Success Criteria**:
- [ ] Hooks installed
- [ ] `pre-commit run --all-files` passes
- [ ] Git commit triggers hooks

---

**Completion Notes**:
- **Implementation**:
- **Files Created**:
- **Files Modified**:
- **Tests**:
- **Build**:
- **Branch**:
- **Notes**:

---

**Subtask 0.2.2: CI/CD Pipeline (Single Session)**

**Prerequisites**:
- [x] 0.2.1: Pre-commit Hooks

**Deliverables**:
- [ ] Create `.github/workflows/test.yml`
- [ ] Configure: run tests on push/PR
- [ ] Configure: Python 3.11, 3.12 matrix
- [ ] Test workflow by pushing to GitHub

**Technology Decisions**:
- GitHub Actions
- pytest for testing
- Matrix testing: Python 3.11, 3.12

**Files to Create**:
- `.github/workflows/test.yml` - CI pipeline

**Success Criteria**:
- [ ] Workflow runs on push
- [ ] Tests pass in CI

---

**Completion Notes**:
- **Implementation**:
- **Files Created**:
- **Files Modified**:
- **Tests**:
- **Build**:
- **Branch**:
- **Notes**:

---

## Remaining Phases

Phases 1-10 follow the same pattern with specific subtasks for:
- Phase 1: Data models (4 subtasks)
- Phase 2: Parser (4 subtasks)
- Phase 3: Templates (7 subtasks)
- Phase 4: Generator (5 subtasks)
- Phase 5: CLI (5 subtasks)
- Phase 6: Validator (5 subtasks)
- Phase 7: Git integration (3 subtasks)
- Phase 8: Testing/docs (6 subtasks)
- Phase 9: Distribution (4 subtasks)
- Phase 10: Dogfooding (2 subtasks)

**Total**: ~50 subtasks over 2 weeks

---

## Success Metrics

**Development Process**:
- Code coverage: >80%
- All tests pass
- Linting clean (ruff)
- Type checking clean (mypy)

**Product Metrics**:
- Generate plan in <5 seconds
- Validation passes with 0 errors
- Can install from PyPI
- Successfully generates own development plan

---

## Timeline Summary

| Phase | Days | Deliverable | Status |
|-------|------|-------------|--------|
| Phase 0 | 1-2 | Foundation | [ ] |
| Phase 1 | 2-3 | Data models | [ ] |
| Phase 2 | 3-4 | Parser | [ ] |
| Phase 3 | 4-5 | Templates | [ ] |
| Phase 4 | 6-7 | Generator | [ ] |
| Phase 5 | 7-8 | CLI | [ ] |
| Phase 6 | 8-9 | Validator | [ ] |
| Phase 7 | 9 | Git integration | [ ] |
| Phase 8 | 10 | Testing/docs | [ ] |
| Phase 9 | 10 | Distribution | [ ] |

**Total**: 2 weeks (10 days)

---

_This development plan is a living document. Update completion notes after each subtask._
```

---
---
---

# END OF FILES

Now copy each section into its respective file in your repo and you're ready to start!

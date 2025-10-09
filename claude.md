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

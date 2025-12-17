# CLAUDE.md - HelloCLI

## Project Overview

HelloCLI is a minimal Python CLI that greets users by name with optional colored output. Built with Click and Rich.

## Quick Reference

| Item | Value |
|------|-------|
| **Language** | Python 3.11+ |
| **CLI Framework** | Click |
| **Colors** | Rich |
| **Test Framework** | pytest + pytest-cov |
| **Linter** | ruff |
| **Type Checker** | mypy |

## Directory Structure

```
hello-cli/
├── src/
│   └── hello_cli/
│       ├── __init__.py      # Version and exports
│       └── cli.py           # CLI implementation
├── tests/
│   └── test_cli.py          # CLI tests
├── pyproject.toml           # Project config
├── PROJECT_BRIEF.md         # Requirements
├── CLAUDE.md                # This file
└── DEVELOPMENT_PLAN.md      # Execution plan
```

## Commands

```bash
# Install in dev mode
pip install -e ".[dev]"

# Run the CLI
hello World              # Output: Hello, World!
hello World --color      # Output: Hello, World! (in green)
hello --version          # Output: hello-cli 0.1.0
hello --help             # Show help

# Development
ruff check src tests     # Lint
mypy src                 # Type check
pytest tests/ -v --cov   # Test with coverage
```

## Coding Standards

### Imports
```python
from __future__ import annotations

# Standard library
from typing import TYPE_CHECKING

# Third-party
import click
from rich.console import Console

# Local
from hello_cli import __version__
```

### Type Hints
All functions must have type hints:
```python
def greet(name: str, color: bool = False) -> str:
    """Generate greeting message."""
    ...
```

### Docstrings
Google style:
```python
def greet(name: str, color: bool = False) -> str:
    """Generate a greeting message.

    Args:
        name: The name to greet.
        color: Whether to use colored output.

    Returns:
        The formatted greeting string.
    """
```

### Testing
- Use `click.testing.CliRunner` for CLI tests
- Test success, failure, and edge cases
- Target 100% coverage

## Session Checklist

Before starting work:
- [ ] Read DEVELOPMENT_PLAN.md for current subtask
- [ ] Check git branch status
- [ ] Verify prerequisites are complete

Before committing:
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] `pytest tests/ -v --cov` passes with 100% coverage
- [ ] DEVELOPMENT_PLAN.md updated with completion notes

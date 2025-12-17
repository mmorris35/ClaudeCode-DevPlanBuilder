# DEVELOPMENT_PLAN.md - HelloCLI

> **Haiku-Executable Plan**: Every subtask contains complete, copy-pasteable code. Claude Haiku can execute this mechanically without inference.

## Project Summary

| Field | Value |
|-------|-------|
| **Project** | HelloCLI |
| **Goal** | Minimal CLI that greets users by name with optional color output |
| **Phases** | 2 |
| **Tasks** | 4 |
| **Subtasks** | 6 |

---

## Phase Overview

| Phase | Name | Tasks | Status |
|-------|------|-------|--------|
| 1 | Project Setup | 2 | Pending |
| 2 | CLI Implementation | 2 | Pending |

---

# Phase 1: Project Setup

## Task 1.1: Initialize Project Structure

**Branch:** `feature/1.1-project-init`

### Subtask 1.1.1: Create pyproject.toml

**Prerequisites:** None

**Deliverables:**
- [ ] `pyproject.toml` - Project configuration

**Complete Code:**

Create file `pyproject.toml`:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "hello-cli"
version = "0.1.0"
description = "A minimal CLI that greets users by name"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[project.scripts]
hello = "hello_cli.cli:main"

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=hello_cli --cov-report=term-missing"

[tool.coverage.run]
source = ["src/hello_cli"]
branch = true

[tool.coverage.report]
fail_under = 100
show_missing = true
```

**Verification:**
```bash
# File exists and is valid TOML
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
# Expected: No output (success)
```

**Success Criteria:**
- [ ] `pyproject.toml` exists
- [ ] TOML parses without error
- [ ] All dependencies listed

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `pyproject.toml`
- **Verification**: [To be filled]

---

### Subtask 1.1.2: Create Package Structure

**Prerequisites:** 1.1.1 complete

**Deliverables:**
- [ ] `src/hello_cli/__init__.py` - Package init with version
- [ ] `src/hello_cli/cli.py` - CLI placeholder
- [ ] `tests/__init__.py` - Test package init

**Complete Code:**

Create file `src/hello_cli/__init__.py`:
```python
"""HelloCLI - A minimal greeting CLI."""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = ["__version__"]
```

Create file `src/hello_cli/cli.py`:
```python
"""CLI entry point for HelloCLI."""

from __future__ import annotations


def main() -> None:
    """Entry point placeholder."""
    pass
```

Create file `tests/__init__.py`:
```python
"""Test package for HelloCLI."""
```

**Verification:**
```bash
# Directory structure exists
ls -la src/hello_cli/
# Expected: __init__.py, cli.py

ls -la tests/
# Expected: __init__.py

# Package imports work
python -c "from hello_cli import __version__; print(__version__)"
# Expected: 0.1.0
```

**Success Criteria:**
- [ ] Package structure created
- [ ] `__version__` importable
- [ ] Tests directory exists

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/hello_cli/__init__.py`, `src/hello_cli/cli.py`, `tests/__init__.py`
- **Verification**: [To be filled]

---

### Task 1.1 Complete - Squash Merge

**Checklist:**
- [ ] All subtasks complete (1.1.1, 1.1.2)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

## Task 1.2: Install and Verify

**Branch:** `feature/1.2-install-verify`

### Subtask 1.2.1: Install Dev Dependencies and Verify Tools

**Prerequisites:** Task 1.1 complete

**Deliverables:**
- [ ] Package installed in editable mode
- [ ] All dev tools working

**Commands to Execute:**
```bash
# Create virtual environment (if not exists)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify tools work
ruff --version
# Expected: ruff 0.x.x

mypy --version
# Expected: mypy 1.x.x

pytest --version
# Expected: pytest 7.x.x
```

**Verification:**
```bash
# CLI entry point exists (will fail with exit 0 since main() does nothing yet)
hello --help || true
# Expected: Error (no --help implemented yet) - this is OK

# Imports work
python -c "from hello_cli import __version__; print('OK')"
# Expected: OK
```

**Success Criteria:**
- [ ] `pip install -e ".[dev]"` succeeds
- [ ] `ruff --version` works
- [ ] `mypy --version` works
- [ ] `pytest --version` works

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Verification**: [To be filled]

---

### Task 1.2 Complete - Squash Merge

**Checklist:**
- [ ] All subtasks complete (1.2.1)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

# Phase 2: CLI Implementation

## Task 2.1: Implement Core CLI

**Branch:** `feature/2.1-core-cli`

### Subtask 2.1.1: Implement Greeting Command

**Prerequisites:** Task 1.2 complete

**Deliverables:**
- [ ] `src/hello_cli/cli.py` - Full CLI implementation
- [ ] `tests/test_cli.py` - Complete test suite

**Complete Code:**

Replace `src/hello_cli/cli.py` with:
```python
"""CLI entry point for HelloCLI."""

from __future__ import annotations

import click
from rich.console import Console

from hello_cli import __version__

console = Console()


@click.command()
@click.argument("name", default="World")
@click.option("--color", is_flag=True, help="Use colored output")
@click.version_option(version=__version__, prog_name="hello-cli")
def main(name: str, color: bool) -> None:
    """Greet NAME with a friendly message.

    If no NAME is provided, greets "World" by default.

    Examples:
        hello Alice        → Hello, Alice!
        hello --color Bob  → Hello, Bob! (in green)
    """
    message = f"Hello, {name}!"

    if color:
        console.print(message, style="bold green")
    else:
        click.echo(message)


if __name__ == "__main__":
    main()
```

Create file `tests/test_cli.py`:
```python
"""Tests for HelloCLI."""

from __future__ import annotations

from click.testing import CliRunner

from hello_cli import __version__
from hello_cli.cli import main


class TestGreetCommand:
    """Test suite for the greet command."""

    def test_greet_default_name(self) -> None:
        """Test greeting with default name."""
        runner = CliRunner()
        result = runner.invoke(main, [])

        assert result.exit_code == 0
        assert "Hello, World!" in result.output

    def test_greet_custom_name(self) -> None:
        """Test greeting with custom name."""
        runner = CliRunner()
        result = runner.invoke(main, ["Alice"])

        assert result.exit_code == 0
        assert "Hello, Alice!" in result.output

    def test_greet_with_color_flag(self) -> None:
        """Test greeting with color flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["Bob", "--color"])

        assert result.exit_code == 0
        # Rich adds ANSI codes, but the name should be present
        assert "Bob" in result.output

    def test_version_flag(self) -> None:
        """Test --version flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert __version__ in result.output
        assert "hello-cli" in result.output

    def test_help_flag(self) -> None:
        """Test --help flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Greet NAME" in result.output
        assert "--color" in result.output
        assert "--version" in result.output


class TestEdgeCases:
    """Test edge cases."""

    def test_empty_string_name(self) -> None:
        """Test with empty string as name."""
        runner = CliRunner()
        result = runner.invoke(main, [""])

        assert result.exit_code == 0
        assert "Hello, !" in result.output

    def test_name_with_spaces(self) -> None:
        """Test name with spaces."""
        runner = CliRunner()
        result = runner.invoke(main, ["John Doe"])

        assert result.exit_code == 0
        assert "Hello, John Doe!" in result.output

    def test_special_characters_in_name(self) -> None:
        """Test name with special characters."""
        runner = CliRunner()
        result = runner.invoke(main, ["José García"])

        assert result.exit_code == 0
        assert "Hello, José García!" in result.output
```

**Verification:**
```bash
# Linting
ruff check src tests
# Expected: All checks passed!

# Type checking
mypy src
# Expected: Success: no issues found

# Tests with coverage
pytest tests/ -v --cov=hello_cli --cov-report=term-missing
# Expected: 8 passed, 100% coverage
```

**Success Criteria:**
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] `pytest` shows 8 tests passing
- [ ] Coverage is 100%

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `tests/test_cli.py`
- **Files Modified**: `src/hello_cli/cli.py`
- **Tests**: 8 tests, 100% coverage
- **Verification**: [To be filled]

---

### Task 2.1 Complete - Squash Merge

**Checklist:**
- [ ] All subtasks complete (2.1.1)
- [ ] All tests pass with 100% coverage
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

## Task 2.2: Final Verification

**Branch:** `feature/2.2-final-verify`

### Subtask 2.2.1: End-to-End Testing

**Prerequisites:** Task 2.1 complete

**Deliverables:**
- [ ] CLI works from command line
- [ ] All flags function correctly

**Commands to Execute:**
```bash
# Test basic greeting
hello
# Expected output: Hello, World!

# Test with name
hello Alice
# Expected output: Hello, Alice!

# Test with color (will show green in terminal)
hello Bob --color
# Expected output: Hello, Bob! (in green)

# Test version
hello --version
# Expected output: hello-cli, version 0.1.0

# Test help
hello --help
# Expected output: Usage info with all options
```

**Verification:**
```bash
# All commands should exit 0
hello && hello Alice && hello --version && hello --help
# Expected: All succeed (exit 0)

# Final test run
pytest tests/ -v --cov=hello_cli --cov-report=term-missing --cov-fail-under=100
# Expected: 8 passed, 100% coverage, exit 0
```

**Success Criteria:**
- [ ] `hello` outputs "Hello, World!"
- [ ] `hello Alice` outputs "Hello, Alice!"
- [ ] `hello --version` shows version
- [ ] `hello --help` shows help
- [ ] All tests pass with 100% coverage

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Verification**: [To be filled]

---

### Task 2.2 Complete - Squash Merge

**Checklist:**
- [ ] All subtasks complete (2.2.1)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

# Project Complete Checklist

- [ ] Phase 1: Project Setup complete
- [ ] Phase 2: CLI Implementation complete
- [ ] All tests pass (8 tests)
- [ ] 100% code coverage
- [ ] CLI works: `hello`, `hello NAME`, `hello --color`, `hello --version`, `hello --help`
- [ ] Clean git history (squash merges only)

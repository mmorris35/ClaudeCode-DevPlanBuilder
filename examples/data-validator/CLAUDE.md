# CLAUDE.md - DataValidator

## Project Overview

DataValidator is a zero-dependency Python library for composable data validation with clear error messages.

## Directory Structure

```
data-validator/
├── pyproject.toml
├── src/
│   └── data_validator/
│       ├── __init__.py       # Public API exports
│       ├── validators.py     # Validator classes
│       ├── constraints.py    # Constraint validators
│       ├── schema.py         # Schema validation
│       ├── combinators.py    # and_/or_ logic
│       └── errors.py         # Error types
└── tests/
    ├── __init__.py
    ├── test_validators.py
    ├── test_constraints.py
    ├── test_schema.py
    └── test_combinators.py
```

## Commands

```bash
# Development setup
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Quality checks
ruff check src tests        # Linting
ruff format src tests       # Formatting
mypy src                    # Type checking

# Testing
pytest tests/ -v --cov=data_validator --cov-report=term-missing
pytest tests/ -v --cov-fail-under=100  # Enforce 100% coverage
```

## Coding Standards

### Type Hints
- All functions must have complete type annotations
- Use `from __future__ import annotations` for forward references
- Generic types: `list[str]`, `dict[str, Any]`, `Callable[[T], bool]`
- Return types always explicit, including `-> None`

### Docstrings
- All public classes and functions must have docstrings
- Use Google-style docstrings
- Include Args, Returns, Raises sections

### Naming
- Classes: PascalCase (`StringValidator`, `ValidationError`)
- Functions: snake_case (`validate`, `is_valid`)
- Constants: UPPER_SNAKE_CASE (`DEFAULT_MAX_LENGTH`)
- Private: leading underscore (`_internal_validate`)

### Error Handling
- Custom exceptions inherit from `ValidationError`
- Include field path in error messages
- Collect all errors, don't fail on first

## Key Patterns

### Validator Protocol
```python
from typing import Protocol, Any

class Validator(Protocol):
    """Protocol for all validators."""

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        """Validate a value and return list of errors."""
        ...

    def is_valid(self, value: Any) -> bool:
        """Return True if value is valid."""
        ...
```

### Validator Implementation
```python
class StringValidator:
    """Validate string values."""

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        if not isinstance(value, str):
            return [ValidationError(f"{path}: expected string, got {type(value).__name__}")]
        return []

    def is_valid(self, value: Any) -> bool:
        return len(self.validate(value)) == 0
```

### Constraint Chaining
```python
validator = StringValidator().min_length(1).max_length(100).pattern(r"^\w+$")
```

### Schema Definition
```python
schema = Schema({
    "name": StringValidator().min_length(1),
    "age": IntValidator().min_value(0).max_value(150),
    "email": StringValidator().pattern(r"^[\w.-]+@[\w.-]+\.\w+$"),
})

errors = schema.validate({"name": "", "age": -5, "email": "invalid"})
```

## Session Checklist

Before starting work:
- [ ] Activate virtual environment
- [ ] Run `pip install -e ".[dev]"` if needed
- [ ] Read current subtask in DEVELOPMENT_PLAN.md

After completing work:
- [ ] Run `ruff check src tests` - no errors
- [ ] Run `mypy src` - no errors
- [ ] Run `pytest tests/ -v --cov=data_validator --cov-fail-under=100` - all pass, 100% coverage
- [ ] Commit with descriptive message

# PROJECT_BRIEF.md - DataValidator

## Project Overview

| Field | Value |
|-------|-------|
| **Project Name** | DataValidator |
| **Project Type** | library |
| **Timeline** | 3 days |
| **Team Size** | 1 |

## Goal

A minimal Python library for validating data structures with composable validation rules and clear error messages.

## Target Users

- Python developers needing lightweight data validation
- Applications that need to validate config files or API inputs
- Teams wanting type-safe validation without heavy frameworks

## Features (MVP)

1. **Type Validators** - Validate basic types (string, int, float, bool)
2. **Constraint Validators** - min/max length, min/max value, regex pattern
3. **Schema Validation** - Validate dict against a schema of validators
4. **Composable Rules** - Chain multiple validators with `and_`/`or_` logic
5. **Clear Errors** - Human-readable error messages with field paths

## Nice-to-Have (v2)

- Async validation support
- Custom validator decorators
- JSON Schema export
- Integration with dataclasses

## Tech Stack

### Must Use
- Python 3.11+
- Type hints throughout
- pytest for testing
- No runtime dependencies (stdlib only)

### Cannot Use
- pydantic (we're building something simpler)
- External validation libraries
- dataclasses (keep it simple with dicts)

## Constraints

- Zero runtime dependencies
- 100% test coverage
- All public APIs must have docstrings
- Must pass mypy strict mode
- Must pass ruff linting

# DEVELOPMENT_PLAN.md - DataValidator

> **Haiku-Executable Plan**: Every subtask contains complete, copy-pasteable code. Claude Haiku can execute this mechanically without inference.

## Project Summary

| Field | Value |
|-------|-------|
| **Project** | DataValidator |
| **Goal** | Zero-dependency Python validation library with composable rules |
| **Phases** | 2 |
| **Tasks** | 4 |
| **Subtasks** | 8 |

---

## Phase Overview

| Phase | Name | Tasks | Status |
|-------|------|-------|--------|
| 1 | Core Foundation | 2 | Pending |
| 2 | Advanced Features | 2 | Pending |

---

# Phase 1: Core Foundation

## Task 1.1: Project Setup

**Branch:** `feature/1.1-project-setup`

### Subtask 1.1.1: Create pyproject.toml and Package Structure

**Prerequisites:** None

**Deliverables:**
- [ ] `pyproject.toml` - Project configuration
- [ ] `src/data_validator/__init__.py` - Package init
- [ ] `src/data_validator/errors.py` - Error types
- [ ] `tests/__init__.py` - Test package init

**Complete Code:**

Create file `pyproject.toml`:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "data-validator"
version = "0.1.0"
description = "A zero-dependency Python library for composable data validation"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=data_validator --cov-report=term-missing"

[tool.coverage.run]
source = ["src/data_validator"]
branch = true

[tool.coverage.report]
fail_under = 100
show_missing = true
```

Create file `src/data_validator/__init__.py`:
```python
"""DataValidator - Zero-dependency Python validation library."""

from __future__ import annotations

from data_validator.errors import ValidationError

__version__ = "0.1.0"
__all__ = ["ValidationError", "__version__"]
```

Create file `src/data_validator/errors.py`:
```python
"""Error types for DataValidator."""

from __future__ import annotations


class ValidationError(Exception):
    """Represents a validation error with path and message.

    Attributes:
        path: The field path where the error occurred (e.g., "user.email").
        message: Human-readable error description.
    """

    def __init__(self, message: str, path: str = "") -> None:
        """Initialize a ValidationError.

        Args:
            message: Human-readable error description.
            path: The field path where the error occurred.
        """
        self.path = path
        self.message = message
        full_message = f"{path}: {message}" if path else message
        super().__init__(full_message)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"ValidationError(path={self.path!r}, message={self.message!r})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another ValidationError."""
        if not isinstance(other, ValidationError):
            return NotImplemented
        return self.path == other.path and self.message == other.message
```

Create file `tests/__init__.py`:
```python
"""Test package for DataValidator."""
```

**Verification:**
```bash
# Create virtual environment and install
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Verify package imports
python -c "from data_validator import ValidationError, __version__; print(__version__)"
# Expected: 0.1.0

# Run initial tests (will fail with no tests yet)
pytest tests/ -v || true
# Expected: no tests collected
```

**Success Criteria:**
- [ ] `pip install -e ".[dev]"` succeeds
- [ ] `ValidationError` is importable
- [ ] `__version__` equals "0.1.0"

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `pyproject.toml`, `src/data_validator/__init__.py`, `src/data_validator/errors.py`, `tests/__init__.py`
- **Verification**: [To be filled]

---

### Task 1.1 Complete - Squash Merge

**When all subtasks (1.1.1) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/1.1-project-setup

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/1.1-project-setup
git commit -m "feat(setup): initialize project structure

- Add pyproject.toml with zero runtime dependencies
- Create ValidationError class
- Configure ruff, mypy, pytest"
git push origin main

# Delete feature branch
git branch -d feature/1.1-project-setup
git push origin --delete feature/1.1-project-setup
```

**Checklist:**
- [ ] All subtasks complete (1.1.1)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

## Task 1.2: Type Validators

**Branch:** `feature/1.2-type-validators`

### Subtask 1.2.1: Implement Base Validators

**Prerequisites:** Task 1.1 complete

**Deliverables:**
- [ ] `src/data_validator/validators.py` - Type validator classes
- [ ] `tests/test_validators.py` - Validator tests
- [ ] Update `src/data_validator/__init__.py` - Export validators

**Complete Code:**

Create file `src/data_validator/validators.py`:
```python
"""Type validators for basic Python types."""

from __future__ import annotations

from typing import Any

from data_validator.errors import ValidationError


class StringValidator:
    """Validate that a value is a string.

    Example:
        >>> v = StringValidator()
        >>> v.is_valid("hello")
        True
        >>> v.is_valid(123)
        False
    """

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        """Validate that value is a string.

        Args:
            value: The value to validate.
            path: The field path for error messages.

        Returns:
            List of validation errors (empty if valid).
        """
        if not isinstance(value, str):
            return [ValidationError(
                f"expected string, got {type(value).__name__}",
                path=path,
            )]
        return []

    def is_valid(self, value: Any) -> bool:
        """Check if value is valid.

        Args:
            value: The value to check.

        Returns:
            True if valid, False otherwise.
        """
        return len(self.validate(value)) == 0


class IntValidator:
    """Validate that a value is an integer.

    Example:
        >>> v = IntValidator()
        >>> v.is_valid(42)
        True
        >>> v.is_valid(3.14)
        False
    """

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        """Validate that value is an integer.

        Args:
            value: The value to validate.
            path: The field path for error messages.

        Returns:
            List of validation errors (empty if valid).
        """
        # bool is subclass of int, so check bool first
        if isinstance(value, bool) or not isinstance(value, int):
            return [ValidationError(
                f"expected integer, got {type(value).__name__}",
                path=path,
            )]
        return []

    def is_valid(self, value: Any) -> bool:
        """Check if value is valid.

        Args:
            value: The value to check.

        Returns:
            True if valid, False otherwise.
        """
        return len(self.validate(value)) == 0


class FloatValidator:
    """Validate that a value is a float or int.

    Example:
        >>> v = FloatValidator()
        >>> v.is_valid(3.14)
        True
        >>> v.is_valid(42)
        True
        >>> v.is_valid("3.14")
        False
    """

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        """Validate that value is a float or int.

        Args:
            value: The value to validate.
            path: The field path for error messages.

        Returns:
            List of validation errors (empty if valid).
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return [ValidationError(
                f"expected number, got {type(value).__name__}",
                path=path,
            )]
        return []

    def is_valid(self, value: Any) -> bool:
        """Check if value is valid.

        Args:
            value: The value to check.

        Returns:
            True if valid, False otherwise.
        """
        return len(self.validate(value)) == 0


class BoolValidator:
    """Validate that a value is a boolean.

    Example:
        >>> v = BoolValidator()
        >>> v.is_valid(True)
        True
        >>> v.is_valid(1)
        False
    """

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        """Validate that value is a boolean.

        Args:
            value: The value to validate.
            path: The field path for error messages.

        Returns:
            List of validation errors (empty if valid).
        """
        if not isinstance(value, bool):
            return [ValidationError(
                f"expected boolean, got {type(value).__name__}",
                path=path,
            )]
        return []

    def is_valid(self, value: Any) -> bool:
        """Check if value is valid.

        Args:
            value: The value to check.

        Returns:
            True if valid, False otherwise.
        """
        return len(self.validate(value)) == 0
```

Create file `tests/test_validators.py`:
```python
"""Tests for type validators."""

from __future__ import annotations

import pytest

from data_validator.validators import (
    BoolValidator,
    FloatValidator,
    IntValidator,
    StringValidator,
)


class TestStringValidator:
    """Tests for StringValidator."""

    def test_valid_string(self) -> None:
        """Test that strings are valid."""
        v = StringValidator()
        assert v.is_valid("hello")
        assert v.is_valid("")
        assert v.validate("test") == []

    def test_invalid_string(self) -> None:
        """Test that non-strings are invalid."""
        v = StringValidator()
        assert not v.is_valid(123)
        assert not v.is_valid(None)
        assert not v.is_valid([])

    def test_error_message(self) -> None:
        """Test error message format."""
        v = StringValidator()
        errors = v.validate(123, path="field")
        assert len(errors) == 1
        assert errors[0].path == "field"
        assert "expected string" in errors[0].message
        assert "int" in errors[0].message


class TestIntValidator:
    """Tests for IntValidator."""

    def test_valid_int(self) -> None:
        """Test that integers are valid."""
        v = IntValidator()
        assert v.is_valid(42)
        assert v.is_valid(0)
        assert v.is_valid(-10)
        assert v.validate(100) == []

    def test_invalid_int(self) -> None:
        """Test that non-integers are invalid."""
        v = IntValidator()
        assert not v.is_valid(3.14)
        assert not v.is_valid("42")
        assert not v.is_valid(None)

    def test_bool_is_not_int(self) -> None:
        """Test that booleans are not considered integers."""
        v = IntValidator()
        assert not v.is_valid(True)
        assert not v.is_valid(False)

    def test_error_message(self) -> None:
        """Test error message format."""
        v = IntValidator()
        errors = v.validate("not int", path="age")
        assert len(errors) == 1
        assert errors[0].path == "age"
        assert "expected integer" in errors[0].message


class TestFloatValidator:
    """Tests for FloatValidator."""

    def test_valid_float(self) -> None:
        """Test that floats are valid."""
        v = FloatValidator()
        assert v.is_valid(3.14)
        assert v.is_valid(0.0)
        assert v.validate(2.718) == []

    def test_int_is_valid(self) -> None:
        """Test that integers are valid as numbers."""
        v = FloatValidator()
        assert v.is_valid(42)
        assert v.is_valid(0)

    def test_invalid_float(self) -> None:
        """Test that non-numbers are invalid."""
        v = FloatValidator()
        assert not v.is_valid("3.14")
        assert not v.is_valid(None)

    def test_bool_is_not_float(self) -> None:
        """Test that booleans are not considered numbers."""
        v = FloatValidator()
        assert not v.is_valid(True)
        assert not v.is_valid(False)

    def test_error_message(self) -> None:
        """Test error message format."""
        v = FloatValidator()
        errors = v.validate("not number", path="price")
        assert len(errors) == 1
        assert errors[0].path == "price"
        assert "expected number" in errors[0].message


class TestBoolValidator:
    """Tests for BoolValidator."""

    def test_valid_bool(self) -> None:
        """Test that booleans are valid."""
        v = BoolValidator()
        assert v.is_valid(True)
        assert v.is_valid(False)
        assert v.validate(True) == []

    def test_invalid_bool(self) -> None:
        """Test that non-booleans are invalid."""
        v = BoolValidator()
        assert not v.is_valid(1)
        assert not v.is_valid(0)
        assert not v.is_valid("true")
        assert not v.is_valid(None)

    def test_error_message(self) -> None:
        """Test error message format."""
        v = BoolValidator()
        errors = v.validate(1, path="active")
        assert len(errors) == 1
        assert errors[0].path == "active"
        assert "expected boolean" in errors[0].message
```

Replace `src/data_validator/__init__.py` with:
```python
"""DataValidator - Zero-dependency Python validation library."""

from __future__ import annotations

from data_validator.errors import ValidationError
from data_validator.validators import (
    BoolValidator,
    FloatValidator,
    IntValidator,
    StringValidator,
)

__version__ = "0.1.0"
__all__ = [
    "BoolValidator",
    "FloatValidator",
    "IntValidator",
    "StringValidator",
    "ValidationError",
    "__version__",
]
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
pytest tests/test_validators.py -v --cov=data_validator --cov-report=term-missing
# Expected: 16 tests passed
```

**Success Criteria:**
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] All 16 tests pass
- [ ] Validators importable from package

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/data_validator/validators.py`, `tests/test_validators.py`
- **Files Modified**: `src/data_validator/__init__.py`
- **Tests**: 16 tests
- **Verification**: [To be filled]

---

### Task 1.2 Complete - Squash Merge

**When all subtasks (1.2.1) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/1.2-type-validators

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/1.2-type-validators
git commit -m "feat(validators): add type validators

- Add StringValidator, IntValidator, FloatValidator, BoolValidator
- Handle bool-is-subclass-of-int edge case
- 16 tests passing"
git push origin main

# Delete feature branch
git branch -d feature/1.2-type-validators
git push origin --delete feature/1.2-type-validators
```

**Checklist:**
- [ ] All subtasks complete (1.2.1)
- [ ] All tests pass
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

# Phase 2: Advanced Features

## Task 2.1: Constraints

**Branch:** `feature/2.1-constraints`

### Subtask 2.1.1: Implement String Constraints

**Prerequisites:** Task 1.2 complete

**Deliverables:**
- [ ] `src/data_validator/constraints.py` - Constraint classes
- [ ] `tests/test_constraints.py` - Constraint tests
- [ ] Update `src/data_validator/__init__.py` - Export constraints

**Complete Code:**

Create file `src/data_validator/constraints.py`:
```python
"""Constraint validators for additional validation rules."""

from __future__ import annotations

import re
from typing import Any

from data_validator.errors import ValidationError
from data_validator.validators import FloatValidator, IntValidator, StringValidator


class ConstrainedString(StringValidator):
    """String validator with constraints.

    Example:
        >>> v = ConstrainedString(min_length=1, max_length=10)
        >>> v.is_valid("hello")
        True
        >>> v.is_valid("")
        False
    """

    def __init__(
        self,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
    ) -> None:
        """Initialize constrained string validator.

        Args:
            min_length: Minimum string length (inclusive).
            max_length: Maximum string length (inclusive).
            pattern: Regex pattern the string must match.
        """
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = re.compile(pattern) if pattern else None

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        """Validate string with constraints.

        Args:
            value: The value to validate.
            path: The field path for error messages.

        Returns:
            List of validation errors (empty if valid).
        """
        errors = super().validate(value, path)
        if errors:
            return errors

        if self.min_length is not None and len(value) < self.min_length:
            errors.append(ValidationError(
                f"length must be at least {self.min_length}",
                path=path,
            ))

        if self.max_length is not None and len(value) > self.max_length:
            errors.append(ValidationError(
                f"length must be at most {self.max_length}",
                path=path,
            ))

        if self.pattern is not None and not self.pattern.match(value):
            errors.append(ValidationError(
                f"must match pattern {self.pattern.pattern}",
                path=path,
            ))

        return errors


class ConstrainedInt(IntValidator):
    """Integer validator with min/max constraints.

    Example:
        >>> v = ConstrainedInt(min_value=0, max_value=100)
        >>> v.is_valid(50)
        True
        >>> v.is_valid(-1)
        False
    """

    def __init__(
        self,
        min_value: int | None = None,
        max_value: int | None = None,
    ) -> None:
        """Initialize constrained integer validator.

        Args:
            min_value: Minimum value (inclusive).
            max_value: Maximum value (inclusive).
        """
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        """Validate integer with constraints.

        Args:
            value: The value to validate.
            path: The field path for error messages.

        Returns:
            List of validation errors (empty if valid).
        """
        errors = super().validate(value, path)
        if errors:
            return errors

        if self.min_value is not None and value < self.min_value:
            errors.append(ValidationError(
                f"must be at least {self.min_value}",
                path=path,
            ))

        if self.max_value is not None and value > self.max_value:
            errors.append(ValidationError(
                f"must be at most {self.max_value}",
                path=path,
            ))

        return errors


class ConstrainedFloat(FloatValidator):
    """Float validator with min/max constraints.

    Example:
        >>> v = ConstrainedFloat(min_value=0.0, max_value=1.0)
        >>> v.is_valid(0.5)
        True
        >>> v.is_valid(1.5)
        False
    """

    def __init__(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> None:
        """Initialize constrained float validator.

        Args:
            min_value: Minimum value (inclusive).
            max_value: Maximum value (inclusive).
        """
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any, path: str = "") -> list[ValidationError]:
        """Validate float with constraints.

        Args:
            value: The value to validate.
            path: The field path for error messages.

        Returns:
            List of validation errors (empty if valid).
        """
        errors = super().validate(value, path)
        if errors:
            return errors

        if self.min_value is not None and value < self.min_value:
            errors.append(ValidationError(
                f"must be at least {self.min_value}",
                path=path,
            ))

        if self.max_value is not None and value > self.max_value:
            errors.append(ValidationError(
                f"must be at most {self.max_value}",
                path=path,
            ))

        return errors
```

Create file `tests/test_constraints.py`:
```python
"""Tests for constraint validators."""

from __future__ import annotations

import pytest

from data_validator.constraints import (
    ConstrainedFloat,
    ConstrainedInt,
    ConstrainedString,
)


class TestConstrainedString:
    """Tests for ConstrainedString."""

    def test_no_constraints(self) -> None:
        """Test with no constraints."""
        v = ConstrainedString()
        assert v.is_valid("anything")
        assert v.is_valid("")

    def test_min_length(self) -> None:
        """Test minimum length constraint."""
        v = ConstrainedString(min_length=3)
        assert v.is_valid("abc")
        assert v.is_valid("abcd")
        assert not v.is_valid("ab")
        assert not v.is_valid("")

    def test_max_length(self) -> None:
        """Test maximum length constraint."""
        v = ConstrainedString(max_length=5)
        assert v.is_valid("abc")
        assert v.is_valid("abcde")
        assert not v.is_valid("abcdef")

    def test_pattern(self) -> None:
        """Test regex pattern constraint."""
        v = ConstrainedString(pattern=r"^\d+$")
        assert v.is_valid("123")
        assert not v.is_valid("abc")
        assert not v.is_valid("12a")

    def test_combined_constraints(self) -> None:
        """Test multiple constraints together."""
        v = ConstrainedString(min_length=2, max_length=4, pattern=r"^\w+$")
        assert v.is_valid("ab")
        assert v.is_valid("abcd")
        assert not v.is_valid("a")  # too short
        assert not v.is_valid("abcde")  # too long
        assert not v.is_valid("a b")  # doesn't match pattern

    def test_error_messages(self) -> None:
        """Test error message format."""
        v = ConstrainedString(min_length=5)
        errors = v.validate("ab", path="name")
        assert len(errors) == 1
        assert errors[0].path == "name"
        assert "at least 5" in errors[0].message

    def test_type_error_first(self) -> None:
        """Test that type errors are returned before constraint errors."""
        v = ConstrainedString(min_length=1)
        errors = v.validate(123, path="field")
        assert len(errors) == 1
        assert "expected string" in errors[0].message


class TestConstrainedInt:
    """Tests for ConstrainedInt."""

    def test_no_constraints(self) -> None:
        """Test with no constraints."""
        v = ConstrainedInt()
        assert v.is_valid(0)
        assert v.is_valid(-100)
        assert v.is_valid(100)

    def test_min_value(self) -> None:
        """Test minimum value constraint."""
        v = ConstrainedInt(min_value=0)
        assert v.is_valid(0)
        assert v.is_valid(100)
        assert not v.is_valid(-1)

    def test_max_value(self) -> None:
        """Test maximum value constraint."""
        v = ConstrainedInt(max_value=100)
        assert v.is_valid(100)
        assert v.is_valid(0)
        assert not v.is_valid(101)

    def test_range(self) -> None:
        """Test both min and max constraints."""
        v = ConstrainedInt(min_value=1, max_value=10)
        assert v.is_valid(1)
        assert v.is_valid(10)
        assert v.is_valid(5)
        assert not v.is_valid(0)
        assert not v.is_valid(11)

    def test_error_messages(self) -> None:
        """Test error message format."""
        v = ConstrainedInt(min_value=0)
        errors = v.validate(-5, path="age")
        assert len(errors) == 1
        assert errors[0].path == "age"
        assert "at least 0" in errors[0].message


class TestConstrainedFloat:
    """Tests for ConstrainedFloat."""

    def test_no_constraints(self) -> None:
        """Test with no constraints."""
        v = ConstrainedFloat()
        assert v.is_valid(0.0)
        assert v.is_valid(-100.5)
        assert v.is_valid(100.5)

    def test_min_value(self) -> None:
        """Test minimum value constraint."""
        v = ConstrainedFloat(min_value=0.0)
        assert v.is_valid(0.0)
        assert v.is_valid(0.1)
        assert not v.is_valid(-0.1)

    def test_max_value(self) -> None:
        """Test maximum value constraint."""
        v = ConstrainedFloat(max_value=1.0)
        assert v.is_valid(1.0)
        assert v.is_valid(0.5)
        assert not v.is_valid(1.1)

    def test_range(self) -> None:
        """Test both min and max constraints."""
        v = ConstrainedFloat(min_value=0.0, max_value=1.0)
        assert v.is_valid(0.0)
        assert v.is_valid(1.0)
        assert v.is_valid(0.5)
        assert not v.is_valid(-0.1)
        assert not v.is_valid(1.1)

    def test_int_as_float(self) -> None:
        """Test that integers work as floats."""
        v = ConstrainedFloat(min_value=0.0, max_value=10.0)
        assert v.is_valid(5)
        assert v.is_valid(0)

    def test_error_messages(self) -> None:
        """Test error message format."""
        v = ConstrainedFloat(max_value=1.0)
        errors = v.validate(2.0, path="percentage")
        assert len(errors) == 1
        assert errors[0].path == "percentage"
        assert "at most 1.0" in errors[0].message
```

Replace `src/data_validator/__init__.py` with:
```python
"""DataValidator - Zero-dependency Python validation library."""

from __future__ import annotations

from data_validator.constraints import (
    ConstrainedFloat,
    ConstrainedInt,
    ConstrainedString,
)
from data_validator.errors import ValidationError
from data_validator.validators import (
    BoolValidator,
    FloatValidator,
    IntValidator,
    StringValidator,
)

__version__ = "0.1.0"
__all__ = [
    "BoolValidator",
    "ConstrainedFloat",
    "ConstrainedInt",
    "ConstrainedString",
    "FloatValidator",
    "IntValidator",
    "StringValidator",
    "ValidationError",
    "__version__",
]
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
pytest tests/ -v --cov=data_validator --cov-report=term-missing
# Expected: 39 tests passed
```

**Success Criteria:**
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] All 39 tests pass (16 + 23 new)
- [ ] Constraint classes importable from package

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/data_validator/constraints.py`, `tests/test_constraints.py`
- **Files Modified**: `src/data_validator/__init__.py`
- **Tests**: 39 tests total
- **Verification**: [To be filled]

---

### Task 2.1 Complete - Squash Merge

**When all subtasks (2.1.1) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/2.1-constraints

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/2.1-constraints
git commit -m "feat(constraints): add constraint validators

- Add ConstrainedString with min_length, max_length, pattern
- Add ConstrainedInt with min_value, max_value
- Add ConstrainedFloat with min_value, max_value
- 39 tests passing"
git push origin main

# Delete feature branch
git branch -d feature/2.1-constraints
git push origin --delete feature/2.1-constraints
```

**Checklist:**
- [ ] All subtasks complete (2.1.1)
- [ ] All tests pass
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

## Task 2.2: Schema Validation

**Branch:** `feature/2.2-schema`

### Subtask 2.2.1: Implement Schema Class

**Prerequisites:** Task 2.1 complete

**Deliverables:**
- [ ] `src/data_validator/schema.py` - Schema validation class
- [ ] `tests/test_schema.py` - Schema tests
- [ ] Update `src/data_validator/__init__.py` - Export Schema

**Complete Code:**

Create file `src/data_validator/schema.py`:
```python
"""Schema validation for dictionaries."""

from __future__ import annotations

from typing import Any, Protocol


class Validator(Protocol):
    """Protocol for validators used in schemas."""

    def validate(self, value: Any, path: str = "") -> list[Any]:
        """Validate a value and return errors."""
        ...


from data_validator.errors import ValidationError


class Schema:
    """Validate a dictionary against a schema of validators.

    Example:
        >>> from data_validator import StringValidator, IntValidator
        >>> schema = Schema({
        ...     "name": StringValidator(),
        ...     "age": IntValidator(),
        ... })
        >>> errors = schema.validate({"name": "Alice", "age": 30})
        >>> len(errors)
        0
    """

    def __init__(
        self,
        fields: dict[str, Validator],
        *,
        allow_extra: bool = False,
    ) -> None:
        """Initialize schema.

        Args:
            fields: Mapping of field names to validators.
            allow_extra: If False, extra fields cause errors.
        """
        self.fields = fields
        self.allow_extra = allow_extra

    def validate(self, data: Any, path: str = "") -> list[ValidationError]:
        """Validate data against schema.

        Args:
            data: The data to validate (should be a dict).
            path: The base path for error messages.

        Returns:
            List of validation errors (empty if valid).
        """
        errors: list[ValidationError] = []

        if not isinstance(data, dict):
            return [ValidationError(
                f"expected dict, got {type(data).__name__}",
                path=path,
            )]

        # Check required fields
        for field_name, validator in self.fields.items():
            field_path = f"{path}.{field_name}" if path else field_name

            if field_name not in data:
                errors.append(ValidationError(
                    "field is required",
                    path=field_path,
                ))
            else:
                field_errors = validator.validate(data[field_name], path=field_path)
                errors.extend(field_errors)

        # Check for extra fields
        if not self.allow_extra:
            for key in data:
                if key not in self.fields:
                    field_path = f"{path}.{key}" if path else key
                    errors.append(ValidationError(
                        "unexpected field",
                        path=field_path,
                    ))

        return errors

    def is_valid(self, data: Any) -> bool:
        """Check if data is valid.

        Args:
            data: The data to check.

        Returns:
            True if valid, False otherwise.
        """
        return len(self.validate(data)) == 0
```

Create file `tests/test_schema.py`:
```python
"""Tests for schema validation."""

from __future__ import annotations

import pytest

from data_validator import (
    ConstrainedInt,
    ConstrainedString,
    IntValidator,
    Schema,
    StringValidator,
)


class TestSchema:
    """Tests for Schema."""

    def test_valid_data(self) -> None:
        """Test with valid data."""
        schema = Schema({
            "name": StringValidator(),
            "age": IntValidator(),
        })
        assert schema.is_valid({"name": "Alice", "age": 30})
        assert schema.validate({"name": "Bob", "age": 25}) == []

    def test_invalid_type(self) -> None:
        """Test with non-dict data."""
        schema = Schema({"name": StringValidator()})
        errors = schema.validate("not a dict")
        assert len(errors) == 1
        assert "expected dict" in errors[0].message

    def test_missing_field(self) -> None:
        """Test with missing required field."""
        schema = Schema({
            "name": StringValidator(),
            "age": IntValidator(),
        })
        errors = schema.validate({"name": "Alice"})
        assert len(errors) == 1
        assert errors[0].path == "age"
        assert "required" in errors[0].message

    def test_invalid_field_value(self) -> None:
        """Test with invalid field value."""
        schema = Schema({
            "name": StringValidator(),
            "age": IntValidator(),
        })
        errors = schema.validate({"name": "Alice", "age": "thirty"})
        assert len(errors) == 1
        assert errors[0].path == "age"
        assert "expected integer" in errors[0].message

    def test_extra_field_not_allowed(self) -> None:
        """Test that extra fields cause errors by default."""
        schema = Schema({"name": StringValidator()})
        errors = schema.validate({"name": "Alice", "extra": "field"})
        assert len(errors) == 1
        assert errors[0].path == "extra"
        assert "unexpected" in errors[0].message

    def test_extra_field_allowed(self) -> None:
        """Test that extra fields are allowed when configured."""
        schema = Schema({"name": StringValidator()}, allow_extra=True)
        assert schema.is_valid({"name": "Alice", "extra": "field"})

    def test_multiple_errors(self) -> None:
        """Test collecting multiple errors."""
        schema = Schema({
            "name": StringValidator(),
            "age": IntValidator(),
        })
        errors = schema.validate({"name": 123, "age": "invalid"})
        assert len(errors) == 2
        paths = {e.path for e in errors}
        assert "name" in paths
        assert "age" in paths

    def test_nested_path(self) -> None:
        """Test path with base path."""
        schema = Schema({"name": StringValidator()})
        errors = schema.validate({"name": 123}, path="user")
        assert len(errors) == 1
        assert errors[0].path == "user.name"

    def test_with_constraints(self) -> None:
        """Test schema with constrained validators."""
        schema = Schema({
            "username": ConstrainedString(min_length=3, max_length=20),
            "age": ConstrainedInt(min_value=0, max_value=150),
        })
        assert schema.is_valid({"username": "alice", "age": 30})
        assert not schema.is_valid({"username": "ab", "age": 30})
        assert not schema.is_valid({"username": "alice", "age": -1})

    def test_empty_schema(self) -> None:
        """Test empty schema."""
        schema = Schema({})
        assert schema.is_valid({})
        assert not schema.is_valid({"extra": "field"})

    def test_empty_schema_allow_extra(self) -> None:
        """Test empty schema that allows extra fields."""
        schema = Schema({}, allow_extra=True)
        assert schema.is_valid({})
        assert schema.is_valid({"any": "field"})
```

Replace `src/data_validator/__init__.py` with:
```python
"""DataValidator - Zero-dependency Python validation library."""

from __future__ import annotations

from data_validator.constraints import (
    ConstrainedFloat,
    ConstrainedInt,
    ConstrainedString,
)
from data_validator.errors import ValidationError
from data_validator.schema import Schema
from data_validator.validators import (
    BoolValidator,
    FloatValidator,
    IntValidator,
    StringValidator,
)

__version__ = "0.1.0"
__all__ = [
    "BoolValidator",
    "ConstrainedFloat",
    "ConstrainedInt",
    "ConstrainedString",
    "FloatValidator",
    "IntValidator",
    "Schema",
    "StringValidator",
    "ValidationError",
    "__version__",
]
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
pytest tests/ -v --cov=data_validator --cov-report=term-missing --cov-fail-under=100
# Expected: 50 tests passed, 100% coverage
```

**Success Criteria:**
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] All 50 tests pass
- [ ] 100% code coverage
- [ ] Schema importable from package

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/data_validator/schema.py`, `tests/test_schema.py`
- **Files Modified**: `src/data_validator/__init__.py`
- **Tests**: 50 tests, 100% coverage
- **Verification**: [To be filled]

---

### Subtask 2.2.2: Add Test for ValidationError

**Prerequisites:** 2.2.1 complete

**Deliverables:**
- [ ] `tests/test_errors.py` - Tests for error module

**Complete Code:**

Create file `tests/test_errors.py`:
```python
"""Tests for error types."""

from __future__ import annotations

import pytest

from data_validator.errors import ValidationError


class TestValidationError:
    """Tests for ValidationError."""

    def test_message_only(self) -> None:
        """Test error with message only."""
        error = ValidationError("something went wrong")
        assert error.message == "something went wrong"
        assert error.path == ""
        assert str(error) == "something went wrong"

    def test_with_path(self) -> None:
        """Test error with path."""
        error = ValidationError("invalid value", path="user.email")
        assert error.message == "invalid value"
        assert error.path == "user.email"
        assert str(error) == "user.email: invalid value"

    def test_repr(self) -> None:
        """Test string representation."""
        error = ValidationError("bad", path="field")
        assert repr(error) == "ValidationError(path='field', message='bad')"

    def test_equality(self) -> None:
        """Test equality comparison."""
        error1 = ValidationError("msg", path="path")
        error2 = ValidationError("msg", path="path")
        error3 = ValidationError("other", path="path")
        error4 = ValidationError("msg", path="other")

        assert error1 == error2
        assert error1 != error3
        assert error1 != error4
        assert error1 != "not an error"

    def test_is_exception(self) -> None:
        """Test that ValidationError is an exception."""
        error = ValidationError("test")
        assert isinstance(error, Exception)

        with pytest.raises(ValidationError):
            raise error
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
pytest tests/ -v --cov=data_validator --cov-report=term-missing --cov-fail-under=100
# Expected: 55 tests passed, 100% coverage
```

**Success Criteria:**
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] All 55 tests pass
- [ ] 100% code coverage

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `tests/test_errors.py`
- **Tests**: 55 tests, 100% coverage
- **Verification**: [To be filled]

---

### Task 2.2 Complete - Squash Merge

**When all subtasks (2.2.1, 2.2.2) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/2.2-schema

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/2.2-schema
git commit -m "feat(schema): add schema validation

- Add Schema class for dict validation
- Support required fields and extra field control
- Add comprehensive ValidationError tests
- 55 tests, 100% coverage"
git push origin main

# Delete feature branch
git branch -d feature/2.2-schema
git push origin --delete feature/2.2-schema
```

**Checklist:**
- [ ] All subtasks complete (2.2.1, 2.2.2)
- [ ] All tests pass with 100% coverage
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

# Project Complete Checklist

- [ ] Phase 1: Core Foundation complete
- [ ] Phase 2: Advanced Features complete
- [ ] All tests pass (55 tests)
- [ ] 100% code coverage
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] Zero runtime dependencies
- [ ] Clean git history (squash merges only)

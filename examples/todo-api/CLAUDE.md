# CLAUDE.md - TodoAPI

## Project Overview

TodoAPI is a minimal REST API for managing todo items, built with FastAPI and SQLite.

## Quick Reference

| Item | Value |
|------|-------|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI |
| **Database** | SQLite + SQLAlchemy |
| **Validation** | Pydantic |
| **Test Framework** | pytest + httpx |
| **Linter** | ruff |
| **Type Checker** | mypy |

## Directory Structure

```
todo-api/
├── src/
│   └── todo_api/
│       ├── __init__.py      # Version and exports
│       ├── main.py          # FastAPI app setup
│       ├── models.py        # SQLAlchemy models
│       ├── schemas.py       # Pydantic schemas
│       ├── database.py      # Database connection
│       └── routes/
│           ├── __init__.py
│           └── todos.py     # Todo endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   └── test_todos.py        # API tests
├── pyproject.toml
├── PROJECT_BRIEF.md
├── CLAUDE.md
└── DEVELOPMENT_PLAN.md
```

## Commands

```bash
# Install in dev mode
pip install -e ".[dev]"

# Run the API
uvicorn todo_api.main:app --reload

# API Endpoints
# POST   /todos           - Create todo
# GET    /todos           - List todos
# GET    /todos/{id}      - Get todo
# PUT    /todos/{id}      - Update todo
# DELETE /todos/{id}      - Delete todo
# PATCH  /todos/{id}/complete - Mark complete

# Development
ruff check src tests     # Lint
mypy src                 # Type check
pytest tests/ -v --cov   # Test with coverage
```

## API Response Format

### Success Response
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "detail": "Todo not found"
}
```

## Coding Standards

### Imports
```python
from __future__ import annotations

# Standard library
from datetime import datetime
from typing import TYPE_CHECKING

# Third-party
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Local
from todo_api.database import get_db
from todo_api.models import Todo
from todo_api.schemas import TodoCreate, TodoResponse
```

### Type Hints
All functions must have type hints:
```python
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> Todo:
    """Get a todo by ID."""
    ...
```

### Docstrings
Google style:
```python
def create_todo(todo: TodoCreate, db: Session) -> Todo:
    """Create a new todo item.

    Args:
        todo: The todo data to create.
        db: Database session.

    Returns:
        The created todo item.

    Raises:
        HTTPException: If validation fails.
    """
```

### HTTP Status Codes
- 200: Success (GET, PUT, PATCH)
- 201: Created (POST)
- 204: No Content (DELETE)
- 404: Not Found
- 422: Validation Error

## Session Checklist

Before starting work:
- [ ] Read DEVELOPMENT_PLAN.md for current subtask
- [ ] Check git branch status
- [ ] Verify prerequisites are complete

Before committing:
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] `pytest tests/ -v --cov` passes with 100% coverage
- [ ] API docs work at http://localhost:8000/docs
- [ ] DEVELOPMENT_PLAN.md updated with completion notes

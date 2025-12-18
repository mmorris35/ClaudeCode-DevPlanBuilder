# DEVELOPMENT_PLAN.md - TodoAPI

> **Haiku-Executable Plan**: Every subtask contains complete, copy-pasteable code. Claude Haiku can execute this mechanically without inference.

## Project Summary

| Field | Value |
|-------|-------|
| **Project** | TodoAPI |
| **Goal** | Minimal REST API for managing todo items with SQLite persistence |
| **Phases** | 2 |
| **Tasks** | 4 |
| **Subtasks** | 7 |

---

## Phase Overview

| Phase | Name | Tasks | Status |
|-------|------|-------|--------|
| 1 | Project Setup | 2 | Pending |
| 2 | API Implementation | 2 | Pending |

---

# Phase 1: Project Setup

## Task 1.1: Initialize Project Structure

**Branch:** `feature/1.1-project-init`

### Subtask 1.1.1: Create pyproject.toml and Package Structure

**Prerequisites:** None

**Deliverables:**
- [ ] `pyproject.toml` - Project configuration
- [ ] `src/todo_api/__init__.py` - Package init
- [ ] `src/todo_api/main.py` - FastAPI app placeholder
- [ ] `tests/__init__.py` - Test package

**Complete Code:**

Create file `pyproject.toml`:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "todo-api"
version = "0.1.0"
description = "A minimal REST API for managing todo items"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "httpx>=0.26.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=todo_api --cov-report=term-missing"

[tool.coverage.run]
source = ["src/todo_api"]
branch = true

[tool.coverage.report]
fail_under = 100
show_missing = true
```

Create file `src/todo_api/__init__.py`:
```python
"""TodoAPI - A minimal REST API for managing todo items."""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = ["__version__"]
```

Create file `src/todo_api/main.py`:
```python
"""FastAPI application setup."""

from __future__ import annotations

from fastapi import FastAPI

from todo_api import __version__

app = FastAPI(
    title="TodoAPI",
    description="A minimal REST API for managing todo items",
    version=__version__,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
```

Create file `tests/__init__.py`:
```python
"""Test package for TodoAPI."""
```

**Verification:**
```bash
# Verify TOML is valid
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
# Expected: No output (success)

# Verify package structure
ls -la src/todo_api/
# Expected: __init__.py, main.py
```

**Success Criteria:**
- [ ] `pyproject.toml` exists and is valid TOML
- [ ] Package structure created
- [ ] `__version__` importable

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `pyproject.toml`, `src/todo_api/__init__.py`, `src/todo_api/main.py`, `tests/__init__.py`
- **Verification**: [To be filled]

---

### Subtask 1.1.2: Create Database Models and Schemas

**Prerequisites:** 1.1.1 complete

**Deliverables:**
- [ ] `src/todo_api/database.py` - Database connection
- [ ] `src/todo_api/models.py` - SQLAlchemy models
- [ ] `src/todo_api/schemas.py` - Pydantic schemas

**Complete Code:**

Create file `src/todo_api/database.py`:
```python
"""Database connection and session management."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Get database session.

    Yields:
        Database session that auto-closes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
```

Create file `src/todo_api/models.py`:
```python
"""SQLAlchemy database models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from todo_api.database import Base


class Todo(Base):
    """Todo item database model."""

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
```

Create file `src/todo_api/schemas.py`:
```python
"""Pydantic schemas for request/response validation."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TodoCreate(BaseModel):
    """Schema for creating a todo."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class TodoUpdate(BaseModel):
    """Schema for updating a todo."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    """Schema for todo response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime
```

**Verification:**
```bash
# Install dependencies first
pip install -e ".[dev]"

# Verify imports work
python -c "from todo_api.database import Base, get_db, init_db; print('OK')"
# Expected: OK

python -c "from todo_api.models import Todo; print('OK')"
# Expected: OK

python -c "from todo_api.schemas import TodoCreate, TodoResponse; print('OK')"
# Expected: OK
```

**Success Criteria:**
- [ ] Database module imports successfully
- [ ] Todo model defined with all fields
- [ ] Pydantic schemas defined

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/todo_api/database.py`, `src/todo_api/models.py`, `src/todo_api/schemas.py`
- **Verification**: [To be filled]

---

### Task 1.1 Complete - Squash Merge

**When all subtasks (1.1.1, 1.1.2) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/1.1-project-init

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/1.1-project-init
git commit -m "feat(setup): initialize project with database models

- Add pyproject.toml with FastAPI, SQLAlchemy dependencies
- Create package structure with database, models, schemas
- Set up SQLite database connection"
git push origin main

# Delete feature branch
git branch -d feature/1.1-project-init
git push origin --delete feature/1.1-project-init
```

**Checklist:**
- [ ] All subtasks complete (1.1.1, 1.1.2)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

## Task 1.2: Setup Testing Infrastructure

**Branch:** `feature/1.2-testing-setup`

### Subtask 1.2.1: Create Test Fixtures and Health Check Test

**Prerequisites:** Task 1.1 complete

**Deliverables:**
- [ ] `tests/conftest.py` - Test fixtures
- [ ] `tests/test_health.py` - Health check test

**Complete Code:**

Create file `tests/conftest.py`:
```python
"""Pytest fixtures for TodoAPI tests."""

from __future__ import annotations

from collections.abc import Generator
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from todo_api.database import Base, get_db
from todo_api.main import app

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database override."""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

Create file `tests/test_health.py`:
```python
"""Tests for health check endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestHealthCheck:
    """Test suite for health check endpoint."""

    def test_health_check_returns_healthy(self, client: TestClient) -> None:
        """Test that health check returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
```

**Verification:**
```bash
# Run health check test
pytest tests/test_health.py -v
# Expected: 1 passed

# Check coverage
pytest tests/test_health.py -v --cov=todo_api --cov-report=term-missing
# Expected: Shows coverage (not 100% yet, that's OK)
```

**Success Criteria:**
- [ ] Test fixtures work
- [ ] Health check test passes

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `tests/conftest.py`, `tests/test_health.py`
- **Verification**: [To be filled]

---

### Task 1.2 Complete - Squash Merge

**When all subtasks (1.2.1) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/1.2-testing-setup

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/1.2-testing-setup
git commit -m "test(setup): add testing infrastructure

- Add pytest fixtures with in-memory SQLite
- Add health check endpoint test"
git push origin main

# Delete feature branch
git branch -d feature/1.2-testing-setup
git push origin --delete feature/1.2-testing-setup
```

**Checklist:**
- [ ] All subtasks complete (1.2.1)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

# Phase 2: API Implementation

## Task 2.1: Implement CRUD Endpoints

**Branch:** `feature/2.1-crud-endpoints`

### Subtask 2.1.1: Create Todo Routes

**Prerequisites:** Task 1.2 complete

**Deliverables:**
- [ ] `src/todo_api/routes/__init__.py` - Routes package
- [ ] `src/todo_api/routes/todos.py` - Todo CRUD endpoints
- [ ] Update `src/todo_api/main.py` - Register routes

**Complete Code:**

Create file `src/todo_api/routes/__init__.py`:
```python
"""API routes package."""

from __future__ import annotations

from todo_api.routes.todos import router as todos_router

__all__ = ["todos_router"]
```

Create file `src/todo_api/routes/todos.py`:
```python
"""Todo CRUD endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todo_api.database import get_db
from todo_api.models import Todo
from todo_api.schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    """Create a new todo item.

    Args:
        todo: Todo data to create.
        db: Database session.

    Returns:
        The created todo item.
    """
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/", response_model=list[TodoResponse])
def list_todos(db: Session = Depends(get_db)) -> list[Todo]:
    """List all todo items.

    Args:
        db: Database session.

    Returns:
        List of all todo items.
    """
    return list(db.query(Todo).all())


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> Todo:
    """Get a single todo item by ID.

    Args:
        todo_id: ID of the todo to retrieve.
        db: Database session.

    Returns:
        The requested todo item.

    Raises:
        HTTPException: If todo not found.
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)
) -> Todo:
    """Update a todo item.

    Args:
        todo_id: ID of the todo to update.
        todo_update: Update data.
        db: Database session.

    Returns:
        The updated todo item.

    Raises:
        HTTPException: If todo not found.
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a todo item.

    Args:
        todo_id: ID of the todo to delete.
        db: Database session.

    Raises:
        HTTPException: If todo not found.
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()


@router.patch("/{todo_id}/complete", response_model=TodoResponse)
def mark_complete(todo_id: int, db: Session = Depends(get_db)) -> Todo:
    """Mark a todo item as complete.

    Args:
        todo_id: ID of the todo to mark complete.
        db: Database session.

    Returns:
        The updated todo item.

    Raises:
        HTTPException: If todo not found.
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = True
    db.commit()
    db.refresh(todo)
    return todo
```

Replace `src/todo_api/main.py` with:
```python
"""FastAPI application setup."""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from todo_api import __version__
from todo_api.database import init_db
from todo_api.routes import todos_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize database on startup."""
    init_db()
    yield


app = FastAPI(
    title="TodoAPI",
    description="A minimal REST API for managing todo items",
    version=__version__,
    lifespan=lifespan,
)

app.include_router(todos_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
```

**Verification:**
```bash
# Verify imports work
python -c "from todo_api.routes import todos_router; print('OK')"
# Expected: OK

# Run the app (in background, then kill)
timeout 5 uvicorn todo_api.main:app --host 0.0.0.0 --port 8000 || true
# Expected: Should start without errors
```

**Success Criteria:**
- [ ] Routes module imports successfully
- [ ] All 6 endpoints defined
- [ ] App starts without errors

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/todo_api/routes/__init__.py`, `src/todo_api/routes/todos.py`
- **Files Modified**: `src/todo_api/main.py`
- **Verification**: [To be filled]

---

### Subtask 2.1.2: Create CRUD Tests

**Prerequisites:** 2.1.1 complete

**Deliverables:**
- [ ] `tests/test_todos.py` - Complete test suite for todo endpoints

**Complete Code:**

Create file `tests/test_todos.py`:
```python
"""Tests for todo CRUD endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestCreateTodo:
    """Test suite for POST /todos."""

    def test_create_todo_success(self, client: TestClient) -> None:
        """Test creating a todo successfully."""
        response = client.post(
            "/todos/",
            json={"title": "Buy groceries", "description": "Milk, eggs, bread"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["description"] == "Milk, eggs, bread"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_create_todo_minimal(self, client: TestClient) -> None:
        """Test creating a todo with only title."""
        response = client.post("/todos/", json={"title": "Simple task"})

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Simple task"
        assert data["description"] is None

    def test_create_todo_empty_title_fails(self, client: TestClient) -> None:
        """Test that empty title fails validation."""
        response = client.post("/todos/", json={"title": ""})

        assert response.status_code == 422


class TestListTodos:
    """Test suite for GET /todos."""

    def test_list_todos_empty(self, client: TestClient) -> None:
        """Test listing todos when none exist."""
        response = client.get("/todos/")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_todos_with_items(self, client: TestClient) -> None:
        """Test listing todos when items exist."""
        client.post("/todos/", json={"title": "Task 1"})
        client.post("/todos/", json={"title": "Task 2"})

        response = client.get("/todos/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task 1"
        assert data[1]["title"] == "Task 2"


class TestGetTodo:
    """Test suite for GET /todos/{id}."""

    def test_get_todo_success(self, client: TestClient) -> None:
        """Test getting a todo by ID."""
        create_response = client.post("/todos/", json={"title": "Test task"})
        todo_id = create_response.json()["id"]

        response = client.get(f"/todos/{todo_id}")

        assert response.status_code == 200
        assert response.json()["title"] == "Test task"

    def test_get_todo_not_found(self, client: TestClient) -> None:
        """Test getting a non-existent todo."""
        response = client.get("/todos/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


class TestUpdateTodo:
    """Test suite for PUT /todos/{id}."""

    def test_update_todo_success(self, client: TestClient) -> None:
        """Test updating a todo."""
        create_response = client.post("/todos/", json={"title": "Original"})
        todo_id = create_response.json()["id"]

        response = client.put(
            f"/todos/{todo_id}",
            json={"title": "Updated", "description": "New description"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["description"] == "New description"

    def test_update_todo_partial(self, client: TestClient) -> None:
        """Test partial update of a todo."""
        create_response = client.post(
            "/todos/", json={"title": "Task", "description": "Original"}
        )
        todo_id = create_response.json()["id"]

        response = client.put(f"/todos/{todo_id}", json={"completed": True})

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Task"
        assert data["description"] == "Original"
        assert data["completed"] is True

    def test_update_todo_not_found(self, client: TestClient) -> None:
        """Test updating a non-existent todo."""
        response = client.put("/todos/999", json={"title": "Updated"})

        assert response.status_code == 404


class TestDeleteTodo:
    """Test suite for DELETE /todos/{id}."""

    def test_delete_todo_success(self, client: TestClient) -> None:
        """Test deleting a todo."""
        create_response = client.post("/todos/", json={"title": "To delete"})
        todo_id = create_response.json()["id"]

        response = client.delete(f"/todos/{todo_id}")

        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404

    def test_delete_todo_not_found(self, client: TestClient) -> None:
        """Test deleting a non-existent todo."""
        response = client.delete("/todos/999")

        assert response.status_code == 404


class TestMarkComplete:
    """Test suite for PATCH /todos/{id}/complete."""

    def test_mark_complete_success(self, client: TestClient) -> None:
        """Test marking a todo as complete."""
        create_response = client.post("/todos/", json={"title": "Task"})
        todo_id = create_response.json()["id"]

        response = client.patch(f"/todos/{todo_id}/complete")

        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_mark_complete_not_found(self, client: TestClient) -> None:
        """Test marking a non-existent todo as complete."""
        response = client.patch("/todos/999/complete")

        assert response.status_code == 404
```

**Verification:**
```bash
# Run all tests
pytest tests/ -v
# Expected: All tests pass (14+ tests)

# Check coverage
pytest tests/ -v --cov=todo_api --cov-report=term-missing
# Expected: 100% coverage
```

**Success Criteria:**
- [ ] All tests pass
- [ ] 100% code coverage
- [ ] All 6 endpoints tested

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `tests/test_todos.py`
- **Tests**: 14+ tests, 100% coverage
- **Verification**: [To be filled]

---

### Task 2.1 Complete - Squash Merge

**When all subtasks (2.1.1, 2.1.2) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/2.1-crud-endpoints

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/2.1-crud-endpoints
git commit -m "feat(api): implement todo CRUD endpoints

- Add POST /todos - create todo
- Add GET /todos - list todos
- Add GET /todos/{id} - get single todo
- Add PUT /todos/{id} - update todo
- Add DELETE /todos/{id} - delete todo
- Add PATCH /todos/{id}/complete - mark complete
- 14+ tests, 100% coverage"
git push origin main

# Delete feature branch
git branch -d feature/2.1-crud-endpoints
git push origin --delete feature/2.1-crud-endpoints
```

**Checklist:**
- [ ] All subtasks complete (2.1.1, 2.1.2)
- [ ] All tests pass with 100% coverage
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

## Task 2.2: Final Verification

**Branch:** `feature/2.2-final-verify`

### Subtask 2.2.1: End-to-End Testing and Linting

**Prerequisites:** Task 2.1 complete

**Deliverables:**
- [ ] All quality checks pass
- [ ] API documentation works

**Commands to Execute:**
```bash
# Linting
ruff check src tests
# Expected: All checks passed!

# Type checking
mypy src
# Expected: Success: no issues found

# All tests with coverage
pytest tests/ -v --cov=todo_api --cov-report=term-missing --cov-fail-under=100
# Expected: All pass, 100% coverage

# Start server and test manually
uvicorn todo_api.main:app --reload &
sleep 2

# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Test create todo
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test todo","description":"Testing"}'
# Expected: JSON response with id, title, etc.

# Test list todos
curl http://localhost:8000/todos/
# Expected: Array with the created todo

# Check OpenAPI docs
curl http://localhost:8000/openapi.json | head -20
# Expected: OpenAPI schema JSON

# Kill the server
pkill -f uvicorn || true
```

**Success Criteria:**
- [ ] `ruff check src tests` passes
- [ ] `mypy src` passes
- [ ] `pytest` shows 100% coverage
- [ ] API responds to requests
- [ ] OpenAPI docs generated at /docs

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Verification**: [To be filled]

---

### Task 2.2 Complete - Squash Merge

**When all subtasks (2.2.1) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/2.2-final-verify

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/2.2-final-verify
git commit -m "test(api): complete end-to-end verification

- All linting and type checking passes
- 100% test coverage achieved
- API documentation verified"
git push origin main

# Delete feature branch
git branch -d feature/2.2-final-verify
git push origin --delete feature/2.2-final-verify
```

**Checklist:**
- [ ] All subtasks complete (2.2.1)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

# Project Complete Checklist

- [ ] Phase 1: Project Setup complete
- [ ] Phase 2: API Implementation complete
- [ ] All tests pass (14+ tests)
- [ ] 100% code coverage
- [ ] All endpoints work: POST, GET, PUT, DELETE, PATCH
- [ ] OpenAPI docs at /docs
- [ ] Clean git history (squash merges only)

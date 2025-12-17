# Producing Haiku-Executable Development Plans

> This guide explains how to write development plans that Claude Haiku can execute mechanically, without creative inference.

## The Problem

Default development plan output produces "Sonnet-level" plans: high-level descriptions that assume the executing model can:
- Infer correct imports from context
- Design appropriate function signatures
- Decide on file structure independently
- Write tests without explicit specifications

**Haiku needs paint-by-numbers precision.** Every ambiguity becomes a potential failure point.

---

## What Makes a Plan Haiku-Executable

### 1. Complete Code Blocks, Not Snippets

**Bad (Sonnet-level):**
```markdown
Create an upload endpoint that accepts video files and saves them to the project directory.
```

**Good (Haiku-executable):**
```markdown
Create `src/myapp/api/upload.py` with this exact content:

\`\`\`python
"""Video upload API endpoints."""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["upload"])

PROJECTS_DIR = Path("projects")
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB


class UploadResponse(BaseModel):
    """Response model for upload endpoint."""
    project_name: str
    file_path: str
    size_bytes: int


@router.post("/upload", response_model=UploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    name: str | None = Form(None),
    template: str = Form("default"),
) -> UploadResponse:
    """Upload a video file.

    Args:
        file: The video file to upload.
        name: Optional project name.
        template: Template to use for processing.

    Returns:
        Upload response with project details.

    Raises:
        HTTPException: If file is too large or invalid type.
    """
    # Validate file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # Generate project name
    project_name = name or f"project-{uuid.uuid4().hex[:8]}"
    project_dir = PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = project_dir / file.filename
    with file_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    return UploadResponse(
        project_name=project_name,
        file_path=str(file_path),
        size_bytes=file_path.stat().st_size,
    )
\`\`\`
```

### 2. Explicit Import Statements

**Bad:**
```markdown
Import the necessary FastAPI components for file uploads.
```

**Good:**
```markdown
Add these imports at the top of the file:
\`\`\`python
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
\`\`\`
```

### 3. Function Signatures with Full Type Hints

**Bad:**
```markdown
Create a function to process the upload.
```

**Good:**
```markdown
\`\`\`python
async def upload_video(
    file: UploadFile = File(...),
    name: str | None = Form(None),
    template: str = Form("default"),
) -> UploadResponse:
\`\`\`
```

### 4. Verification Commands with Expected Output

**Bad:**
```markdown
Run the tests to verify the implementation.
```

**Good:**
```markdown
**Verification:**
\`\`\`bash
pytest tests/api/test_upload.py -v
\`\`\`

Expected output:
\`\`\`
tests/api/test_upload.py::TestUploadEndpoint::test_upload_success PASSED
tests/api/test_upload.py::TestUploadEndpoint::test_upload_no_file PASSED
tests/api/test_upload.py::TestUploadEndpoint::test_upload_invalid_type PASSED
\`\`\`
```

### 5. Test Files with Complete Test Cases

**Bad:**
```markdown
Write tests for the upload endpoint covering success and error cases.
```

**Good:**
```markdown
Create `tests/api/test_upload.py`:

\`\`\`python
"""Tests for upload API."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from myapp.api.upload import router


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestUploadEndpoint:
    """Tests for POST /api/upload."""

    def test_upload_success(self, client: TestClient, tmp_path: Path) -> None:
        """Test successful video upload."""
        test_file = tmp_path / "test.mp4"
        test_file.write_bytes(b"fake video content")

        with patch("myapp.api.upload.PROJECTS_DIR", tmp_path):
            response = client.post(
                "/api/upload",
                files={"file": ("test.mp4", test_file.read_bytes(), "video/mp4")},
                data={"template": "default"},
            )

        assert response.status_code == 200
        data = response.json()
        assert "project_name" in data
        assert data["size_bytes"] > 0

    def test_upload_no_file(self, client: TestClient) -> None:
        """Test upload without file returns 422."""
        response = client.post("/api/upload", data={"template": "default"})
        assert response.status_code == 422

    def test_upload_file_too_large(self, client: TestClient, tmp_path: Path) -> None:
        """Test upload with oversized file returns 413."""
        # Implementation depends on how size checking is done
        pass
\`\`\`
```

### 6. Line-by-Line Edit Instructions

**Bad:**
```markdown
Add the upload router to the FastAPI app.
```

**Good:**
```markdown
In `src/myapp/api/main.py`, add this import after line 8:
\`\`\`python
from myapp.api.upload import router as upload_router
\`\`\`

Then add this line after the existing `app.include_router()` calls (around line 25):
\`\`\`python
app.include_router(upload_router)
\`\`\`
```

### 7. Explicit File Paths

**Bad:**
```markdown
Create the upload module in the API directory.
```

**Good:**
```markdown
Create file: `src/myapp/api/upload.py`
```

### 8. Checkpoint-Style Deliverables

**Bad:**
```markdown
- [ ] Upload endpoint works
- [ ] Tests pass
```

**Good:**
```markdown
- [ ] File exists: `src/myapp/api/upload.py`
- [ ] File exists: `tests/api/test_upload.py`
- [ ] `ruff check src/myapp/api/upload.py` exits 0
- [ ] `mypy src/myapp/api/upload.py` exits 0
- [ ] `pytest tests/api/test_upload.py -v` shows 3 passed
- [ ] Manual test: `curl -X POST -F "file=@test.mp4" http://localhost:8000/api/upload` returns JSON
```

---

## Recommended Subtask Structure

Each subtask should follow this template:

```markdown
### Subtask X.Y.Z: [Descriptive Name] (Single Session)

**Objective**: One sentence describing what this subtask accomplishes.

**Prerequisites**:
- [ ] X.Y.Z-1: [Previous subtask name]

**Deliverables**:
- [ ] `path/to/file1.py` - Brief description
- [ ] `path/to/file2.py` - Brief description
- [ ] `tests/path/to/test_file.py` - Test coverage

---

#### Step 1: Create [filename]

Create `path/to/file.py` with this exact content:

\`\`\`python
"""Module docstring."""

from __future__ import annotations

# Complete, copy-pasteable code here
\`\`\`

---

#### Step 2: Create tests

Create `tests/path/to/test_file.py`:

\`\`\`python
"""Tests for module."""

from __future__ import annotations

# Complete test file here
\`\`\`

---

#### Step 3: Wire up (if needed)

In `path/to/existing.py`, add this import after line X:
\`\`\`python
from module import thing
\`\`\`

Add this line after line Y:
\`\`\`python
# exact code to add
\`\`\`

---

#### Step 4: Update __init__.py exports

In `src/myapp/module/__init__.py`, add:
\`\`\`python
from myapp.module.file import ClassName, function_name

__all__ = ["ClassName", "function_name"]
\`\`\`

---

**Verification**:
\`\`\`bash
ruff check path/to/file.py
mypy path/to/file.py
pytest tests/path/to/test_file.py -v
\`\`\`

Expected: All commands exit 0, pytest shows N tests passed.

---

**Success Criteria**:
- [ ] File exists: `path/to/file.py`
- [ ] File exists: `tests/path/to/test_file.py`
- [ ] `ruff check path/to/file.py` exits 0
- [ ] `mypy path/to/file.py` exits 0
- [ ] `pytest tests/path/to/test_file.py -v` shows N tests passed

---

**Completion Notes**:
- **Implementation**:
- **Files Created**:
- **Files Modified**:
- **Tests**:
- **Build**:
- **Branch**:
- **Notes**:
```

---

## Common Gaps in Default Output

When reviewing or generating plans, watch for these common issues:

1. **Missing `__init__.py` exports**: When creating new modules, specify what to export
2. **Incomplete Pydantic models**: Need all fields, types, validators, and `model_config`
3. **Vague "update the config"**: Need exact keys, values, and file paths
4. **Missing error handling**: Specify which exceptions to catch and raise
5. **No test fixtures**: Need complete fixture code, not just "create a fixture"
6. **Unclear async vs sync**: Explicitly state `async def` vs `def`
7. **Missing type imports**: Include `from typing import ...` or `from __future__ import annotations`
8. **No expected output**: Every verification command needs expected results
9. **Ambiguous file locations**: Always use full paths from project root
10. **Missing dependencies**: Specify if new packages need to be installed

---

## Quality Checklist for Haiku-Executable Plans

Before considering a plan complete, verify each subtask has:

- [ ] Every code block is complete and copy-pasteable
- [ ] Every file has its full path specified
- [ ] Every function has complete type hints
- [ ] Every import is explicitly listed
- [ ] Every test file has complete test methods
- [ ] Every verification step has expected output
- [ ] Every edit instruction specifies exact location (line number or after what)
- [ ] Every new module specifies `__init__.py` updates
- [ ] Every Pydantic model has all fields defined
- [ ] Every API endpoint has request/response models

---

## Metrics for Success

A Haiku-executable plan should enable:

1. **Zero creative decisions**: Model just copies code and runs commands
2. **Mechanical verification**: Each step has a pass/fail check
3. **Atomic commits**: Each subtask is one coherent commit
4. **No backtracking**: Prerequisites contain everything needed
5. **Reproducible execution**: Two runs produce identical results

---

## Example: Before and After

### Before (Sonnet-level):

```markdown
### Subtask 2.1.1: Create User Model

Create a User model with fields for email, password hash, and creation timestamp.
Add validation and tests.
```

### After (Haiku-executable):

```markdown
### Subtask 2.1.1: Create User Model (Single Session)

**Objective**: Create the User database model with email, hashed password, and timestamps.

**Prerequisites**:
- [x] 0.1.1: Project setup complete

**Deliverables**:
- [ ] `src/myapp/models/user.py` - User SQLAlchemy model
- [ ] `tests/models/test_user.py` - Model tests

---

#### Step 1: Create User model

Create `src/myapp/models/user.py`:

\`\`\`python
"""User database model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from myapp.db.base import Base

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class User(Base):
    """User account model.

    Attributes:
        id: Primary key.
        email: Unique email address.
        password_hash: Bcrypt hashed password.
        created_at: Account creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(60), nullable=False)  # bcrypt hash length
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self) -> str:
        """Return string representation."""
        return f"<User(id={self.id}, email='{self.email}')>"
\`\`\`

---

#### Step 2: Update models __init__.py

In `src/myapp/models/__init__.py`, add:

\`\`\`python
from myapp.models.user import User

__all__ = ["User"]
\`\`\`

---

#### Step 3: Create tests

Create `tests/models/test_user.py`:

\`\`\`python
"""Tests for User model."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from myapp.db.base import Base
from myapp.models.user import User


@pytest.fixture
def db_session() -> Session:
    """Create in-memory database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


class TestUserModel:
    """Tests for User model."""

    def test_create_user(self, db_session: Session) -> None:
        """Test creating a user."""
        user = User(
            email="test@example.com",
            password_hash="$2b$12$hashedpassword",
        )
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.created_at is not None

    def test_user_repr(self, db_session: Session) -> None:
        """Test user string representation."""
        user = User(email="test@example.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()

        assert "test@example.com" in repr(user)

    def test_email_unique_constraint(self, db_session: Session) -> None:
        """Test that duplicate emails raise error."""
        user1 = User(email="test@example.com", password_hash="hash1")
        user2 = User(email="test@example.com", password_hash="hash2")

        db_session.add(user1)
        db_session.commit()

        db_session.add(user2)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
\`\`\`

---

**Verification**:
\`\`\`bash
ruff check src/myapp/models/user.py tests/models/test_user.py
mypy src/myapp/models/user.py
pytest tests/models/test_user.py -v
\`\`\`

Expected:
\`\`\`
All checks passed!
Success: no issues found in 1 source file
tests/models/test_user.py::TestUserModel::test_create_user PASSED
tests/models/test_user.py::TestUserModel::test_user_repr PASSED
tests/models/test_user.py::TestUserModel::test_email_unique_constraint PASSED
\`\`\`

---

**Success Criteria**:
- [ ] File exists: `src/myapp/models/user.py`
- [ ] File exists: `tests/models/test_user.py`
- [ ] `ruff check src/myapp/models/user.py` exits 0
- [ ] `mypy src/myapp/models/user.py` exits 0
- [ ] `pytest tests/models/test_user.py -v` shows 3 passed

---

**Completion Notes**:
- **Implementation**:
- **Files Created**:
- **Files Modified**:
- **Tests**:
- **Build**:
- **Branch**:
- **Notes**:
```

---

---

## Complete Example

See **[examples/hello-cli/](../examples/hello-cli/)** for a complete, minimal Haiku-executable example:

- `PROJECT_BRIEF.md` - Simple CLI requirements
- `CLAUDE.md` - Coding standards
- `DEVELOPMENT_PLAN.md` - **Full Haiku-executable plan** with complete code blocks
- `hello-cli-executor.md` - Executor agent

This example demonstrates every principle in this guide.

---

*This guide was created based on lessons learned from building development plans targeting Claude Haiku execution.*

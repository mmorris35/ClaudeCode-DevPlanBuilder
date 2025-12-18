# Best Practices and Anti-Patterns

> Learn what makes a good development plan vs. a bad one. Avoid common mistakes that break Haiku-executability.

---

## Anti-Patterns (What NOT to Do)

### 1. Vague Deliverables

**❌ Bad:**
```markdown
**Deliverables:**
- [ ] Implement user authentication
- [ ] Add error handling
- [ ] Create database models
```

**✅ Good:**
```markdown
**Deliverables:**
- [ ] `src/auth/login.py` - Create `login(email: str, password: str) -> Token` function
- [ ] `src/auth/exceptions.py` - Create `AuthenticationError`, `InvalidCredentialsError` classes
- [ ] `src/models/user.py` - Create `User` dataclass with `id`, `email`, `hashed_password` fields
```

**Why it matters:** Haiku needs explicit file paths and function signatures. "Implement authentication" requires inference about what files to create, what functions to write, and what patterns to use.

---

### 2. Missing Code Blocks

**❌ Bad:**
```markdown
**Deliverables:**
- [ ] Add error handling to the API endpoints

**Complete Code:**
(no code provided)
```

**✅ Good:**
```markdown
**Deliverables:**
- [ ] `src/api/errors.py` - Error handler middleware

**Complete Code:**

Create file `src/api/errors.py`:
```python
"""Error handling middleware for API."""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from myapp.exceptions import AppError, NotFoundError, ValidationError


async def error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle application errors with structured JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": str(exc),
            "details": exc.details,
        },
    )
```
```

**Why it matters:** Without complete code, Haiku must infer the implementation. This leads to inconsistent patterns, missing imports, and code that doesn't match project conventions.

---

### 3. Circular Prerequisites

**❌ Bad:**
```markdown
### Subtask 1.2.1: Create User Model
**Prerequisites:** 1.3.1 complete (needs database connection)

### Subtask 1.3.1: Setup Database Connection
**Prerequisites:** 1.2.1 complete (needs User model for testing)
```

**✅ Good:**
```markdown
### Subtask 1.2.1: Setup Database Connection
**Prerequisites:** 1.1.1 complete

### Subtask 1.2.2: Create User Model
**Prerequisites:** 1.2.1 complete (database connection available)

### Subtask 1.2.3: Test Database with User Model
**Prerequisites:** 1.2.2 complete
```

**Why it matters:** Circular dependencies make execution impossible. The executor will be stuck waiting for prerequisites that can never be met.

---

### 4. Oversized Subtasks

**❌ Bad:**
```markdown
### Subtask 2.1.1: Implement Complete User Management System (Single Session)

**Deliverables:**
- [ ] User registration endpoint
- [ ] User login endpoint
- [ ] Password reset flow
- [ ] Email verification
- [ ] User profile CRUD
- [ ] Avatar upload
- [ ] Account deletion
- [ ] Admin user management
- [ ] Role-based permissions
- [ ] Audit logging
- [ ] Session management
- [ ] OAuth integration
- [ ] 2FA setup
- [ ] API rate limiting
- [ ] Tests for all above
```

**✅ Good:**
```markdown
### Subtask 2.1.1: User Registration Endpoint (Single Session)

**Deliverables:**
- [ ] `src/api/routes/auth.py` - POST /register endpoint
- [ ] `src/services/user.py` - `create_user()` function
- [ ] `src/models/user.py` - User model with validation
- [ ] `tests/test_registration.py` - Registration tests

### Subtask 2.1.2: User Login Endpoint (Single Session)
...

### Subtask 2.1.3: Password Reset Flow (Single Session)
...
```

**Why it matters:** Subtasks should be completable in 2-4 hours. Oversized subtasks lead to incomplete work, context loss between sessions, and difficulty tracking progress.

**Rule of thumb:** 3-7 deliverables per subtask. If you have more, split it.

---

### 5. Implicit Knowledge Required

**❌ Bad:**
```markdown
**Technology Decisions:**
- Use standard error handling patterns
- Follow project conventions for logging
- Apply typical security best practices
```

**✅ Good:**
```markdown
**Technology Decisions:**
- Error handling: Use `try/except` with custom `AppError` base class, log with `structlog`
- Logging: `logger = structlog.get_logger(__name__)`, log at INFO for success, ERROR for failures
- Security: Hash passwords with `bcrypt`, validate input with Pydantic, sanitize SQL with parameterized queries
```

**Why it matters:** "Standard patterns" means different things to different models/sessions. Explicit decisions ensure consistency across the entire project.

---

### 6. Missing Tests in Subtasks

**❌ Bad:**
```markdown
### Subtask 2.1.1: Create User Service (Single Session)

**Deliverables:**
- [ ] `src/services/user.py` - UserService class
- [ ] `src/models/user.py` - User model

### Subtask 2.5.1: Write All Tests (Single Session)

**Deliverables:**
- [ ] Tests for UserService
- [ ] Tests for User model
- [ ] Tests for everything else...
```

**✅ Good:**
```markdown
### Subtask 2.1.1: Create User Service (Single Session)

**Deliverables:**
- [ ] `src/services/user.py` - UserService class
- [ ] `src/models/user.py` - User model
- [ ] `tests/test_user_service.py` - UserService tests
- [ ] `tests/test_user_model.py` - User model tests
```

**Why it matters:** Tests written alongside code catch bugs immediately. Deferred testing leads to tests that don't match implementation, or tests that never get written.

---

### 7. Branching at Subtask Level

**❌ Bad:**
```markdown
### Subtask 1.2.1: Create Models
**Branch:** `feature/1.2.1-create-models`

### Subtask 1.2.2: Create Routes
**Branch:** `feature/1.2.2-create-routes`

### Subtask 1.2.3: Add Tests
**Branch:** `feature/1.2.3-add-tests`
```

**✅ Good:**
```markdown
## Task 1.2: User Authentication
**Branch:** `feature/1.2-user-auth`

### Subtask 1.2.1: Create Models
(commits to feature/1.2-user-auth)

### Subtask 1.2.2: Create Routes
(commits to feature/1.2-user-auth)

### Subtask 1.2.3: Add Tests
(commits to feature/1.2-user-auth)

### Task 1.2 Complete - Squash Merge
(squash merge feature/1.2-user-auth to main)
```

**Why it matters:** One branch per subtask creates merge chaos. You end up with dozens of branches, complex merge conflicts, and a messy git history. One branch per task keeps things clean.

---

### 8. Verification Without Expected Output

**❌ Bad:**
```markdown
**Verification:**
```bash
pytest tests/
ruff check src/
mypy src/
```
```

**✅ Good:**
```markdown
**Verification:**
```bash
# Run tests
pytest tests/test_user.py -v
# Expected: 5 passed in 0.XXs

# Lint check
ruff check src/services/user.py
# Expected: All checks passed!

# Type check
mypy src/services/user.py
# Expected: Success: no issues found in 1 source file
```
```

**Why it matters:** Without expected output, the executor doesn't know if the command succeeded or failed. Explicit expectations enable automated verification.

---

## Best Practices (What TO Do)

### 1. Complete, Copy-Pasteable Code

Every subtask should have code that can be copied directly into files:

```markdown
**Complete Code:**

Create file `src/utils/helpers.py`:
```python
"""Utility helper functions."""

from __future__ import annotations

from pathlib import Path


def ensure_directory(path: Path) -> Path:
    """Ensure directory exists, creating if necessary.

    Args:
        path: Directory path to ensure exists.

    Returns:
        The same path, guaranteed to exist.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
```
```

---

### 2. Explicit File Paths

Never use vague language. Always specify exact paths:

```markdown
**Files to Create:**
- `src/myapp/services/user.py` - User service with CRUD operations
- `src/myapp/models/user.py` - User dataclass with validation
- `tests/services/test_user.py` - User service tests

**Files to Modify:**
- `src/myapp/__init__.py` - Add `UserService` to exports
- `src/myapp/services/__init__.py` - Add `user` module import
```

---

### 3. Testable Success Criteria

Success criteria should be verifiable with commands:

```markdown
**Success Criteria:**
- [ ] `pytest tests/test_user.py -v` shows 5 tests passing
- [ ] `ruff check src/services/user.py` exits with code 0
- [ ] `mypy src/services/user.py` reports no errors
- [ ] `python -c "from myapp.services import UserService"` imports successfully
```

---

### 4. Linear Prerequisite Chain

Each subtask should build on previous work:

```markdown
### Subtask 1.1.1: Create pyproject.toml
**Prerequisites:** None

### Subtask 1.1.2: Create package structure
**Prerequisites:** 1.1.1 complete

### Subtask 1.1.3: Install dependencies
**Prerequisites:** 1.1.2 complete

### Subtask 1.2.1: Create base models
**Prerequisites:** 1.1.3 complete (dependencies available)
```

---

### 5. Single Session Scope

Each subtask must be completable in one sitting (2-4 hours):

**Checklist for right-sizing:**
- [ ] 3-7 deliverables (not more)
- [ ] Creates/modifies 1-3 files (not more)
- [ ] One logical unit of work
- [ ] Can be tested independently
- [ ] Clear start and end points

---

### 6. Verification Commands with Expected Output

Always include what success looks like:

```markdown
**Verification:**
```bash
# Test the CLI
python -m myapp.cli --help
# Expected output:
# Usage: python -m myapp.cli [OPTIONS] COMMAND [ARGS]...
#
# Options:
#   --version  Show version and exit.
#   --help     Show this message and exit.
#
# Commands:
#   process  Process input files.
#   validate Validate configuration.
```
```

---

### 7. Task Complete Sections with Git Commands

Every task ends with explicit merge instructions:

```markdown
### Task 1.2 Complete - Squash Merge

**When all subtasks (1.2.1, 1.2.2, 1.2.3) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/1.2-user-auth

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/1.2-user-auth
git commit -m "feat(auth): implement user authentication

- Add User model with validation
- Create login/register endpoints
- Add JWT token generation
- 15 tests, 95% coverage"
git push origin main

# Delete feature branch
git branch -d feature/1.2-user-auth
git push origin --delete feature/1.2-user-auth
```

**Checklist:**
- [ ] All subtasks complete
- [ ] All tests pass
- [ ] Squash merged to main
- [ ] Feature branch deleted
```

---

### 8. Completion Notes Template

Provide a template for knowledge capture:

```markdown
**Completion Notes:**
- **Implementation**: [What was done, key decisions made]
- **Files Created**: [List with line counts]
- **Files Modified**: [List with changes]
- **Tests**: [Number of tests, coverage percentage]
- **Build**: [ruff/mypy/pytest results]
- **Branch**: [Branch name]
- **Notes**: [Any issues encountered, future considerations]
```

---

## Quick Reference Checklist

Before considering a subtask complete, verify:

- [ ] All deliverables have explicit file paths
- [ ] All code blocks are complete and copy-pasteable
- [ ] All imports are listed (no implicit imports)
- [ ] All function signatures have type hints
- [ ] Tests are included in the same subtask
- [ ] Verification commands have expected output
- [ ] Prerequisites reference valid, earlier subtask IDs
- [ ] Single session scope (3-7 deliverables, 2-4 hours)

---

## See Also

- [examples/hello-cli/DEVELOPMENT_PLAN.md](../examples/hello-cli/DEVELOPMENT_PLAN.md) - Complete example following all best practices
- [HAIKU_EXECUTABLE_PLANS.md](HAIKU_EXECUTABLE_PLANS.md) - Deep dive into Haiku-executable plans
- [ERROR_RECOVERY.md](ERROR_RECOVERY.md) - What to do when things go wrong

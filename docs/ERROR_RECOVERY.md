# Error Recovery Guide

> What to do when things go wrong during development plan execution.

---

## 1. Test Failures Mid-Subtask

### Symptoms
- `pytest` exits with non-zero code
- Test output shows `FAILED` or `ERROR`
- Coverage below required threshold

### Immediate Action
**DO NOT commit broken code.** Stop and diagnose.

### Resolution Steps

1. **Read the error message carefully**
   ```bash
   pytest tests/test_failing.py -v --tb=long
   ```

2. **Identify the root cause**
   - Is the test wrong? (Testing incorrect behavior)
   - Is the implementation wrong? (Bug in code)
   - Is it a setup issue? (Missing fixture, wrong import)

3. **Fix and re-run**
   ```bash
   # Fix the issue, then:
   pytest tests/test_failing.py -v
   # Expected: All tests pass
   ```

4. **Update DEVELOPMENT_PLAN.md** with what you learned:
   ```markdown
   **Completion Notes:**
   - **Implementation**: Fixed off-by-one error in pagination logic
   - **Notes**: Test initially failed due to edge case with empty results
   ```

### When to Mark as Blocked

Mark subtask as **BLOCKED** if:
- External dependency is broken
- Prerequisite was incorrectly marked complete
- Requirement is unclear/contradictory

```markdown
**Completion Notes:**
- **Status**: BLOCKED
- **Error**: `ImportError: No module named 'missing_dep'`
- **Root Cause**: Dependency not in pyproject.toml
- **Suggested Fix**: Add `missing_dep>=1.0.0` to dependencies
```

### Prevention
- Run tests after every file change
- Write tests before implementation (TDD)
- Use `pytest --tb=short` for quick feedback

---

## 2. Merge Conflicts

### Symptoms
- `git merge` or `git pull` shows conflict markers
- Files contain `<<<<<<<`, `=======`, `>>>>>>>`
- Git status shows "both modified"

### Immediate Action
**DO NOT force push or blindly accept one side.**

### Resolution Steps

1. **See what's conflicted**
   ```bash
   git status
   # Shows files with conflicts
   ```

2. **Open each conflicted file** and look for markers:
   ```python
   <<<<<<< HEAD
   def process(data: str) -> str:
       return data.upper()
   =======
   def process(data: str) -> str:
       return data.strip().upper()
   >>>>>>> feature/1.2-user-auth
   ```

3. **Resolve by choosing the correct version** (or combining):
   ```python
   def process(data: str) -> str:
       return data.strip().upper()
   ```

4. **Mark as resolved and complete merge**
   ```bash
   git add path/to/resolved/file.py
   git commit -m "resolve: merge conflict in process function"
   ```

5. **Verify resolution is correct**
   ```bash
   pytest tests/ -v
   ruff check src/
   mypy src/
   ```

### When to Keep Local vs Remote

| Scenario | Keep |
|----------|------|
| Your change is newer and correct | Local (HEAD) |
| Remote has a bug fix you need | Remote (incoming) |
| Both changes are needed | Combine manually |
| Unsure | Ask for clarification |

### Prevention
- Pull from main before starting new work
- Keep feature branches short-lived
- Communicate with team about file ownership

---

## 3. Incomplete Prerequisites

### Symptoms
- Code references functions/classes that don't exist
- Import errors for modules that should exist
- Tests fail because fixtures are missing

### Immediate Action
**DO NOT proceed with current subtask.** Fix prerequisites first.

### Resolution Steps

1. **Identify what's missing**
   ```bash
   # If import fails:
   python -c "from myapp.services import UserService"
   # Error: cannot import name 'UserService'
   ```

2. **Check prerequisite subtask**
   - Open DEVELOPMENT_PLAN.md
   - Find the subtask that should have created this
   - Verify its completion notes

3. **If prerequisite was incorrectly marked complete:**
   ```markdown
   ### Subtask 1.2.1: Create User Service

   **Completion Notes:**
   - **Status**: INCOMPLETE (reopened)
   - **Issue**: Missing `get_user_by_email()` method
   - **Action**: Adding missing method
   ```

4. **Complete the missing work**
   - Add the missing code
   - Add tests for it
   - Run verification
   - Update completion notes

5. **Then continue with current subtask**

### Prevention
- Cross-check prerequisites actually exist in code before starting
- Run imports at start of each subtask
- Use verification commands that catch missing dependencies

---

## 4. External Dependency Issues

### Symptoms
- `pip install` fails
- Package version conflicts
- API changes in dependencies

### Immediate Action
**Document the error.** Don't waste time on repeated attempts.

### Resolution Steps

#### Package Installation Failures

1. **Check the error message**
   ```bash
   pip install problematic-package 2>&1 | tail -20
   ```

2. **Common fixes:**
   ```bash
   # Try different version
   pip install "problematic-package>=1.0,<2.0"

   # Update pip
   pip install --upgrade pip

   # Use system package manager for system deps
   # (e.g., libpq-dev for psycopg2)
   sudo apt-get install libpq-dev
   ```

3. **If unfixable, update the plan:**
   ```markdown
   **Technology Decisions:**
   - Changed from `problematic-package` to `alternative-package` due to installation issues
   ```

#### Version Conflicts

1. **See what's conflicting**
   ```bash
   pip check
   ```

2. **Create a clean environment**
   ```bash
   rm -rf .venv
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. **Pin versions in pyproject.toml** if needed

#### API Changes

1. **Check the changelog/migration guide**
2. **Update code to new API**
3. **Document the change in completion notes**

### Prevention
- Pin major versions in dependencies
- Use `pip freeze > requirements.lock` for reproducibility
- Test in clean environment periodically

---

## 5. Session Interruption

### Symptoms
- Need to stop mid-subtask
- Context will be lost
- Work is partially complete

### Immediate Action
**Save progress safely.** Don't leave uncommitted changes.

### Resolution Steps

1. **Create a WIP commit**
   ```bash
   git add .
   git commit -m "WIP: subtask 1.2.3 in progress

   - Created user service (complete)
   - Tests partially written (3/5)
   - TODO: Add error handling tests"
   ```

2. **Update DEVELOPMENT_PLAN.md** with progress:
   ```markdown
   **Completion Notes:**
   - **Status**: IN PROGRESS
   - **Completed**: UserService class, basic tests
   - **Remaining**: Error handling tests, docstrings
   - **Next Steps**: Run pytest, add missing tests
   ```

3. **Push to remote** (backup):
   ```bash
   git push origin feature/1.2-user-auth
   ```

### Resuming in New Session

1. **Read DEVELOPMENT_PLAN.md** to see where you left off
2. **Check the WIP commit** message for context
3. **Run verification** to see current state:
   ```bash
   pytest tests/ -v  # See what passes
   ruff check src/   # See lint status
   ```
4. **Complete remaining work**
5. **Amend the WIP commit** or create new commit:
   ```bash
   git add .
   git commit --amend -m "feat(user): add user service with full test coverage"
   ```

### Prevention
- Work in small increments
- Commit after each logical piece
- Keep subtasks sized for single sessions

---

## 6. Plan Needs Modification

### Symptoms
- Subtask requirements don't match reality
- Missing subtask discovered
- Order of subtasks is wrong

### When It's OK to Modify

✅ **OK to modify:**
- Adding missing prerequisite subtask
- Splitting oversized subtask
- Fixing incorrect file paths
- Adding forgotten deliverables

❌ **NOT OK to modify:**
- Changing requirements to match buggy code
- Removing tests to make subtask "complete"
- Skipping subtasks without documenting why

### Resolution Steps

1. **Document the deviation**
   ```markdown
   **Plan Modification Note:**
   - **Date**: 2024-01-15
   - **Change**: Split subtask 2.1.3 into 2.1.3 and 2.1.4
   - **Reason**: Original scope too large for single session
   - **Impact**: Renumbered subsequent subtasks
   ```

2. **Make the minimum necessary change**
   - Add missing subtask with proper structure
   - Update prerequisite references
   - Don't refactor unrelated parts

3. **Commit the plan change separately**
   ```bash
   git add DEVELOPMENT_PLAN.md
   git commit -m "docs(plan): split subtask 2.1.3 for better sizing"
   ```

4. **Continue execution** with updated plan

### When to Stop and Re-Plan

Stop execution and create a new plan if:
- More than 30% of subtasks need modification
- Fundamental architecture assumption was wrong
- New requirements invalidate existing work

```markdown
**Execution Halted:**
- **Reason**: API redesign required - REST → GraphQL
- **Completed**: Phase 0, Phase 1 (foundation still valid)
- **Action**: Create new DEVELOPMENT_PLAN_v2.md for Phase 2+
```

### Prevention
- Validate plan thoroughly before starting
- Do a "dry run" review of first few subtasks
- Build foundation phase first to catch issues early

---

## Quick Reference: Error Decision Tree

```
Error occurred
│
├── Tests failing?
│   ├── Test is wrong → Fix test
│   ├── Implementation is wrong → Fix code
│   └── Setup issue → Fix environment
│
├── Merge conflict?
│   ├── Your change is correct → Keep yours
│   ├── Their change is correct → Keep theirs
│   └── Both needed → Combine manually
│
├── Missing prerequisite?
│   ├── Was marked complete incorrectly → Reopen and fix
│   └── Was never created → Add missing subtask
│
├── Dependency issue?
│   ├── Version conflict → Pin versions
│   ├── Install failure → Check system deps
│   └── API changed → Update code
│
├── Session interrupted?
│   ├── Work done → WIP commit
│   └── No work → Just document progress
│
└── Plan wrong?
    ├── Minor issue → Fix and document
    └── Major issue → Stop and re-plan
```

---

## See Also

- [BEST_PRACTICES.md](BEST_PRACTICES.md) - Avoid errors in the first place
- [AUTONOMOUS_EXECUTION.md](AUTONOMOUS_EXECUTION.md) - Handling errors in autonomous mode
- [examples/hello-cli/](../examples/hello-cli/) - Reference example

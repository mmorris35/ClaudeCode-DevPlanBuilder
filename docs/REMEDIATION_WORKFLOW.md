# Remediation Workflow Guide

> **Purpose**: This document explains how to use devplan for post-release maintenance, converting GitHub issues into actionable remediation tasks.

---

## Overview

After your project ships, bugs and enhancement requests will come in through GitHub issues. The remediation workflow helps you:

1. **Parse GitHub issues** into structured task definitions
2. **Generate remediation phases** that integrate with your existing development plan
3. **Execute fixes systematically** using the same executor agent pattern
4. **Capture lessons learned** for future plan generation

This workflow uses two MCP tools:
- `devplan_parse_issue` - Analyze and classify GitHub issues
- `devplan_issue_to_task` - Generate remediation tasks from parsed issues

---

## R.X Phase Notation

Remediation phases use the `R.X` prefix (R.1, R.2, R.3, etc.) instead of numeric phases. This design avoids conflicts with your existing development plan phases.

### Why R.X?

```
Existing DEVELOPMENT_PLAN.md:
├── Phase 0: Foundation
├── Phase 1: Core Features
├── Phase 2: User Interface
├── Phase 3: Testing & Polish
└── Phase 4: Distribution

After remediation tasks appended:
├── Phase 0: Foundation
├── Phase 1: Core Features
├── Phase 2: User Interface
├── Phase 3: Testing & Polish
├── Phase 4: Distribution
├── Phase R.1: Fix authentication token expiry (Issue #803)
└── Phase R.2: Add dark mode support (Issue #815)
```

The `R.` prefix makes it clear these are remediation/maintenance tasks added post-release, not part of the original development plan.

### Task and Subtask IDs

Remediation tasks follow the same hierarchical structure:

| Level | Format | Example |
|-------|--------|---------|
| Phase | R.X | R.1, R.2, R.3 |
| Task | R.X.Y | R.1.1, R.2.1 |
| Subtask | R.X.Y.Z | R.1.1.1, R.1.1.2 |

---

## Issue Classification

When you parse an issue with `devplan_parse_issue`, it's automatically classified based on content analysis:

| Type | Indicator | Priority |
|------|-----------|----------|
| **security** | CVE, vulnerability, auth bypass, injection | critical |
| **regression** | "worked before", "broke after", version mentions | high |
| **bug** | Error messages, stack traces, unexpected behavior | medium-high |
| **performance** | Slow, timeout, memory, latency | medium |
| **enhancement** | Feature request, improvement, add support | medium |
| **documentation** | Docs, README, typo, unclear | low |

Classification affects:
- **Severity assignment** (critical/high/medium/low)
- **Subtask generation** (security issues get verification subtasks)
- **Git branch naming** (e.g., `fix/803-auth-token` vs `feat/815-dark-mode`)

---

## Subtask Generation

The `devplan_issue_to_task` tool generates subtasks based on issue type:

### Standard Bug Fix (2-3 subtasks)

```markdown
### Subtask R.1.1.1: Fix: [Root cause] (Quick Fix)
- [ ] Identify the root cause
- [ ] Implement the fix
- [ ] Add inline comments explaining the fix
- [ ] Run existing tests

### Subtask R.1.1.2: Test: Add regression test
- [ ] Create test case reproducing the original bug
- [ ] Verify test fails without fix, passes with fix
- [ ] Add edge case tests
```

### Security Issue (3 subtasks)

```markdown
### Subtask R.1.1.1: Fix: [Security issue] (Quick Fix)
- [ ] Implement security fix
- [ ] Follow security best practices
- [ ] Update dependencies if needed

### Subtask R.1.1.2: Test: Security regression tests
- [ ] Add test cases for the vulnerability
- [ ] Test related attack vectors

### Subtask R.1.1.3: Verify: Security validation
- [ ] Run security scanning tools
- [ ] Verify fix doesn't introduce new vulnerabilities
- [ ] Update security documentation
```

### Enhancement (2-4 subtasks)

```markdown
### Subtask R.1.1.1: Implement: [Feature name]
- [ ] Implement core functionality
- [ ] Add configuration options
- [ ] Update documentation

### Subtask R.1.1.2: Test: [Feature] tests
- [ ] Add unit tests
- [ ] Add integration tests if applicable
```

---

## Modes: Append vs Standalone

### Append Mode (Default)

Add remediation phases to your existing DEVELOPMENT_PLAN.md:

```
Use devplan_issue_to_task with mode: "append" to add phase R.1 to DEVELOPMENT_PLAN.md
```

**When to use:**
- The fix relates to existing code in the project
- You want a unified view of all work
- Multiple small fixes can share context
- You're actively maintaining the project

### Standalone Mode

Create a separate REMEDIATION_PLAN.md:

```
Use devplan_issue_to_task with mode: "standalone" to create REMEDIATION_PLAN.md
```

**When to use:**
- Isolated hotfix that shouldn't clutter the main plan
- Different team member handling the fix
- Emergency fix that needs its own tracking
- Multiple related issues being fixed together

---

## Complete Workflow

### Step 1: Fetch the GitHub Issue

```bash
gh issue view 803 --json number,title,body,labels,comments,url
```

Save the output or pipe it directly to the next step.

### Step 2: Parse the Issue (Optional)

```
Use devplan_parse_issue to analyze this issue:
[paste issue JSON]
```

This gives you:
- Issue classification (bug, security, enhancement, etc.)
- Severity assessment
- Suggested approach

### Step 3: Generate Remediation Task

```
Use devplan_issue_to_task to generate a remediation plan:
- Issue: [paste issue JSON]
- Mode: append (or standalone)
- Phase: R.1 (or next available R.X)
```

### Step 4: Review Generated Plan

The tool generates:
- Phase with goal and context
- Task with git strategy
- Subtasks with deliverables and success criteria

Review and adjust as needed before executing.

### Step 5: Execute Subtasks

Use your executor agent as usual:

```
Use the {project}-executor agent to execute subtask R.1.1.1
```

### Step 6: Capture Lessons (Optional)

If the fix reveals a pattern worth remembering:

```
Use devplan_add_lesson to capture this pattern:
- Category: [error-handling/testing/security/etc.]
- Pattern: [what went wrong or what we learned]
- Solution: [how to prevent this in future plans]
```

---

## Integration with Lessons Learned

The remediation workflow connects to the lessons learned system:

1. **During task generation**: Relevant lessons from `GLOBAL_LESSONS.md` are surfaced based on the issue classification

2. **After fixing**: Capture new lessons with `devplan_add_lesson` to improve future plans

3. **In future plans**: The plan generator incorporates these lessons automatically

Example: If you fix a security issue caused by missing input validation, capture the lesson:

```
Category: security
Pattern: User input passed directly to database queries
Solution: Always sanitize and validate user input. Add input validation subtask to all data-entry features.
```

Future plans will automatically include input validation requirements.

---

## Best Practices

### When to Batch Issues

Group related issues into a single remediation session when:
- They affect the same component
- They have the same root cause
- They're all low-priority and can be done together

```
Fetch issues #801, #803, #807 and generate as R.1, R.2, R.3
```

### When to Use Standalone Mode

- **Hotfixes**: Critical bugs needing immediate attention
- **External contributors**: Provide focused scope for PRs
- **Isolated features**: New functionality unrelated to main development

### Prioritization

Handle issues in this order:
1. **Security** - Immediate attention required
2. **Regression** - User expectations broken
3. **Bug** - Functionality impaired
4. **Performance** - Experience degraded
5. **Enhancement** - Nice to have
6. **Documentation** - Important but not urgent

### Git Workflow

Remediation tasks follow the same git discipline:

```
Branch: fix/803-auth-token-expiry (from main)
├── Subtask R.1.1.1 commit
├── Subtask R.1.1.2 commit
└── Squash merge to main when complete
```

---

## Example: Complete Remediation Flow

### The Issue

```json
{
  "number": 803,
  "title": "Authentication token expires during long operations",
  "body": "When uploading large files, the auth token expires mid-upload...",
  "labels": ["bug", "auth"],
  "url": "https://github.com/org/repo/issues/803"
}
```

### Generated Remediation Plan

```markdown
## Phase R.1: Fix authentication token expiry (Issue #803)

**Type**: Bug Fix
**Severity**: high
**Goal**: Resolve issue #803 - Authentication token expires during long operations

### Task R.1.1: Fix authentication token expiry

**Git Strategy**:
- **Branch**: `fix/803-auth-token-expiry` (from `main`)
- **Commit Prefix**: `fix`
- **Merge**: squash when task complete

---

#### Subtask R.1.1.1: Fix: Token refresh logic (Quick Fix)

**Prerequisites**: None

**Deliverables**:
- [ ] Implement token refresh before expiry
- [ ] Add buffer time (refresh when 80% of TTL elapsed)
- [ ] Handle refresh failure gracefully
- [ ] Add logging for token refresh events

**Files to Modify**:
- `src/auth/token_manager.py`

**Success Criteria**:
- [ ] Tokens refresh automatically during long operations
- [ ] No auth failures during 30+ minute uploads
- [ ] Refresh failures logged with clear error messages

---

#### Subtask R.1.1.2: Test: Token expiry regression tests

**Prerequisites**: R.1.1.1

**Deliverables**:
- [ ] Add test case simulating long operation
- [ ] Mock time advancement to trigger refresh
- [ ] Test refresh failure handling
- [ ] Verify logging output

**Files to Create**:
- `tests/test_token_refresh.py`

**Success Criteria**:
- [ ] Test reproduces original issue (fails without fix)
- [ ] Test passes with fix applied
- [ ] Edge cases covered (network timeout, invalid refresh token)

---

### Task R.1.1 Complete - Squash Merge

- [ ] All subtasks complete
- [ ] All tests pass
- [ ] PR created: `gh pr create --title "fix: token refresh during long operations" --body "Fixes #803"`
- [ ] Squash merged to main
- [ ] Issue closed
```

### Execution

```bash
# Execute fix
claude "Use the project-executor agent to execute subtask R.1.1.1"

# Execute tests
claude "Use the project-executor agent to execute subtask R.1.1.2"

# Merge and close
git checkout main && git merge --squash fix/803-auth-token-expiry
git commit -m "fix: token refresh during long operations (#803)"
gh issue close 803 --comment "Fixed in [commit hash]"
```

---

## Tool Reference

### devplan_parse_issue

Analyzes a GitHub issue and returns structured data:

**Input**: GitHub issue JSON (from `gh issue view --json`)

**Output**:
- `type`: bug, security, enhancement, etc.
- `severity`: critical, high, medium, low
- `summary`: One-line description
- `technical_details`: Extracted technical information
- `suggested_approach`: Recommended fix strategy

### devplan_issue_to_task

Generates a complete remediation task:

**Input**:
- `issue`: GitHub issue JSON
- `mode`: "append" or "standalone"
- `phase_id`: e.g., "R.1" (optional, auto-increments)

**Output**: Markdown content for phase/task/subtasks

---

## Related Documentation

- **[PROMPT_SEQUENCE.md](../PROMPT_SEQUENCE.md)** - Includes remediation prompts
- **[LESSONS_LEARNED.md](LESSONS_LEARNED.md)** - How the feedback loop works
- **[EXECUTOR_AGENT.md](EXECUTOR_AGENT.md)** - Executing remediation subtasks
- **[examples/remediation/](../examples/remediation/)** - Example remediation plans

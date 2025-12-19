# Verifier Agent

> **Purpose**: Validate that a completed application actually works and meets the requirements in PROJECT_BRIEF.md.

---

## Why a Separate Verifier?

The executor agent uses **haiku** to mechanically execute subtasks. It checks boxes and runs tests, but it doesn't *think critically* about whether the product works as intended.

The verifier agent uses **sonnet** to:
- **Reason about requirements** - Does this actually do what was promised?
- **Try adversarial inputs** - What happens with edge cases the plan didn't anticipate?
- **Test integration** - Do the components work together, not just in isolation?
- **Provide actionable feedback** - What's broken and how to fix it?

---

## When to Use

Run the verifier after:
- Autonomous execution completes (`--dangerously-skip-permissions`)
- All phases/tasks in a plan are marked complete
- Before deploying or releasing

```bash
# After your build completes
claude "Use the {project}-verifier agent to validate the application against PROJECT_BRIEF.md"
```

---

## What It Checks

### 1. Smoke Tests
- Does the application start?
- Do basic commands/endpoints respond?
- Are there obvious crashes or errors?

### 2. Feature Verification
- Walk through each feature in PROJECT_BRIEF.md
- Verify it works as described
- Note any gaps or deviations

### 3. Edge Cases
- Empty inputs, very long inputs
- Invalid data types
- Boundary conditions (min/max values)
- Concurrent operations (if applicable)

### 4. Error Handling
- Does it fail gracefully?
- Are error messages helpful?
- Does it recover from errors?

### 5. Non-Functional Requirements
- Performance (response times, resource usage)
- Security (input validation, no obvious vulnerabilities)
- Accessibility (if applicable)

---

## Verification Report Format

The verifier produces a structured report:

```markdown
# Verification Report: {Project Name}

## Summary
- **Status**: PASS / PARTIAL / FAIL
- **Features Verified**: X/Y
- **Critical Issues**: N
- **Warnings**: M

## Feature Verification

### Feature 1: {Name}
- **Status**: ✅ PASS / ⚠️ PARTIAL / ❌ FAIL
- **Test**: {What was tested}
- **Result**: {What happened}
- **Notes**: {Any observations}

### Feature 2: {Name}
...

## Edge Case Testing

| Test Case | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Empty input | Error message | Crashed | ❌ |
| Max length | Truncate | Works | ✅ |
...

## Issues Found

### Critical (Must Fix)
1. {Description} - {How to reproduce} - {Suggested fix}

### Warnings (Should Fix)
1. {Description} - {Impact} - {Suggested fix}

### Observations (Nice to Have)
1. {Description}

## Recommendations
- {Next steps to address issues}
```

---

## Creating a Verifier Agent

Each project should have a `{project}-verifier.md` alongside the executor:

```
.claude/agents/
├── {project}-executor.md   # Haiku - executes plan
└── {project}-verifier.md   # Sonnet - validates result
```

See [examples/hello-cli/hello-cli-verifier.md](../examples/hello-cli/hello-cli-verifier.md) for a complete template.

---

## Key Differences from Executor

| Aspect | Executor | Verifier |
|--------|----------|----------|
| **Model** | haiku | sonnet |
| **Purpose** | Execute plan mechanically | Think critically about quality |
| **Input** | DEVELOPMENT_PLAN.md subtasks | PROJECT_BRIEF.md requirements |
| **Output** | Code + commits | Verification report |
| **Mindset** | "Check off deliverables" | "Try to break it" |

---

## Integration with Autonomous Workflow

For fully autonomous builds:

```bash
# 1. Execute the entire plan
claude --dangerously-skip-permissions \
  "Use the {project}-executor agent to execute the entire development plan"

# 2. Verify the result
claude "Use the {project}-verifier agent to validate against PROJECT_BRIEF.md"

# 3. Review the verification report before deploying
```

The verifier runs *without* `--dangerously-skip-permissions` so you can review its findings interactively.

---

## When Verification Fails

If the verifier reports issues, don't panic. Here's how to handle different failure types:

### Minor Issues (Typos, Small Bugs)

Fix directly in a normal Claude conversation:

```
The verifier found this issue: [paste from report]

Please fix it.
```

Claude will read the code, understand the problem, and make the fix. No special agent needed.

### Missing Edge Cases

If the verifier found edge cases the plan didn't anticipate:

```
The verifier found these edge cases aren't handled:
- Empty input causes crash
- Unicode characters display incorrectly

Please add handling for these cases and update the tests.
```

### Plan Was Wrong

If the plan's code blocks had bugs (so executing them perfectly still produced broken code):

1. Fix the immediate issue in the codebase
2. Optionally update DEVELOPMENT_PLAN.md so future executions don't repeat the mistake
3. Re-run verification on the affected area

### Multiple Failures

For reports with many issues, prioritize:

1. **Critical** - Fix these first, they're blockers
2. **Warnings** - Fix before release, but not urgent
3. **Observations** - Nice to have, fix if time permits

Work through them one at a time:

```
Let's fix the critical issues from the verification report.

Starting with: [first critical issue]
```

### Re-Verification

After fixing issues, re-run verification:

```
Use the {project}-verifier agent to re-verify the fixes for:
- [issue 1]
- [issue 2]
```

Or run full verification again if changes were extensive.

### When to Stop

The goal isn't a perfect verification report - it's working software. Stop when:

- All **critical** issues are resolved
- The application does what PROJECT_BRIEF.md promised
- Remaining issues are cosmetic or low-priority

Ship it, then address remaining items in a future iteration.

---

## Capturing Lessons Learned

After completing verification, capture valuable lessons to improve future projects.

### When to Capture

Capture a lesson when you find an issue that:
- Could have been prevented with better planning
- Is likely to recur in similar projects
- Reveals a pattern that should be documented

### How to Capture

**Option 1: Automatic Extraction**
```
Use devplan_extract_lessons_from_report with the verification report to automatically identify potential lessons
```

**Option 2: Manual Capture**
Use `devplan_add_lesson` with:
- issue: What went wrong
- root_cause: Why it happened
- fix: How to prevent it
- pattern: Short identifier
- project_types: Which project types it applies to
- severity: critical/warning/info

### Impact

Captured lessons are automatically incorporated into future plan generation:
1. As a "Lessons Learned Safeguards" section in DEVELOPMENT_PLAN.md
2. Injected directly into subtask success criteria for relevant tasks

This creates a feedback loop: **Execute → Verify → Capture → Improve → Execute better**

### Example

After finding that empty input crashes a CLI:

```bash
# The verifier found this issue
devplan_add_lesson \
  --issue "CLI crashes on empty string argument" \
  --root_cause "No guard clause for empty input" \
  --fix "Add 'if not arg: arg = default_value' guard" \
  --pattern "empty-input-guard" \
  --project_types "cli" \
  --severity "warning"
```

Future CLI plans will include this safeguard automatically.

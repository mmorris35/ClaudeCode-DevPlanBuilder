# Global Lessons Learned

> **Community-contributed patterns from real verification failures.**
>
> These lessons are read by Claude when generating new development plans.

---

## How to Use This File

**For Claude (Plan Generation):**
When generating a DEVELOPMENT_PLAN.md, read this file and incorporate relevant patterns based on project type.

**For Contributors:**
Submit lessons via GitHub Issues with label `lesson-learned`, or via Discussions.

---

## CLI Patterns

### Empty Input Handling
- **Pattern**: Always validate/handle empty string inputs for CLI arguments
- **Implementation**: Add guard clause `if not arg: arg = default_value`
- **Test**: Include `cli ""` in verification commands
- **Source**: Common failure across multiple CLI projects

### Unicode in Arguments
- **Pattern**: CLI arguments may contain unicode characters (emoji, non-ASCII)
- **Implementation**: Ensure string handling doesn't assume ASCII
- **Test**: Include `cli "José 🎉"` in edge case tests
- **Source**: User-submitted lesson

---

## API Patterns

### Structured Error Responses
- **Pattern**: All API errors should return JSON, not plain text
- **Implementation**: Add exception handlers that return `{"error": code, "message": msg}`
- **Test**: Verify 404/500 responses are valid JSON
- **Source**: Common FastAPI/Flask oversight

### Input Validation at Boundaries
- **Pattern**: Validate all input at API boundaries, not deep in business logic
- **Implementation**: Use Pydantic/marshmallow for request validation
- **Test**: Send malformed JSON, missing fields, wrong types
- **Source**: Security best practice

### Empty Request Bodies
- **Pattern**: Handle empty or null request bodies gracefully
- **Implementation**: Add explicit check before parsing
- **Test**: `curl -X POST /endpoint -d ''`
- **Source**: User-submitted lesson

---

## Web App Patterns

### Hydration Mismatches
- **Pattern**: Server-rendered HTML must match client hydration
- **Implementation**: Use `suppressHydrationWarning` sparingly, fix root cause
- **Test**: Check console for hydration warnings in dev mode
- **Source**: Next.js/React common issue

### Dark Mode Flash
- **Pattern**: Theme should be determined before first paint
- **Implementation**: Read localStorage in a blocking script or use cookies
- **Test**: Hard refresh with dark mode enabled, check for flash
- **Source**: User-submitted lesson

---

## Library Patterns

### Bool is Subclass of Int
- **Pattern**: In Python, `isinstance(True, int)` is True
- **Implementation**: Check `isinstance(x, bool)` before `isinstance(x, int)`
- **Test**: Verify `IntValidator().is_valid(True)` returns False
- **Source**: data-validator example discovery

### Zero Dependencies Verification
- **Pattern**: If claiming zero deps, verify imports don't pull extras
- **Implementation**: Test import in clean venv with no extras installed
- **Test**: `pip install . --no-deps && python -c "import mylib"`
- **Source**: Library best practice

---

## Universal Patterns

### Test What You Ship
- **Pattern**: Verification should test the installed package, not source
- **Implementation**: Run tests against `pip install -e .` not raw source
- **Test**: Verify import paths match package structure
- **Source**: Common oversight

### Verification Commands Need Expected Output
- **Pattern**: Don't just run commands, specify what success looks like
- **Implementation**: Add `# Expected: ...` comments after each command
- **Test**: Verifier can compare actual vs expected
- **Source**: BEST_PRACTICES.md

---

## Contributing

Found a pattern from your verification failures? Share it:

```bash
gh issue create \
  --repo mmorris35/ClaudeCode-DevPlanBuilder \
  --title "Lesson: [Your pattern title]" \
  --label "lesson-learned" \
  --body "## Pattern
[What to always do]

## Implementation
[How to do it]

## Test
[How to verify it]

## Project Type
[cli|api|web|library|all]"
```

Maintainers will review and add valuable patterns to this file.

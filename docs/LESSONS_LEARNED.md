# Lessons Learned System

> **Purpose**: Capture patterns from verification failures to improve future plans.

---

## How It Works

```
Execute → Verify → Capture Lessons → Generate Better Plans
```

1. **Verifier finds issues** during QA
2. **Lessons get appended** to `LESSONS_LEARNED.md` in the project
3. **Future plan generation** reads lessons and incorporates patterns
4. **Plans get better** over time based on real failures

---

## LESSONS_LEARNED.md Format

Each project can have a `LESSONS_LEARNED.md` file:

```markdown
# Lessons Learned

## YYYY-MM-DD: Short Title

- **Issue**: What went wrong
- **Root Cause**: Why it happened
- **Fix**: How it was resolved
- **Pattern**: Reusable lesson for future plans
- **Applies To**: [cli|api|web|library|all]

---
```

### Example Entry

```markdown
## 2025-12-17: Empty Input Crash

- **Issue**: CLI crashed with IndexError when given empty string
- **Root Cause**: Plan didn't include edge case test for empty input
- **Fix**: Added `if not name: name = "World"` guard in cli.py
- **Pattern**: Always validate/handle empty string inputs for CLI arguments
- **Applies To**: cli

---

## 2025-12-17: API Error Format

- **Issue**: 404 errors returned plain text instead of JSON
- **Root Cause**: FastAPI default error handler not overridden
- **Fix**: Added custom exception handler returning JSONResponse
- **Pattern**: All API errors should return structured JSON with error code and message
- **Applies To**: api

---
```

---

## Integration Points

### 1. Verifier Appends Lessons

After verification, the verifier should append any issues found:

```
After completing verification, append lessons learned to LESSONS_LEARNED.md:

For each issue found:
1. Create an entry with today's date
2. Document the issue, root cause, fix, and pattern
3. Tag with applicable project types

If LESSONS_LEARNED.md doesn't exist, create it with the header.
```

### 2. Plan Generation Reads Lessons

When generating a new DEVELOPMENT_PLAN.md, check for lessons:

```
Before generating the plan:
1. Check if LESSONS_LEARNED.md exists in the project
2. Read patterns that match this project type
3. Proactively include edge cases and guards based on lessons
4. Reference specific lessons in subtask notes where applicable
```

### 3. Cross-Project Learning (Advanced)

For learning across projects, maintain a global lessons file:

```
~/.claude/lessons/global-lessons.md
```

Or in the DevPlanBuilder repo itself:

```
examples/GLOBAL_LESSONS.md
```

---

## Verifier Integration

Add this to the end of each verifier agent:

```markdown
## After Verification

After producing the verification report, update LESSONS_LEARNED.md:

1. If any issues were found (Critical or Warning level):
   - Read existing LESSONS_LEARNED.md (or create if missing)
   - For each issue, create a lesson entry
   - Append to the file

2. Format each lesson as:
   ```markdown
   ## YYYY-MM-DD: {Short descriptive title}

   - **Issue**: {What the verifier found}
   - **Root Cause**: {Why it happened - was the plan wrong? Missing edge case?}
   - **Fix**: {How it was resolved}
   - **Pattern**: {Generalized lesson for future plans}
   - **Applies To**: {cli|api|web|library|all}

   ---
   ```

3. Commit the updated LESSONS_LEARNED.md
```

---

## Plan Generator Integration

When Claude generates a new DEVELOPMENT_PLAN.md, include this step:

```markdown
## Before Generating Plan

1. Check if LESSONS_LEARNED.md exists
2. If yes, read it and extract patterns matching this project type
3. For each relevant pattern:
   - Consider adding explicit edge case handling
   - Include in verification commands
   - Add to success criteria where appropriate

Example: If lessons show "empty input crashes CLIs", add:
- Test case for empty input in test file
- Guard clause in main function
- Verification command: `{cli} ""`
```

---

## Example Flow

**Project A (CLI) - First Build:**
1. Plan generated without lessons
2. Executor builds it
3. Verifier finds: empty string crashes
4. Lesson captured: "Always handle empty CLI args"

**Project B (CLI) - Later Build:**
1. Plan generator reads LESSONS_LEARNED.md
2. Sees pattern: "Always handle empty CLI args"
3. Plan includes empty string test case
4. Executor builds it with guard clause
5. Verifier passes on empty string test

---

---

## Reporting Lessons to the Mothership

Lessons learned locally can be shared back to improve DevPlanBuilder for everyone.

### Option 1: GitHub Discussions (Recommended)

Create a discussion in the "Lessons Learned" category:

```bash
gh api repos/mmorris35/ClaudeCode-DevPlanBuilder/discussions \
  -f title="Lesson: Empty CLI input handling" \
  -f body="$(cat <<'EOF'
## Issue
CLI crashed with IndexError when given empty string

## Root Cause
Plan didn't include edge case test for empty input

## Fix
Added guard clause: `if not name: name = "World"`

## Pattern
Always validate/handle empty string inputs for CLI arguments

## Project Type
cli
EOF
)" \
  -f category_id="DIC_kwDON..."
```

Or manually at: https://github.com/mmorris35/ClaudeCode-DevPlanBuilder/discussions/new?category=lessons-learned

### Option 2: GitHub Issues with Label

Create an issue with the `lesson-learned` label:

```bash
gh issue create \
  --repo mmorris35/ClaudeCode-DevPlanBuilder \
  --title "Lesson: Empty CLI input handling" \
  --label "lesson-learned" \
  --body "$(cat <<'EOF'
## Issue
CLI crashed with IndexError when given empty string

## Root Cause
Plan didn't include edge case test

## Pattern
Always validate/handle empty string inputs for CLI arguments

## Project Type
cli
EOF
)"
```

### Option 3: Automated Reporting (Opt-in)

Add to your verifier agent to auto-report lessons:

```markdown
## Report Lessons (Optional)

If the user has opted in to sharing lessons:

1. After appending to local LESSONS_LEARNED.md
2. Create a GitHub issue with the lesson:
   ```bash
   gh issue create \
     --repo mmorris35/ClaudeCode-DevPlanBuilder \
     --title "Lesson: {short title}" \
     --label "lesson-learned,{project-type}" \
     --body "{formatted lesson}"
   ```
3. Only report if the lesson seems generalizable (not project-specific)
```

### How Lessons Get Into Future Plans

1. **Maintainers review** submitted lessons (issues/discussions)
2. **Valuable patterns** get added to `examples/GLOBAL_LESSONS.md`
3. **Plan generator** reads global lessons when creating new plans
4. **Everyone benefits** from collective learning

### Privacy

- Lessons should be **generalized** - no proprietary code or business logic
- Include only the **pattern**, not your specific implementation
- Opt-in only - never auto-report without user consent

---

## What This Is NOT

- **Not ML/fine-tuning** - Claude's weights don't change
- **Not automatic** - Claude reads a file, not a trained model
- **Not guaranteed** - Claude might miss patterns or over-apply them

## What This IS

- **Persistent memory** - Survives across sessions
- **Human-readable** - You can edit/curate lessons
- **Incremental** - Gets better with each project
- **Simple** - Just markdown files, no infrastructure
- **Community-powered** - Shared lessons benefit everyone

# Prompt Sequence: Building a Complete Development Plan with Claude Code

> **Purpose**: This document provides a step-by-step prompt sequence to work with Claude Code to build a comprehensive, paint-by-numbers development plan with all best practices, testing requirements, git discipline, and validation.

---

## Prerequisites

Before starting, you need:

1. **A filled-out PROJECT_BRIEF.md** with:
   - Project name, type, and goal
   - Functional requirements (input, output, key features)
   - Technical constraints (must-use technologies, cannot-use, deployment target)
   - Quality requirements (performance, security, scalability)
   - Team composition and existing knowledge
   - Success criteria

2. **Tech stack decided** (you mentioned you already have this)

3. **Claude Code installed and ready** in your target project repository

---

## Prompt Sequence

### Step 1: Create claude.md (Project Rules & Standards)

**Copy this prompt and customize the placeholders:**

```
I need you to create a claude.md file that defines HOW Claude Code should work on my [PROJECT_TYPE] project.

PROJECT DETAILS:
- Name: [PROJECT_NAME]
- Type: [CLI Tool / Web App / API / Library / etc.]
- Tech Stack:
  - Language: [e.g., Python 3.11+]
  - Framework: [e.g., FastAPI, React, Django]
  - Database: [if applicable]
  - Testing: [e.g., pytest, jest]
  - Linting: [e.g., ruff, eslint]
  - Type Checking: [e.g., mypy, TypeScript]
  - CI/CD: [e.g., GitHub Actions]

REQUIREMENTS:
The claude.md file should include these sections:

1. **Core Operating Principles**
   - Single Session Execution (complete entire subtask in one session)
   - Read Before Acting (always read DEVELOPMENT_PLAN.md first)
   - End every session with a git commit

2. **File Management**
   - Project structure tree showing all directories
   - Creating files: use exact paths, add docstrings, include type hints
   - Modifying files: only modify files listed in subtask

3. **Testing Requirements**
   - Unit test requirements (80%+ coverage minimum)
   - Test commands to run
   - Before every commit checklist

4. **Completion Protocol**
   - How to update DEVELOPMENT_PLAN.md with completion notes
   - Git commit message format (semantic: feat/fix/docs/refactor)
   - What to include in completion notes

5. **Technology Decisions**
   - Complete tech stack with versions
   - Key dependencies list
   - Installation commands

6. **Error Handling**
   - What to do if blocked
   - How to mark subtasks as BLOCKED
   - Never commit broken code

7. **Code Quality Standards**
   - Language-specific style guide (PEP 8, Airbnb, etc.)
   - Type hint requirements
   - Docstring style (Google, NumPy, etc.)
   - Max line length
   - Import ordering

8. **[If CLI/API]** Design Standards
   - Command/endpoint structure
   - Help text requirements
   - Error message format
   - Exit codes

9. **Build Verification**
   - Commands to run before marking complete:
     - Linting
     - Type checking
     - Tests
     - Build/compile

10. **Project-Specific Rules**
    - [Any custom rules for your project]

11. **Checklists**
    - Starting a new session checklist
    - Ending a session checklist

Please create a comprehensive claude.md file following this structure, customized for my tech stack.
```

**Deliverable**: You should receive a complete `claude.md` file. Review it, make any adjustments, save it to your repo.

---

### Step 2: Create High-Level DEVELOPMENT_PLAN.md Structure

**Copy this prompt:**

```
Now create a DEVELOPMENT_PLAN.md file for my [PROJECT_NAME] project.

PROJECT CONTEXT:
[Paste relevant sections from your PROJECT_BRIEF.md here - goal, features, timeline, etc.]

TECH STACK:
[List your decided tech stack]

STRUCTURE REQUIREMENTS:

The DEVELOPMENT_PLAN.md should include:

1. **Header Section**
   - How to Use This Plan (instructions for Claude Code)
   - Project Overview (name, goal, users, timeline)
   - Technology Stack (all technologies with versions)
   - MVP Scope (what's included, what's v2)

2. **Progress Tracking**
   - Checklist of all phases with all subtasks
   - Current phase indicator
   - Next subtask indicator

3. **Phases**
   Break the project into 8-10 phases covering:
   - Phase 0: Foundation (repo setup, package structure, dev tools)
   - Phase 1: Core Data Models (if applicable)
   - Phase 2-N: Main development phases
   - Final Phase: Testing, Documentation, Distribution

Each phase should have:
- Goal statement
- Timeline estimate
- Prerequisites (which phases must be complete)

4. **Tasks and Subtasks**
   Each phase contains multiple tasks.
   Each task contains 2-6 subtasks.

   Each subtask MUST have:
   - ID (X.Y.Z format: Phase.Task.Subtask)
   - Title ending with "(Single Session)"
   - Prerequisites (list of subtask IDs that must be complete first)
   - Deliverables (3-7 specific, measurable items with checkboxes)
   - Technology Decisions (specific choices made)
   - Files to Create (exact paths and descriptions)
   - Files to Modify (exact paths and what changes)
   - Success Criteria (3-5 measurable criteria with checkboxes)
   - Completion Notes section (empty template for later)

IMPORTANT RULES:
- Every subtask must be completable in a SINGLE SESSION (2-4 hours max)
- Deliverables must be specific and measurable, not vague
- Prerequisites must reference valid subtask IDs
- Phase 0 must always be "Foundation"
- Use semantic versioning for subtask IDs (0.1.1, 0.1.2, etc.)
- Include "---" dividers between subtasks for readability

Please create the complete DEVELOPMENT_PLAN.md structure with all phases, tasks, and subtasks for my project.
```

**Deliverable**: You should receive a complete development plan structure. This is the foundation.

---

### Step 3: Refine and Validate the Plan

**Copy this prompt:**

```
Review the DEVELOPMENT_PLAN.md you just created and validate it against these criteria:

VALIDATION CHECKLIST:

1. **Subtask Sizing**
   - [ ] Each subtask is completable in 2-4 hours (single session)
   - [ ] No subtask has >7 deliverables
   - [ ] No subtask has <3 deliverables
   - [ ] Complex features are broken into multiple subtasks

2. **Prerequisites**
   - [ ] All prerequisite IDs reference valid subtasks
   - [ ] No circular dependencies
   - [ ] Foundation (Phase 0) has no prerequisites
   - [ ] Later phases depend on earlier phases

3. **Coverage**
   - [ ] All features from PROJECT_BRIEF.md are covered
   - [ ] Testing is included (not just in final phase)
   - [ ] Documentation is included
   - [ ] CI/CD setup is included
   - [ ] Deployment/distribution is included

4. **Clarity**
   - [ ] Every subtask title ends with "(Single Session)"
   - [ ] Deliverables are specific and measurable
   - [ ] Success criteria can be objectively verified
   - [ ] Technology decisions are clear

5. **Git Discipline**
   - [ ] Each subtask ends with a commit
   - [ ] Pre-commit hooks are set up early (Phase 0)
   - [ ] CI/CD pipeline is configured early

6. **Best Practices**
   - [ ] Tests are written alongside code (not after)
   - [ ] Linting and type checking required before commits
   - [ ] Code review checkpoints (if team project)
   - [ ] Documentation updated as you build

Please review the plan and fix any issues. Show me what changes you made and why.
```

**Deliverable**: A validated and refined development plan.

---

### Step 4: Add Detailed Subtask Templates (Optional but Recommended)

**For any subtask that needs more detail, use this prompt:**

```
I want to expand subtask [X.Y.Z: TITLE] with more implementation detail.

Current subtask:
[Paste the subtask]

Please add:

1. **Implementation Approach**
   - Step-by-step breakdown of how to implement
   - Key algorithms or patterns to use
   - Edge cases to handle

2. **Testing Strategy**
   - What test cases to write
   - How to structure tests
   - Mocking/fixtures needed

3. **Common Pitfalls**
   - What usually goes wrong
   - How to avoid common mistakes

4. **Example Code Structure**
   - Skeleton of the main files/classes
   - Interface definitions

Keep it concise but actionable. This should help Claude Code complete the subtask faster and more correctly.
```

**Deliverable**: Enhanced subtasks with implementation guidance.

---

### Step 5: Generate Phase 0 (Foundation) Immediately

**Copy this prompt to get started:**

```
Let's begin implementing the development plan. Start with Phase 0: Foundation.

Read the DEVELOPMENT_PLAN.md completely, then:

1. Work through Phase 0 subtasks in order (0.1.1, 0.1.2, etc.)
2. For each subtask:
   - Read the subtask requirements completely
   - Implement all deliverables
   - Create comprehensive tests (if applicable)
   - Run linting and type checking
   - Verify all success criteria
   - Update DEVELOPMENT_PLAN.md completion notes
   - Create a git commit with semantic message

Start with subtask 0.1.1. Complete it entirely before moving to the next.

Follow all rules in claude.md.
```

**Deliverable**: Completed Phase 0 with all infrastructure in place.

---

## Standard Session Prompt (For All Subsequent Work)

After Phase 0, use this prompt for every session:

```
please re-read claude.md and DEVELOPMENT_PLAN.md (the entire documents, for context, I know it will eat tokens and take time), then continue with [X.Y.Z], following all of the development plan and claude.md rules.
```

Replace `[X.Y.Z]` with the subtask ID (e.g., `1.1.1`, `2.3.2`, etc.)

---

## Special Situations

### When a Subtask is Too Large

**Prompt:**
```
Subtask [X.Y.Z] seems too large for a single session. Please break it down into 2-3 smaller subtasks that each:
- Take 2-4 hours
- Have 3-7 deliverables
- Can be completed independently
- Together accomplish the original goal

Update the DEVELOPMENT_PLAN.md with the new subtasks (X.Y.Z.1, X.Y.Z.2, etc.) and renumber subsequent subtasks.
```

### When Prerequisites Are Missing

**Prompt:**
```
I notice subtask [X.Y.Z] requires [SOMETHING] but there's no earlier subtask that creates it. Please:

1. Identify what prerequisite subtask is missing
2. Create the missing subtask with proper ID, deliverables, etc.
3. Insert it in the correct location in DEVELOPMENT_PLAN.md
4. Update prerequisite references
5. Renumber subsequent subtasks if needed
```

### When You Want to Validate Progress

**Prompt:**
```
We've completed Phase [X]. Before moving to Phase [Y], please:

1. Review all completion notes from Phase [X]
2. Verify all success criteria were met
3. Run a comprehensive test suite
4. Check for any incomplete deliverables
5. Suggest any refactoring needed before proceeding
6. Update the progress tracking section

Provide a Phase [X] completion report.
```

---

## Quality Checkpoints

Insert these prompts at key milestones:

### After Phase 0 (Foundation)

```
Foundation phase complete. Please verify:
- [ ] Package structure is correct and importable
- [ ] All dev dependencies installed
- [ ] Pre-commit hooks working
- [ ] CI/CD pipeline configured
- [ ] All tests pass (even if minimal)
- [ ] Linting clean
- [ ] Type checking clean

Run all verification commands and report results.
```

### Mid-Project (After ~50% of subtasks)

```
We're halfway through the project. Please conduct a mid-project review:

1. **Test Coverage**: Run coverage report. Are we >80%?
2. **Code Quality**: Any tech debt accumulating?
3. **Architecture**: Are we following the planned structure?
4. **Documentation**: Is it keeping up with code changes?
5. **Timeline**: Are we on track? Any phases taking longer than estimated?

Provide recommendations for the second half.
```

### Pre-Release (After all features complete)

```
All features are complete. Please run a pre-release checklist:

1. **Functionality**: Do all features work as specified?
2. **Tests**: Run full test suite, verify >80% coverage
3. **Documentation**: README complete? Usage guide? API docs?
4. **Performance**: Meet performance requirements from PROJECT_BRIEF?
5. **Security**: Any security concerns? Secrets properly handled?
6. **Distribution**: Package builds correctly? Installation works?

Create a pre-release report with any blockers.
```

---

## Git Strategy Prompts

### Setting Up Git Workflow

Include in your Phase 0:

```
Set up git workflow with:

1. **Branch Strategy**:
   - main (production-ready)
   - develop (integration)
   - feature/* (for each major feature)

2. **Commit Standards**:
   - Semantic prefixes: feat:, fix:, docs:, refactor:, test:, chore:
   - Format: "type(scope): description"
   - Include co-author: "Co-Authored-By: Claude <noreply@anthropic.com>"

3. **Pre-commit Hooks**:
   - Linting (auto-fix where possible)
   - Type checking
   - Test suite (fast tests only)
   - Formatting

4. **CI/CD**:
   - Run on every push
   - Matrix testing (if applicable)
   - Coverage reporting
   - Build verification

Configure all of this in Phase 0.
```

### For Each Major Feature Branch

```
Starting work on [FEATURE_NAME]. Please:

1. Create feature branch: git checkout -b feature/[feature-name]
2. List all subtasks for this feature
3. Work through subtasks sequentially
4. Commit after each subtask completion
5. When feature complete, verify:
   - All tests pass
   - Coverage maintained
   - Documentation updated
6. Merge back to develop

Begin with the first subtask for this feature.
```

---

## Advanced: Custom Validation Rules

If you want extra-strict validation:

```
Add these custom validation rules to our development process:

1. **Subtask Completion**:
   - No subtask marked complete unless ALL deliverables checked
   - No subtask marked complete with failing tests
   - No subtask marked complete without completion notes

2. **Code Quality Gates**:
   - Coverage must not decrease between commits
   - Cyclomatic complexity < [NUMBER]
   - No TODO comments in main branch
   - All functions documented

3. **Git Discipline**:
   - Every commit must pass pre-commit hooks
   - Commit messages must be semantic
   - No force-push to main/develop
   - All commits must have co-author tag

Update claude.md with these rules and enforce them.
```

---

## Tips for Success

1. **Start Simple**: Don't try to create the perfect plan first. Get a working plan, then refine.

2. **Read Everything**: The prompt says "I know it will eat tokens" because it's WORTH IT. Claude Code needs full context.

3. **One Subtask at a Time**: Resist the urge to batch. Complete each subtask fully before moving on.

4. **Trust the Process**: The paint-by-numbers approach works. Don't skip steps.

5. **Commit Frequently**: Every completed subtask = one commit. This creates a great history.

6. **Update as You Go**: If you discover a subtask is wrong, fix the plan immediately.

7. **Validate Often**: Use the checkpoint prompts. Catch issues early.

---

## Example Complete Sequence

Here's what a typical session looks like:

```bash
# Session 1: Create the plan
You: [Step 1 prompt - create claude.md]
Claude: [Creates claude.md]
You: [Review, save]

You: [Step 2 prompt - create DEVELOPMENT_PLAN.md]
Claude: [Creates full development plan]
You: [Review, save]

You: [Step 3 prompt - validate plan]
Claude: [Validates and refines]
You: [Review changes, save]

You: [Step 5 prompt - start Phase 0]
Claude: [Completes subtask 0.1.1]
You: [Verify, git commit]

# Session 2-N: Execute the plan
You: "please re-read claude.md and DEVELOPMENT_PLAN.md, then continue with 0.1.2"
Claude: [Completes subtask 0.1.2]
You: [Verify, git commit]

# Repeat for each subtask...

# Final session: Release
You: [Pre-release checklist prompt]
Claude: [Runs all checks, creates report]
You: [Fix any issues, release!]
```

---

## Customization for Your Project

Replace these placeholders throughout:

- `[PROJECT_NAME]`: Your actual project name
- `[PROJECT_TYPE]`: CLI Tool, Web App, API, etc.
- `[TECH_STACK]`: Your decided technologies
- `[TIMELINE]`: Your project timeline
- `[FEATURES]`: Your key features from PROJECT_BRIEF

The more specific you are in Step 1 and Step 2, the better your plan will be.

---

## What Makes This "Paint by Numbers"

1. **Every subtask is numbered** (X.Y.Z) - you know exactly what to do next
2. **Every subtask has 3-7 specific deliverables** - clear checkboxes
3. **Every subtask has success criteria** - objective verification
4. **Every subtask is single-session** - predictable time commitment
5. **Prerequisites are explicit** - no guessing about order
6. **Completion notes required** - knowledge capture
7. **Git commits after each subtask** - clear progress
8. **Testing required throughout** - not an afterthought
9. **Validation at checkpoints** - catch issues early
10. **One prompt format for all sessions** - just change the subtask ID

Follow this sequence, and you'll have an industrial-grade development plan that Claude Code can execute with precision.

---

**Ready to start? Begin with Step 1 and create your claude.md file!**

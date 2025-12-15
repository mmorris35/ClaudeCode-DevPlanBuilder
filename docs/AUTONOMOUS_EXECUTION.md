# Autonomous Execution with Claude Code

> **Run your executor agent hands-free to build your entire project**

This guide explains how to use Claude Code's `--dangerously-skip-permissions` flag to let the executor agent build your project autonomously, without requiring approval for each action.

---

## When This Is Safe

**This approach is SAFE when:**
- ✅ You're building a brand new project from scratch
- ✅ The folder contains only DevPlan-generated planning files
- ✅ You're working in an isolated directory (not your home folder or system directories)
- ✅ You've reviewed the DEVELOPMENT_PLAN.md and trust the planned actions
- ✅ You're on a development machine, not a production server

**This approach is DANGEROUS when:**
- ❌ You're modifying existing production code
- ❌ The project has access to sensitive data or credentials
- ❌ You're running in a directory with important files that could be overwritten
- ❌ The development plan includes deployment or infrastructure changes
- ❌ You haven't reviewed what the agent will do

The `--dangerously-skip-permissions` flag exists for a reason - it bypasses the safety prompts that normally prevent Claude from executing potentially harmful commands. For greenfield projects in isolated directories, this is fine. For anything touching production systems, **do not use this flag**.

---

## Prerequisites

Before starting autonomous execution:

1. **Complete the planning phase** - You should have:
   - `PROJECT_BRIEF.md`
   - `DEVELOPMENT_PLAN.md`
   - `CLAUDE.md`
   - `.claude/agents/{project}-executor.md`

2. **Initialize git and push to GitHub** - Your planning files should be committed:
   ```bash
   git status  # Should show a clean working tree
   ```

3. **Review your development plan** - Read through DEVELOPMENT_PLAN.md and understand what will be built

4. **Ensure you're in an isolated directory**:
   ```bash
   pwd  # Should be something like ~/projects/my-new-app
   ls   # Should only show your planning files
   ```

---

## Quick Start

### Option 1: Execute a Single Subtask

Run one subtask autonomously:

```bash
cd ~/projects/my-project

claude --dangerously-skip-permissions \
  "Read CLAUDE.md and DEVELOPMENT_PLAN.md, then execute subtask 0.1.2 using the executor agent protocol. Verify, implement, test, and commit."
```

### Option 2: Execute an Entire Task

Run all subtasks in a task (e.g., Task 1.2 with subtasks 1.2.1, 1.2.2, 1.2.3):

```bash
cd ~/projects/my-project

claude --dangerously-skip-permissions \
  "Read CLAUDE.md and DEVELOPMENT_PLAN.md, then execute all subtasks in Task 1.2 sequentially. For each subtask: verify prerequisites, implement deliverables, run tests, and commit. Continue until Task 1.2 is complete."
```

### Option 3: Execute an Entire Phase

Run all tasks in a phase:

```bash
cd ~/projects/my-project

claude --dangerously-skip-permissions \
  "Read CLAUDE.md and DEVELOPMENT_PLAN.md, then execute all tasks in Phase 1 sequentially. For each task, create the feature branch, execute all subtasks with commits, then merge to main when complete. Continue until Phase 1 is done."
```

### Option 4: Build the Entire Project

Let Claude build everything:

```bash
cd ~/projects/my-project

claude --dangerously-skip-permissions \
  "Read CLAUDE.md and DEVELOPMENT_PLAN.md, then execute the entire development plan from the current progress point. Follow git discipline (one branch per task, commits per subtask, merge when task complete). Run verification after each subtask. Continue until all phases are complete."
```

---

## Recommended Workflow

### Step 1: Plan (Interactive)

Start with the interactive planning phase - you want to be involved here:

```bash
cd ~/projects/my-project
claude
```

Answer the interview questions, review the generated files, and commit.

### Step 2: Foundation Phase (Interactive)

Execute Phase 0 interactively to set up the project foundation:

```bash
claude
> Execute subtask 0.1.1 following the development plan.
> Execute subtask 0.1.2 following the development plan.
# ... continue through Phase 0
```

This ensures your dev environment, dependencies, and CI/CD are set up correctly.

### Step 3: Development Phases (Autonomous)

Once the foundation is solid, switch to autonomous mode for the development phases:

```bash
claude --dangerously-skip-permissions \
  "Execute Phase 1 of DEVELOPMENT_PLAN.md completely. For each task: create feature branch, execute all subtasks with verification and commits, merge to main when done."
```

### Step 4: Review and Continue

After each autonomous session:

1. Review the git history: `git log --oneline -20`
2. Run the test suite: `pytest` (or your test command)
3. Check the DEVELOPMENT_PLAN.md for completion notes
4. Decide whether to continue autonomously or switch to interactive

---

## Using the Executor Agent Directly

If your project has an executor agent at `.claude/agents/{project}-executor.md`, you can invoke it directly:

```bash
claude --dangerously-skip-permissions \
  "@taskflow-executor execute subtask 1.2.3"
```

Or for multiple subtasks:

```bash
claude --dangerously-skip-permissions \
  "@taskflow-executor execute all subtasks in Task 1.2, committing after each one"
```

---

## Monitoring Progress

### Watch the Terminal

Claude Code will output what it's doing. Keep the terminal visible to monitor progress.

### Check Git History

After autonomous execution, review what was committed:

```bash
git log --oneline -20
git diff HEAD~5..HEAD --stat  # See files changed in last 5 commits
```

### Review Completion Notes

Check DEVELOPMENT_PLAN.md for the completion notes Claude added:

```bash
grep -A5 "Completion Notes" DEVELOPMENT_PLAN.md
```

### Run Tests

Verify everything works:

```bash
# Whatever test command is in your CLAUDE.md
pytest
npm test
go test ./...
```

---

## Stopping Autonomous Execution

To stop Claude mid-execution:

- **Ctrl+C** - Interrupt the current command
- Claude will stop at the current point; any uncommitted work may be lost

To resume after stopping:

```bash
claude --dangerously-skip-permissions \
  "Read DEVELOPMENT_PLAN.md and find the last completed subtask. Resume from the next incomplete subtask."
```

---

## Troubleshooting

### Claude Gets Stuck in a Loop

If Claude keeps retrying a failing operation:

1. Press Ctrl+C to stop
2. Check the error message
3. Fix the issue manually if needed
4. Resume with: `claude "Continue from where you left off, the issue was [X]"`

### Tests Keep Failing

If autonomous execution keeps failing on tests:

1. Stop autonomous execution
2. Switch to interactive mode: `claude`
3. Debug the failing tests manually
4. Once fixed, resume autonomous execution

### Git Conflicts

If Claude encounters merge conflicts:

1. Stop autonomous execution
2. Resolve conflicts manually: `git status`, edit files, `git add`, `git commit`
3. Resume: `claude --dangerously-skip-permissions "Continue with the development plan"`

### Context Gets Too Long

For very long autonomous sessions, Claude may run out of context:

1. Let the current subtask complete
2. Start a fresh session for the next subtask
3. Claude will re-read CLAUDE.md and DEVELOPMENT_PLAN.md to restore context

---

## Safety Checklist

Before running `--dangerously-skip-permissions`, verify:

- [ ] I'm in an isolated project directory (not ~/ or /etc or similar)
- [ ] The directory only contains my project files
- [ ] I've reviewed DEVELOPMENT_PLAN.md and understand what will be built
- [ ] I've committed my planning files to git (so I can revert if needed)
- [ ] I'm not connected to production databases or services
- [ ] I don't have sensitive credentials in this directory
- [ ] I'm on a development machine, not a production server

If all boxes are checked, you're good to go!

---

## Example: Full Autonomous Build

Here's a complete example of building a CLI tool autonomously:

```bash
# 1. Create and enter project directory
mkdir -p ~/projects/taskflow
cd ~/projects/taskflow

# 2. Start Claude and complete the planning phase (interactive)
claude
# > "Use DevPlan Builder to plan a CLI task management tool called TaskFlow"
# > [Answer interview questions]
# > [Review and approve generated files]
# > "Initialize git and create a GitHub repo called taskflow"
# > exit

# 3. Verify planning files exist
ls -la
# PROJECT_BRIEF.md  DEVELOPMENT_PLAN.md  CLAUDE.md  .claude/agents/taskflow-executor.md

# 4. Execute Phase 0 interactively (foundation)
claude
# > "Execute all subtasks in Phase 0"
# > exit

# 5. Execute remaining phases autonomously
claude --dangerously-skip-permissions \
  "Read CLAUDE.md and DEVELOPMENT_PLAN.md. Execute all remaining phases (1 through completion). For each task: create feature branch, execute subtasks with verification and commits, merge when complete. Continue until the project is fully built."

# 6. Review the result
git log --oneline
pytest
taskflow --help  # Your new CLI tool!
```

---

## Summary

| Mode | Flag | Use Case |
|------|------|----------|
| Interactive | (none) | Planning, debugging, production code |
| Autonomous | `--dangerously-skip-permissions` | Greenfield development in isolated directories |

**Remember**: The flag is called "dangerously" for a reason. Use it responsibly on new projects in isolated directories, never on production systems.

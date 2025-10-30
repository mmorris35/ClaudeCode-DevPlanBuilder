# 🎯 Claude Code Dev Plan Builder

> **Turn your product idea into a production-ready development plan in minutes**

Tell Claude Code to read this repo, and it will guide you through building a comprehensive, paint-by-numbers development plan with all the testing, git discipline, and best practices baked in.

---

## 🚀 Quick Start (For Users)

**Got a product idea? Here's all you need to do:**

### Step 1: Start a Conversation with Claude Code

In your new project repository, paste this prompt:

```
Go read the README at https://github.com/mmorris35/ClaudeCode-DevPlanBuilder and help me develop my idea into a complete development plan.
```

### Step 2: Answer Claude's Questions

Claude Code will guide you through creating a `PROJECT_BRIEF.md` by asking about:
- What you're building (the goal)
- Who it's for (target users)
- What it needs to do (key features)
- Your tech stack (if decided)
- Timeline and constraints

### Step 3: Get Your Development Plan

Claude Code will generate:
- ✅ **claude.md** - Rules for how Claude Code should work on your project
- ✅ **DEVELOPMENT_PLAN.md** - Paint-by-numbers roadmap with numbered subtasks
- ✅ **Complete project structure** - Ready to start building

### Step 4: Build Your Product

Use this simple prompt for every work session:

```
please re-read claude.md and DEVELOPMENT_PLAN.md (the entire documents, for context, I know it will eat tokens and take time), then continue with [X.Y.Z], following all of the development plan and claude.md rules.
```

Replace `[X.Y.Z]` with the next subtask number (like `0.1.1`, `1.2.3`, etc.)

**That's it!** Claude Code will:
- Complete each subtask fully (2-4 hours of work)
- Write comprehensive tests (>80% coverage)
- Run linting and type checking
- Create semantic git commits
- Update progress in DEVELOPMENT_PLAN.md

---

## 🎨 What Makes This "Paint by Numbers"?

Your development plan will have:

1. **Numbered subtasks** (0.1.1, 0.1.2, etc.) - Always know what's next
2. **3-7 specific deliverables per subtask** - Clear checkboxes for completion
3. **Single-session sizing** - Each subtask takes 2-4 hours max
4. **Explicit prerequisites** - No guessing about order
5. **Success criteria** - Objective verification of completion
6. **Git commits built-in** - One commit per completed subtask
7. **Testing throughout** - Not an afterthought, >80% coverage required
8. **Quality gates** - Linting, type checking, validation at every step
9. **Completion notes** - Knowledge capture for every subtask
10. **One simple prompt** - Same format for every session

---

## 📚 What's In This Repo?

This repository contains:

### For Users (You!)

- **[PROMPT_SEQUENCE.md](PROMPT_SEQUENCE.md)** - Detailed guide with all the prompts you'll need
- **[PROJECT_BRIEF.md](PROJECT_BRIEF.md)** - Example of a complete project brief (for this tool itself!)
- **This README** - Everything you need to get started

### Example Artifacts (What You'll Get)

- **[claude.md](claude.md)** - Example rules document for a Python CLI project
- **[DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md)** - Example development plan with 100+ subtasks
- Templates, generators, and validators (this is a working tool!)

---

## 💡 How Claude Code Will Help You

When you ask Claude Code to help you develop your idea, it will:

### 1. **Interview You** About Your Project

Claude will ask clarifying questions like:
- "What problem does this solve?"
- "Who are your target users?"
- "What are the must-have features for MVP?"
- "What's your tech stack? (Or would you like recommendations?)"
- "What's your timeline?"

### 2. **Create Your PROJECT_BRIEF.md**

A comprehensive document covering:
- Basic information (name, type, goal, users, timeline)
- Functional requirements (input, output, key features)
- Technical constraints (must-use tech, cannot-use, deployment)
- Quality requirements (performance, security, scalability)
- Success criteria

### 3. **Generate claude.md**

Project-specific rules defining:
- How Claude Code should work on YOUR project
- Testing requirements (coverage, frameworks)
- Code quality standards (linting, type checking, style guides)
- Git workflow and commit standards
- Build verification steps
- Project-specific best practices

### 4. **Build DEVELOPMENT_PLAN.md**

A complete roadmap with:
- **Phase 0: Foundation** - Repo setup, dependencies, CI/CD
- **Phase 1-N: Development** - Your features broken into digestible pieces
- **Final Phase: Testing & Distribution** - Polish and release

Each subtask includes:
- Exact deliverables (what to build)
- Files to create/modify (where to build it)
- Success criteria (how to verify it works)
- Completion notes template (knowledge capture)

### 5. **Guide You Through Execution**

For every subtask, Claude Code will:
- Read the full context (claude.md + DEVELOPMENT_PLAN.md)
- Implement all deliverables
- Write comprehensive tests
- Run quality checks (linting, type checking)
- Update completion notes
- Create semantic git commit

---

## 🎯 Who Is This For?

### Perfect For:

- ✅ **Solo developers** building side projects or startups
- ✅ **Small teams** wanting consistent development practices
- ✅ **Experienced developers** who want to move fast with quality
- ✅ **Anyone using Claude Code** for software development

### Works Great For These Project Types:

- 🖥️ **CLI Tools** - Command-line applications and utilities
- 🌐 **Web Apps** - Full-stack web applications
- 🔌 **APIs** - RESTful services and microservices
- 📦 **Libraries** - Reusable packages and frameworks
- 🤖 **Automation Tools** - Scripts and workflow automation

---

## 📖 Documentation & Resources

### Essential Reading

- **[PROMPT_SEQUENCE.md](PROMPT_SEQUENCE.md)** - Complete guide with all prompts
  - 5-step setup sequence
  - Special situation prompts
  - Quality checkpoint prompts
  - Git strategy guidance

### Example Artifacts

- **[PROJECT_BRIEF.md](PROJECT_BRIEF.md)** - See a complete project brief
- **[claude.md](claude.md)** - See project rules in action
- **[DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md)** - See a real development plan

### Quick Reference

**Standard session prompt** (use this every time):
```
please re-read claude.md and DEVELOPMENT_PLAN.md (the entire documents, for context, I know it will eat tokens and take time), then continue with [X.Y.Z], following all of the development plan and claude.md rules.
```

**When a subtask is too large:**
```
Subtask [X.Y.Z] seems too large for a single session. Please break it down into 2-3 smaller subtasks that each take 2-4 hours, have 3-7 deliverables, and can be completed independently.
```

**Progress validation:**
```
We've completed Phase [X]. Before moving to Phase [Y], please review all completion notes, verify success criteria, run tests, and provide a Phase [X] completion report.
```

---

## 🏗️ What This Repository Actually Is

This is **both**:

1. **A methodology** for building development plans with Claude Code
2. **A working CLI tool** (in development) that automates the plan generation

The tool is being built using its own generated development plan - meta! 🎉

### Current Status

🚧 **In Development** - Following subtask 5.1.1 (CLI Entry Point)

The CLI tool will eventually let you run:
```bash
claude-planner generate my-project --brief PROJECT_BRIEF.md
```

But right now, you can use the **methodology** (the prompts in PROMPT_SEQUENCE.md) to build dev plans for any project!

---

## 🎓 Example Workflow

Here's what a typical project looks like:

### Session 1: Planning (30-60 minutes)
```
You: Go read the README at https://github.com/mmorris35/ClaudeCode-DevPlanBuilder
     and help me develop my idea

Claude: [Asks questions about your project]
You: [Answers questions]
Claude: [Creates PROJECT_BRIEF.md]
You: [Reviews and approves]

Claude: [Creates claude.md]
You: [Reviews and approves]

Claude: [Creates DEVELOPMENT_PLAN.md with all phases/tasks/subtasks]
You: [Reviews and approves]

Claude: [Validates the plan]
You: [Git commit - your plan is ready!]
```

### Session 2: Foundation (2-4 hours)
```
You: please re-read claude.md and DEVELOPMENT_PLAN.md, then continue with 0.1.1

Claude: [Completes subtask 0.1.1]
        [Runs tests, linting, type checking]
        [Updates DEVELOPMENT_PLAN.md]
        [Creates git commit]

You: [Reviews] Looks good!

You: please re-read claude.md and DEVELOPMENT_PLAN.md, then continue with 0.1.2

Claude: [Completes subtask 0.1.2]
...
```

### Sessions 3-N: Development (2-4 hours each)
```
You: please re-read claude.md and DEVELOPMENT_PLAN.md, then continue with [next ID]

Claude: [Completes subtask]
You: [Reviews, commits, moves to next]
```

Just keep going until all subtasks are complete!

---

## 💪 Why This Works

### Traditional Approach:
- ❌ Vague requirements
- ❌ No clear next step
- ❌ Testing as an afterthought
- ❌ Inconsistent code quality
- ❌ No progress tracking
- ❌ Git history is a mess

### With Dev Plan Builder:
- ✅ Crystal clear requirements (PROJECT_BRIEF.md)
- ✅ Always know what's next (numbered subtasks)
- ✅ Tests written alongside code (every subtask)
- ✅ Quality enforced (linting, type checking, pre-commit hooks)
- ✅ Progress visible (checkboxes, completion notes)
- ✅ Clean git history (semantic commits, one per subtask)

---

## 🤝 Contributing

Want to improve the methodology or the tool? Contributions welcome!

This project follows its own strict development guidelines defined in [claude.md](claude.md). Each subtask must:
- Be completed in a single session
- Include comprehensive tests (>80% coverage)
- Pass all linting and type checking
- End with a semantic git commit

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

Use this for anything - personal projects, commercial products, open source, whatever!

---

## 🙏 Acknowledgments

Built with [Claude Code](https://claude.ai/claude-code) - An AI pair programmer that executes development plans with precision.

This methodology emerged from real-world usage of Claude Code on production projects. It codifies best practices for:
- Project planning and task breakdown
- Testing and quality assurance
- Git workflow and discipline
- Progress tracking and knowledge capture

---

## 🚀 Ready to Start?

**Just paste this in Claude Code:**

```
Go read the README at https://github.com/mmorris35/ClaudeCode-DevPlanBuilder and help me develop my idea into a complete development plan.
```

**Then answer Claude's questions about your project, and you're off to the races!** 🎉

---

## ❓ Questions?

- 📖 **Read**: [PROMPT_SEQUENCE.md](PROMPT_SEQUENCE.md) for detailed guidance
- 👀 **See**: [PROJECT_BRIEF.md](PROJECT_BRIEF.md) for an example
- 🔍 **Check**: [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for a real plan
- 💬 **Ask**: Open an issue at https://github.com/mmorris35/ClaudeCode-DevPlanBuilder/issues

---

**Built with Claude Code • Powered by Anthropic • Open Source MIT License**

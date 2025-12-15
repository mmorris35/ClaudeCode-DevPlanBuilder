# DevPlan Builder Screencast Script

> **Video Title**: "Building a Development Plan with DevPlan Builder MCP"
> **Duration**: ~12-18 minutes
> **Prerequisites**: Claude Code installed, GitHub CLI (`gh`) authenticated

---

## Pre-Recording Checklist

- [ ] Clean terminal (clear history, neutral prompt)
- [ ] Empty project folder ready (e.g., `~/projects/my-new-app`)
- [ ] Claude Code installed (`claude --version` works)
- [ ] GitHub CLI authenticated (`gh auth status` shows logged in)
- [ ] Screen recording software ready (QuickTime or Cmd+Shift+5 on Mac)
- [ ] This script printed or on second monitor

---

## SCENE 1: Introduction (30 seconds)

**[Terminal visible, empty folder]**

> "Hey everyone. Today I'm going to show you how to use DevPlan Builder to create a comprehensive development plan that Claude can execute step by step.
>
> We're starting from scratch - an empty folder with no git repo, no GitHub repo, nothing. By the end of this video, we'll have a GitHub repository with four planning files and the beginning of our actual code.
>
> Let's get started."

---

## SCENE 2: Install the MCP Server (1-2 minutes)

**[Show terminal, possibly split with Claude Code settings]**

> "First, we need to install the DevPlan Builder MCP server. This gives Claude Code the tools to interview us and generate our development plan."

**Option A: Install from npm (if published)**
```bash
# Install the MCP server globally
npm install -g @devplan/builder-mcp

# Or with npx (no install needed)
npx @devplan/builder-mcp
```

**Option B: Install from source**
```bash
# Clone the repo
git clone https://github.com/your-username/devplan-builder.git
cd devplan-builder

# Install dependencies
pip install -e .
```

**[Open Claude Code settings - show how to add MCP server]**

> "Now we add it to Claude Code's MCP configuration. You can do this through the settings UI or by editing the config file directly."

**[Show the MCP config in ~/.claude/claude_desktop_config.json or similar]**

```json
{
  "mcpServers": {
    "devplan": {
      "command": "npx",
      "args": ["@devplan/builder-mcp"]
    }
  }
}
```

> "Once configured, restart Claude Code and the DevPlan tools will be available. You'll see them when Claude lists available MCP tools."

---

## SCENE 3: Start Claude Code in Empty Folder (30 seconds)

**[Type in terminal]**
```bash
mkdir -p ~/projects/taskflow
cd ~/projects/taskflow
claude
```

**[Wait for Claude Code to start]**

> "I've created an empty project folder and started Claude Code here.
>
> Claude Code now has the DevPlan Builder MCP server configured, which gives us tools to interview ourselves about our project, generate a brief, and then create a full development plan."

---

## SCENE 4: Initialize DevPlan (1 minute)

**[Type in Claude Code]**
```
Let's use DevPlan Builder to plan a new project. Start the interview.
```

**[Wait for Claude to call devplan_start or devplan_interview_questions]**

> "I'm asking Claude to start the DevPlan Builder process. It will use the MCP tools to walk me through a structured interview about my project.
>
> This interview covers the essential questions: what we're building, who it's for, what tech stack to use, timeline, and key features."

---

## SCENE 5: Answer Interview Questions (3-4 minutes)

**[Claude asks questions one at a time. Answer each naturally]**

> "Now Claude is going to ask me questions about my project. I'll answer them one at a time.
>
> The key here is to be specific. Vague answers lead to vague plans. The more detail I provide now, the better the generated plan will be."

**Example answers to have ready:**

| Question | Example Answer |
|----------|----------------|
| Project name? | "TaskFlow - a CLI task management tool" |
| Project type? | "CLI tool" |
| One-sentence goal? | "Help developers track tasks and todos from the command line without leaving their terminal" |
| Target users? | "Software developers who prefer terminal workflows" |
| Must-have features? | "Add tasks, list tasks, mark complete, filter by status, persist to local JSON file" |
| Nice-to-have features? | "Due dates, priorities, tags, export to markdown" |
| Tech stack requirements? | "Must use Python 3.11+, Click for CLI, no external database" |
| Cannot use? | "No cloud services, no API calls, must work offline" |
| Timeline? | "1 week MVP" |
| Team size? | "Solo developer" |

> "Notice I'm being specific about constraints - offline only, no cloud, specific Python version. These constraints help DevPlan Builder make better technology decisions."

---

## SCENE 6: Generate PROJECT_BRIEF.md (1 minute)

**[Claude calls devplan_create_brief]**

> "Now Claude is taking my answers and creating a structured PROJECT_BRIEF.md file.
>
> This brief captures everything we discussed in a standardized format. It's the source of truth for the project - both for generating the plan and for reference during development."

**[Show the generated PROJECT_BRIEF.md]**

> "Let me show you what it generated... You can see it has sections for the goal, target users, features, tech constraints, and more. This is the seed document that drives everything else."

---

## SCENE 7: Generate DEVELOPMENT_PLAN.md (2 minutes)

**[Type in Claude Code]**
```
Now generate the full development plan from this brief.
```

**[Wait for Claude to call devplan_generate_plan]**

> "Now I'm asking Claude to generate the full development plan.
>
> DevPlan Builder will analyze the brief, select the appropriate template - in our case, the CLI template - and generate a phased development plan with tasks and subtasks."

**[Show the generated DEVELOPMENT_PLAN.md]**

> "Here's the development plan. Notice it has:
> - A project overview with our goal and tech stack
> - Phases broken down into tasks
> - Each task has a git strategy - one branch per task, not per subtask
> - Subtasks are designed to be completable in a single session
>
> This structure is important. Each subtask should be something Claude can pick up and complete in one go, then commit."

---

## SCENE 8: Generate CLAUDE.md (1 minute)

**[Type in Claude Code]**
```
Generate the claude.md coding standards file too.
```

**[Wait for Claude to call devplan_generate_claude_md]**

> "Next, we generate CLAUDE.md. This file defines HOW Claude should work on this project - coding standards, testing requirements, commit conventions.
>
> It's like an engineering style guide, but specifically formatted for Claude to follow."

**[Show the generated CLAUDE.md]**

> "You can see it has our tech stack, testing commands, linting setup, and completion protocols. Every time Claude starts a session, it reads this file to know the rules."

---

## SCENE 9: Show the Agent File (1 minute)

**[Navigate to .claude/agents/]**

```
ls -la .claude/agents/
cat .claude/agents/taskflow-executor.md
```

> "DevPlan Builder also created an agent file in .claude/agents/.
>
> This is a specialized agent that knows how to execute our development plan. It has the project context baked in - tech stack, phases, directory structure.
>
> When I want to work on a subtask, I can invoke this agent and say 'execute subtask 0.1.1' and it knows exactly what to do."

**[Scroll through the agent file]**

> "Notice it expects 'Haiku-executable' plans - meaning the plan should have complete, copy-pasteable code, not vague descriptions. If the plan is vague, the agent will stop and ask for clarification."

---

## SCENE 10: Initialize Git and Create GitHub Repo (1-2 minutes)

**[Type in Claude Code]**
```
Initialize a git repo, make the first commit with these planning files, and create a GitHub repository called "taskflow".
```

**[Wait for Claude to run git init, commit, and gh repo create]**

> "Now I'm asking Claude to set up our repository. It will:
> 1. Initialize git locally
> 2. Commit our planning files
> 3. Create a new GitHub repository using the GitHub CLI
> 4. Push our initial commit
>
> This is subtask 0.1.1 in most DevPlan projects - setting up the repository foundation."

**[Show the commands Claude runs]**

```bash
# What Claude will execute:
git init
git add .
git commit -m "chore: initialize project with DevPlan planning files"
gh repo create taskflow --public --source=. --push
```

> "Notice we didn't have to leave Claude Code or go to GitHub's website. Claude used the `gh` CLI to create the repo directly. The planning files are now safely versioned and pushed to GitHub."

---

## SCENE 11: Execute First Subtask (2 minutes)

**[Type in Claude Code]**
```
Execute subtask 0.1.2 following the development plan.
```

> "Now let's execute the next subtask. Claude will:
> 1. Read CLAUDE.md for coding standards
> 2. Find subtask 0.1.2 in DEVELOPMENT_PLAN.md
> 3. Check prerequisites are complete
> 4. Implement the deliverables
> 5. Run verification (linting, type checking, tests)
> 6. Commit the changes
>
> This is the core workflow. One subtask, one session, one commit."

**[Watch Claude execute the subtask]**

> "Notice Claude is following the plan exactly - creating the files specified, running the verification commands, and updating the completion notes in the plan."

---

## SCENE 12: Wrap Up (1 minute)

**[Show the file tree]**
```
tree -a -I '.git'
```

> "Let's see what we have now...
>
> We started with an empty folder. Now we have:
> - PROJECT_BRIEF.md - our requirements
> - DEVELOPMENT_PLAN.md - our phased roadmap
> - CLAUDE.md - our coding standards
> - .claude/agents/taskflow-executor.md - our specialized executor
> - And the beginning of our actual code
>
> From here, I just keep executing subtasks until the project is done. The plan tracks progress, and each session builds on the last."

---

## SCENE 13: Call to Action (30 seconds)

> "That's DevPlan Builder. It turns a conversation about your project into a structured, executable development plan - complete with a GitHub repo, ready to go.
>
> To get started:
> 1. Install Claude Code
> 2. Configure the DevPlan Builder MCP server
> 3. Create an empty folder and ask Claude to start the DevPlan interview
>
> Links to the repo and setup instructions are in the description.
>
> Thanks for watching!"

---

## Post-Recording Notes

**Potential B-roll / Overlays:**
- Show file tree growing as files are created
- Highlight key sections of generated files
- Show the MCP tool calls in Claude Code's output
- Show the GitHub repo page after creation

**Editing Suggestions:**
- Speed up waiting periods (MCP calls, generation)
- Add chapter markers for each scene
- Include setup instructions as text overlay at start
- Consider adding a "before/after" split screen showing empty folder → complete project

**Recording Tips for Mac:**
- Use QuickTime Player → File → New Screen Recording
- Or use Cmd+Shift+5 for built-in screen recording
- Record at 1080p or 4K for best quality
- Use a clean desktop background
- Hide desktop icons and dock if possible

**Common Issues to Watch For:**
- MCP server not responding → restart Claude Code
- Generation takes too long → mention this is normal for complex projects
- Typos in answers → don't worry, can edit brief manually later
- `gh` not authenticated → run `gh auth login` before recording
- GitHub repo name conflict → use a unique name or delete existing repo

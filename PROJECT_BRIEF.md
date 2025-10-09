# Project Brief: Claude Code Project Planner

## Basic Information

- **Project Name**: Claude Code Project Planner
- **Project Type**: [x] CLI Tool + [x] Library
- **Primary Goal**: A tool that takes a PROJECT_BRIEF.md as input and produces complete, validated claude.md and DEVELOPMENT_PLAN.md files ready to seed new Claude Code project repositories
- **Target Users**: Developers (including yourself) who want to quickly bootstrap new projects with Claude Code
- **Timeline**: 2 weeks
- **Team Size**: 1 senior developer (you)

## Functional Requirements

### Input
What does the system receive?

- PROJECT_BRIEF.md file (filled-out questionnaire)
- Project ID/name for the new project
- Optional: Technology preferences override
- Optional: Template selection (web-app, api, cli)
- Configuration file for customizations (company standards, etc.)

### Output
What does the system produce?

- claude.md (customized behavior rules)
- DEVELOPMENT_PLAN.md (complete roadmap with all subtasks)
- Repository structure (directories, .gitignore, etc.)
- README.md (setup instructions)
- Validation report (quality checks)
- Optional: Git repository initialization

### Key Features
(MVP - must-haves)

1. **CLI Command**: `claude-planner generate my-project --brief PROJECT_BRIEF.md` creates complete project plan
2. **Template Library**: Pre-built templates (web-app, api, cli) from the Kit
3. **Validation Engine**: Check generated plans for quality (subtask size, prerequisites, etc.)
4. **Customization System**: Support company-specific rules via config file
5. **Interactive Mode**: Walk user through PROJECT_BRIEF.md if file not provided

### Nice-to-Have Features
(v2 - not MVP)

- Web UI for generating plans (no CLI needed)
- Integration with Claude API for auto-generation
- Project evolution (update existing DEVELOPMENT_PLAN.md)
- Export to other formats (Jira, Linear, Notion)
- Analytics on generated plans (average subtask count, etc.)
- Team templates (save and share custom templates)

## Technical Constraints

### Must Use
- Python 3.11+ (you're familiar, good CLI support)
- Click framework (excellent CLI library)
- Jinja2 (template engine for generating files)
- PyYAML (for config files)
- Git via subprocess (for repo initialization)

### Cannot Use
- GUI frameworks (CLI only for MVP)
- External APIs unless explicitly configured (should work offline)
- Databases (keep it simple, file-based)

### Deployment Target
- [x] Local only (runs on developer's machine)
- Must support: Linux, macOS, Windows 10+
- Distributed as: pip package (pypi) or standalone binary

### Budget Constraints
- [x] Free/open-source only

## Quality Requirements

### Performance
- **Generation Time**: <5 seconds for basic plan (without Claude API)
- **Generation Time with API**: <2 minutes for complete plan
- **Memory Usage**: <200 MB
- **Startup Time**: <1 second

### Security
- **Authentication**: N/A (local tool)
- **Data Sensitivity**: [x] Internal (project plans may contain company info)
- **Encryption**: N/A (files stored locally)
- **API Keys**: Support environment variables for Claude API key

### Scalability
- **Plan Size**: Handle projects with 200+ subtasks
- **Template Count**: Support 50+ custom templates
- **Concurrent Usage**: N/A (single-user tool)

### Availability
- **Offline Mode**: Must work without internet (for basic generation)
- **API Mode**: Optional Claude API integration for enhanced generation

## Team & Resources

### Team Composition
- **Skill Levels**: [x] Senior (you, with extensive Python and Claude Code experience)
- **Roles**: [x] Full-stack (CLI + library + documentation)

### Existing Knowledge
- Python (expert level)
- Click (CLI frameworks)
- Jinja2 (template engines)
- Git (version control)
- Claude Code (extensive experience)
- The Project Initialization Kit (you created it!)

### Learning Budget
- [ ] None - using only familiar technologies

### Infrastructure Access
- **Development**: [x] Local machines (your Ubuntu 24.04 + Mac Mini)
- **CI/CD**: [x] GitHub Actions (for testing and releases)
- **Distribution**: [x] PyPI (Python Package Index)

## Success Criteria

How will we know this project succeeded?

1. **Self-Hosting**: Use this tool to generate its own development plan (dogfooding)
2. **Speed**: Generate a complete plan in <5 seconds (without API) or <2 min (with API)
3. **Quality**: Generated plans pass validation with 0 errors
4. **Usability**: You can create new project plans without referring to docs
5. **Distribution**: Available on PyPI, installable via `pip install claude-code-planner`

## Integration Requirements

### External Systems
- System: Anthropic Claude API | Purpose: Optional AI-enhanced generation | API Type: REST | Auth: API key (optional)
- System: Git | Purpose: Repository initialization | API Type: CLI subprocess | Auth: None

### Data Sources
- Source: PROJECT_BRIEF.md | Type: Markdown file | Frequency: On-demand
- Source: Template library | Type: Jinja2 templates + YAML | Frequency: On-demand
- Source: Config file | Type: YAML | Frequency: Once per invocation

### Data Destinations
- Destination: New project directory | Type: Files (claude.md, DEVELOPMENT_PLAN.md, etc.) | Format: Markdown | Frequency: On-demand
- Destination: Git repository | Type: Version control | Format: Git | Frequency: Optional (on-demand)

## Known Challenges

1. **Template Flexibility**: Templates must be generic enough for any project yet specific enough to be useful. Need good abstraction.
2. **Subtask Sizing**: Automatically breaking features into "single session" subtasks is hard. May need AI assistance or conservative splitting.
3. **Prerequisite Detection**: Determining which subtasks depend on others requires understanding project structure. May need heuristics.
4. **Cross-Platform Path Handling**: Windows uses backslashes, Unix uses forward slashes. Need careful path handling.
5. **Validation Accuracy**: False positives (flagging good plans) or false negatives (missing issues) would reduce trust.

## Reference Materials

- The Project Initialization Kit (all artifacts created above)
- Click documentation: https://click.palletsprojects.com/
- Jinja2 documentation: https://jinja.palletsprojects.com/
- Anthropic API: https://docs.anthropic.com/
- Similar tools: cookiecutter (Python project templates), yeoman (JS scaffolding)

## Questions & Clarifications Needed

1. **Template Format**: Store as Jinja2 files or Python code? → Decision: Jinja2 (easier to edit, version)
2. **Validation Rules**: How strict? → Decision: Errors must block, warnings are OK
3. **Git Integration**: Auto-init or user does it? → Decision: Optional flag `--init-git`
4. **API Integration**: Default on or off? → Decision: Off by default (privacy), opt-in via `--use-api`
5. **Config Location**: Where to store user config? → Decision: `~/.claude-planner/config.yaml` or `./claude-planner.yaml` in project

**Decisions Made**:
- Jinja2 templates for flexibility
- Strict validation (block on errors, warn on issues)
- Optional git initialization (`--init-git` flag)
- Claude API opt-in only (`--use-api` flag)
- Config hierarchy: project dir > home dir > defaults

## Architecture Vision

```
Input: PROJECT_BRIEF.md
        ↓
    [Parser] → Extract requirements
        ↓
    [Template Selector] → Choose base template (web-app/api/cli)
        ↓
    [Plan Generator]
        ├─ [Tech Stack Generator] → Choose technologies
        ├─ [Phase Generator] → Break into phases
        ├─ [Task Generator] → Break into tasks
        └─ [Subtask Generator] → Break into single-session subtasks
        ↓
    [Template Engine] → Render claude.md + DEVELOPMENT_PLAN.md
        ↓
    [Validator] → Check quality
        ↓
    [Output] → Write files to disk
        ↓
    [Optional: Git Init] → Initialize repository
```

## Use Cases

### Use Case 1: Quick Project Bootstrap
```bash
# You have a PROJECT_BRIEF.md ready
claude-planner generate my-new-api --brief brief.md --template api

# Output:
# ✅ Generated claude.md
# ✅ Generated DEVELOPMENT_PLAN.md (47 subtasks)
# ✅ Validation passed (0 errors, 2 warnings)
# ✅ Project ready in: ./my-new-api/
```

### Use Case 2: Interactive Mode
```bash
# No brief file? Interactive prompts
claude-planner generate my-app --interactive

# Prompts you for:
# - Project type? (web-app/api/cli)
# - Tech stack preferences?
# - Timeline?
# - Key features?
# Then generates plan
```

### Use Case 3: Enhanced with Claude API
```bash
# Use Claude API for better plans
export ANTHROPIC_API_KEY=your_key
claude-planner generate my-app --brief brief.md --use-api

# Runs all 10 prompts through Claude API
# Higher quality but takes ~2 minutes
```

### Use Case 4: Seed New Repo
```bash
# Generate plan AND initialize git
claude-planner generate my-app --brief brief.md --init-git

# Output:
# ✅ Generated claude.md
# ✅ Generated DEVELOPMENT_PLAN.md
# ✅ Initialized git repository
# ✅ Created initial commit
#
# Next: cd my-app && git remote add origin <url>
```

## Project Deliverables

At the end of this 2-week project, you'll have:

1. **CLI Tool**: `claude-planner` command with `generate`, `validate`, `list-templates` commands
2. **Template Library**: 3+ project templates (web-app, api, cli)
3. **Validator**: Checks plans for quality issues
4. **Documentation**: README, usage guide, template creation guide
5. **Tests**: Unit tests for all core functionality (>80% coverage)
6. **Distribution**: Published to PyPI, installable via pip
7. **Example Plans**: Generate plans for 5 different projects to test

---

**Next Step**: Use this brief with the planning prompts to generate claude.md and DEVELOPMENT_PLAN.md for this project. Then use Claude Code to BUILD the tool using its own generated plan. Meta! 🎉

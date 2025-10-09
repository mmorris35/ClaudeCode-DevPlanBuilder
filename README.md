# Claude Code Project Planner

A CLI tool that takes a `PROJECT_BRIEF.md` as input and produces complete, validated `claude.md` and `DEVELOPMENT_PLAN.md` files ready to seed new Claude Code project repositories.

## Overview

This tool helps developers quickly bootstrap new projects with Claude Code by automating the generation of project planning artifacts. Simply provide a filled-out project brief, and get back a complete development plan with properly structured phases, tasks, and subtasks.

## Features

- **CLI Interface**: Simple command-line tool for generating project plans
- **Template Library**: Pre-built templates for common project types (web-app, API, CLI)
- **Validation Engine**: Ensures generated plans meet quality standards
- **Customization**: Support for company-specific rules via configuration files
- **Git Integration**: Optional repository initialization

## Quick Start

```bash
# Install the package
pip install claude-code-planner

# Generate a project plan
claude-planner generate my-project --brief PROJECT_BRIEF.md --template api

# Validate an existing plan
claude-planner validate DEVELOPMENT_PLAN.md

# List available templates
claude-planner list-templates
```

## Project Status

🚧 **In Development** - This project is currently under active development following its own generated development plan.

## Installation

Requirements:
- Python 3.11 or higher
- pip

```bash
# Development installation
git clone https://github.com/yourusername/claude-code-project-planner.git
cd claude-code-project-planner
pip install -e ".[dev]"
```

## Documentation

- [PROJECT_BRIEF.md](PROJECT_BRIEF.md) - Complete project requirements and specifications
- [claude.md](claude.md) - Development rules and operating principles
- [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) - Detailed development roadmap with all phases and subtasks

## Use Cases

### Bootstrap a New API Project
```bash
claude-planner generate my-api --brief brief.md --template api --init-git
```

### Interactive Project Setup
```bash
claude-planner generate my-app --interactive
```

### Validate Existing Development Plan
```bash
claude-planner validate DEVELOPMENT_PLAN.md --strict
```

## Contributing

This project follows strict development guidelines defined in [claude.md](claude.md). Each subtask must:
- Be completed in a single session
- Include comprehensive tests (>80% coverage)
- Pass all linting and type checking
- End with a semantic git commit

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- Issues: https://github.com/yourusername/claude-code-project-planner/issues
- Documentation: https://github.com/yourusername/claude-code-project-planner/docs

## Technology Stack

- **Language**: Python 3.11+
- **CLI Framework**: Click 8.1+
- **Template Engine**: Jinja2 3.1+
- **Testing**: pytest, pytest-cov
- **Linting**: ruff
- **Type Checking**: mypy

---

**Built with Claude Code** - A tool that uses its own generated development plan to build itself. Meta! 🎉

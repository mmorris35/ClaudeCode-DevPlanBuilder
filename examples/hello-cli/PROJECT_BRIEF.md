# PROJECT_BRIEF.md

## Project Overview

| Field | Value |
|-------|-------|
| **Name** | HelloCLI |
| **Type** | CLI Tool |
| **Goal** | A minimal CLI that greets users by name with optional color output |
| **Timeline** | 1 day |
| **Team Size** | 1 |

## Target Users

- Developers learning CLI patterns
- Anyone needing a simple greeting tool

## MVP Features (Must Have)

1. Accept a name argument and print a greeting
2. Support `--color` flag for colored output
3. Support `--version` flag to show version
4. Provide helpful `--help` output

## Nice-to-Have (v2)

- Multiple language greetings
- ASCII art banner option
- Config file support

## Tech Stack

### Must Use
- Python 3.11+
- Click (CLI framework)
- Rich (colored output)

### Cannot Use
- argparse (use Click instead)
- print() for colors (use Rich)

## Constraints

- Single file implementation (src/hello_cli/cli.py)
- 100% test coverage
- Must work on Linux, macOS, Windows
